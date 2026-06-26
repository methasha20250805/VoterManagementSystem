from datetime import datetime

# initializing
DISTRICTS = ["Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya", "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar", "Vavuniya", "Mullaitivu", "Batticaloa", "Ampara", "Trincomalee", "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla", "Monaragala", "Ratnapura", "Kegalle"]
AGE = 18

class ValidationError(Exception):
    """Raised when a field fails validation. Caller decides how to display it."""
    pass

#Initializing Voter class
class Voter:
    def __init__(self, voter_id, district, age=AGE):
        self.voter_id = voter_id
        self.district = district
        self.age = age
# Validate voter ID
    def validate_voter_id(voter_id):
        if not (isinstance(voter_id, str) and len(voter_id) == 10 and voter_id.isdigit()):
            raise ValidationError("Invalid Voter Id: must be exactly 10 digits.")
        return voter_id
# Validate district
    def validate_district(district):
        for d in DISTRICTS:
            if d.lower() == str(district).strip().lower():
                return d
        raise ValidationError("Invalid District: must be one of the 25 Sri Lankan districts.")
# Validate age
    def validate_age(age):
        try:
            age_int = int(age)
        except (ValueError, TypeError):
            raise ValidationError("Invalid Age: must be numeric.")
        if age_int < 0 or age_int > 120:
            raise ValidationError("Invalid Age: out of realistic range.")
        return age_int

    def to_row(self):
        return [self.voter_id, self.district, self.age]

    def __str__(self):
        return f"VoterID: {self.voter_id} | District: {self.district} | Age: {self.age}"


#Initialising the candidate class
class Candidate:
    def __init__(self, candidate_id, first_name, seat_number):
        self.candidate_id = candidate_id
        self.first_name = first_name
        self.seat_number = seat_number
#Validate first Name
    def validate_first_name(first_name):
        if not (isinstance(first_name, str) and 1 <= len(first_name) <= 10 and first_name.isalpha()):
            raise ValidationError("Invalid First Name: letters only, max 10 characters.")
        return first_name
# Validate Seat Number
    def validate_seat_number(seat_number):
        if not (isinstance(seat_number, str) and len(seat_number) == 2 and seat_number.isdigit()):
            raise ValidationError("Invalid Seat Number: must be exactly 2 digits (e.g. 01).")
        return seat_number

    def to_row(self):
        return [self.candidate_id, self.first_name, self.seat_number]

    def __str__(self):
        return (f"CandidateID: {self.candidate_id} | Name: {self.first_name} "
                f"| Seat No: {self.seat_number}")

#Initialising ballot class
class Ballot:
    def __init__(self, date, voter_id, candidate_id, candidate_seat, voter_age, district):
        self.date = date
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.candidate_seat = candidate_seat
        self.voter_age = voter_age
        self.district = district
#Validate date
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValidationError("Invalid Date: must be in yyyy-mm-dd format.")
        return date_str

    def to_row(self):
        return [self.date, self.voter_id, self.candidate_id,
                self.candidate_seat, self.voter_age, self.district]

    def __str__(self):
        return (f"Date: {self.date} | VoterID: {self.voter_id} | "
                f"CandidateID: {self.candidate_id} | Seat: {self.candidate_seat}")