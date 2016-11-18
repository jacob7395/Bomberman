class Class_Factory:
    """Class factory to dinamicly generate classes with uniqe ID values."""

    def __init__(self, name_Wanted, base_Class):
        """Init functions requreing class name and base calls."""
        self.classID = 0
        self.name = name_Wanted
        self.baseClass = base_Class

    def New(self, *args):
        """Generate new class and incroment ID."""
        name = self.name + str(self.classID)
        self.classID += 1
        name = type(name, (self.baseClass,), {})

        new_Class = self.baseClass(*args)
        new_Class.__class__ = name
        new_Class.__name__ = self.name + str(self.classID)
        new_Class.ID = self.classID
        return new_Class
