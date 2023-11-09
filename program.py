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

# Database engine instance.
engine = create_engine("sqlite:///db.sqlite3", echo=False)
# Get the Session class by using SQLAlchemy's sessionmaker
Session = sessionmaker(bind=engine)
# Make instance of Session class.
session = Session()


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
            ###################################
            # Query and print out all entries #
            ###################################
            ui.print_text("Query and print out all entries")

            # Query out all of the entries from the database
            employees = session.query(Employee).all()

            # Create string for concatenation
            output_string = ""

            # Convert each employee to a string and add it to the outputstring
            for employee in employees:
                # Concatenate to the output_string
                output_string += f"{employee}{os.linesep}"

            # Use the UI class to print out the string
            ui.print_list(output_string)

            #####################################
            # Query single entry by primary key #
            #####################################
            ui.print_text("Query single entry by primary key")
            employee_by_pk = session.query(Employee).get(1)
            ui.print_entry(employee_by_pk)

            ##################################
            # Query single entry by criteria #
            ##################################
            ui.print_text("Query single entry by criteria")
            single_employee_by_criteria = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "Jean-Luc",
                )
                .first()
            )
            ui.print_entry(single_employee_by_criteria)

            ######################################
            # Query multiple entries by criteria #
            ######################################
            ui.print_text("Query multiple entries by criteria")
            employees_by_criteria = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.weekly_salary > 400,
                )
                .all()
            )
            output_string = ""
            for employee in employees_by_criteria:
                output_string += f"{employee}{os.linesep}"
            ui.print_list(output_string)

            ###################################
            # Add a new entry to the database #
            ###################################
            ui.print_text("Add a new entry to the database")
            # Make new instance of Employee class
            new_employee = Employee("David", "Barnes", 999.99)
            # Add employee to the database session
            session.add(new_employee)
            # Commit the work to the database
            session.commit()

            # Query and print to verify it got added.
            employees = session.query(Employee).all()
            output_string = ""
            for employee in employees:
                output_string += f"{employee}{os.linesep}"
            ui.print_list(output_string)

            ###################################
            # Update an entry in the database #
            ###################################
            ui.print_text("Update an entry to the database")
            # Fetch out employee to update.
            employee_to_update = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_update)

            # Actually do the update
            employee_to_update.last_name = "BBBBBARRRNESSSSS"
            session.commit()
            # Fetch back out of DB to verify has been updated.
            employee_to_update = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_update)

            #####################################
            # Delete an entry from the database #
            #####################################
            ui.print_text("Delete an entry from the database")
            # Find and print the thing we want to delete.
            employee_to_delete = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_delete)
            # Actually delete it from the database
            session.delete(employee_to_delete)
            session.commit()

            # Try to find the employee again. Should be gone now.
            employee_to_delete = (
                session.query(
                    Employee,
                )
                .filter(
                    Employee.first_name == "David",
                )
                .first()
            )
            ui.print_entry(employee_to_delete)
            if employee_to_delete is None:
                ui.print_text("Record successfully deleted")

            ############################################
            # Print out some raw SQL that is generated #
            ############################################
            ui.print_text(
                session.query(
                    Employee,
                ).filter(
                    Employee.first_name == "James",
                    Employee.weekly_salary > 30,
                )
                # NOTE: That I left off the `get`, `all`, or `first`
            )

        # Check for different choice here if there was one to check.

        # Lastly, re-prompt user for input on what to do.
        selection = ui.display_menu_and_get_response()


def create_database():
    # Use child classes of Base class to read the attributes of each
    # child and then create database tables that contain those attributes.
    Base.metadata.create_all(engine)


def populate_database(employees):
    for employee in employees:
        session.add(employee)
        session.commit()
