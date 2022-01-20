from src.utils.utils import *


class PersonRepository:
    def __init__(self, person_list=None):
        if person_list is None:
            person_list = []
        if person_list is Container:
            self._person_list = person_list
        else:
            self._person_list = Container(person_list)

    @property
    def persons(self):
        return self._person_list

    def find_person_by_id(self, person_id):
        """
        Method for finding a person by its id
        """
        aux = custom_filter(self._person_list, lambda x: x.person_id == person_id)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def find_person_by_name(self, name):
        """
        Method for finding a person by its name
        """
        aux = custom_filter(self._person_list, lambda x: x.name == name)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def find_person_by_phone_number(self, phone_number):
        """
        Method for finding a person by its phone number
        """
        aux = custom_filter(self._person_list, lambda x: x.phone_number == phone_number)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def add_person(self, person):
        """
        Method for adding a person to the class
        """
        self._person_list.append(person)

    def remove_person(self, person):
        """
        Method for removing a person from the class
        """
        self._person_list.remove(person)

    def update_person(self, person_id, name, phone_number):
        """
        Method for updating a person in the class
        """
        person = self.find_person_by_id(person_id)
        person.name = name
        person.phone_number = phone_number
