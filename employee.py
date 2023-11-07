class Employee:
    """Class to represent a single employee"""

    WEEKS_PER_YEAR = 52

    def __init__(self, first_name, last_name, weekly_salary):
        """Constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.weekly_salary = weekly_salary

    def __str__(self):
        """String method"""
        return f"{self.first_name:<10} {self.last_name:<20} {self.formatted_weekly_salary:>14}"

    def first_and_last_name(self):
        """Return first and last name concatenated together"""
        return f"{self.first_name:<10} {self.last_name:<20}"

    @property
    def formatted_weekly_salary(self):
        """Property for weekly salary formatted as currency"""
        return f"${self.weekly_salary:.2f}"

    @property
    def yearly_salary(self):
        """Property for yearly salary"""
        return self.weekly_salary * self.WEEKS_PER_YEAR

    @property
    def formatted_yearly_salary(self):
        """Property for yearly salary formatted as currency"""
        return f"${self.yearly_salary:.2f}"

    def apply_percentage_raise(self, percentage):
        """Accept a percentage raise and apply it to the weekly salary"""
        self.weekly_salary = self.weekly_salary * (1 + (percentage / 100))
