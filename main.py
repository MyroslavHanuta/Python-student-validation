from tabulate import tabulate # importing library "tabulate"
from datetime import datetime # import date for calculating age
from pathlib import Path # importing library for reading files
import re # importing lib to check name

# Validation functions -------------------------------------------

# ID validation --------------------------------------------------
def id_validation(id_number):
    if id_number.isdigit(): # check is it digit
        if len(id_number) >= 2: return 1 # check is it more than 2 elements
        else:
            print("Entered ID value is less than 2 digits") # Error throws
            return 0
    else:
        print("Entered ID value is not a digit") # Error throws
        return 0
# ----------------------------------------------------------------

# Name validation ------------------------------------------------
def name_validation(name_string):
    # ^ - start of the string
    # a-z and A-Z - lower and upper case
    # \s any kind of white space
    # * in combination with \s allow zero or more time
    # \ slash
    # ' Apostrophe
    # - dash
    # [] - set of characters
    # $ - end of the string

    # + means one or more of the proceeding character must exist
    pattern = r"^[a-zA-Z\s\-']+$"

    if len(name_string.split(" ")) < 2:
        print("Entered name is do not have name and Surname") # Error throws
        return 0
    else:
        if re.fullmatch(pattern, name_string): # checking for full match
            return 1
        else:
            print("Entered name does not match pattern") # Error throws
            return 0
# -----------------------------------------------------------------

# Module name validation ------------------------------------------
def module_name_validation(name_string):
    # ^ - start of the string
    # a-z and A-Z - lower and upper case
    # \s any kind of white space
    # * in combination with \s allow zero or more time
    # 0-9 numbers from 0 to 9
    # [] - set of characters
    # $ - end of the string

    # + means one or more of the proceeding character must exist
    pattern = r"^[a-zA-Z\s0-9]+$"

    if re.fullmatch(pattern, name_string): return 1 # check for a full match
    else:
        print("\nEntered module name have unintended symbols\n")# Error throws
        return 0
# --------------------------------------------------------------------

# Date of Birth validation -------------------------------------------
def date_of_birth_validation(date,student_database):#
    try:
        dob_date = datetime.strptime(date, "%Y-%m-%d").date() # format to pattern xxxx-xx-xx
    except ValueError:
        print("Entered date pattern is not valid") # Error throws
        return 0
    else:
        # date can not be larger than current date
        if dob_date > datetime.now().date():
            print("Entered date is greater than current date") # Error throws
            return 0
        else:
            student_database["age"] = determine_age(dob_date)
            return 1
        # ----------------------------------------
# -----------------------------------------------------------------------

# Mark validation -------------------------------------------------------
def mark_validation(mark):
    try: mark = int(mark)
    except ValueError: print("Entered mark is not an integer") # Error throws
    else:
        if mark < 0 or mark > 100:
            print("This is not a number or it is out of range, please try again.") # Error throws
            return 0
        else: return 1
# ------------------------------------------------------------------------

# Module weight validation -----------------------------------------------
def module_weight_validation(weight_list):
    weight_check = 0
    for weight in weight_list:
        weight_check += weight
    if weight_check != 100:
        print("Entered weight is more or less than 100") # Error throws
        return 0
    else: return 1
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

