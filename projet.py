import csv
from colorama import Fore, Style
from datetime import datetime   

# Family tree data
family_tree = {
    1: [2, 3],
    2: [],
    3: []
}

def menu():
    while True:
        print("")
        print("Family tree")
        print("(1) Log In ")
        print("(2) Sign Up")
        print("(3) Quit")

        choice = input("Enter your choice (1, 2, or 3): ")
        print("")

        if choice == '1':
            if login():
                # Actions after successful login, if needed
                pass
            else:
                print(Fore.RED + "Login failed. Please try again." + Style.RESET_ALL)
        elif choice == '2':
            if signup():
                pass
            else:
                print(Fore.RED + "Sign up failed. Please try again." + Style.RESET_ALL)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 (to log in), 2 (to sign up), or 3 (to quit).")


def login():
    # CSV path
    csv_file = 'csv/users.csv' 
    # Ask the user to enter their username
    username = input("Username (LastName): ")

    # Ask the user to enter their password
    password = input("Password: ")

    # Check logins in the CSV file
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['lastName'] == username and row['password'] == password:
                print(Fore.GREEN + "Login successful as " + username + Style.RESET_ALL)
                if row['admin'] == 'y':
                    print("You are an administrator.")
                else:
                    print("You are not an administrator.")
                return True


    return False




def signup():
    # CSV path
    csv_file = 'csv/users.csv'

    # Ask user personal informations
    while True:
        first_name = input("Enter your first name: ")
        if first_name.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        last_name = input("Enter your last name: ")
        if last_name.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid last name." + Style.RESET_ALL)

    while True:
        password = input("Choose a password: ")
        # Vous pouvez ajouter des vérifications de complexité de mot de passe ici
        if len(password) >= 6:
            break
        else:
            print(Fore.RED + "Invalid input. Password should be at least 6 characters long." + Style.RESET_ALL)

    while True:
        phoneNumber = input("Enter your phone number: ")
        if phoneNumber.isdigit() and len(phoneNumber) == 10:
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        nationality = input("Enter your nationality: ")
        if nationality.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        birthdate = input("Enter your birthday (DD/MM/YYYY format) : ")
        
        try:
            # Verif for date format
            birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
            
            # Can't be in the futur
            today = datetime.today()
            if birthdate <= today:
                break
            else:
                print(Fore.RED + "Invalid input. Please enter a valid birthday." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid date in DD/MM/YYYY format." + Style.RESET_ALL)

    while True:
        dadName = input("Enter your dad first name: ")
        if first_name.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        dadBirthdate = input("Enter your father's birthday (DD/MM/YYYY format): ")
        
        try:
            # Date format
            dadBirthdate = datetime.strptime(dadBirthdate, "%d/%m/%Y")
            
            # Can't be in the futur
            today = datetime.today()
            if dadBirthdate <= today:
                # Father can't be born after the son
                if dadBirthdate < birthdate:
                    break
                else:
                    print(Fore.RED + "Your father can't be born after you." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a valid birthday." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid date in DD/MM/YYYY format." + Style.RESET_ALL)


    while True:
        momName = input("Enter your mom first name: ")
        if first_name.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        momBirthdate = input("Enter your mother's birthday (DD/MM/YYYY format): ")
        
        try:
            # Date format
            momBirthdate = datetime.strptime(momBirthdate, "%d/%m/%Y")
            
            # Can't be in the futur
            today = datetime.today()
            if momBirthdate <= today:
                # Mother can't be born after the son
                if momBirthdate < birthdate:
                    break
                else:
                    print(Fore.RED + "Your mother can't be born after you." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a valid birthday." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid date in DD/MM/YYYY format." + Style.RESET_ALL)

    isAdmin = 'n'


    # Look for max(id) to create an unused one
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        ids = [int(row['id']) for row in csv_reader]

    new_id = max(ids) + 1

    # Add new user to csv
    with open(csv_file, 'a', newline='') as file:
        fieldnames = ['id', 'password', 'firstName', 'lastName', 'phoneNumber', 'nationality' , 'birthdate' , 'dadName' , 'dadBirthdate' , 'momName' , 'momBirthdate', 'admin']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writerow({
            'id': new_id,
            'password': password,
            'firstName': first_name,
            'lastName': last_name,
            'phoneNumber' : phoneNumber,
            'nationality' : nationality,
            'birthdate' : birthdate,
            'dadName' : dadName,
            'dadBirthdate' : dadBirthdate,
            'momName' : momName,
            'momBirthdate' : momBirthdate,
            'admin': isAdmin
        })

    print(Fore.GREEN + "Registration successful!" + Style.RESET_ALL)
    return True

menu()