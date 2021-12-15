from src.domain.activity import Activity
from src.repository.baseRepository.activityRepository import ActivityRepository
import datetime
import json
import os


class ActivityRepositoryJson(ActivityRepository):
    def __init__(self, file_name):

        ActivityRepository.__init__(self)
        self.file_name = file_name
        file = open(self.file_name, "r")
        if os.stat(file_name).st_size != 0:
            for obj in json.load(file):
                date = obj["date"]
                day, month, year = self.split_date(str(date))
                new_date = datetime.date(year, month, day)
                time = obj["time"]
                hour, minute, second = self.split_time(time)
                new_time = datetime.time(hour, minute, second)
                self.add_activity(
                    Activity(int(obj["activity_id"]), obj["person_id"], new_date, new_time, obj["description"]))
            file.close()

    def _save_file(self):
        """
        Method for saving activities to a file in binary form
        :return:
        """
        file = open(self.file_name, "w")
        json.dump([x.to_dict() for x in self._activity_list], file, indent=4)
        file.close()

    def add_activity(self, activity):
        """
        Method for adding an activity fto a binary file
        :param activity:
        :return:
        """
        ActivityRepository.add_activity(self, activity)
        self._save_file()

    def update_activity(self, activity_id, person_id, date, time, description):
        """
        Method for updating an activity on a binary file
        :param activity_id:
        :param person_id:
        :param date:
        :param time:
        :param description:
        :return:
        """
        ActivityRepository.update_activity(self, activity_id, person_id, date, time, description)
        self._save_file()

    def remove_activity(self, activity):
        """
        Method for removing an activity from a binary file
        :param activity:
        :return:
        """
        ActivityRepository.remove_activity(self, activity)
        self._save_file()

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
