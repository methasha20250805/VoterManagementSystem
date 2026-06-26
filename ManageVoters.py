import csv
import os
from Validations import Voter, ValidationError, AGE

VOTER_FILE = "voter.csv"
VOTER_HEADER = ["VoterID", "District", "Age"]

# Initializing Voter manager class
class VoterManager:
    def __init__(self, filepath=VOTER_FILE):
        self.filepath = filepath
        self.voters = {}
        self._load()
#Load the Voter.csv
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
                voter_id, district, age = row[0], row[1], row[2]
                self.voters[voter_id] = Voter(voter_id, district, int(age))
# Save data to the Voter.csv
    def _save(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(VOTER_HEADER)
            for voter in self.voters.values():
                writer.writerow(voter.to_row())
#Add a voter
    def add_voter(self, voter_id, district, age=AGE):
        voter_id = Voter.validate_voter_id(voter_id)
        district = Voter.validate_district(district)
        age = Voter.validate_age(age)

        if voter_id in self.voters:
            raise ValidationError(f"Voter Id {voter_id} already exists.")

        voter = Voter(voter_id, district, age)
        self.voters[voter_id] = voter
        self._save()
        return voter
# Edit a voter
    def edit_voter(self, voter_id, new_district=None, new_age=None):
        voter = self.voters.get(voter_id)
        if voter is None:
            raise ValidationError(f"Voter Id {voter_id} not found.")

        if new_district is not None and new_district != "":
            voter.district = Voter.validate_district(new_district)
        if new_age is not None and new_age != "":
            voter.age = Voter.validate_age(new_age)

        self._save()
        return voter
#Search a voter
    def search_voter(self, voter_id):
        voter = self.voters.get(voter_id)
        if voter is None:
            raise ValidationError(f"Voter Id {voter_id} not found.")
        return voter
#Delete a voter
    def delete_voter(self, voter_id):
        if voter_id not in self.voters:
            raise ValidationError(f"Voter Id {voter_id} not found.")
        del self.voters[voter_id]
        self._save()

    def exists(self, voter_id):
        return voter_id in self.voters

    def get_age_district(self, voter_id):
        voter = self.voters.get(voter_id)
        if voter is None:
            return None, None
        return voter.age, voter.district

    def list_all(self):
        return list(self.voters.values())