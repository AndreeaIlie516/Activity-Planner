from src.repository.baseRepository.personRepository import PersonRepository
import datetime
from src.utils.utils import *


class ActivityRepository:
    def __init__(self, activity_list=None):
        if activity_list is None:
            activity_list = []
        if activity_list is Container:
            self._activity_list = activity_list
        else:
            self._activity_list = Container(activity_list)
        person_repository = PersonRepository()
        self._person_repository = person_repository

    @property
    def activities(self):
        return self._activity_list

    def find_activity_by_id(self, activity_id):
        """
        Method for finding an activity by its id
        """
        aux = custom_filter(self._activity_list, lambda x: x.activity_id == activity_id)
        if len(aux) == 0:
            return None
        else:
            return aux[0]

    def find_activity_by_date(self, date):
        """
        Method for finding an activity by its date
        """
        aux = custom_filter(self._activity_list, lambda x: x.date == date)
        if len(aux) == 0:
            return None
        else:
            return aux

    def find_activity_by_time(self, date, time):
        """
        Method for finding an activity by its time
        """
        activity_list = self._activity_list
        ok = 1
        for i in activity_list:
            if i.date == date:
                activ_time = i.time
                datetime1 = datetime.datetime.combine(date, activ_time)
                time_change = datetime.timedelta(hours=1)
                new_time = datetime1 + time_change
                hour = new_time.hour
                minute = new_time.minute
                new_activity = datetime.time(hour, minute)
                if activ_time <= time <= new_activity:
                    ok = 0
        if ok == 0:
            return activity_list[0]
        return None

    def find_activity_by_persons(self, person_id):
        """
        Method for finding an activity by the participating persons
        """
        list_of_activities = []
        for i in self._activity_list:
            for j in i.person_id:
                if j == person_id:
                    list_of_activities.append(i.activity_id)
        return list_of_activities

    def add_activity(self, activity):
        """
        Method for adding an activity to the class
        """
        self._activity_list.append(activity)

    def remove_activity(self, activity):
        """
        Method for removing an activity from the class
        """
        self._activity_list.remove(activity)

    def update_activity(self, activity_id, person_id, date, time, description):
        """
        Method for updating an activity in the class
        """
        activity = self.find_activity_by_id(activity_id)
        activity.person_id = person_id
        activity.date = date
        activity.time = time
        activity.description = description
