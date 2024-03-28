import os
import csv
from datetime import datetime   
from colorama import Fore, Style



def menu():     # Dysplay the menu before being connected
    while True:
        print("")
        print(Fore.BLUE + Style.BRIGHT + "Family tree" + Style.RESET_ALL)
        print("     (1) Log In ")
        print("     (2) Sign Up")
        print("     (3) Quit")

        choice = input("Enter your choice (1, 2, or 3): ")
        print("")

        if choice == '1':
            success, userId, admin = login()
            if success:
                # Actions after successful login, if needed
                connected(userId, admin)
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
    csv_file = 'users.csv' 
    # Ask the user to enter their username
    username = input("Username (LastName): ")
    username2 = input("Username (id): ")

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
                    return True, id, 'y'
                else:
                    print("You are not an administrator.")
                    return True, id, 'n'


    return False, 0, 'n'



def signup():       # create an account and register in the database
    # CSV path
    csv_file = 'users.csv'

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
    csv_file = 'users.csv'
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
        chosenDadId = 0  


    if choosenMom == 'y':
        if potential_mothers:
            chosenMomId = potential_mothers[0]['id']
    else:
        chosenMomId = 0 


    linkFile= 'links.csv'
    with open(linkFile, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([id, chosenDadId, chosenMomId])

    print(Fore.GREEN + "You are successfully added in the tree !" + Style.RESET_ALL)



def update_link_parent(id, idParent, parent, tree):    # Add new parents into dico
    for person, parents in tree.items():
        if str(person) == str(id):
            if parent == 1:
                parents[0] = idParent
            elif parent == 2:
                parents[1] = idParent
            break



def update_link_child(childId, dadId, momId, tree):    # Add new child into dico
    # the child isn't in the tree
    if childId not in tree:
        tree[childId] = [dadId, momId]
    else:
        # if child was already in tree
        tree[childId]['dadId'] = dadId
        tree[childId]['momId'] = momId



def signup_parent():        # Add a parent
    # CSV path
    csv_file = 'users.csv'

    # Ask user personal informations
    while True:
        firstName = input("Enter your parent first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        lastName = input("Enter your parent last name: ")
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
        phoneNumber = input("Enter your parent phone number: ")
        if phoneNumber.isdigit() and len(phoneNumber) == 10:
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        nationality = input("Enter your parent nationality: ")
        if nationality.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        birthdate = input("Enter your parent birthday (DD/MM/YYYY format) : ")
        
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
        dadName = input("Enter your grandfather first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        dadBirthdate = input("Enter your grandfather's birthday (DD/MM/YYYY format): ")
        
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
                    print(Fore.RED + "Your grandfather can't be born after you." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a valid birthday." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid date in DD/MM/YYYY format." + Style.RESET_ALL)


    while True:
        momName = input("Enter your grandmother first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        momBirthdate = input("Enter your grandmother's birthday (DD/MM/YYYY format): ")
        
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
                    print(Fore.RED + "Your grand-mother can't be born after you." + Style.RESET_ALL)
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
    return True,new_id



def signup_child():         # Add a child
    # CSV path
    csv_file = 'users.csv'

    # Ask user personal informations
    while True:
        firstName = input("Enter your child's first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        lastName = input("Enter your child's last name: ")
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
        phoneNumber = input("Enter your child's phone number: ")
        if phoneNumber.isdigit() and len(phoneNumber) == 10:
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        nationality = input("Enter your child's nationality: ")
        if nationality.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    while True:
        birthdate = input("Enter your child's birthday (DD/MM/YYYY format) : ")
        
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
        dadName = input("Enter your child's dad first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        dadBirthdate = input("Enter your child dad birthday (DD/MM/YYYY format): ")
        
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
                    print(Fore.RED + "Your grandfather can't be born after you." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a valid birthday." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid date in DD/MM/YYYY format." + Style.RESET_ALL)


    while True:
        momName = input("Enter your child's mom first name: ")
        if firstName.isalpha():
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid first name." + Style.RESET_ALL)

    while True:
        momBirthdate = input("Enter your child's mom birthday (DD/MM/YYYY format): ")
        
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
                    print(Fore.RED + "Your child's mom can't be born after him." + Style.RESET_ALL)
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
    return True,new_id



def printPersonFromId(idList):
    csv_file = 'users.csv' 
    idListStr = [str(id) for id in idList]
    names = []
    
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['id'] in idListStr:
                names.append((row['firstName'], row['lastName']))
    
    return names
    


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



def getSibling(tree, id, dadId, momId):
    siblings = []

    for person, parents in tree.items():  # Utilisez .items() pour itérer sur les paires clé-valeur
        if parents[0] == dadId and parents[1] == momId and person != id:
            siblings.append(person)

    return siblings



"""def printFamilyTree(tree, current_id, user_info, indent="", root=True):
    if root:
        # Afficher le nom et prénom de l'utilisateur racine
        print(f"{indent}Arbre Généalogique de {user_info.get(str(current_id), 'ID inconnu')}:")
        parentsId = getParentsId(tree,current_id)
        tabSiblings = getSibling(tree,current_id, parentsId[0], parentsId[1])
        tabC = getAuntsUncles(tree, current_id)
        tabS = getSpouse(tree, current_id)

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
            printFamilyTree(tree, child_id, user_info, indent + "  ", root=False)"""


def printFamilyTree(tree, current_id, user_info, indent="", root=True):
    if root:
        # Afficher le nom et prénom de l'utilisateur racine
        print(f"{indent}Arbre Généalogique de {user_info.get(str(current_id), 'ID inconnu')}:")
        parentsId = getParentsId(tree,current_id)
        tabSiblings = getSibling(tree,current_id, parentsId[0], parentsId[1])
        tabC = getAuntsUncles(tree, current_id)
        tabS = getSpouse(tree, current_id)
        tabD = getCousins(tree, current_id)

        print(Fore.BLUE + "Siblings: " + Style.RESET_ALL)
        for sibling in tabSiblings:
            siblingName = user_info.get(str(sibling), 'ID inconnu')
            print(" - " + siblingName)
                
        print(Fore.BLUE + "\nSpouse: " + Style.RESET_ALL)
        spouse_id = tabS[0] if tabS else None
        spouse_name = user_info.get(str(spouse_id), 'Non marié(e)')
        print(" - " + spouse_name)
        
        print(Fore.BLUE + "\nUncles and Aunts: " + Style.RESET_ALL)
        for uncleaunt_id in tabC:
            uncleaunt_name = user_info.get(str(uncleaunt_id), 'ID inconnu')
            print(" - " + uncleaunt_name)

        print(Fore.BLUE + "\nCousins: " + Style.RESET_ALL)
        for cousins_id in tabD:
            cousins_name = user_info.get(str(cousins_id), 'ID inconnu')
            print(" - " + cousins_name)


        print(Fore.BLUE + "\nAncestry: " + Style.RESET_ALL)
    if current_id in tree:
        for child_id in tree[current_id]:
            # Utiliser user_info pour récupérer le nom et prénom en fonction de l'ID
            child_name = user_info.get(str(child_id), 'ID inconnu')
            print(f"{indent}- {child_name}")
            # Appel récursif pour afficher les enfants
            printFamilyTree(tree, child_id, user_info, indent + "  ", root=False)



def noDescendants(familyTree):      # Print everyone who don't have descendants 
    noDesc = []
    csv_file = 'users.csv' 
    

    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            noDesc.append(row['id'])

    noDesc = [int(id) for id in noDesc]

    descendants = set() # initialize a set

    for parents in familyTree.values():
        for id in parents:
            descendants.add(id)     # add to the set for non key ids (parents)

    noDesc2 = [id for id in noDesc if id not in descendants]    # add ids to noDesc2 if the id is in the descendants set

    return noDesc2  



def noAncestry(familyTree):     # Print everyone who don't have ancestry
    noAsc = []
    csv_file = 'users.csv' 
    

    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            noAsc.append(row['id'])

    noAsc = [int(id) for id in noAsc]

    noAsc = [id for id in noAsc if id not in familyTree]

    return noAsc    



def printAncestry(tree, current_id, user_info, indent=""):
    if current_id in tree:
        for parent_id in tree[current_id]:
            parent_name = user_info.get(str(parent_id), 'Unknown')
            print(f"{indent}- {parent_name}")
            printAncestry(tree, parent_id, user_info, indent + "  ")



def printDescendants(tree, current_id, user_info, indent="", root=True):
    if root:
        # Afficher le nom et prénom de l'individu dont on cherche les descendants
        print(" ")
        print(Fore.BLUE + "Descendants: " + Style.RESET_ALL)

    descendants = set()

    # Fonction récursive pour récupérer tous les descendants
    def get_descendants(person_id):
        if person_id in tree:
            for parent_id, child_id in tree.items():
                if person_id in child_id:
                    descendants.add(parent_id)
                    get_descendants(parent_id)

    get_descendants(current_id)

    for descendant_id in descendants:
        descendant_name = user_info.get(str(descendant_id), 'ID inconnu')
        print(f"{indent}- {descendant_name}")





def addParent(tree,id):
    for person, parents in tree.items():
        
        if int(person) == id :
            if len(parents) == 2 and parents[0] != 0 and parents[1] != 0 :
                print("You already have 2 parents registered in the family tree")
                
                
            #  ADD YOUR DAD
            elif(len(parents) == 2 and parents[0] == 0 and parents[1] != 0):
                print("Do you wish to add your dad ?")
                while True:
                    choice = input("(y/n): ")
                    if choice == 'y' or choice == 'n':
                        break
                    else:
                        print(Fore.RED + "Invalid input. Please enter y or n." + Style.RESET_ALL)
                
                if choice == 'y' :
                    success, idParent = signup_parent()  
                    update_link_parent(id, idParent, 1, tree)


            # ADD YOUR MOM
            elif(len(parents) == 2 and parents[0] != 0 and parents[1] == 0):
                print("Do you wish to add your mom ?")
                while True:
                    choice = input("(y/n): ")
                    if choice == 'y' or choice == 'n':
                        break
                    else:
                        print(Fore.RED + "Invalid input. Please enter y or n." + Style.RESET_ALL)

                if choice == 'y' :
                    success, idParent = signup_parent()  
                    update_link_parent(id, idParent, 2, tree)


            # ADD YOUR DAD OR MOM
            elif(len(parents) == 2 and parents[0] == 0 and parents[1] == 0):
                print("Do you wish to add your dad or mom ?")
                while True:
                    choice = input("(dad/mom/n): ")
                    if choice == 'y' or choice == 'n':
                        break
                    else:
                        print(Fore.RED + "Invalid input. Please enter y or n." + Style.RESET_ALL)
            
                if choice == 'dad' :
                    success, idParent = signup_parent()  
                    update_link_parent(id, idParent, 1, tree)

                elif choice == 'mom' :
                    success, idParent = signup_parent()  
                    update_link_parent(id, idParent, 2, tree)

        
    return True



def addChild(tree, id):


    success, childId = signup_child()

    while True:
        sex = input("Are you the dad or mom? (dad/mom): ")
        if sex == 'dad' or sex == 'mom':
            break
        else:
            print(Fore.RED + "Invalid input. Please enter dad or mom." + Style.RESET_ALL)

    if sex == 'dad':
        update_link_child(childId, id, 0, tree)
        
    if sex == 'mom':
        update_link_child(childId, 0, id, tree)



def deleteYourself(id, tree):
    
    # Copy the tree
    tree_copy = tree.copy()
    
    for person, parents in tree_copy.items():
        if person == id:
            # Delete rows where you are the son
            del tree[id]
        elif parents[0] == id:
            # Delete links with your child
            parents[0] = 0
        elif parents[1] == id:  
            # Delete links with your child
            parents[1] = 0

    # Delete in csv
    csv_file = 'users.csv'
    temp_file = 'users_temp.csv'    # use a temp file

    with open(csv_file, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)
        
        for row in reader:        
            if row[0] == 'id' or int(row[0]) != id:  # Copy the rows except yours 
                writer.writerow(row)

    # Use the temp file as the new file
    os.remove(csv_file)
    os.rename(temp_file, csv_file)



def deleteParent(id, tree):

    while True:
        choice = input("Do you wish to delete your mom or dad? (dad/mom):")
        if choice == 'mom' or choice == 'dad':
            break
        else:
            print(Fore.RED + "Invalid input. Please enter mom or dad." + Style.RESET_ALL)

    for person, parents in tree.items():
        if person == id and choice == 'dad':
            idParent = parents[0]
        elif person == id and choice == 'mom':
            idParent = parents[1]

    print(idParent)

    tree_copy = tree.copy()
    for person1, parents1 in tree_copy.items():
        if idParent == person1:
            # Delete rows where you are the son
            del tree[idParent]
        if parents1[0] == idParent:
            # Delete links with your child
            parents1[0] = 0
        if parents1[1] == idParent:  
            # Delete links with your child
            parents1[1] = 0

     # Delete in csv
    csv_file = 'users.csv'
    temp_file = 'users_temp.csv'    # use a temp file

    with open(csv_file, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)
        
        for row in reader:        
            if row[0] == 'id' or int(row[0]) != idParent:  # Copy the rows except yours 
                writer.writerow(row)

    # Use the temp file as the new file
    os.remove(csv_file)
    os.rename(temp_file, csv_file)
    


def deleteChild(id, tree):

    # Find all the childs
    childs = []
    for person1, parents1 in tree.items():
        if parents1[0] == id or parents1[1] == id:
            childs.append(person1)

    # Choose the child
    if len(childs) == 0:
        print("You don't have any child in the tree")
        idChild = -1

    elif len(childs) == 1:
        idChild = childs[0]     
        printPersonFromId(childs[0])

    else:
        print("Children found:")
        for index, child in enumerate(childs, start=1):
            print(f"({index})")
            printPersonFromId(child)
        
        choice = input("Choose which child you want to delete (enter the corresponding number): ")
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(childs):
            choice = input("Invalid choice. Please enter a valid number: ")
        
        idChild = childs[int(choice) - 1]
        


    # Delete the child
    tree_copy = tree.copy()
    for person, parents in tree_copy.items():
        if idChild == person:
            # Delete rows where you are the son
            del tree[idChild]
        if parents[0] == idChild:
            # Delete links with your child
            parents[0] = 0
        if parents[1] == idChild:  
            # Delete links with your child
            parents[1] = 0

     # Delete in csv
    csv_file = 'users.csv'
    temp_file = 'users_temp.csv'    # use a temp file

    with open(csv_file, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)
        
        for row in reader:        
            if row[0] == 'id' or int(row[0]) != idChild:  # Copy the rows except yours 
                writer.writerow(row)

    # Use the temp file as the new file
    os.remove(csv_file)
    os.rename(temp_file, csv_file)



def lookupFamilyTies(family_tree, user_id, user_info):
    print("Choose a family tie to look up:")
    print("(1) Grandparents")
    print("(2) Parents")
    print("(3) Siblings")
    print("(4) Children")
    print("(5) Aunts and Uncles")
    print("(6) Partenaire")
    print("(7) GrandChildrens")
    print("(8) Cousins")
    
    while True:
        choice = input("\nEnter your choice: ")
        if choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == '5' or choice == '6' or choice =='7' or choice =='8':
            break
        else:
            print(Fore.RED + "Invalid input. Please enter a valid phone number." + Style.RESET_ALL)

    if choice == '1':  # Grandparents
        print("Looking up grandparents...")
        grandparents = getGrandparents(family_tree, user_id)
        print(Fore.BLUE + "\nGrandparents: " + Style.RESET_ALL)
        printPersonsFromId(grandparents, user_info)

    elif choice == '2':  # Parents
        print("Looking up parents...")
        parents = getParents(family_tree, user_id)
        print(Fore.BLUE + "\nParents:" + Style.RESET_ALL)
        printPersonsFromId(parents, user_info)

    elif choice == '3':  # Siblings
        print("Looking up siblings...")
        siblings = getSiblings(family_tree, user_id)
        print(Fore.BLUE + "\nSiblings:" + Style.RESET_ALL)
        printPersonsFromId(siblings, user_info)

    elif choice == '4':  # Children
        print("Looking up children...")
        children = getChildren(family_tree, user_id)
        print(Fore.BLUE + "\nChildren:" + Style.RESET_ALL)
        printPersonsFromId(children, user_info)

    elif choice == '5':  # Aunts and Uncles
        print("Looking up aunts and uncles...")
        aunts_uncles = getAuntsUncles(family_tree, user_id)
        print(Fore.BLUE + "\nAunts and Uncles:" + Style.RESET_ALL )
        printPersonsFromId(aunts_uncles, user_info)
    
    elif choice == '6':  # Spouse
        print("Looking up spouse")
        spouse = getSpouse(family_tree, user_id)
        print(Fore.BLUE + "\nSpouse:" + Style.RESET_ALL)
        printPersonsFromId(spouse, user_info)

    elif choice == '7':  # GrandChildrens
        print("Looking up GrandChildrens")
        grandchildren= getGrandChildren(family_tree, user_id)
        print(Fore.BLUE + "\nGrandChildrens:" + Style.RESET_ALL)
        printPersonsFromId(grandchildren, user_info)

    elif choice == '8':  # Cousins
        print("Looking up Cousins")
        cousins= getCousins(family_tree, user_id)
        print(Fore.BLUE + "\nCousins:" + Style.RESET_ALL)
        printPersonsFromId(cousins, user_info)
    else:
        print("Invalid choice.")

def getParents(family_tree, user_id): 
    parents = family_tree.get(user_id, [])
    return parents

def getGrandparents(family_tree, user_id):
    grandparents = set()
    parents = getParents(family_tree, user_id)
    for parent_id in parents:
        grandparents.update(getParents(family_tree, parent_id))
    return grandparents

def getChildren(family_tree, user_id):
    children = []
    for person_id, parent_ids in family_tree.items():
        if user_id in parent_ids:
            children.append(person_id)
    return children

def getSiblings(family_tree, user_id):
    siblings = set()  
    parents = getParents(family_tree, user_id)
    for parent in parents:
        parent_children = getChildren(family_tree, parent)
        siblings.update(child for child in parent_children if child != user_id)
    return list(siblings)  

def getAuntsUncles(family_tree, user_id):
    aunts_uncles = set()
    grandparents = []
    parents = getParents(family_tree, user_id)
    for parent in parents:
        grandparents.extend(getParents(family_tree, parent))

    for grandparent in grandparents:
        grandparent_children = getChildren(family_tree, grandparent)
        for aunt_uncle in grandparent_children:
            if aunt_uncle != user_id and aunt_uncle not in parents:
                aunts_uncles.add(aunt_uncle)

    return list(aunts_uncles)

def getGrandChildren(family_tree, user_id):
    grand_children = []
    children = getChildren(family_tree, user_id)
    for child in children:
        grand_children.extend(getChildren(family_tree, child))
    return grand_children

def getSpouse(family_tree, user_id):
    spouse = set()
    children = getChildren(family_tree, user_id)
    for child in children:
        parents = getParents(family_tree, child)
        for parent in parents:
            if parent != user_id:
                spouse.add(parent)
    return list(spouse)

def getCousins(family_tree, user_id):
    cousins = set()
    aunts_uncles = getAuntsUncles(family_tree, user_id)
    for aunt_uncle in aunts_uncles:
        cousins.update(getChildren(family_tree, aunt_uncle))
    return list(cousins)





def printPersonsFromId(ids, user_info):
    for id in ids:
        print(user_info.get(str(id), "Unknown"))



def mostAncestryAlive(tree, user_info):
    max_ancestry_count = 0
    persons_with_max_ancestry = []

    for person_id in tree.keys():
        ancestry_count = countAncestry(tree, person_id)
        if ancestry_count > max_ancestry_count:
            max_ancestry_count = ancestry_count
            persons_with_max_ancestry = [person_id]
        elif ancestry_count == max_ancestry_count:
            persons_with_max_ancestry.append(person_id)

    if persons_with_max_ancestry:
        print("Persons with the most ancestry alive:")
        for person_id in persons_with_max_ancestry:
            print(f"{user_info.get(str(person_id), 'Unknown')}:")
            printAncestry(tree, person_id, user_info)
            print(f"They have {max_ancestry_count} ancestors.\n")
    else:
        print("No person with ancestry found in the tree.")



def countAncestry(tree, person_id):
    visited = set()

    def dfs(current_id):
        if current_id not in visited:
            visited.add(current_id)
            count = 1
            if current_id in tree:
                for parent_id in tree[current_id]:
                    count += dfs(parent_id)
            return count
        return 0

    return dfs(person_id) - 1  



def connex(tree, current_id, visited=None, connected_ids=None):
    if visited is None:
        visited = set()
    if connected_ids is None:
        connected_ids = []

    # Ignore if id == 0 
    if current_id == 0:
        return connected_ids

    visited.add(current_id)
    connected_ids.append(current_id)

    if current_id in tree:
        for id in tree[current_id]:
            if id not in visited:
                connex(tree, id, visited, connected_ids)

    # Look entry links
    for key, values in tree.items():
        if current_id in values and key not in visited:
            connex(tree, key, visited, connected_ids)

    return connected_ids



def treeSize(tree):
    # Get the id of someone to know which tree
    while True:
        id = input("Enter the id of someone who is in the tree you want to see the size: ")
        if id.isdigit() and idInCsv(id):
            break
        else:
            print("Invalid input. Please enter a valid id.")

    idList = [id]

    names = printPersonFromId(idList)
    name_strings = [f"{first} {last}" for first, last in names]     # Transform the id in a name 
    names_str = ', '.join(name_strings)

    print(f"The tree of {names_str} contains {len(connex(tree,int(id)))} persons")



def idInCsv(id):
    csv_file = "users.csv"
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == str(id):
                return True
    return False







def print_connected_names(id, family_tree, user_info):
    connected_ids = connex(family_tree, id)
    print("\n\033[94mFamily:\033[0m")  # Utilisation de codes d'échappement ANSI pour afficher en bleu
    for person_id in connected_ids:
        print(user_info.get(str(person_id), "Unknown"))



def print_all_connected_trees():
    user_info = load_user_info('users.csv')
    family_tree = csvToTree()
    visited_ids = set()  # Pour stocker les IDs des personnes déjà rencontrées
    tree_count = 1  # Compteur pour numéroter les arbres connexes
    with open('users.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            person_id = int(row['id'])
            if person_id not in visited_ids:  # Vérifie si la personne a déjà été rencontrée
                connected_ids = connex(family_tree, person_id)  # Récupère l'arbre connexe de la personne
                print(Fore.BLUE + f"\nFamily {tree_count}:" + Style.RESET_ALL)
                tree_count += 1  # Incrémente le compteur pour le prochain arbre connexe
                for id in connected_ids:
                    print(user_info.get(str(id), "Unknown"))  # Affiche le nom de la personne à partir de son ID
                visited_ids.update(connected_ids)  # Met à jour les IDs des personnes déjà rencontrées
    print()  # Ajoute une ligne vide après avoir parcouru tous les arbres connexes





def print_largest_connected_tree():
    user_info = load_user_info('users.csv')
    family_tree = csvToTree()
    visited_ids = set()  # Pour stocker les IDs des personnes déjà rencontrées
    largest_tree = []  # Liste pour stocker l'arbre connexe avec le plus grand nombre d'individus
    max_size = 0  # Variable pour suivre la taille maximale de l'arbre connexe

    for person_id in family_tree.keys():
        if person_id not in visited_ids:  # Vérifie si la personne a déjà été rencontrée
            connected_ids = connex(family_tree, person_id)  # Récupère l'arbre connexe de la personne
            if len(connected_ids) > max_size:  # Vérifie si l'arbre connexe actuel est le plus grand rencontré jusqu'à présent
                max_size = len(connected_ids)
                largest_tree = connected_ids

    if largest_tree:
        print(Fore.BLUE + f"\nLargest Family (Size: {max_size}):" + Style.RESET_ALL)
        for id in largest_tree:
            print(user_info.get(str(id), "Unknown"))  # Affiche le nom de la personne à partir de son ID
    else:
        print("No connected tree found.")
























































def get_descendants(tree, person_id):
    descendants = set()

    # Fonction récursive pour récupérer tous les descendants
    def recursive_descendants(current_id):
        if current_id in tree:
            for parent_id, child_ids in tree.items():
                if current_id in child_ids:
                    descendants.add(parent_id)
                    recursive_descendants(parent_id)

    recursive_descendants(person_id)
    return descendants


def delete_node_and_descendants(id, tree, user_info):
    has_spouse = bool(getSpouse(tree, id))

    descendants = get_descendants(tree, id)

    if descendants:
        print("Deleting descendants...")
        for descendant_id in descendants:
            delete_node_and_descendants(descendant_id, tree, user_info)

    print(f"Deleting person {user_info.get(str(id), 'Unknown')} and their descendants...")
    delete_person(id, tree)
    print(f"Person {user_info.get(str(id), 'Unknown')} and their descendants have been deleted.")

    # Remove person from users.csv
    remove_person_from_csv(id)
    print(f"Person {user_info.get(str(id), 'Unknown')} has been removed from users.csv.")


def delete_person(id, tree):
    if id in tree:
        del tree[id]
    for person, parents in tree.items():
        if parents[0] == id:
            parents[0] = 0
        if parents[1] == id:
            parents[1] = 0


def remove_person_from_csv(id):
    csv_file = 'users.csv'
    temp_file = 'users_temp.csv'

    with open(csv_file, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)
        
        for row in reader:        
            if row[0] == 'id' or int(row[0]) != id:
                writer.writerow(row)

    os.remove(csv_file)
    os.rename(temp_file, csv_file)













def connected(id, admin):    # Display the menu when you are connected

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
    print("(10) look-up your ancestry and descndants")
    print("(11) look-up family ties")
    print("(12) look-up persons without ancestry")
    print("(13) look-up persons without descendants")
    print("(14) look-up persons with the most ancestry alive")

    if admin == 'y':
            print(Fore.YELLOW + " -- ADMIN --" + Style.RESET_ALL)
            print("(15) deleting a node and its descendants")
            print("(16) track the evolution of family tree size.")  
            print("(17) find the most represented family in the global tree")  

    print(Fore.RED + "(0) Quit" + Style.RESET_ALL)
    
    # Info collection for different cases
    user_info = load_user_info('users.csv')
    familyTree = csvToTree()
    id = int(id)

    # Run the choice 
    while True:
        choice = input("\nEnter your choice: ")

        if choice == '1':   # add a parent
            addParent(familyTree,id)
                
        elif choice == '2':     # add a child 
            addChild(familyTree,id)

        elif choice == '3':     # delete yourself 
            deleteYourself(id, familyTree)
            treeToCsv(familyTree)
            print(Fore.RED + "Delete successfull" + Style.RESET_ALL )
            
        elif choice == '4':     # delete a parent
            deleteParent(id, familyTree)
            treeToCsv(familyTree)
            print(Fore.RED + "Delete successfull" + Style.RESET_ALL )
            
        elif choice == '5':     # delete a child
            deleteChild(id, familyTree)
            treeToCsv(familyTree)
            print(Fore.RED + "Delete successfull" + Style.RESET_ALL )

        elif choice == '6':     # look-up the entire tree
            print_all_connected_trees()

        elif choice == '7':     # look-up your family tree  
            printFamilyTree(familyTree, id, user_info)
            printDescendants(familyTree, id, user_info)


            """print_connected_names(id, familyTree, user_info)"""
            
        elif choice == '8':     # look-up your descendants 
            printDescendants(familyTree, id, user_info)

        elif choice == '9':     # look-up your ancestry
            printAncestry(familyTree, id, user_info)
            
        elif choice == '10':     # look-up ancestry and descendants
            printAncestry(familyTree, id, user_info)
            printDescendants(familyTree, id, user_info)

        elif choice == '11':     # look-up a family ties
           lookupFamilyTies(familyTree, id, user_info)

        elif choice == '12':     # look-up persons without ancestry
            print(Fore.YELLOW + "\nPersons with no recorded ancestry: " + Style.RESET_ALL)
            printPersonFromId(noAncestry(familyTree))
            
        elif choice == '13':     # look-up persons without descendants
            print(" ")
            print(Fore.YELLOW + "\nPersons with no recorded descendants: " + Style.RESET_ALL )
            printPersonFromId(noDescendants(familyTree))
            
        elif choice == '14':     # look-up persons with the most ancestry alive
            mostAncestryAlive(familyTree, user_info)

        elif choice == '15' and admin == 'y':       # deleting a node and its descendants
            delete_node_and_descendants(id, familyTree, user_info)
            


        elif choice == '16' and admin == 'y':       # track the evolution of family tree size.
            treeSize(familyTree)

        elif choice == '17' and admin == 'y':       # find the most represented family in the global tree
            print_largest_connected_tree()
        
        elif choice == '0':     # Quit
            treeToCsv(familyTree)
            break

    
def csvToTree():    # Initialise the whole family tree from links.csv
    family_tree = {}
    
    file_path = 'links.csv'

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = list(map(int, line.strip().split(',')))
                
                family_tree[parts[0]] = parts[1:]
    
    return family_tree



def treeToCsv(family_tree):
    file_path = 'links.csv'

    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for person, parents in family_tree.items():
            csv_writer.writerow([person] + parents)




#print(familyTree)
#print_family_tree(family_tree, 6, user_info)
menu()
#addParent(familyTree,11)

"""familyTree = csvToTree()
print("Les id connexes: ",connex(familyTree, 1))
treeSize(familyTree)"""
