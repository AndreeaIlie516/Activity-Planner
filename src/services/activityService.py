from src.domain.activity import Activity
from src.repository.baseRepository.activityRepository import ActivityRepository
from src.repository.baseRepository.personRepository import PersonRepository
from src.exception.exception import ActivityServiceException
import random
import datetime
import re
from src.services.undoService import *


class ActivityService:
    def __init__(self, person_repository, activity_repository, person_service, undoController=False, generate=False):
        self._person_repository = person_repository
        self._person_service = person_service
        self._activity_repository = activity_repository
        if generate:
            self._activity_repository = ActivityRepository(self.generate_activities())
        self._undoController = undoController

    @property
    def activities(self):
        return self._activity_repository.activities

    @staticmethod
    def random_date():
        """
        Method for generating a random date
        """
        start = datetime.datetime.strptime('10/12/2021 1:00 PM', '%d/%m/%Y %I:%M %p')
        end = datetime.datetime.strptime('30/01/2022 1:00 PM', '%d/%m/%Y %I:%M %p')
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + datetime.timedelta(seconds=random_second)

    def generate_activities(self):
        """
        Method for generating activities
        """
        descriptions = self.list_of_descriptions()
        activities = []
        for i in range(30):
            activity_id = random.randint(1000, 9999)
            while activity_id in [x.activity_id for x in activities]:
                activity_id = random.randint(1000, 9999)
            person_id = []
            for j in range(random.randint(0, 10)):
                pid = random.choice(self._person_service.persons).person_id
                if pid not in person_id:
                    person_id.append(pid)
            description = random.choice(descriptions)
            random_date_time = self.random_date()
            day = random_date_time.day
            month = random_date_time.month
            year = random_date_time.year
            hour = random_date_time.hour
            minute = random_date_time.minute
            date = datetime.date(year, month, day)
            time = datetime.time(hour, minute)
            activities.append(Activity(activity_id, person_id, date, time, description))
        return activities

    def add_activity(self, activity_id, person_id, date, time, description):
        """
        Method for adding an activity to the class
        """
        activity = Activity(activity_id, person_id, date, time, description)
        if self._activity_repository is not None:
            if self._activity_repository.find_activity_by_id(activity_id):
                raise ActivityServiceException("Activity with the ID " + str(activity_id) + " already exists!\n")
        if self._activity_repository.find_activity_by_date(date):
            if self._activity_repository.find_activity_by_time(date, time):
                raise ActivityServiceException(
                    "You cannot perform two or more activities at the same time (hypothetically)!\n")
        if person_id:
            exists = 0
            id = 0
            for i in person_id:
                id1 = i
                for j in self._person_service.persons:
                    if int(i) == int(j.person_id):
                        exists = 1
                        id1 = 0
                if id1 == i:
                    id = i
            if exists == 0:
                raise ActivityServiceException("The is no person with the ID " + str(id) + " in the list!\n")

        if self._undoController is not False:
            undo = FunctionCall(self.remove_activity, activity_id)
            redo = FunctionCall(self.add_activity, activity_id, person_id, date, time, description)
            op = Operation(undo, redo)
            self._undoController.recordOperation(op)

        self._activity_repository.add_activity(activity)

    def remove_activity(self, activity_id):
        """
        Method for removing an activity from the class
        """
        activity = self._activity_repository.find_activity_by_id(activity_id)
        if not activity:
            raise ActivityServiceException("There is no activity with the ID " + str(activity_id) + "!\n")

        if self._undoController is not False:
            undo = FunctionCall(self.add_activity, activity.activity_id, activity.person_id, activity.date,
                                activity.time,
                                activity.description)
            redo = FunctionCall(self.remove_activity, activity_id)
            op = Operation(undo, redo)
            self._undoController.recordOperation(op)

        self._activity_repository.remove_activity(activity)

    def update_activity(self, activity_id, person_id, date, time, description):
        """
        Method for updating an activity in the class
        """
        activity = self._activity_repository.find_activity_by_id(activity_id)
        if not activity:
            raise ActivityServiceException("There is no activity with the ID " + str(activity_id) + "!\n")

        if self._undoController is not False:
            undo = FunctionCall(self.update_activity, activity.activity_id, activity.person_id, activity.date,
                                activity.time,
                                activity.description)
            redo = FunctionCall(self.update_activity, activity_id, person_id, date, time, description)
            op = Operation(undo, redo)
            self._undoController.recordOperation(op)

        self._activity_repository.update_activity(activity_id, person_id, date, time, description)

    @staticmethod
    def remove_person_activities(person_id, activity_list):
        for activity in activity_list:
            if person_id in activity:
                activity.remove(person_id)

    def add_person_activities(self, person_id, activity_list):
        for activity in activity_list:
            activity.append(person_id)

    def update_activity_from_person(self, activity_id, person_id, date, time, description):
        """
        Method for updating an activity in the class
        """

        activity = self._activity_repository.find_activity_by_id(activity_id)
        if not activity:
            raise ActivityServiceException("There is no activity with the ID " + str(activity_id) + "!\n")

        self._activity_repository.update_activity(activity_id, person_id, date, time, description)

    @staticmethod
    def split_command_param(user_input):
        """
        Method for splitting an input
        """
        list_of_persons = []
        user_input = user_input.strip()
        tokens = user_input.split()
        length = len(tokens)
        index = 0
        while index < length:
            list_of_persons.append(int(tokens[index]))
            index += 1
        return list_of_persons

    @staticmethod
    def split_date(date):
        """
        Method for splitting a date
        """
        date = date.strip()
        new_date = []
        try:
            tokens = date.split('/')
            length = len(tokens)
            index = 0
            while index < length:
                new_date.append(tokens[index])
                index += 1
            if length < 3:
                for i in range(length, 3):
                    new_date.append(0)
            return int(new_date[0]), int(new_date[1]), int(new_date[2])
        except Exception as ve:
            print(ve)

    @staticmethod
    def split_date_2(date):
        """
        Method for splitting a date
        """
        date = date.strip()
        new_date = []
        try:
            tokens = date.split('-')
            length = len(tokens)
            index = 0
            while index < length:
                new_date.append(tokens[index])
                index += 1
            return int(new_date[2]), int(new_date[1]), int(new_date[0])
        except Exception as ve:
            print(ve)

    @staticmethod
    def split_time(time):
        """
        Method for splitting time
        """
        time = time.strip()
        new_time = []
        try:
            tokens = time.split(':')
            length = len(tokens)
            index = 0
            while index < length:
                new_time.append(tokens[index])
                index += 1
            if length < 3:
                for i in range(length, 3):
                    new_time.append(0)
            return int(new_time[0]), int(new_time[1]), int(new_time[2])
        except Exception as ve:
            print(ve)

    def search_activity_by_date(self, date):
        """
        Method for searching for an activity by it date
        """
        date = str(date)
        date = date.replace("/0000", "")
        date = date.replace("00/", "")
        date = date.replace("00", "")
        return [activity for activity in self._activity_repository.activities if
                re.search(str(date), str(activity.date.strftime("%d/%m/%Y")), re.IGNORECASE)]

    def search_activity_by_time(self, time):
        """
        Method for searching for an activity by its time
        """
        time = str(time)
        time = time.replace(":00", "")
        return [activity for activity in self._activity_repository.activities if
                re.search(str(time), str(activity.time), re.IGNORECASE)]

    def search_activity_by_description(self, description):
        """
        Method for searching for an activity by its description
        """
        return [activity for activity in self._activity_repository.activities
                if re.search(description, activity.description, re.IGNORECASE)]

    def search_activity_by_person1(self, person_id):
        """
        Method for searching for an activity by the persons participating
        """
        ls = list()
        for i in self._activity_repository.activities:
            if person_id in i.person_id:
                ls.append(i.person_id)
        return ls

    def search_activity_by_person2(self, person_id):
        """
        Method for searching for an activity by the persons participating
        """
        return [activity for activity in self._activity_repository.activities
                if re.search(str(person_id), str(activity.person_id), re.IGNORECASE)]

    def create_statistic_activities_by_date(self, date):
        """
        Method for creating a statistics for a given date
        """
        activity_list = self.search_activity_by_date(date)
        activity_list_time = sorted((str(activity.time) for activity in activity_list))
        activity_list_sorted = []
        for i in activity_list_time:
            for activity in activity_list:
                if str(i) == str(activity.time):
                    activity_list_sorted.append(activity)
        return activity_list_sorted

    def number_of_activities_in_a_day(self, date):
        """
        Method for counting the activities on a specific day
        """
        list_of_activities = self._activity_repository.find_activity_by_date(date)
        count = 0
        for i in list_of_activities:
            count += 1
        return count

    def create_statistic_activities_by_free_time(self):
        """
        Method for creating a statistics for the busiest days
        """
        activity_list = self.activities
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        now = datetime.date(year, month, day)
        list_of_date = []
        list_ = []
        for i in activity_list:
            date = i.date
            day, month, year = self.split_date_2(str(date))
            new_date = datetime.date(year, month, day)
            new_date = new_date.strftime("%d/%m/%Y")
            if str(date) >= str(now):
                new_list = [str(i.date.strftime("%d/%m/%Y")), self.number_of_activities_in_a_day(i.date)]
                if new_list not in list_of_date:
                    list_of_date.append([str(new_date), self.number_of_activities_in_a_day(i.date)])
        for i in range(0, len(list_of_date)):
            for j in range(i + 1, len(list_of_date)):
                if list_of_date[i][1] < list_of_date[j][1]:
                    aux = list_of_date[i]
                    list_of_date[i] = list_of_date[j]
                    list_of_date[j] = aux
        for i in range(0, len(list_of_date)):
            for j in range(0, len(list_of_date)):
                for k in range(j + 1, len(list_of_date)):
                    if list_of_date[j][1] == list_of_date[k][1] == list_of_date[i][1]:
                        if list_of_date[j][0] > list_of_date[k][0]:
                            aux = list_of_date[j]
                            list_of_date[j] = list_of_date[k]
                            list_of_date[k] = aux
        return list_of_date

    def create_statistic_activities_by_person(self, person_id):
        """
        Method for creating a statistics for activities with a given person
        """
        activity_list = self.search_activity_by_person2(person_id)
        activity_list_date_time = sorted((str(datetime.datetime.combine(activity.date, activity.time)) for activity
                                          in activity_list))
        activity_list_sorted = []
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        for i in activity_list_date_time:
            if str(i) > str(now):
                for activity in activity_list:
                    if str(i) == str(datetime.datetime.combine(activity.date, activity.time)):
                        activity_list_sorted.append(activity)

        return activity_list_sorted

    @staticmethod
    def list_of_descriptions():
        try:
            file = open("files/activity_descriptions.txt", "r")
            list_of_descriptions = []
            for x in file.readlines():
                list_of_descriptions.append(x[:-1])
            file.close()
            return list_of_descriptions
        except FileNotFoundError:
            list_of_descriptions = [
                "Read (You little nerd)",
                "Study (Still hope to pass the exams, ha?)",
                "Attend classes (We all know that you are sleeping)",
                "Cook (Be careful not to start a fire)",
                "Relax (Just another excuse to procrastinate)",
                "Go to the gym (It's pointless, but at least you tried)",
                "Swim (Be careful not to drown)",
                "Meditate (You hope to become a new Buddha, but you are still angry af)",
                "Go shopping (You don't have enough money!!!)",
                "Eat outside ((You don't have enough money!!! x2)",
                "Take a walk (Oh, fresh air, just to forget how stupid you are)",
                "Skincare (You little princess)",
                "Go to party (We all know it doesn't happen)",
                "Watch a movie (Just another bullshit teenager romance movie)",
                "Play board games (We all know you have no friends)",
                "Drink alcohol like only computer science students can do",
                "Listen to music (Maneaua Otelul Galati, right?)",
                "Go to a concert (We all know you will headbang all night long and then complaining about neck pain "
                "an entire week) "
            ]
            return list_of_descriptions
