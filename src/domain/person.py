from src.exception.exception import PersonDomainException


class Person:
    def __init__(self, person_id, name, phone_number):
        """
        Create Person with person_id(the id of the person), name(the name of the person),
        phone_number(the phone number of the person)
        """
        if person_id < 1000 or person_id > 9999:
            raise PersonDomainException("Invalid person ID\n")
        self._person_id = person_id
        self._name = name
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise PersonDomainException("Invalid phone number\n")
        self._phone_number = phone_number

    def __str__(self):
        return "ID: " + str(self._person_id) + "\nName: " + str(self._name) + "\nPhone Number: " + str(
            self._phone_number) + '\n'

    def __eq__(self, other):
        return self.person_id == other.person_id

    def to_dict(self):
        return {"person_id": self._person_id, "name": self._name, "phone_number": self._phone_number}

    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return self._name

    @property
    def phone_number(self):
        return self._phone_number

    @person_id.setter
    def person_id(self, x):
        if x < 1000 or x > 9999:
            raise PersonDomainException("Invalid person ID")
        self._person_id = x

    @name.setter
    def name(self, x):
        self._name = x

    @phone_number.setter
    def phone_number(self, x):
        if len(x) != 10 or not x.isdigit():
            raise PersonDomainException("Invalid phone number")
        self._phone_number = x