# Function to read file ---------------------------------------------------
def advanced(list_of_students, module_info):
    # get current .py file path
    current_path = Path.cwd()
    # -------------------------

    # Checking for path to exist --------------------
    if current_path.exists():
        if current_path.is_dir():
            print("Path successfully found")
        else:
            print("Current path is not a directory")
    else:
        print("Current path does not exist")
    print("\nChecking for files...\n")
    # -----------------------------------------------

    # Printing founded result -----------------------
    files = list(current_path.glob("*.txt")) # looking for all files ends with .txt
    for index, file in enumerate(files):
        print(f"{file.name}, {index}") # print them
    # -----------------------------------------------

    # We ask user what file we need to open ---------
    while True:
        decision = input("\nIf you want to use any of items listed above please enter number, if not enter 'No': ")
        try:
            decision = int(decision)
            if decision > len(files) - 1: raise IndexError
            elif decision < 0: raise IndexError
        except ValueError:
            if decision == "No":
                print("\nNo file selected")
                print("\nEnding programme")
                return 0
            else: print("\nEntered value is not an integer or not equal 'No'")
        except IndexError: print("\nEntered value is larger or less than listed range")
        else: break
    # -----------------------------------------------

    print(f"\nProcessing file {files[decision].name} Please be sure that items in you file in separated by ','", "\n")

    # Open selected file ----------------------------
    with open(files[decision], "r") as input_file:

        for list_index, line in enumerate(input_file): # we use enumerate to get line and index of loop

            # variables ------------------------------------------
            student_database = {} # dictionary to hold information
            line_list_items = line.split(",") # get every line
            # ----------------------------------------------------

            # Check for empty line -------------------------------
            if len(line_list_items) <= 1:
                print(f"Data in {files[decision].name} Error")
                continue
            # ----------------------------------------------------

            # Check for exact amount of values in line -----------
            if module_info["custom"]:
                if len(line_list_items) != 3 + module_info["loop"]:
                    print(f"Line {list_index} corrupted")
                    continue
            else:
                if len(line_list_items) != 7:
                    print(f"Line {list_index} corrupted")
                    continue
            # ----------------------------------------------------

            # Get student information ----------------------------
            if not get_student_information_file(student_database, line_list_items, module_info):
                # The validation function inside printed the error, so we skip to the next line.
                print(f"(Line {list_index} skipped due to validation error)")
                continue
            # ----------------------------------------------------

            # Check if some information missing in database ------
            if module_info["custom"]:
                if len(student_database) != 4 + module_info["loop"]:
                    print(f"Line {list_index} corrupted")
                    continue
                else:
                    calculate_overall_scores_multiple(student_database, module_info)
                    determine_category(student_database)
                    list_of_students.append(student_database)
            # ----------------------------------------------------

            # Check if some information missing in database ------
            else:
                if len(student_database) != 8:
                    print(f"Line {list_index} corrupted")
                    continue
                else:
                    calculate_overall_scores(student_database)
                    determine_category(student_database)
                    list_of_students.append(student_database)
            # ----------------------------------------------------
    # ----------------------------------------------------
# -------------------------------------------------------------------------

# Getting information from file -----------------------------------------------------------
def get_student_information_file(student_database, line_list_items, module_info):

    # Getting ID -------------------------------------------
    storage = line_list_items[0].strip()

    if id_validation(storage): student_database["ID"] = storage
    else: return 0
    # ------------------------------------------------------

    # Getting name -----------------------------------------
    storage = line_list_items[1].strip()

    if name_validation(storage): student_database["name"] = storage
    else: return 0
    # -------------------------------------------------------

    # Getting Date of Birth ---------------------------------
    storage = line_list_items[2].strip()

    if date_of_birth_validation(storage, student_database): student_database["DoB"] = storage
    else: return 0
    # --------------------------------------------------------

    # Getting marks ------------------------------------------
    if module_info["custom"]:
        for mark_index, i in enumerate(range(3, 3 + module_info["loop"])):
            storage = line_list_items[i].strip()
            if mark_validation(storage): student_database[f"test{mark_index+1}"] = int(storage)
            else: return 0

    else:
        for mark_index, i in enumerate(range(3, 7)):
            storage = line_list_items[i].strip()
            if mark_validation(storage): student_database[f"test{mark_index+1}"] = int(storage)
            else: return 0
    # ---------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Calculation overall score --------------------------------------------
def calculate_overall_scores(student_database): # Calculation for standard pattern
    student_database["overall_raw"] = student_database["test1"] * 0.10 + student_database["test2"] * 0.20 + student_database["test3"] * 0.30 + student_database["test4"] * 0.40
    return None
