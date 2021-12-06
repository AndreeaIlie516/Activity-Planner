from src.domain.person import Person
from src.repo.personRepository import PersonRepository
from src.exception.exception import PersonServiceException
from src.service.activityService import ActivityService
from src.service.undoService import *
import random
import re


class PersonService:
    def __init__(self, person_repository, activity_repository, undoController=False, generate=False):
        self._person_repository = person_repository
        self._activity_repository = activity_repository
        # activity_service = ActivityService(person_repository, activity_repository, self, undoController)
        self._activity_service = ActivityService(person_repository, activity_repository, self, undoController)
        if generate:
            self._person_repository = PersonRepository(self.generate_person())
        self._undoController = undoController

    @property
    def persons(self):
        return self._person_repository.persons

    def generate_person(self):
        """
        Function for generating persons
        """
        persons = []
        names = self.list_of_names()
        for i in range(0, 20):
            name = random.choice(names)
            names.remove(name)
            person_id = random.randint(1000, 9999)
            while person_id in [x.person_id for x in persons]:
                person_id = random.randint(1000, 9999)
            phone_number = "07"
            for digit in range(0, 8):
                phone_number = phone_number + str(random.randint(0, 9))
            persons.append(Person(person_id, name, phone_number))
        return persons

    def add_person(self, person_id, name, phone_number, activity_list):
        """
        Function for adding a person to the class
        """
        person = Person(person_id, name, phone_number)
        if self._person_repository.find_person_by_id(person_id):
            raise PersonServiceException("Person with the ID " + str(person_id) + " already exists!\n")
        if self._person_repository.find_person_by_phone_number(phone_number):
            raise PersonServiceException("Person with the phone number " + str(phone_number) + " already exists!\n")

        if self._undoController is not False:
            undo = FunctionCall(self.remove_person, person.person_id, activity_list)
            redo = FunctionCall(self.add_person, person_id, name, phone_number, activity_list)
            op = Operation(undo, redo)
            self._undoController.recordOperation(op)

        self._person_repository.add_person(person)

    # TODO: check activity by removing a person
    def remove_person(self, person_id, activity_list):
        """
        Function for removing a person from the class
        """
        person = self._person_repository.find_person_by_id(person_id)
        if not person:
            raise PersonServiceException("There is no person with the ID " + str(person_id) + "!\n")

        self._activity_service.remove_person_activities(person_id, activity_list)

        if self._undoController is not False:
            undo_person = FunctionCall(self.add_person, person.person_id, person.name, person.phone_number)
            redo_person = FunctionCall(self.remove_person, person_id, activity_list)
            op_person = Operation(undo_person, redo_person)
            undo_activity = FunctionCall(
                self._activity_service.add_person_activities, person_id, activity_list)
            redo_activity = FunctionCall(self._activity_service.remove_person_activities, person_id, activity_list)
            op_activity = Operation(undo_activity, redo_activity)
            self._undoController.recordOperation(op_activity)

        self._person_repository.remove_person(person)

    def update_person(self, person_id, name, phone_number):
        """
        Function for updating a person in the class
        """
        person = self._person_repository.find_person_by_id(person_id)
        if not person:
            raise PersonServiceException("There is no person with the ID " + str(person_id) + "!\n")

        if self._undoController is not False:
            undo = FunctionCall(self.update_person, person.person_id, person.name, person.phone_number)
            redo = FunctionCall(self.update_person, person_id, name, phone_number)
            op = Operation(undo, redo)
            self._undoController.recordOperation(op)

        self._person_repository.update_person(person_id, name, phone_number)

    def search_person_by_name(self, name):
        """
        Function for searching to a person by its name
        """
        return [person for person in self._person_repository.persons if re.search(name, person.name, re.IGNORECASE)]

    def search_person_by_phone_number(self, phone_number):
        """
        Function for searching for a person by its phone number
        """
        return [person for person in self._person_repository.persons if
                re.search(phone_number, person.phone_number, re.IGNORECASE)]

    @staticmethod
    def list_of_names():
        list_of_names = [
            "Jacob Fletcher",
            "Morgan McLean",
            "Lydia Boyle",
            "Courtney Norton",
            "Aidan Griffiths",
            "Louie Wheeler",
            "Sam Brady",
            "Paige Lamb",
            "Joseph Carter",
            "Erin Nelson",
            "Alexander Wong",
            "Isabelle Goddard",
            "Elise Faulkner",
            "Freddie Mitchell",
            "Katherine Allan",
            "Leon Matthews",
            "Elizabeth Herbert",
            "Sarah Mellor",
            "Hollie Farmer",
            "Jennifer Barton",
            "Henry Stevenson",
            "Aaliyah Simmons",
            "Michael Dickinson",
            "Louie Weston",
            "Daisy Clements",
            "Riley Garner",
            "Cameron Reed",
            "Jasmine Coleman",
            "Katherine Sanderson",
            "Daniel Hall"
        ]
        return list_of_names
