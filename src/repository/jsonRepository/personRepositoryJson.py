from src.repository.baseRepository.personRepository import PersonRepository
from src.domain.person import Person
import json
import os


class PersonRepositoryJson(PersonRepository):
    def __init__(self, file_name):
        PersonRepository.__init__(self)
        self.file_name = file_name
        file = open(self.file_name, "r")
        if os.stat(file_name).st_size != 0:
            for obj in json.load(file):
                self.add_person(Person(int(obj["person_id"]), obj["name"], obj["phone_number"]))
            file.close()

    def _save_file(self):
        """
        Method for saving persons to a CSV file
        :return:
        """
        file = open(self.file_name, "w")
        json.dump([x.to_dict() for x in self._person_list], file, indent=4)
        file.close()

    def add_person(self, person):
        """
        Method for adding a person to a CSV file
        :param person:
        :return:
        """
        PersonRepository.add_person(self, person)
        self._save_file()

    def remove_person(self, person_id):
        """
        Method for removing a person from a CSv file
        :param person_id:
        :return:
        """
        PersonRepository.remove_person(self, person_id)
        self._save_file()

    def update_person(self, person_id, name, phone_number):
        """
        Method for updating a person on a CSV file
        :param person_id:
        :param name:
        :param phone_number:
        :return:
        """
        PersonRepository.update_person(person_id, name, phone_number)
        self._save_file()
