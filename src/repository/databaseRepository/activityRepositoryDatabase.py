from src.domain.activity import Activity
from src.repository.baseRepository.activityRepository import ActivityRepository
import mysql.connector
import datetime


class ActivityRepositoryDatabase(ActivityRepository):
    def __init__(self, file_name):
        ActivityRepository.__init__(self)
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            port='3306',
            database=file_name
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS activities (activity_id INTEGER PRIMARY KEY, person_id VARCHAR(40), '
            'date VARCHAR(11), time VARCHAR(10), desciption VARCHAR(70))')

    @property
    def activities(self):
        self.cursor.execute('SELECT * FROM activities;')
        activities = list(self.cursor.fetchall())
        for i in range(0, len(activities)):
            activities[i] = list(activities[i])
            activities[i][1] = self.split_command_param(activities[i][1])
            date = activities[i][2]
            day, month, year = self.split_date(str(date))
            activities[i][2] = datetime.date(year, month, day)
            time = activities[i][3]
            hour, minute, second = self.split_time(time)
            activities[i][3] = datetime.time(hour, minute, second)
        self._activity_list = [
                Activity(x[0], x[1], x[2], x[3], x[4]) for x in
                activities]
        return [Activity(x[0], x[1], x[2], x[3], x[4]) for x in
                activities]

    def find_activity_by_id(self, activity_id):
        self.cursor.execute('SELECT * FROM activities WHERE activity_id=%s;', (activity_id,))
        activities = list(self.cursor.fetchall())
        if len(activities) == 0:
            return None
        self._activity_list = [
            Activity(x[0], x[1], x[2], x[3], x[4]) for x in
            activities]
        return \
            [Activity(x[0], x[1], x[2], x[3], x[4]) for x in
             activities][0]

    def add_activity(self, activity):
        self.cursor.execute(
            'INSERT INTO `activity_planner_database`.`activities`(`activity_id`,`person_id`,`date`,`time`,'
            '`description`) VALUES (%s, %s, %s, %s, %s);',
            (activity.activity_id, self.create_string_with_spaces_from_list(activity.person_id),
             str(activity.date.strftime("%d/%m/%Y")), str(activity.time),
             str(activity.description)))
        print(type(activity.date))
        ActivityRepository.add_activity(self, activity)
        self.connection.commit()

    def remove_activity(self, activity):
        self.cursor.execute('DELETE FROM activities WHERE activity_id= %s;', (activity.activity_id,))
        ActivityRepository.remove_activity(self, activity)
        self.connection.commit()

    def update_activity(self, activity_id, person_id, date, time, description):
        print(person_id, date, time)
        self.cursor.execute(
            "UPDATE activities SET person_id= %s, date= %s, time= %s, description= %s WHERE activity_id= %s;",
            (
                self.create_string_with_spaces_from_list(person_id), str(date.strftime("%d/%m/%Y")), str(time),
                description,
                activity_id))
        ActivityRepository.update_activity(self, activity_id, self.create_string_with_spaces_from_list(person_id),
                                           str(date.strftime("%d/%m/%Y")), time, description)
        self.connection.commit()

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
    def create_string_with_spaces_from_list(person_id_list):
        string = ""
        for person_id in person_id_list:
            string += str(person_id)
            string += " "
        string = string[:len(string) - 1]
        return string
