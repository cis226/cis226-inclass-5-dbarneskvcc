"""Program code"""

# System Imports
import os

# Third-Part imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# First-Party imports
from employee import Base, Employee
from user_interface import UserInterface
from utils import CSVProcessor


def main(*args):
    """Method to run program"""

    # Make a new instance of the UserInterface class
    ui = UserInterface()

    # Path to CSV file
    path_to_csv_file = "employees.csv"

    # Make new instance of CSVProcessor class
    csv_processor = CSVProcessor()

    # If we do not have the database, we can create it.
    if not os.path.exists("./db.sqlite3"):
        # Create the database
        create_database()

        # List of employees
        employees = []

        # Reading the CSV file could raise exceptions. Be sure to catch them.
        try:
            # Call the import_csv method sending in our path to the csv and the Employee list.
            csv_processor.import_csv(path_to_csv_file, employees)
        except FileNotFoundError:
            ui.print_file_not_found_error()
        except EOFError:
            ui.print_empty_file_error()

        # Populate the database with data from the CSV
        populate_database(employees)

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


# Database engine instance.
engine = create_engine("sqlite:///db.sqlite3", echo=False)
# Get the Session class by using SQLAlchemy's sessionmaker
Session = sessionmaker(bind=engine)
# Make instance of Session class.
session = Session()


def create_database():
    # Use child classes of Base class to read the attributes of each
    # child and then create database tables that contain those attributes.
    Base.metadata.create_all(engine)


def populate_database(employees):
    for employee in employees:
        session.add(employee)
        session.commit()
