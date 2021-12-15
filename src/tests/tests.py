import unittest

from src.domain.person import Person
from src.domain.activity import Activity
from src.repository.baseRepository.activityRepository import ActivityRepository
from src.repository.baseRepository.personRepository import PersonRepository
from src.services.activityService import ActivityService
from src.services.personService import PersonService
from src.exception.exception import *
from src.services.undoService import UndoController
import datetime


class PersonDomainTest(unittest.TestCase):
    """
    Person domain test class
    """

    def test_person_domain(self):
        """
        Test function for person domain
        """
        person = Person(3564, "Mike Jordan", "0768321455")
        self.assertEqual(person.person_id, 3564)
        self.assertEqual(person.name, "Mike Jordan")
        self.assertEqual(person.phone_number, "0768321455")

        with self.assertRaises(PersonDomainException):
            Person(10, "Mike Jordan", "0768321455")
        with self.assertRaises(PersonDomainException):
            Person(1024, "Mike Jordan", "07683214")

        with self.assertRaises(PersonDomainException):
            person.person_id = 24

        person.person_id = 4563
        self.assertEqual(person.person_id, 4563)

        with self.assertRaises(PersonDomainException):
            person.phone_number = "0742"

    def test_person_representation(self):
        """
        Test function for person domain representation
        """
        person = Person(4573, "Alex Barton", "0789631456")
        self.assertEqual(str(person), "ID: 4573\nName: Alex Barton\nPhone Number: 0789631456\n")

    def test_person_equals(self):
        """
        Test function for person domain equality
        """
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(1234, "James Hetfield", "0786352410")
        person3 = Person(4256, "Dave Mustaine", "0784564213")

        self.assertEqual(person1, person2)
        self.assertNotEqual(person1, person3)


