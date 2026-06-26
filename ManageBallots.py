import csv
import os
from Validations import Ballot, ValidationError

BALLOT_FILE = "ballots.csv"
BALLOT_HEADER = ["Date", "VoterID", "CandidateID", "CandidateSeat", "VoterAge", "District"]

#Initializing the ballot manager class
class BallotManager:
    def __init__(self, voter_manager, candidate_manager, filepath=BALLOT_FILE):
        self.voter_manager = voter_manager
        self.candidate_manager = candidate_manager
        self.filepath = filepath
        self.ballots = {}
        self._load()
#Load the ballots.csv
    def _load(self):
        if not os.path.exists(self.filepath):
            self._save()
            return
        with open(self.filepath, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                date, voter_id, candidate_id, seat, age, district = row
                self.ballots[voter_id] = Ballot(date, voter_id, candidate_id, seat, int(age), district)
#Save data to ballots.csv
    def _save(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(BALLOT_HEADER)
            for ballot in self.ballots.values():
                writer.writerow(ballot.to_row())

#Casting a vote
    def cast_vote(self, date, voter_id, seat_number):
        if not self.voter_manager.exists(voter_id):
            raise ValidationError("Invalid Voter Id.")

        if not self.candidate_manager.seat_exists(seat_number):
            raise ValidationError("Invalid Seat Number.")

        if voter_id in self.ballots:
            raise ValidationError("Vote already cast by voter.")

        Ballot.validate_date(date)

        candidate_id = self.candidate_manager.id_for_seat(seat_number)
        age, district = self.voter_manager.get_age_district(voter_id)

        ballot = Ballot(date, voter_id, candidate_id, seat_number, age, district)
        self.ballots[voter_id] = ballot
        self._save()
        return ballot
#Delete a vote
    def delete_vote(self, voter_id):
        if not self.voter_manager.exists(voter_id):
            raise ValidationError("Invalid Voter Id.")
        if voter_id not in self.ballots:
            raise ValidationError("Vote does not exist.")
        del self.ballots[voter_id]
        self._save()

    def list_all(self):
        return list(self.ballots.values())

    def vote_counts_by_candidate(self):
        counts = {}
        for ballot in self.ballots.values():
            counts[ballot.candidate_id] = counts.get(ballot.candidate_id, 0) + 1
        return counts

#Trend graph
    def plot_trend_graph(self, save_path="vote_trend.html", show=True):

        import pandas as pd
        import numpy as np
        import plotly.express as px

        if not self.ballots:
            raise ValidationError("No votes have been cast yet, nothing to plot.")

        # Build a DataFrame directly from the ballots so Pandas can group it
        df = pd.DataFrame([b.to_row() for b in self.ballots.values()],
                          columns=BALLOT_HEADER)

        # NumPy is used here for the underlying count aggregation
        candidate_ids, counts = np.unique(df["CandidateID"], return_counts=True)
        names = [self.candidate_manager.name_for_id(cid) for cid in candidate_ids]

        result_df = pd.DataFrame({
            "CandidateID": candidate_ids,
            "CandidateName": names,
            "Votes": counts
        }).sort_values("Votes", ascending=False)

        fig = px.bar(
            result_df,
            x="CandidateName",
            y="Votes",
            text="Votes",
            title="Votes Received by Each Candidate",
            labels={"CandidateName": "Candidate", "Votes": "Number of Votes"}
        )
        fig.update_traces(textposition="outside")

        fig.write_html(save_path)
        if show:
            fig.show()

        return result_df