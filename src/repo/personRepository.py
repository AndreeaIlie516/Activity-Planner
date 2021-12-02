class PersonRepository:
    def __init__(self, person_list=None):
        if person_list is None:
            person_list = []
        self._person_list = person_list

    @property
    def persons(self):
        return self._person_list

    @staticmethod
    def filter(iterable, accept):
        """
        Method for filtering different things
        """
        new_list = type(iterable)()
        for x in iterable:
            if accept(x):
                new_list.append(x)
        return new_list

    def find_person_by_id(self, person_id):
        """
        Method for finding a person by its id
        """
        aux = self.filter(self._person_list, lambda x: x.person_id == person_id)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def find_person_by_name(self, name):
        """
        Method for finding a person by its name
        """
        aux = self.filter(self._person_list, lambda x: x.name == name)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def find_person_by_phone_number(self, phone_number):
        """
        Method for finding a person by its phone number
        """
        aux = self.filter(self._person_list, lambda x: x.phone_number == phone_number)
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
        Function for removing a person from the class
        """
        self._person_list.remove(person)

    def update_person(self, person_id, name, phone_number):
        """
        Function for updating a person in the class
        """
        person = self.find_person_by_id(person_id)
        person.name = name
        person.phone_number = phone_number
