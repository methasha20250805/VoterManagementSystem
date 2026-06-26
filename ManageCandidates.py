import csv
import os
from Validations import Candidate, ValidationError

CANDIDATE_FILE = "candidate.csv"
CANDIDATE_HEADER = ["CandidateID", "FirstName", "SeatNumber"]

#Initialising the Candidate Manager
class CandidateManager:
    def __init__(self, filepath=CANDIDATE_FILE):
        self.filepath = filepath
        self.candidates = {}
        self.seat_to_id = {}
        self._load()

#Load the Candidate.csv
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
            cid, name, seat = row[0], row[1], row[2]
            self.candidates[cid] = Candidate(cid, name, seat)
            self.seat_to_id[seat] = cid

# Save the Candidate.csv
def _save(self):
    with open(self.filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CANDIDATE_HEADER)
        for c in self.candidates.values():
            writer.writerow(c.to_row())

#Add a candidate
    def add_candidate(self, candidate_id, first_name, seat_number):
        candidate_id = Candidate.validate_candidate_id(candidate_id)
        first_name = Candidate.validate_first_name(first_name)
        seat_number = Candidate.validate_seat_number(seat_number)

        if candidate_id in self.candidates:
            raise ValidationError(f"Candidate Id {candidate_id} already exists.")
        if seat_number in self.seat_to_id:
            raise ValidationError(f"Seat Number {seat_number} is already taken.")

        candidate = Candidate(candidate_id, first_name, seat_number)
        self.candidates[candidate_id] = candidate
        self.seat_to_id[seat_number] = candidate_id
        self._save()
        return candidate

#View all candidates
    def view_candidate(self, candidate_id):
        candidate = self.candidates.get(candidate_id)
        if candidate is None:
            raise ValidationError(f"Candidate Id {candidate_id} not found.")
        return candidate

    def list_all(self):
        return list(self.candidates.values())

    def seat_exists(self, seat_number):
        return seat_number in self.seat_to_id

    def id_for_seat(self, seat_number):
        return self.seat_to_id.get(seat_number)

    def name_for_id(self, candidate_id):
        c = self.candidates.get(candidate_id)
        return c.first_name if c else "Unknown"