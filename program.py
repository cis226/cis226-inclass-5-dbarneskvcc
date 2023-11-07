"""Program code"""

# System Imports
import os

# First-Party imports
from employee import Employee
from user_interface import UserInterface
from utils import CSVProcessor


def main(*args):
    """Method to run program"""

    # Make a new instance of Employee class
    # my_employee = Employee(None, None, None)

    # my_employee.first_name = "David"
    # my_employee.last_name = "Barnes"
    # my_employee.weekly_salary = 2453.45

    # print(my_employee)

    # my_employee = Employee("Joe", "Somebody", 345.56)

    # print(my_employee)

    # The above code was just for demo.
    # The actual program will be using the array defined below.
    # TODO: The above lines can be removed or commented when program is finished.

    employees = []
    # employees.append(Employee("David", "Barnes", 835.00))
    # employees.append(Employee("James", "Kirk", 453.00))
    # employees.append(Employee("Jean-Luc", "Picard", 290.00))
    # employees.append(Employee("Benjamin", "Sisko", 587.00))
    # employees.append(Employee("Kathryn", "Janeway", 184.00))
    # employees.append(Employee("Jonathan", "Archer", 135.00))

    # Make a new instance of the UserInterface class
    ui = UserInterface()

    # Path to CSV file
    path_to_csv_file = "employees.csv"

    # Make new instance of CSVProcessor class
    csv_processor = CSVProcessor()

    # Reading the CSV file could raise exceptions. Be sure to catch them.
    try:
        # Call the import_csv method sending in our path to the csv and the Employee list.
        csv_processor.import_csv(path_to_csv_file, employees)
    except FileNotFoundError:
        ui.print_file_not_found_error()
    except EOFError:
        ui.print_empty_file_error()

    # Get some input from the user
    selection = ui.display_menu_and_get_response()

    # While the choice they selected is not 2, continue to do work.
    while selection != ui.MAX_MENU_CHOICES:
        # See if the input they sent is equal to 1.
        if selection == 1:
            # Create string for concatenation
            output_string = ""

            # Convert each employee to a string and add it to the outputstring
            for employee in employees:
                # Concatenate to the output_string
                output_string += f"{employee}{os.linesep}"

            # Use the UI class to print out the string
            ui.print_list(output_string)

        # Check for different choice here if there was one to check.

        # Lastly, re-prompt user for input on what to do.
        selection = ui.display_menu_and_get_response()