# ----------------------------------------------------------------------

# Calculation overall score if user enter custom module ----------------
def calculate_overall_scores_multiple(student_database, module_info): # Calculation for custom pattern
    overall_raw = 0
    for i in range(module_info["loop"]):
        overall_raw += student_database[f"test{i+1}"] * (module_info[f"weight{i+1}"] / 100)
    student_database["overall_raw"] = overall_raw
    return None
# ----------------------------------------------------------------------

# Determine category and get rounded score --------------------------------
def determine_category(student_database):
    overall_raw = student_database["overall_raw"]

    if 0 <= overall_raw <= 2.4:
        student_database["category"] = "No Submission"
        student_database["overall_round"] = 0
    elif 2.5 <= overall_raw <= 9.9:
        student_database["category"] = "Fail"
        student_database["overall_round"] = 5
    elif 10 <= overall_raw <= 19.9:
        student_database["category"] = "Fail"
        student_database["overall_round"] = 15
    elif 20 <= overall_raw <= 28.4:
        student_database["category"] = "Fail"
        student_database["overall_round"] = 25
    elif 28.5 <= overall_raw <= 33.4:
        student_database["category"] = "Condonable Fail"
        student_database["overall_round"] = 32
    elif 33.5 <= overall_raw <= 36.4:
        student_database["category"] = "Condonable Fail"
        student_database["overall_round"] = 35
    elif 36.5 <= overall_raw <= 39.9:
        student_database["category"] = "Condonable Fail"
        student_database["overall_round"] = 38
    elif 40 <= overall_raw <= 43.4:
        student_database["category"] = "Third"
        student_database["overall_round"] = 42
    elif 43.5 <= overall_raw <= 46.4:
        student_database["category"] = "Third"
        student_database["overall_round"] = 45
    elif 46.5 <= overall_raw <= 49.9:
        student_database["category"] = "Third"
        student_database["overall_round"] = 48
    elif 50 <= overall_raw <= 53.4:
        student_database["category"] = "Lower Second"
        student_database["overall_round"] = 52
    elif 53.5 <= overall_raw <= 56.4:
        student_database["overall_round"] = 55
        student_database["category"] = "Lower Second"
    elif 56.5 <= overall_raw <= 59.9:
        student_database["category"] = "Lower Second"
        student_database["overall_round"] = 58
    elif 60 <= overall_raw <= 63.4:
        student_database["category"] = "Upper Second"
        student_database["overall_round"] = 62
    elif 63.5 <= overall_raw <= 66.4:
        student_database["category"] = "Upper Second"
        student_database["overall_round"] = 65
    elif 66.5 <= overall_raw <= 69.9:
        student_database["category"] = "Upper Second"
        student_database["overall_round"] = 68
    elif 70 <= overall_raw <= 73.4:
        student_database["category"] = "First"
        student_database["overall_round"] = 72
    elif 73.5 <= overall_raw <= 76.4:
        student_database["category"] = "First"
        student_database["overall_round"] = 75
    elif 76.5 <= overall_raw <= 79.9:
        student_database["category"] = "First"
        student_database["overall_round"] = 78
    elif 80 <= overall_raw <= 83.4:
        student_database["category"] = "Upper First"
        student_database["overall_round"] = 82
    elif 83.5 <= overall_raw <= 88.4:
        student_database["category"] = "Upper First"
        student_database["overall_round"] = 85
    elif 88.5 <= overall_raw <= 95.9:
        student_database["category"] = "Upper First"
        student_database["overall_round"] = 92
    elif 96 <= overall_raw <= 100:
        student_database["category"] = "Gold Standard"
        student_database["overall_round"] = 100
    return None
# ---------------------------------------------------------------------------------

