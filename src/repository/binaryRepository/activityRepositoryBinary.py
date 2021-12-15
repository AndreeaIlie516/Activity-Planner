from src.domain.activity import Activity
from src.repository.baseRepository.activityRepository import ActivityRepository
import pickle
import os


class ActivityRepositoryBinary(ActivityRepository):
    def __init__(self, file_name):

        ActivityRepository.__init__(self)
        self.file_name = file_name
        if os.stat(file_name).st_size != 0:
            file = open(self.file_name, "rb")
            for obj in pickle.load(file):
                self.add_activity(
                    Activity(int(obj["activity_id"]), obj["person_id"], obj["date"], obj["time"], obj["description"]))
            file.close()

    def _save_file(self):
        """
        Method for saving activities to a file in binary form
        :return:
        """
        file = open(self.file_name, "wb")
        pickle.dump([x.to_dict() for x in self._activity_list], file)
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
