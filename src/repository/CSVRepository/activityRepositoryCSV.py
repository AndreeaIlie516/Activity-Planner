from src.repository.baseRepository.activityRepository import ActivityRepository
from src.domain.activity import Activity
import datetime


class ActivityRepositoryCSV(ActivityRepository):
    def __init__(self, file_name):
        ActivityRepository.__init__(self)
        self.file_name = file_name
        file = open(self.file_name, "r")
        for line in file.readlines():
            line = line.strip(" \n")
            stuff = line.split(",")
            person_id = self.split_command_param(stuff[1])
            date = stuff[2]
            day, month, year = self.split_date(date)
            new_date = datetime.date(year, month, day)
            time = stuff[3]
            hour, minute, second = self.split_time(time)
            new_time = datetime.time(hour, minute, second)
            self.add_activity(Activity(int(stuff[0]), person_id, new_date, new_time, stuff[4]))
        file.close()

    def _save_file(self):
        """
        Method for saving activities to a CSV file
        :return:
        """
        file = open(self.file_name, "w")
        for activity in self._activity_list:
            date = activity.date.strftime("%d/%m/%Y")
            person_id = self.reformat_person_list(activity.person_id)
            file.write(
                "{0},{1},{2},{3},{4}\n".format(activity.activity_id, person_id, date, activity.time,
                                               activity.description))
        file.close()

    def add_activity(self, activity):
        """
        Method for adding an activity to a CSV file
        :param activity:
        :return:
        """
        ActivityRepository.add_activity(self, activity)
        self._save_file()

    def remove_activity(self, activity_id):
        """
        Method for removing an activity from a CSV file
        :param activity_id:
        :return:
        """
        ActivityRepository.remove_activity(self, activity_id)
        self._save_file()

    def update_activity(self, activity_id, person_id, date, time, description):
        """
        Method for updating an activity on a CSV file
        :param activity_id:
        :param person_id:
        :param date:
        :param time:
        :param description:
        :return:
        """
        ActivityRepository.update_activity(activity_id, person_id, date, time, description)
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

    @staticmethod
    def reformat_person_list(person_id):
        """
        Method for reformatting persons list for printing in file
        :param person_id:
        :return:
        """
        person_id = str(person_id)
        person_id = person_id[1:]
        person_id = person_id[:1]
        person_id = person_id.replace(",", "")
        return person_id