# Determine age according to the provided date of birth ------------------------------------------------
def determine_age(dob_date):

    age = datetime.now().year - dob_date.year # Now after all checks we need to calculate age basic thing is just subtract

    # if the entered date is larger than current we will subtract from age 1
    if (datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day):
        age -= 1

    return age
# -------------------------------------------------------------------------------------------------------

# Print function --------------------------------------------------------
def print_information(list_of_students, module_info):

    database_for_tabulate = [] # we use it to print data in table
    temp_list = [] # list if module custom

    list_of_students.sort(key=lambda student: int(student["ID"])) # sort list by ID values

    # choosing header title, and filling database depends on what user selection -------------
    if module_info["custom"]:
        header_titles = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category", module_info["module"]]
        for j in range(module_info["loop"]):
            temp_list.append(module_info[f"component{j + 1}"])
    else:
        header_titles = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category"]

    for i in range(len(list_of_students)):
        database = [list_of_students[i]["ID"], list_of_students[i]["name"],
                    list_of_students[i]["DoB"], list_of_students[i]["age"],
                    list_of_students[i]["overall_raw"], list_of_students[i]["overall_round"],
                    list_of_students[i]["category"]]
        if module_info["custom"]:
            database.append(temp_list)
        database_for_tabulate.extend([database])
    # ----------------------------------------------------------------------------------------

    print(tabulate(database_for_tabulate, headers=header_titles)) # print into terminal

    # print into file ------------------------------------------------------------------------
    decision_print = input("\n Do you want to write this data into file student_grades.txt?(y/n) ")
    if decision_print.lower() == "y":
        with open("student_grades.txt", "w") as output_file:
            output_file.write(tabulate(database_for_tabulate, headers=header_titles))

    elif decision_print.lower() == "n":
        print("\nThank you for using this program")
        return 0
    else:
        print("\nPlease enter a valid input")
    # -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------


def get_student_information(student_database, module_info):

    # ID input ---------------------------------------------------------------------------------
    while True: # We check if entered ID is real integer and if it is end if not we repeat
        temp_variable_holder = input("\nEnter student ID: ").strip() # Get information from user about studen ID

        # when exit from function ----------
        if temp_variable_holder == "end": return 0
        # ----------------------------------

        if id_validation(temp_variable_holder):
            student_database["ID"] = temp_variable_holder
            break
        # ----------------------------------------


    # -------------------------------------------------------------------------------------------

    # Name input --------------------------------------------------------------------------------
    while True:
        # We get input and split it for future check
        temp_variable_holder = input("\nEnter student name: ").strip()

        if name_validation(temp_variable_holder):
            student_database["name"] = temp_variable_holder
            break
    # --------------------------------------------------------------------------------------------

    # Date of Birth input ------------------------------------------------------------------------
    while True:
        # Get input --------------------------------
        temp_variable_holder = input("\nEnter student date of birth YEAR-MONTH-DAY : ").strip()
        # ------------------------------------------

        if date_of_birth_validation(temp_variable_holder,student_database):
            student_database["DoB"] = temp_variable_holder
            break
    # ---------------------------------------------------------------------------------------------

    # Get coursework information ------------------------------------------------------------------
    if module_info["custom"]:
        for i in range(module_info["loop"]):
            while True:
                student_database[f"test{i+1}"] = input(f"\nEnter student mark for {module_info[f"component{i+1}"]}: ").strip()
                if mark_validation(student_database[f"test{i+1}"]):
                    student_database[f"test{i+1}"] = int(student_database[f"test{i+1}"])
                    break
    else:
        for i in range(4):
            while True:
                student_database[f"test{i+1}"] = input(f"\nEnter student mark for Coursework {i+1}: ")
                if mark_validation(student_database[f"test{i+1}"]):
                    student_database[f"test{i+1}"] = int(student_database[f"test{i+1}"])
                    break
    # --------------------------------------------------------------------------------------------

