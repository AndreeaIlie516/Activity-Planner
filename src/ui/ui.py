import datetime


class UI:
    def __init__(self, person_service, activity_service, undo_controller):
        self._undo_controller = undo_controller
        self._person_service = person_service
        self._activity_service = activity_service

    @staticmethod
    def print_menu():
        """
        Print the menu
        :return:
        """
        print("Please select one of the following options:")
        print("(A) Manage persons or activities")
        print("\t Persons")
        print("\t \t 1.Add a person")
        print("\t \t 2.Remove a person")
        print("\t \t 3.Update a person")
        print("\t \t 4.List persons")
        print("\t Activities")
        print("\t \t 5.Add an activity")
        print("\t \t 6.Remove an activity")
        print("\t \t 7.Update an activity")
        print("\t \t 8.List activities")
        print("(B) Search for persons or activities")
        print("\t Persons")
        print("\t \t 9. Search for persons by name")
        print("\t \t10. Search for persons by phone number")
        print("\t Activities")
        print("\t \t11. Search for activities by date")
        print("\t \t12. Search for activities by time")
        print("\t \t13. Search for activities by description")
        print("(C) Create statistics")
        print("\t \t14. Activities for a given date. List the activities for a given date, in the order of their "
              "start time.")
        print(
            "\t \t15. Busiest days. This will provide the list of upcoming dates with activities, sorted in ascending "
            "order "
            "of the free time in that day (all intervals with no activities).")
        print("\t \t16. Activities with a given person. List all upcoming activities to which a given person will "
              "participate. ")
        print("(D) Undo/redo")
        print("\t \t17.Undo")
        print("\t \t18.Redo")
        print("(E) Exit the aplications")
        print("\t \t19.Exit the application")
        print()

    def start(self):
        """
        Create the menu-driven console user interface
        """
        while True:
            UI.print_menu()
            option = int(input('>'))
            if option == 1:
                self.ui_add_person()
            elif option == 2:
                self.ui_remove_person()
            elif option == 3:
                self.ui_update_person()
            elif option == 4:
                self.list_persons(self._person_service.persons)
            elif option == 5:
                self.ui_add_activity()
            elif option == 6:
                self.ui_remove_activity()
            elif option == 7:
                self.ui_update_activity()
            elif option == 8:
                self.list_activities(self._activity_service.activities)
            elif option == 9:
                self.ui_search_person_by_name()
            elif option == 10:
                self.ui_search_person_by_phone_number()
            elif option == 11:
                self.ui_search_activity_by_date()
            elif option == 12:
                self.ui_search_activity_by_time()
            elif option == 13:
                self.ui_search_activity_by_description()
            elif option == 14:
                self.ui_create_statistic_activities_by_date()
            elif option == 15:
                self.ui_create_statistic_activities_by_free_time()
            elif option == 16:
                self.ui_create_statistic_activities_by_person()
            elif option == 17:
                self.ui_undo()
            elif option == 18:
                self.ui_redo()
            elif option == 19:
                print("You exited the application.")
                return 0
            else:
                print('Invalid number. Please select one of the five options!')

    @staticmethod
    def list_persons(persons):
        """
        UI function for listing the persons
        """
        print('\n')
        print("There are " + str(len(persons)) + " persons in total in the Activity Planner.\n")
        for i in persons:
            print(i)
        print('\n')

    def ui_add_person(self):
        """
        UI function for reading and adding a person
        """
        print("Please add a person:")
        person_id = input("ID of the person (4 digits): ")
        try:
            person_id = int(person_id)
        except Exception as ve:
            print(ve)
        name = input("Name of the person: ")
        phone_number = str(input("Phone number of the person: "))
        try:
            activity_list = self._activity_service.search_activity_by_person1(person_id)
            self._person_service.add_person(person_id, name, phone_number, activity_list)
            print("Person added successfully!\n")
        except Exception as e:
            print(e)

    def ui_remove_person(self):
        """
        UI function for removing a person
        """
        print("Please select a person to remove:")
        person_id = input("ID of the person:")
        try:
            person_id = int(person_id)
        except Exception as ve:
            print(ve)
        if person_id < 1000 or person_id > 9999:
            print("Invalid person ID")
        print('\n')
        try:
            activity_list = self._activity_service.search_activity_by_person1(person_id)
            self._person_service.remove_person(person_id, activity_list)
            print("Person removed successfully!\n")
        except Exception as ve:
            print(ve)

    def ui_update_person(self):
        """
        UI function for updating a person
        """
        print("Please select a person to update:")
        person_id = input("ID of the person:")
        try:
            person_id = int(person_id)
        except Exception as ve:
            print(ve)
        if person_id < 1000 or person_id > 9999:
            print("Invalid person ID")
            return
        name = input("Name of the person: ")
        phone_number = str(input("Phone number of the person: "))
        if len(phone_number) != 10 or not phone_number.isdigit():
            print("Invalid phone number")
        print('\n')
        try:
            self._person_service.update_person(person_id, name, phone_number)
            print("Person updated successfully!\n")
        except Exception as ve:
            print(ve)

    @staticmethod
    def list_activities(activities):
        """
        UI function for listing the activities
        """
        print('\n')
        print("There are " + str(len(activities)) + " activities in total in the Activity Planner")
        for i in activities:
            print(i)
        print('\n')

    def ui_add_activity(self):
        """
        UI function for reading and adding an activity
        """
        print("Please add an activity:")
        activity_id = str(input("ID of the activity (4 digits): "))
        try:
            activity_id = int(activity_id)
        except Exception as ve:
            print(ve)
        """print("Please select persons from the following list to add to the activity:")
        self.list_persons(self._person_service.persons)"""
        person_id = str(input("List of the ids of the persons, separated by space: "))
        person_id = self._activity_service.split_command_param(person_id)
        date = str(input("The date of the activity (in the format dd/mm/yyyy) is: "))
        day, month, year = self._activity_service.split_date(date)
        new_date = datetime.date(year, month, day)
        time = str(input("The time of the activity (in the format hh:mm:ss) is: "))
        hour, minute, second = self._activity_service.split_time(time)
        new_time = datetime.time(hour, minute, second)
        description = str(input("The description of the activity is: "))
        print('\n')
        #try:
        self._activity_service.add_activity(activity_id, person_id, new_date, new_time, description)
        print("Activity added successfully!\n")
        # except Exception as e:
            #print(e)

    def ui_remove_activity(self):
        """
        UI function for removing an activity
        """
        print("Please select an activity to remove:")
        activity_id = input("ID of the activity:")
        try:
            activity_id = int(activity_id)
        except Exception as ve:
            print(ve)
        if activity_id < 1000 or activity_id > 9999:
            print("Invalid person ID")
            return
        print('\n')
        try:
            self._activity_service.remove_activity(activity_id)
            print("Activity removed successfully!\n")
        except Exception as ve:
            print(ve)

    def ui_update_activity(self):
        """
        UI function for updating an activity
        """
        print("Please select an activity to update:")
        activity_id = str(input("ID of the activity: "))
        try:
            activity_id = int(activity_id)
        except Exception as ve:
            print(ve)
        if activity_id < 1000 or activity_id > 9999:
            print("Invalid person ID")
            return
        person_id = str(input("List of the ids of the persons, separated by space: "))
        person_id = self._activity_service.split_command_param(person_id)
        date = str(input("The date of the activity (in the format dd/mm/yyyy) is: "))
        try:
            day, month, year = self._activity_service.split_date(date)
            new_date = datetime.date(year, month, day)
        except Exception as ve:
            print(ve)
        time = str(input("The time of the activity (in the format hh:mm:ss) is: "))
        try:
            hour, minute, second = self._activity_service.split_time(time)
            new_time = datetime.time(hour, minute, second)
        except Exception as ve:
            print(ve)
        description = str(input("The description of the activity is: "))
        print('\n')
        try:
            self._activity_service.update_activity(activity_id, person_id, new_date, new_time, description)
            print("Activity updated successfully!\n")
        except Exception as ve:
            print(ve)

    def ui_search_person_by_name(self):
        """
        UI function for searching for a person by the name
        """
        name = str(input("The name of the person you are looking for: "))
        self.list_persons(self._person_service.search_person_by_name(name))

    def ui_search_person_by_phone_number(self):
        """
        UI function for searching for a person by the phone number
        """
        phone_number = str(input("The phone number of the person you are looking for: "))
        self.list_persons(self._person_service.search_person_by_phone_number(phone_number))

    def ui_search_activity_by_date(self):
        """
        UI function for searching for an activity by the date
        """
        date = str(input("The date of the activity you are looking for (in the format dd/mm/yyyy): "))
        day, month, year = self._activity_service.split_date(date)
        if year != 0 and month != 0 and day != 0:
            new_date = datetime.date(year, month, day)
            new_date = new_date.strftime("%d/%m/%Y")
        else:
            if year == 0:
                year = "0000"
            if month == 0:
                month = "00"
            if day == 0:
                day = "00"
            if int(day) > 1000:
                year = day
                day = "00"
            if int(month) > 1000:
                year = month
                month = "00"
            new_date = str(day) + '/' + str(month) + '/' + str(year)

        self.list_activities(self._activity_service.search_activity_by_date(new_date))

    def ui_search_activity_by_time(self):
        """
        UI function for searching for an activity by the time
        """
        time = str(input("The time of the activity you are looking for (in the format hh:mm:ss): "))
        hour, minute, second = self._activity_service.split_time(time)
        new_time = datetime.time(hour, minute, second)
        self.list_activities(self._activity_service.search_activity_by_time(new_time))

    def ui_search_activity_by_description(self):
        """
        UI function for searching for an activity by the description
        """
        description = str(input("The description of the activity you are looking for: "))
        self.list_activities(self._activity_service.search_activity_by_description(description))

    def ui_create_statistic_activities_by_date(self):
        """
        UI function for creating a statistics for a given date
        """
        date = str(input("The date of the activities (in the format dd/mm/yyyy): "))
        day, month, year = self._activity_service.split_date(date)
        if year != 0 and month != 0 and day != 0:
            new_date = datetime.date(year, month, day)
            new_date = new_date.strftime("%d/%m/%Y")
        else:
            if year == 0:
                year = "0000"
            if month == 0:
                month = "00"
            if day == 0:
                day = "00"
            if int(day) > 1000:
                year = day
                day = "00"
            if int(month) > 1000:
                year = month
                month = "00"
            new_date = str(day) + '/' + str(month) + '/' + str(year)
        self.list_activities(self._activity_service.create_statistic_activities_by_date(new_date))

    def ui_create_statistic_activities_by_free_time(self):
        """
        UI function for creating a statistics for the busiest days
        """
        list_of_date = self._activity_service.create_statistic_activities_by_free_time()
        print("These are your free days: ")
        for i in list_of_date:
            print("On the day " + str(i[0]) + " you have " + str(i[1]) + " upcoming activities")
        print('\n')

    def ui_create_statistic_activities_by_person(self):
        """
        UI function for creating a statistics for activities with a given person
        """
        person_id = int(input("The ID of the person which participates at the activities: "))
        self.list_activities(self._activity_service.create_statistic_activities_by_person(person_id))

    def ui_undo(self):
        try:
            self._undo_controller.undo()
            print("Operation successfully undone!\n")
        except Exception as e:
            print(e)

    def ui_redo(self):
        try:
            self._undo_controller.redo()
            print("Operation successfully redone!\n")
        except Exception as e:
            print(e)


def print_exception(ve):
    print(ve)
