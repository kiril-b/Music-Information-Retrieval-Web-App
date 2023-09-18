class DatabaseError(Exception):
    """Exception raised for database-related errors."""

    def __init__(self, message="A database error occurred"):
        self.message = message
        super().__init__(self.message)
    

class InvalidAttributeCombination(Exception):
    def __init__(self, message="Wrong combination of attributes passed"):
        self.message = message
        super().__init__(self.message)