def filling_database(list_of_students, module_info):

    print("Welcome to the Student Grading System First, let's set up the module configuration\n")

    # Getting information how user want to define assessment -------------------------------------
    while True: # While to get correct information from user

        # Decision -------------------------------------------------------------------------------
        setup_module_decision = input("Do you want to define the assessment criteria or use standard pattern?(standard/custom) ").strip().lower()
        print("")
        # ----------------------------------------------------------------------------------------

        if setup_module_decision == "standard":
            print("Coursework 1: 10%")
            print("Coursework 2: 20%")
            print("Coursework 3: 30%")
            print("Coursework 4: 40%\n")

            module_info["custom"] = False # We will use it for decision
            break

        elif setup_module_decision == "custom":

            # Get module name -----------------------------------------------------------------
            while True:
                module_info["module"] = input("Enter module name: ").strip()
                if module_name_validation(module_info["module"]): break # check for correct name
            # ---------------------------------------------------------------------------------

            # Setting up counter which we will use for count how much components --------------
            while True:
                try: module_info["loop"] = int(input("\nHow much assessment components does this module have? ").strip())
                except ValueError: print("\nEntered value is not a number\n") # Catching errors
                else: break
            # ---------------------------------------------------------------------------------

            # Getting details of each component -----------------------------------------------
            while True:

                # Initialization list which will be used in this part only -----------------------------
                module_weight = []  # list to store percentage of each component
                # ---------------------------------------------------------------------------------

                for i in range(module_info["loop"]): # filling exact amount of components as user said

                    # Part to get component name, we also use construction f"something{i+1}" to make tracking more common
                    while True:
                        module_info[f"component{i + 1}"] = input(f"\nComponent {i + 1} name: ").strip()
                        if module_name_validation(module_info[f"component{i + 1}"]): break
                    # ---------------------------------------------------------------------------------------------------

                    # Getting weight of each component ------------------------------------------------------------------
                    try: module_weight.append(int(input(f"\nComponent{i + 1} weight (%): ").strip()))
                    except ValueError: print("Entered value is not a number") # Catching non value error
                    # ---------------------------------------------------------------------------------------------------

                # We check after getting all weight numbers, to check if percentage equal 100, because we need all weight
                if module_weight_validation(module_weight):
                    for j in range(module_info["loop"]): # after checking write data into student database
                        module_info[f"weight{j + 1}"] = module_weight[j]
                    module_info["custom"] = True  # We will use it for decision
                    break # break from "Getting details of each component"
            # --------------------------------------------------------------------------------------------

            # ---------------------------------------------------------------------------------------
            break # break from "While to get correct information from user"

        else: print("Please enter a valid choice.") # We can not proceed if entered value is wrong
    # --------------------------------------------------------------------------------------------

    # Block of code to choose how to process data -------
    choose_programme_type = input("\nHow do you want to run the programme? File or enter manually? (file/manually): ").strip().lower()
    print("")

    if choose_programme_type == "file":

        if not advanced(list_of_students, module_info): return 0 # Question for now

    elif choose_programme_type == "manually":
        while True:
            student_database = {}

            get_student_information(student_database, module_info)  # Fill basic information
            if not student_database: return 0  # Condition to exit we check for empty because, if user enter end it just return and do not assign any values

            if not module_info["custom"]: calculate_overall_scores(student_database) # calculate score
            else: calculate_overall_scores_multiple(student_database, module_info)

            determine_category(student_database)
            list_of_students.append(student_database)
    else :
        print("Entered value is incorrect, programme interrupted")
        return 0
    # ----------------------------------------------------

def main():

    # Initiate variables -----------------------------
    list_of_students = []  # this list will hold student_databases
    module_info = {} # dictionary which will be used if user want custom pattern
    # ------------------------------------------------

    # Filling database -------------------------------
    filling_database(list_of_students, module_info)
    # ------------------------------------------------

    # Output information -----------------------------
    print_information(list_of_students, module_info)
    # Output information -----------------------------
    
if __name__ == '__main__':
    main()