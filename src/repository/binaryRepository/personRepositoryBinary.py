from src.domain.person import Person
from src.repository.baseRepository.personRepository import PersonRepository
import pickle
import os

class PersonRepositoryBinary(PersonRepository):
    def __init__(self, file_name):

        PersonRepository.__init__(self)
        self.file_name = file_name
        if os.stat(file_name).st_size != 0:
            file = open(self.file_name, "rb")
            for obj in pickle.load(file):
                self.add_person(Person(int(obj["person_id"]), obj["name"], obj["phone_number"]))
            file.close()

    def _save_file(self):
        """
        Method for saving persons to a file in binary form
        :return:
        """
        file = open(self.file_name, "wb")
        pickle.dump([x.to_dict() for x in self._person_list], file)
        file.close()

    def add_person(self, person):
        """
        Method for adding a person to a binary file
        :param person:
        :return:
        """
        PersonRepository.add_person(self, person)
        self._save_file()

    def update_person(self, person_id, name, phone_number):
        """
        Method for updating a person to a binary file
        :param person_id:
        :param name:
        :param phone_number:
        :return:
        """
        PersonRepository.update_person(self, person_id, name, phone_number)
        self._save_file()

    def remove_person(self, person):
        """
        Method for removing a person to a binary file
        :param person:
        :return:
        """
        PersonRepository.remove_person(self, person)
        self._save_file()
