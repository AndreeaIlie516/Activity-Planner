from src.exception.exception import ActivityDomainException


class Activity:
    def __init__(self, activity_id, person_id, date, time, description):
        """
        Create Activity with activity_id(the id of the activity), person_id(the ids of the persons participating),
        date(the date of the activity), time(the time of the activity), description(the description of the activity)
        :param
        """
        if activity_id < 1000 or activity_id > 9999:
            raise ActivityDomainException("Invalid activity ID")
        self._activity_id = activity_id
        self._person_id = person_id
        self._date = date
        self._time = time
        self._description = description

    def __str__(self):
        date = self._date.strftime("%d/%m/%Y")
        return "ID: " + str(self._activity_id) + "\nPerson ids: " + str(self._person_id) + "\nDate: " + str(
            date) + "\nTime: " + str(self._time) + "\nDescription: " + str(self._description) + '\n'

    def __eq__(self, other):
        return self.activity_id == other.activity_id

    @property
    def activity_id(self):
        return self._activity_id

    @property
    def person_id(self):
        return self._person_id

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def description(self):
        return self._description

    @activity_id.setter
    def activity_id(self, x):
        if x < 1000 or x > 9999:
            raise ActivityDomainException("Invalid activity ID")
        self._activity_id = x

    @person_id.setter
    def person_id(self, x):
        self._person_id = x

    @date.setter
    def date(self, x):
        self._date = x

    @time.setter
    def time(self, x):
        self._time = x

    @description.setter
    def description(self, x):
        self._description = x


