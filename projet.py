import csv
from colorama import Fore, Style
from datetime import datetime   


def menu():     # Dysplay the menu before being connected
    while True:
        print("")
        print("Family tree")
        print("(1) Log In ")
        print("(2) Sign Up")
        print("(3) Quit")

        choice = input("Enter your choice (1, 2, or 3): ")
        print("")

        if choice == '1':
            success, userId = login()
            if success:
                # Actions after successful login, if needed
                connected(userId)
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



def login():    # Log into the platform
    # CSV path
    csv_file = 'csv/users.csv' 
    # Ask the user to enter their username
    username = input("Username (LastName): ")
    username2 = input("Username (FirstName): ")

    # Ask the user to enter their password
    password = input("Password: ")

    # Check logins in the CSV file
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['lastName'] == username and row['firstName'] == username2 and row['password'] == password:
                print(Fore.GREEN + "Login successful as " + username + Style.RESET_ALL)
                id = row['id']
                if row['admin'] == 'y':
                    print("You are an administrator.")
                else:
                    print("You are not an administrator.")
                return True, id


    return False



def signup():       # create an account and register in the database
    # CSV path
    csv_file = 'csv/users.csv'

    # Ask user personal informations
    while True:
        firstName = input("Enter your first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        lastName = input("Enter your last name: ")
        if lastName.isalpha():
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
        if firstName.isalpha():
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
        if firstName.isalpha():
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
            'firstName': firstName,
            'lastName': lastName,
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
    get_potential_parents(dadName, dadBirthdate, momName, momBirthdate, lastName, new_id)
    return True



def get_potential_parents(dadName, dadbirthdate, momName, mombirthdate, lastName, id):      # Get a list of potential parents
    csv_file = 'csv/users.csv'
    potential_fathers = []
    potential_mothers = []
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['firstName'] == dadName :
                potential_fathers.append(row)
            elif row['firstName'] == momName :
                potential_mothers.append(row)

   
    print("Potential fathers:")
    i = 1
    j = 1
    for father in potential_fathers:
        print("    ",i,"_ ", f"{father['firstName']} {father['lastName']} - {father['birthdate']}")
        i+=1
    
    while True:
        choosenDad = input("is this your dad ? (y/n) ")
        if choosenDad == 'y' or choosenDad == 'n':
            break
        else:
            print("Please answer by 'y' or 'n'")


    print(" ")
    print("Potential mothers:")
    for mother in potential_mothers:
        print("    ",i,"_ ", f"{mother['firstName']} {mother['lastName']} - {mother['birthdate']}")
        j+=1

    while True:
        choosenMom = input("is this your mom ? (y/n) ")
        if choosenMom == 'y' or choosenMom == 'n':
            break
        else:
            print("Please answer by 'y' or 'n'")

    if choosenDad == 'y':
        if potential_fathers:
            chosenDadId = potential_fathers[0]['id']
        else:
            chosenDadId = None  


    if choosenMom == 'y':
        if potential_mothers:
            chosenMomId = potential_mothers[0]['id']
        else:
            chosenMomId = None 


    linkFile= 'csv/links.csv'
    with open(linkFile, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([id, chosenDadId, chosenMomId])

    print(Fore.GREEN + "You are successfully added in the tree !" + Style.RESET_ALL)

    



def load_user_info(file_path):
    user_info = {}
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            user_id = row['id']
            name = f"{row['firstName']} {row['lastName']}"
            user_info[user_id] = name
    return user_info


def getParentsId(tree, id):
    parentsId = []
    for person, parents in tree.items():  # Utilisez .items() pour obtenir les paires clé-valeur
        if person == id:
            parentsId.extend(parents)  # Utilisez .extend() pour ajouter les éléments de 'parents' à 'parentsId'
    return parentsId


def getSiblings(tree, id, dadId, momId):
    siblings = []

    for person, parents in tree.items():  # Utilisez .items() pour itérer sur les paires clé-valeur
        if parents[0] == dadId and parents[1] == momId and person != id:
            siblings.append(person)

    return siblings



def printFamilyTree(tree, current_id, user_info, indent="", root=True):
    if root:
        # Afficher le nom et prénom de l'utilisateur racine
        print(f"{indent}Arbre Généalogique de {user_info.get(str(current_id), 'ID inconnu')}:")
        parentsId = getParentsId(tree,current_id)
        tabSiblings = getSiblings(tree,current_id, parentsId[0], parentsId[1])

        print(Fore.BLUE + "Siblings: " + Style.RESET_ALL)
        for sibling in tabSiblings:
            siblingName = user_info.get(str(sibling), 'ID inconnu')
            print(" - " + siblingName)
        
        print(" ")
        print(Fore.BLUE + "Ancestry: " + Style.RESET_ALL)

    if current_id in tree:
        for child_id in tree[current_id]:
            # Utiliser user_info pour récupérer le nom et prénom en fonction de l'ID
            child_name = user_info.get(str(child_id), 'ID inconnu')
            print(f"{indent}- {child_name}")
            # Appel récursif pour afficher les enfants
            printFamilyTree(tree, child_id, user_info, indent + "  ", root=False)



def printAncestry(tree, current_id, user_info, indent="", root=True):
    if root:
        # Afficher le nom et prénom de l'utilisateur racine
        print(f"{indent}Arbre Généalogique de {user_info.get(str(current_id), 'ID inconnu')}:")
        parentsId = getParentsId(tree,current_id)
        print(" ")
        print(Fore.BLUE + "Ancestry: " + Style.RESET_ALL)

    if current_id in tree:
        for child_id in tree[current_id]:
            # Utiliser user_info pour récupérer le nom et prénom en fonction de l'ID
            child_name = user_info.get(str(child_id), 'ID inconnu')
            print(f"{indent}- {child_name}")
            # Appel récursif pour afficher les enfants
            printFamilyTree(tree, child_id, user_info, indent + "  ", root=False)


def connected(id):    # Display the menu whan you are connected

    # Menu display
    print("Family tree")
    print(Fore.YELLOW + " -- ADD --" + Style.RESET_ALL)
    print("(1) add a parent")
    print("(2) add a child")
    print(Fore.YELLOW + " -- DELETE --" + Style.RESET_ALL)
    print("(3) delete yourself")
    print("(4) delete a parent")
    print("(5) delete a child")
    print(Fore.YELLOW + " -- LOOK-UP --" + Style.RESET_ALL)
    print("(6) look-up the entire tree")
    print("(7) look-up your family tree")  
    print("(8) look-up your descendants")  
    print("(9) look-up your ancestry")
    print("(10) look-up a family ties")
    print("(11) look-up persons without ancestry")
    print("(12) look-up persons with the most ancestry alive")
    print(Fore.RED + "(13) Quit" + Style.RESET_ALL)

    # Info collection for different cases
    user_info = load_user_info('csv/users.csv')
    family_tree = csvToTree()
    id = int(id)

    # Run the choice 
    while True:
        choice = input("Enter your choice: ")

        if choice == '1':   # add a parent
            break
        elif choice == '2':     # add a child 
            break
        elif choice == '3':     # delete yourself 
            break
        elif choice == '4':     # delete a parent
            break
        elif choice == '5':     # delete a child
            break
        elif choice == '6':     # look-up the entire tree
            break
        elif choice == '7':     # look-up your family tree  
            printFamilyTree(family_tree, id, user_info)
            break
        elif choice == '8':     # look-up your descendants 
            break
        elif choice == '9':     # look-up your ancestry
            printAncestry(family_tree, id, user_info)
            break
        elif choice == '10':     # look-up a family ties
            break
        elif choice == '11':     # look-up persons without descendants
            break
        elif choice == '12':     # look-up persons with the most ancestry alive
            break
        elif choice == '13':     # Quit
            break

        break
        
    
    
def csvToTree():    # Initialise the whole family tree from links.csv
    family_tree = {}
    
    file_path = 'csv/links.csv'

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = list(map(int, line.strip().split(',')))
                
                family_tree[parts[0]] = parts[1:]
    
    return family_tree





#print_family_tree(family_tree, 6, user_info)

menu()