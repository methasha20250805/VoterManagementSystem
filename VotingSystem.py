from Validations import ValidationError, AGE, DISTRICTS
from ManageVoters import VoterManager
from ManageCandidates import CandidateManager
from ManageBallots import BallotManager

def pause():
    input("\nPress Enter to continue...")

def show_districts():
    print("\nValid Districts:")
    for i in range(0, len(DISTRICTS), 5):
        print("  " + ", ".join(DISTRICTS[i:i + 5]))

#Display Voter Menu
def voter_menu(vm: VoterManager):
    while True:
        print("\n--- Voter Registration ---")
        print("1. Add Voter")
        print("2. Edit Voter")
        print("3. Search Voter")
        print("4. Delete Voter")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                voter_id = input("Voter Id (10 digits): ").strip()
                show_districts()
                district = input("District: ").strip()
                age_input = input(f"Age (press Enter for default {AGE}): ").strip()
                age = age_input if age_input else AGE
                voter = vm.add_voter(voter_id, district, age)
                print(f"Voter added successfully: {voter}")

            elif choice == "2":
                voter_id = input("Voter Id to edit: ").strip()
                show_districts()
                new_district = input("New District (Enter to skip): ").strip()
                new_age = input("New Age (Enter to skip): ").strip()
                voter = vm.edit_voter(voter_id, new_district or None, new_age or None)
                print(f"Voter updated successfully: {voter}")

            elif choice == "3":
                voter_id = input("Voter Id to search: ").strip()
                voter = vm.search_voter(voter_id)
                print(f"Found: {voter}")

            elif choice == "4":
                voter_id = input("Voter Id to delete: ").strip()
                vm.delete_voter(voter_id)
                print("Voter deleted successfully.")

            elif choice == "0":
                break
            else:
                print("Invalid option.")

        except ValidationError as e:
            print(f"Error: {e}")
        pause()

#Display Candidate Menu
def candidate_menu(cm: CandidateManager):
        while True:
            print("\n--- Candidate Registration ---")
            print("1. Add Candidate")
            print("2. View Candidate")
            print("3. View All Candidates")
            print("0. Back")
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    candidate_id = input("Candidate Id (10 digits): ").strip()
                    first_name = input("First Name (letters only, max 10 chars): ").strip()
                    seat_number = input("Seat Number (2 digits, e.g. 01): ").strip()
                    candidate = cm.add_candidate(candidate_id, first_name, seat_number)
                    print(f"Candidate added successfully: {candidate}")

                elif choice == "2":
                    candidate_id = input("Candidate Id to view: ").strip()
                    candidate = cm.view_candidate(candidate_id)
                    print(f"Found: {candidate}")

                elif choice == "3":
                    candidates = cm.list_all()
                    if not candidates:
                        print("No candidates registered yet.")
                    for c in candidates:
                        print(c)

                elif choice == "0":
                    break
                else:
                    print("Invalid option.")

            except ValidationError as e:
                print(f"Error: {e}")
            pause()

# Voting options
def cast_vote_flow(bm: BallotManager):
    print("\n--- Cast a Vote ---")
    try:
        date = input("Date (yyyy-mm-dd): ").strip()
        voter_id = input("Voter Id: ").strip()
        seat_number = input("Candidate Seat Number (2 digits): ").strip()
        ballot = bm.cast_vote(date, voter_id, seat_number)
        print(f"Vote cast successfully: {ballot}")
    except ValidationError as e:
        print(f"Error: {e}")
    pause()


def delete_vote_flow(bm: BallotManager):
    print("\n--- Delete a Vote ---")
    try:
        voter_id = input("Voter Id: ").strip()
        bm.delete_vote(voter_id)
        print("Vote deleted successfully. Voter may now cast a new vote.")
    except ValidationError as e:
        print(f"Error: {e}")
    pause()


def trend_graph_flow(bm: BallotManager):
    print("\n--- Trend Graph ---")
    try:
        result_df = bm.plot_trend_graph(save_path="vote_trend.html", show=False)
        print(result_df.to_string(index=False))
        print("\nGraph saved to vote_trend.html (open it in a browser to view).")
    except ValidationError as e:
        print(f"Error: {e}")
    except ImportError as e:
        print(f"Missing library: {e}. Run: pip install pandas numpy plotly")
    pause()

# Main Menu
def main():
    vm = VoterManager()
    cm = CandidateManager()
    bm = BallotManager(vm, cm)

    while True:
        print("\nVOTING SYSTEM")
        print("1. Voter Registration")
        print("2. Candidate Registration")
        print("3. Cast a Vote")
        print("4. Delete a Vote")
        print("5. Trend Graph (votes per candidate)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            voter_menu(vm)
        elif choice == "2":
            candidate_menu(cm)
        elif choice == "3":
            cast_vote_flow(bm)
        elif choice == "4":
            delete_vote_flow(bm)
        elif choice == "5":
            trend_graph_flow(bm)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()