class ActivityDomainTest(unittest.TestCase):
    """
    Activity domain test class
    """

    def test_activity_domain(self):
        """
        Test function for activity domain
        """
        activity = Activity(2453, [3425, 4745, 5235], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        self.assertEqual(activity.activity_id, 2453)
        self.assertEqual(activity.person_id, [3425, 4745, 5235])
        self.assertEqual(activity.date, datetime.date(2021, 7, 30))
        self.assertEqual(activity.date.day, 30)
        self.assertEqual(activity.date.month, 7)
        self.assertEqual(activity.date.year, 2021)
        self.assertEqual(activity.time, datetime.time(15, 30))
        self.assertEqual(activity.time.hour, 15)
        self.assertEqual(activity.time.minute, 30)
        self.assertEqual(activity.time.second, 0)
        self.assertEqual(activity.description, "FP homework")

        with self.assertRaises(ActivityDomainException):
            Activity(23, [3425, 4745, 5235], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")

        with self.assertRaises(ActivityDomainException):
            activity.activity_id = 24

        activity.activity_id = 4563
        self.assertEqual(activity.activity_id, 4563)

    def test_activity_representation(self):
        """
        Test function for activity domain representation
        """
        activity = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        self.assertEqual(str(
            activity), "ID: 3246\nPerson ids: [2743, 3281, 9483]\nDate: 30/07/2021\nTime: 15:30:00\n"
                       "Description: FP homework\n")

    def test_activity_equal(self):
        """
        Test function for activity domain equality
        """
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity3 = Activity(3247, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "Reading")

        self.assertEqual(activity1, activity2)
        self.assertNotEqual(activity1, activity3)


class PersonRepoTest(unittest.TestCase):

    def test_find_person_by_id(self):
        """
        Test function for finding a person by its id
        """
        person_repo = PersonRepository()
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        person_repo.add_person(person1)
        person_repo.add_person(person2)
        person_repo.add_person(person3)

        person = person_repo.find_person_by_id(1278)
        self.assertEqual(person, None)
        person = person_repo.find_person_by_id(1234)
        self.assertEqual(person, person1)

    def test_find_person_by_name(self):
        """
        Test function for finding a person by its name
        """
        person_repo = PersonRepository()
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        person_repo.add_person(person1)
        person_repo.add_person(person2)
        person_repo.add_person(person3)

        person = person_repo.find_person_by_name("John")
        self.assertEqual(person, None)
        person = person_repo.find_person_by_name("James Hetfield")
        self.assertEqual(person, person1)

    def test_find_person_by_phone_number(self):
        """
        Test function for finding a person by its phone number
        """
        person_repo = PersonRepository()
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        person_repo.add_person(person1)
        person_repo.add_person(person2)
        person_repo.add_person(person3)

        person = person_repo.find_person_by_phone_number("072465325")
        self.assertEqual(person, None)
        person = person_repo.find_person_by_phone_number("0786352410")
        self.assertEqual(person, person1)

    def test_add_person(self):
        """
        Test function for adding a person to the class
        """
        person_repo = PersonRepository()
        person1 = Person(1452, "Lars Ulrich", "0756845612")
        person2 = Person(1246, "Robb Flynn", "0745236548")

        person_repo.add_person(person1)
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [person1])

        person_repo.add_person(person2)
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [person1, person2])

    def test_remove_person(self):
        """
        Test function for removing a person from the class
        """
        person_repo = PersonRepository()
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        person_repo.add_person(person1)
        person_repo.add_person(person2)
        person_repo.add_person(person3)

        person_repo.remove_person(person2)
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [person1, person3])

        person_repo.remove_person(person3)
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [person1])

        person_repo.remove_person(person1)
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [])

    def test_update_person(self):
        """
        Test function for updating a person in the class
        """
        person_repo = PersonRepository()
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(1452, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        person_repo.add_person(person1)
        person_repo.add_person(person2)

        person_repo.update_person(1452, "Lars Ulrich", "0756845612")
        person_list = list(person_repo.persons)
        self.assertEqual(person_list, [person1, person3])


class ActivityRepoTest(unittest.TestCase):

    def test_find_activity_by_id(self):
        """
        Test function for finding an activity by its id
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(4785, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)
        activity_repo.add_activity(activity3)
        activity = activity_repo.find_activity_by_id(1278)
        self.assertEqual(activity, None)
        activity = activity_repo.find_activity_by_id(3246)
        self.assertEqual(activity, activity1)

    def test_find_activity_by_time(self):
        """
        Test function for finding an activity by its time
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(4785, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)
        activity_repo.add_activity(activity3)
        activity = activity_repo.find_activity_by_time(datetime.date(2021, 7, 30), datetime.time(17, 30))
        self.assertEqual(activity, None)
        activity = activity_repo.find_activity_by_time(datetime.date(2021, 7, 30), datetime.time(15, 30))
        self.assertEqual(activity, activity1)
        activity = activity_repo.find_activity_by_time(datetime.date(2021, 7, 30), datetime.time(15, 50))
        self.assertEqual(activity, activity1)

    def test_find_activity_by_date(self):
        """
        Test function for finding an activity by its date
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(4785, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)
        activity_repo.add_activity(activity3)
        activity = activity_repo.find_activity_by_date(datetime.date(2021, 12, 30))
        self.assertEqual(activity, None)
        activity = activity_repo.find_activity_by_date(datetime.date(2021, 7, 30))
        self.assertNotEqual(activity, None)

    def test_find_activity_by_persons(self):
        """
        Test function for finding an activity by the persons participating
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(4785, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)
        activity_repo.add_activity(activity3)
        activity = activity_repo.find_activity_by_persons(2453)
        self.assertEqual(activity, [])
        activity = activity_repo.find_activity_by_persons(3281)
        self.assertEqual(activity, [3246])

    def test_add_activity(self):
        """
        Test function for adding an activity to the class
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_repo.add_activity(activity1)
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [activity1])

        activity_repo.add_activity(activity2)
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [activity1, activity2])

    def test_remove_activity(self):
        """
        Test function for removing an activity from the class
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(4785, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)
        activity_repo.add_activity(activity3)

        activity_repo.remove_activity(activity2)
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [activity1, activity3])

        activity_repo.remove_activity(activity3)
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [activity1])

        activity_repo.remove_activity(activity1)
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [])

    def test_update_activity(self):
        """
        Test function for updating an activity in the class
        """
        activity_repo = ActivityRepository()
        activity1 = Activity(3246, [2743, 3281, 9483], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [4785, 4123, 7856], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(5485, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")
        activity_repo.add_activity(activity1)
        activity_repo.add_activity(activity2)

        activity_repo.update_activity(5485, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00),
                                      "Swimming")
        activity_list = list(activity_repo.activities)
        self.assertEqual(activity_list, [activity1, activity3])


class PersonServiceTest(unittest.TestCase):

    def test_generate_person(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo, generate=True)
        self.assertEqual(len(person_service.persons), 20)

    def test_add_person(self):
        """
        Test function for adding a person to the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        undo_controller = UndoController()
        person_service = PersonService(person_repo, activity_repo, undo_controller)
        person1 = Person(1452, "Lars Ulrich", "0756845612")
        person2 = Person(1246, "Robb Flynn", "0745236548")

        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1])

        person_service.add_person(1246, "Robb Flynn", "0745236548", activity_list)
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person2])

        with self.assertRaises(PersonServiceException):
            person_service.add_person(1246, "Robb Flynn", "0745436548", activity_list)
        with self.assertRaises(PersonServiceException):
            person_service.add_person(1546, "Robb Flynn", "0745236548", activity_list)

        undo_controller.undo()
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1])

        undo_controller.redo()
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person2])

    def test_remove_person(self):
        """
        Test function for removing a person from the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)

        person_service.remove_person(4256, activity_list)
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person3])

        person_service.remove_person(1452, activity_list)
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1])

        person_service.remove_person(1234, activity_list)
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [])

        with self.assertRaises(PersonServiceException):
            person_service.remove_person(1256, activity_list)

    def test_update_person(self):
        """
        Test function for updating a person in the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        undo_controller = UndoController()
        person_service = PersonService(person_repo, activity_repo, undo_controller)
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(1452, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(1452, "Dave Mustaine", "0784564213", activity_list)

        person_service.update_person(1452, "Lars Ulrich", "0756845612")
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person3])

        with self.assertRaises(PersonServiceException):
            person_service.update_person(1256, "Lars Ulrich", "0756845612")

        undo_controller.undo()
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person2])

        undo_controller.redo()
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person3])

        undo_controller.undo()
        person_list = list(person_service.persons)
        self.assertEqual(person_list, [person1, person2])
        undo_controller.undo()
        undo_controller.undo()
        with self.assertRaises(UndoServiceException):
            undo_controller.undo()

        undo_controller.redo()
        undo_controller.redo()
        undo_controller.redo()
        with self.assertRaises(UndoServiceException):
            undo_controller.redo()

    def test_search_person_by_name(self):
        """
        Test function for searching for a person by its name
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)

        person = person_service.search_person_by_name("James Hetfield")
        self.assertNotEqual(person, None)

    def test_search_person_by_phone_number(self):
        """
        Test function for searching for a person by its phone number
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        person1 = Person(1234, "James Hetfield", "0786352410")
        person2 = Person(4256, "Dave Mustaine", "0784564213")
        person3 = Person(1452, "Lars Ulrich", "0756845612")

        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)

        person = person_service.search_person_by_phone_number("078635")
        self.assertNotEqual(person, None)


class ActivityServiceTest(unittest.TestCase):
    def test_random_date(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        random_date = activity_service.random_date()
        day = random_date.day
        month = random_date.month
        year = random_date.year
        hour = random_date.hour
        minute = random_date.minute
        second = random_date.second
        self.assertEqual(random_date, datetime.datetime(year, month, day, hour, minute, second))

    def test_generate_activity(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo, generate=True)
        activity_service = ActivityService(person_repo, activity_repo, person_service, generate=True)

        self.assertEqual(len(activity_service.activities), 20)

    def test_add_activity(self):
        """
        Test function for adding an activity to the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        undo_controller = UndoController()
        person_service = PersonService(person_repo, activity_repo, undo_controller)
        activity_service = ActivityService(person_repo, activity_repo, person_service, undo_controller)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service, undo_controller)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [activity1])

        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [activity1, activity2])

        with self.assertRaises(ActivityServiceException):
            activity_service.add_activity(1485, [1452, 4256], datetime.date(2021, 10, 14), datetime.time(11, 40),
                                          "Cooking")
        with self.assertRaises(ActivityServiceException):
            activity_service.add_activity(5485, [1452, 4256], datetime.date(2021, 10, 15), datetime.time(11, 40),
                                          "Cooking")
        with self.assertRaises(ActivityServiceException):
            activity_service.add_activity(7852, [1862], datetime.date(2021, 10, 15), datetime.time(11, 40),
                                          "Cooking")

        undo_controller.undo()
        self.assertEqual(activity_list, [activity1, activity2])

        undo_controller.undo()

    def test_remove_activity(self):
        """
        Test function for removing an activity from the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.remove_activity(3246)
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [activity2])

        activity_service.remove_activity(5485)
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [])

        with self.assertRaises(ActivityServiceException):
            activity_service.remove_activity(2534)

    def test_update_activity(self):
        """
        Test function for updating an activity in the class
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        undo_controller = UndoController()
        person_service = PersonService(person_repo, activity_repo, undo_controller)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service, undo_controller)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")
        activity3 = Activity(5485, [4256], datetime.date(2021, 11, 20), datetime.time(14, 00), "Swimming")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.update_activity(5485, [1234, 7845, 1452], datetime.date(2021, 11, 20), datetime.time(14, 00),
                                         "Swimming")
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [activity1, activity3])

        with self.assertRaises(ActivityServiceException):
            activity_service.update_activity(1425, [1452, 4256], datetime.date(2021, 10, 15), datetime.time(11, 40),
                                             "Cooking")

        undo_controller.undo()
        activity_list = list(activity_service.activities)
        self.assertEqual(activity_list, [activity1, activity2])

    def test_split_command_param(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        text = "1452 2452 3654"
        self.assertEqual(activity_service.split_command_param(text), [1452, 2452, 3654])

    def test_split_date(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        date = "12/12/2021"
        day, month, year = activity_service.split_date(date)
        self.assertEqual(str(day) + '/' + str(month) + '/' + str(year), date)

    def test_split_date2(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        date = "2021-12-12"
        day, month, year = activity_service.split_date_2(date)
        self.assertEqual(str(year) + '-' + str(month) + '-' + str(day), date)

    def test_split_time(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        time = "12:30"
        hour, minute, second = activity_service.split_time(time)
        self.assertEqual(
            str(hour) + ":" + str(minute) + ":" + str(second), "12:30:0")

    def test_search_activity_by_date(self):
        """
        Test function for searching for an activity by its date
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity = activity_service.search_activity_by_date("30/07/2021")
        self.assertNotEqual(activity, None)

    def test_search_activity_by_time(self):
        """
        Test function for searching for an activity by its time
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity = activity_service.search_activity_by_time("11:30")
        self.assertNotEqual(activity, None)

    def test_search_activity_by_description(self):
        """
        Test function for searching for an activity by its description
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity = activity_service.search_activity_by_description("Read")
        self.assertEqual(activity, [activity2])

    def test_search_activity_by_person(self):
        """
        Test function for searching for an activity by the person participating
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")

        activity_service.add_activity(5485, [1452], datetime.date(2021, 10, 14), datetime.time(11, 30), "Reading")

        activity = activity_service.search_activity_by_time(1234)
        self.assertEqual(activity, [])

    def test_create_statistic_activities_by_date(self):
        """
        Test function for creating a statistics for a given date
        """
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 7, 30), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 7, 30), datetime.time(11, 30), "Reading")

        list_activities_by_date = activity_service.create_statistic_activities_by_date("30/07/2021")
        self.assertEqual(list_activities_by_date, [activity2, activity1])

    def test_number_of_activities_in_a_day(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 7, 30), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 7, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 7, 30), datetime.time(11, 30), "Reading")
        number = activity_service.number_of_activities_in_a_day(datetime.date(2021, 7, 30))
        self.assertEqual(number, 2)

    def test_create_statistic_activities_by_free_time(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 12, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")

        activity_service.add_activity(5475, [1452], datetime.date(2021, 12, 29), datetime.time(11, 30), "Reading")
        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 12, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")
        activity_service.add_activity(5175, [1452], datetime.date(2021, 12, 17), datetime.time(11, 30), "Reading")
        list_of_date = activity_service.create_statistic_activities_by_free_time()
        self.assertEqual(list_of_date, [['30/12/2021', 2], ['17/12/2021', 1], ['29/12/2021', 1]])

    def test_create_statistic_activities_by_person(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person2(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234, 4256], datetime.date(2021, 12, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")
        activity3 = Activity(5485, [1452, 1234], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")

        activity_service.add_activity(5475, [1452], datetime.date(2021, 12, 29), datetime.time(11, 30), "Reading")
        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 12, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452, 1234], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")

        activities = activity_service.create_statistic_activities_by_person(1234)

        self.assertEqual(activities, [activity3, activity1])

    def test_remove_person_from_activities(self):
        person_repo = PersonRepository()
        activity_repo = ActivityRepository()
        person_service = PersonService(person_repo, activity_repo)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity_list = activity_service.search_activity_by_person1(0)
        person_service.add_person(1234, "James Hetfield", "0786352410", activity_list)
        person_service.add_person(4256, "Dave Mustaine", "0784564213", activity_list)
        person_service.add_person(1452, "Lars Ulrich", "0756845612", activity_list)
        activity_service = ActivityService(person_repo, activity_repo, person_service)
        activity1 = Activity(3246, [1234], datetime.date(2021, 12, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")
        activity3 = Activity(5245, [1234, 1452], datetime.date(2021, 12, 17), datetime.time(11, 30), "Reading")

        activity_service.add_activity(3246, [1234, 4256], datetime.date(2021, 12, 30), datetime.time(15, 30),
                                      "FP homework")
        activity_service.add_activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")
        activity_service.add_activity(5245, [1234, 1452], datetime.date(2021, 12, 17), datetime.time(11, 30), "Reading")
        activity_service.remove_person_activities(4256, activity_list)
        activity_list = list(activity_service.activities)

        self.assertEqual(activity_list, [activity1, activity2, activity3])

        activity1 = Activity(3246, [], datetime.date(2021, 12, 30), datetime.time(15, 30), "FP homework")
        activity2 = Activity(5485, [1452], datetime.date(2021, 12, 30), datetime.time(11, 30), "Reading")
        activity3 = Activity(5245, [1452], datetime.date(2021, 12, 17), datetime.time(11, 30), "Reading")

        activity_list = activity_service.search_activity_by_person1(1234)
        activity_service.remove_person_activities(1234, activity_list)
        activity_list = list(activity_service.activities)

        self.assertEqual(activity_list, [activity1, activity2, activity3])


if __name__ == "__main__":
    unittest.main()
