# First-part Imports
from employee import Employee


class CSVProcessor:
    """CSV Processor Class to read and process an employee csv file."""

    # No Constructor as we do not need to accept any parameters or set any
    # class level variables. But, this does not mean that we can't do that
    # in the event that we do need something.

    def import_csv(self, path_to_csv_file, employee_list):
        """Accept a path to a csv file, then read the file in and process it
        into a list of employee instances"""

        # With open of file
        with open(path_to_csv_file, "r") as file:
            # Priming line read
            line = file.readline()
            # While the line is not None
            while line:
                # Process the line.
                self._process_line(line, employee_list)
                # Read next line.
                line = file.readline()

    def _process_line(self, line, employee_list):
        """Process a line from a CSV file"""

        # Split line by comma
        parts = line.split(",")

        # Assign each part to a var
        first_name = parts[0]
        last_name = parts[1]
        weekly_salary = float(parts[2])

        # Add a new beverage to the collection with the properties of what was read in.
        employee_list.append(Employee(first_name, last_name, weekly_salary))
