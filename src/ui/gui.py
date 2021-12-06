import tkinter
import tkinter as tk
from tkinter import END
from tkinter import font as tkfont
from tkinter import *
import datetime
from PIL import ImageTk, Image
import os

from src.service.personService import PersonService
from src.service.activityService import ActivityService


class GUI:
    def __init__(self, person_service, activity_service, undo_controller):
        self._person_service = person_service
        self._activity_service = activity_service
        self._undo_controller = undo_controller

    def start(self):
        root = MainMenu(self)
        root.iconbitmap("D:/Fuckulta_2.0_(Babes)/An 1/Sem 1/Fundamentals of "
                        "Programming/Laboratory/Assignment8/src/ui/calendar.ico")
        """bg = PhotoImage(file="D:/Fuckulta_2.0_(Babes)/An 1/Sem 1/Fundamentals "
                        "of_Programming/Laboratory/Assignment8/src/ui/background.jpg)")
        label1 = Label(root, image=bg)
        label1.place(x=0, y=0)"""

        root.mainloop()

    def gui_list_persons(self, textbox):
        textbox.txt.delete(1.0, END)
        show = '\n'
        show = "There are " + str(len(self._person_service.persons)) + " persons in the Activity Planner.\n"
        print(show)
        for i in self._person_service.persons:
            print(i)
        for i in self._person_service.persons:
            show += str(i) + "\n"
        textbox.txt.insert(1.0, show)

    def gui_add_person(self, textbox, person_id, name, phone_number):
        textbox.txt.delete(1.0, END)
        try:
            person_id = int(person_id)
            self._person_service.add_person(person_id, name, phone_number)
            for i in self._person_service.persons:
                print(i)
            textbox.txt.insert(1.0, "Person added successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_remove_person(self, textbox, person_id):
        textbox.txt.delete(1.0, END)
        try:
            person_id = int(person_id)
            if person_id < 1000 or person_id > 9999:
                textbox.txt.insert(1.0, "Invalid person ID")
            self._person_service.remove_person(person_id)
            self._activity_service.remove_person_from_activities(person_id)
            textbox.txt.insert(1.0, "Person removed successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_update_person(self, textbox, person_id, name, phone_number):
        textbox.txt.delete(1.0, END)
        try:
            person_id = int(person_id)
            self._person_service.update_person(person_id, name, phone_number)
            textbox.txt.insert(1.0, "Person updated successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_list_activities(self, textbox):
        textbox.txt.delete(1.0, END)
        show = "There are " + str(len(self._activity_service.activities)) + " activities in the Activity Planner.\n"
        for i in self._activity_service.activities:
            print(i)
        for i in self._activity_service.activities:
            show += str(i) + "\n"
        textbox.txt.insert(1.0, show)

    def gui_add_activity(self, textbox, activity_id, person_id, date, time, description):
        textbox.txt.delete(1.0, END)
        try:
            activity_id = int(activity_id)
            self._activity_service.add_activity(activity_id, person_id, date, time, description)

            textbox.txt.insert(1.0, "Activity added successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_remove_activity(self, textbox, activity_id):
        textbox.txt.delete(1.0, END)
        try:
            activity_id = int(activity_id)
            if activity_id < 1000 or activity_id > 9999:
                textbox.txt.insert(1.0, "Invalid activity ID")
            self._activity_service.remove_activity(activity_id)
            textbox.txt.insert(1.0, "Activity removed successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_update_activity(self, textbox, activity_id, person_id, date, time, description):
        textbox.txt.delete(1.0, END)
        try:
            activity_id = int(activity_id)
            self._activity_service.update_activity(activity_id, person_id, date, time, description)

            textbox.txt.insert(1.0, "Activity added successfully!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_create_statistic_activities_by_free_time(self, textbox):
        textbox.txt.delete(1.0, END)
        list_of_date = self._activity_service.create_statistic_activities_by_free_time()
        show = "These are the busiest days: "
        for i in list_of_date:
            show += "On the day " + str(i[0]) + " you have " + str(i[1]) + " upcoming activities" + '\n'
        textbox.txt.insert(1.0, show)

    def gui_create_statistics_by_date(self, textbox, date):
        textbox.txt.delete(1.0, END)
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
            print(new_date)
            activities = self._activity_service.create_statistic_activities_by_date(new_date)
            show = "There are " + str(len(activities)) + " activities in total in the Activity Planner"
            for i in activities:
                show += str(i) + "\n"
            textbox.txt.insert(1.0, show)

    def gui_undo(self, textbox):
        textbox.txt.delete(1.0, END)
        try:
            self._undo_controller.undo()
            textbox.txt.insert(1.0, "Operation successfully undone!")
        except Exception as e:
            textbox.txt.insert(1.0, e)

    def gui_redo(self, textbox):
        textbox.txt.delete(1.0, END)
        try:
            self._undo_controller.redo()
            textbox.txt.insert(1.0, "Operation successfully redone!")
        except Exception as e:
            textbox.txt.insert(1.0, e)


class MainMenu(tk.Tk):
    def __init__(self, gui):
        tk.Tk.__init__(self)
        self.geometry("1080x720")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Activity Planner")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (
                StartPage, ListPersonsPage, ListActivitiesPage, ManagePersonsActivities, ManagePersons,
                ManageActivities, AddPerson, RemovePerson, UpdatePerson, AddActivity, RemoveActivity,
                UpdateActivity, CreateStatistics, StatisticsDate, StatisticsBusiest):
            page_name = F.__name__
            if F == StartPage:
                frame = F(parent=container, controller=self, gui=gui)
            else:
                frame = F(parent=container, controller=self, gui=gui, textbox=self.frames["StartPage"].textbox)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartText(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, padx=0, pady=2)
        self.configure(bg="#c48aff")
        self.txt.configure(bg="#c48aff", font=("Lucida Calligraphy", 20), pady=50)
        self.txt.tag_configure("tag", justify='center')
        self.txt.insert(1.0, "Welcome to your Activity Planner!")
        self.txt.tag_add("tag", "1.0", "end")


class Text(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, padx=0, pady=2)
        self.configure(bg="#c48aff")
        self.txt.configure(bg="#c48aff", pady=10)
        self.txt.tag_configure("tag", justify='center')
        self.txt.tag_add("tag", "1.0", "end")


class StartPage(tk.Frame):
    def __init__(self, parent, controller, gui):
        tk.Frame.__init__(self, parent)
        color_page = "#c48aff"
        color_bg = "#c48aff"
        color_button = "#adadff"
        color_active = "#d6adff"

        """root = tk.Tk()

        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'background.gif')
        photo = PhotoImage(file=image_path)"""

        self.configure(bg=color_bg)
        self.controller = controller

        self.textbox = StartText(self)
        self.textbox.place(relx=-0.15, rely=-0.01, relwidth=5.5, relheight=0.25)
        button_height = 0.1
        button_width = 0.4
        button1 = tk.Button(self, text="Manage persons and activities", font=40,
                            command=lambda: controller.show_frame("ManagePersonsActivities"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button1.place(relx=0.33, rely=0.15, relheight=button_height, relwidth=button_width)
        button2 = tk.Button(self, text="List persons", font=40,
                            command=lambda: controller.show_frame("ListPersonsPage"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button2.place(relx=0.33, rely=0.27, relheight=button_height, relwidth=button_width)
        button3 = tk.Button(self, text="List activities", font=40,
                            command=lambda: controller.show_frame("ListActivitiesPage"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button3.place(relx=0.33, rely=0.39, relheight=button_height, relwidth=button_width)
        button4 = tk.Button(self, text="Search for persons or activities", font=40,
                            command=lambda: controller.show_frame("SearchPage"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button4.place(relx=0.33, rely=0.51, relheight=button_height, relwidth=button_width)
        button5 = tk.Button(self, text="Create Statistics", font=40,
                            command=lambda: controller.show_frame("CreateStatistics"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button5.place(relx=0.33, rely=0.63, relheight=button_height, relwidth=button_width)


class TextScrollCombo(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scroll = tk.Scrollbar(self, command=self.txt.yview)
        scroll.grid(row=0, column=1, sticky='nsew')
        self.configure(bg="#e5d7f4")
        self.txt.configure(bg="#e5d7f4")
        self.txt['yscrollcommand'] = scroll.set
        self.txt.insert(1.0, "This is the list of the persons")


class ListPersonsPage(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#c48aff"
        self.color_bg = "#c48aff"
        self.color_active = "#d6adff"
        self.gui = gui
        color_page = "#c48aff"
        starting_point = 0.2
        space_between = 0.06
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)

        self.configure(bg=color_page)
        self.controller = controller

        self.textbox = textbox
        self.textbox = TextScrollCombo(self)
        self.textbox.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.8)

        gui.gui_list_persons(self.textbox)


class ListActivitiesPage(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#c48aff"
        self.color_bg = "#c48aff"
        self.color_active = "#d6adff"
        self.gui = gui
        self.textbox = textbox
        color_page = "#c48aff"
        starting_point = 0.2
        space_between = 0.06
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)

        self.configure(bg=color_page)
        self.controller = controller
        self.textbox = TextScrollCombo(self)
        self.textbox.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.8)
        gui.gui_list_activities(self.textbox)


class ManagePersonsActivities(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        self.button_height = 0.1
        self.button_width = 0.4
        button1 = tk.Button(self, text="Manage persons", font=40,
                            command=lambda: controller.show_frame("ManagePersons"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button1.place(relx=0.33, rely=0.15, relheight=self.button_height, relwidth=self.button_width)
        button2 = tk.Button(self, text="Manage activities", font=40,
                            command=lambda: controller.show_frame("ManageActivities"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button2.place(relx=0.33, rely=0.27, relheight=self.button_height, relwidth=self.button_width)


class ManagePersons(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        self.button_height = 0.1
        self.button_width = 0.4
        button1 = tk.Button(self, text="Add a person", font=40,
                            command=lambda: controller.show_frame("AddPerson"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button1.place(relx=0.33, rely=0.15, relheight=self.button_height, relwidth=self.button_width)
        button2 = tk.Button(self, text="Remove a person", font=40,
                            command=lambda: controller.show_frame("RemovePerson"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button2.place(relx=0.33, rely=0.27, relheight=self.button_height, relwidth=self.button_width)
        button3 = tk.Button(self, text="Update a person", font=40,
                            command=lambda: controller.show_frame("UpdatePerson"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button3.place(relx=0.33, rely=0.39, relheight=self.button_height, relwidth=self.button_width)


class ManageActivities(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        self.button_height = 0.1
        self.button_width = 0.4
        button1 = tk.Button(self, text="Add an activity", font=40,
                            command=lambda: controller.show_frame("AddActivity"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button1.place(relx=0.33, rely=0.15, relheight=self.button_height, relwidth=self.button_width)
        button2 = tk.Button(self, text="Remove an activity", font=40,
                            command=lambda: controller.show_frame("RemoveActivity"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button2.place(relx=0.33, rely=0.27, relheight=self.button_height, relwidth=self.button_width)
        button3 = tk.Button(self, text="Update an activity", font=40,
                            command=lambda: controller.show_frame("UpdateActivity"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button3.place(relx=0.33, rely=0.39, relheight=self.button_height, relwidth=self.button_width)


class AddPerson(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_name_phone_field(starting_point, self.add_person_action, "Add person")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)

    def add_person_action(self, entry_id, entry_name, entry_phone):
        self.gui.gui_add_person(self.textbox, entry_id.get(), entry_name.get(), entry_phone.get())
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        entry_phone.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_name_phone_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        entry_name = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_name.place(relx=0.11 + self.button_width, rely=0.3,
                         relheight=self.button_height, relwidth=0.3)
        entry_name.insert(0, "Name: ")
        entry_name.bind("<FocusIn>", lambda args: entry_name.delete(0, END) if entry_name.get() == "Name: " else None)
        entry_name.bind("<FocusOut>", lambda args: entry_name.insert(0, "Name: ") if entry_name.get() == "" else None)

        entry_phone = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_phone.place(relx=0.11 + self.button_width, rely=0.4,
                          relheight=self.button_height, relwidth=0.3)
        entry_phone.insert(0, "Phone number: ")
        entry_phone.bind("<FocusIn>",
                         lambda args: entry_phone.delete(0, END) if entry_phone.get() == "Phone number: " else None)
        entry_phone.bind("<FocusOut>",
                         lambda args: entry_phone.insert(0, "Phone number: ") if entry_phone.get() == "" else None)

        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id, entry_name, entry_phone),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class RemovePerson(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_field(starting_point, self.remove_person_action, "Remove person")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)

    def remove_person_action(self, entry_id):
        self.gui.gui_remove_person(self.textbox, entry_id.get())
        entry_id.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class UpdatePerson(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_name_phone_field(starting_point, self.update_person_action, "Update person")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 10, relheight=0.05, relwidth=0.1)

    def update_person_action(self, entry_id, entry_name, entry_phone):
        self.gui.gui_update_person(self.textbox, entry_id.get(), entry_name.get(), entry_phone.get())
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        entry_phone.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_name_phone_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        entry_name = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_name.place(relx=0.11 + self.button_width, rely=0.3,
                         relheight=self.button_height, relwidth=0.3)
        entry_name.insert(0, "Name: ")
        entry_name.bind("<FocusIn>", lambda args: entry_name.delete(0, END) if entry_name.get() == "Name: " else None)
        entry_name.bind("<FocusOut>", lambda args: entry_name.insert(0, "Name: ") if entry_name.get() == "" else None)

        entry_phone = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_phone.place(relx=0.11 + self.button_width, rely=0.4,
                          relheight=self.button_height, relwidth=0.3)
        entry_phone.insert(0, "Phone number: ")
        entry_phone.bind("<FocusIn>",
                         lambda args: entry_phone.delete(0, END) if entry_phone.get() == "Phone number: " else None)
        entry_phone.bind("<FocusOut>",
                         lambda args: entry_phone.insert(0, "Phone number: ") if entry_phone.get() == "" else None)

        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id, entry_name, entry_phone),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class AddActivity(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_pers_date_time_descr_field(starting_point, self.add_activity_action, "Add activity")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 11, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 11, relheight=0.05, relwidth=0.1)

    def add_activity_action(self, entry_id, entry_person_id, entry_date, entry_time, entry_description):
        self.gui.gui_add_activity(self.textbox, entry_id.get(), entry_person_id.get(), entry_date.get(),
                                  entry_time.get(), entry_description.get())
        entry_id.delete(0, END)
        entry_person_id.delete(0, END)
        entry_date.delete(0, END)
        entry_time.delete(0, END)
        entry_description.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_pers_date_time_descr_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        entry_person_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_person_id.place(relx=0.11 + self.button_width, rely=0.3,
                              relheight=self.button_height, relwidth=0.3)
        entry_person_id.insert(0, "Persons ids: ")
        entry_person_id.bind("<FocusIn>",
                             lambda args: entry_person_id.delete(0,
                                                                 END) if entry_person_id.get() == "Persons ids: " else None)
        entry_person_id.bind("<FocusOut>",
                             lambda args: entry_person_id.insert(0,
                                                                 "Persons ids: ") if entry_person_id.get() == "" else None)

        entry_date = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_date.place(relx=0.11 + self.button_width, rely=0.4,
                         relheight=self.button_height, relwidth=0.3)
        entry_date.insert(0, "Date (in the format dd/mm/yyyy): ")
        entry_date.bind("<FocusIn>",
                        lambda args: entry_date.delete(0,
                                                       END) if entry_date.get() == "Date (in the format dd/mm/yyyy): " else None)
        entry_date.bind("<FocusOut>",
                        lambda args: entry_date.insert(0,
                                                       "Date (in the format dd/mm/yyyy): ") if entry_date.get() == "" else None)

        entry_time = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_time.place(relx=0.11 + self.button_width, rely=0.5,
                         relheight=self.button_height, relwidth=0.3)
        entry_time.insert(0, "Time (in the format hh:mm:ss): ")
        entry_time.bind("<FocusIn>",
                        lambda args: entry_time.delete(0,
                                                       END) if entry_time.get() == "Time (in the format hh:mm:ss): " else None)
        entry_time.bind("<FocusOut>",
                        lambda args: entry_time.insert(0,
                                                       "Time (in the format hh:mm:ss): ") if entry_time.get() == "" else None)

        entry_description = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_description.place(relx=0.11 + self.button_width, rely=0.6,
                                relheight=self.button_height, relwidth=0.3)
        entry_description.insert(0, "Description: ")
        entry_description.bind("<FocusIn>",
                               lambda args: entry_description.delete(0,
                                                                     END) if entry_description.get() == "Description: " else None)
        entry_description.bind("<FocusOut>",
                               lambda args: entry_description.insert(0,
                                                                     "Description: ") if entry_description.get() == "" else None)

        button = tk.Button(self, text=button_text, font=50,
                           command=lambda: function(entry_id, entry_person_id, entry_date, entry_time,
                                                    entry_description),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class RemoveActivity(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_field(starting_point, self.remove_activity_action, "Remove activity")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 7, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 7, relheight=0.05, relwidth=0.1)

    def remove_activity_action(self, entry_id):
        self.gui.gui_remove_activity(self.textbox, entry_id.get())
        entry_id.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        button = tk.Button(self, text=button_text, font=50,
                           command=lambda: function(entry_id),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class UpdateActivity(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.id_pers_date_time_descr_field(starting_point, self.update_activity_action, "Updateactivity")
        self.textbox = Text(self)
        self.textbox.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)
        button_undo = tk.Button(self, text="Undo", font=40,
                                command=self.undo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_undo.place(relx=0.1, rely=starting_point + space_between * 11, relheight=0.05, relwidth=0.1)
        button_redo = tk.Button(self, text="Redo", font=40,
                                command=self.redo_action,
                                bg=self.color_bg, activebackground=self.color_active,
                                highlightbackground=self.color_page)
        button_redo.place(relx=0.21, rely=starting_point + space_between * 11, relheight=0.05, relwidth=0.1)

    def update_activity_action(self, entry_id, entry_person_id, entry_date, entry_time, entry_description):
        self.gui.gui_update_activity(self.textbox, entry_id.get(), entry_person_id.get(), entry_date.get(),
                                     entry_time.get(), entry_description.get())
        entry_id.delete(0, END)
        entry_person_id.delete(0, END)
        entry_date.delete(0, END)
        entry_time.delete(0, END)
        entry_description.delete(0, END)

    def undo_action(self):
        self.gui.gui_undo(self.textbox)

    def redo_action(self):
        self.gui.gui_redo(self.textbox)

    def id_pers_date_time_descr_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)

        entry_person_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_person_id.place(relx=0.11 + self.button_width, rely=0.3,
                              relheight=self.button_height, relwidth=0.3)
        entry_person_id.insert(0, "Persons ids: ")
        entry_person_id.bind("<FocusIn>",
                             lambda args: entry_person_id.delete(0,
                                                                 END) if entry_person_id.get() == "Persons ids: " else None)
        entry_person_id.bind("<FocusOut>",
                             lambda args: entry_person_id.insert(0,
                                                                 "Persons ids: ") if entry_person_id.get() == "" else None)

        entry_date = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_date.place(relx=0.11 + self.button_width, rely=0.4,
                         relheight=self.button_height, relwidth=0.3)
        entry_date.insert(0, "Date (in the format dd/mm/yyyy): ")
        entry_date.bind("<FocusIn>",
                        lambda args: entry_date.delete(0,
                                                       END) if entry_date.get() == "Date (in the format dd/mm/yyyy): " else None)
        entry_date.bind("<FocusOut>",
                        lambda args: entry_date.insert(0,
                                                       "Date (in the format dd/mm/yyyy): ") if entry_date.get() == "" else None)

        entry_time = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_time.place(relx=0.11 + self.button_width, rely=0.5,
                         relheight=self.button_height, relwidth=0.3)
        entry_time.insert(0, "Time (in the format hh:mm:ss): ")
        entry_time.bind("<FocusIn>",
                        lambda args: entry_time.delete(0,
                                                       END) if entry_time.get() == "Time (in the format hh:mm:ss): " else None)
        entry_time.bind("<FocusOut>",
                        lambda args: entry_time.insert(0,
                                                       "Time (in the format hh:mm:ss): ") if entry_time.get() == "" else None)

        entry_description = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_description.place(relx=0.11 + self.button_width, rely=0.6,
                                relheight=self.button_height, relwidth=0.3)
        entry_description.insert(0, "Description: ")
        entry_description.bind("<FocusIn>",
                               lambda args: entry_description.delete(0,
                                                                     END) if entry_description.get() == "Description: " else None)
        entry_description.bind("<FocusOut>",
                               lambda args: entry_description.insert(0,
                                                                     "Description: ") if entry_description.get() == "" else None)

        button = tk.Button(self, text=button_text, font=50,
                           command=lambda: function(entry_id, entry_person_id, entry_date, entry_time,
                                                    entry_description),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class CreateStatistics(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        self.button_height = 0.15
        self.button_width = 0.4
        button1 = tk.Button(self,
                            text="Activities for a given date.\n List the activities for a given date\n "
                                 "in the order of their start time.", font=40,
                            command=lambda: controller.show_frame("StatisticsDate"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button1.place(relx=0.33, rely=0.15, relheight=self.button_height, relwidth=self.button_width)
        button2 = tk.Button(self, text="Busiest days. This will provide the list\nof upcoming dates with activities,"
                                       " sorted in \nascending order of the free time in that day \n(all intervals "
                                       "with no activities).", font=40,
                            command=lambda: controller.show_frame("StatisticsBusiest"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button2.place(relx=0.33, rely=0.38, relheight=self.button_height, relwidth=self.button_width)
        button3 = tk.Button(self, text="Activities with a given person.\n List all upcoming activities to which a"
                                       " given\n person will participate.", font=40,
                            command=lambda: controller.show_frame("StatisticsPerson"),
                            bg=self.color_button, activebackground=self.color_active,
                            highlightbackground=self.color_page)
        button3.place(relx=0.33, rely=0.60, relheight=self.button_height, relwidth=self.button_width)


class StatisticsDate(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#39d668"
        self.color_bg = "#d2b0fc"
        self.color_active = "#bc88fc"
        self.color_field = "#d7d7f4"
        self.color_button = "#adadff"
        self.id_height = self.button_height
        self.id_width = 0.1
        self.gui = gui
        self.textbox = textbox
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)
        starting_point = 0.2
        space_between = 0.06
        self.date_field(starting_point, self.create_statistics_date_action, "Create statistics")
        self.textbox = TextScrollCombo(self)
        self.textbox.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    def create_statistics_date_action(self, entry_date):
        self.gui.gui_create_statistics_by_date(self.textbox, entry_date.get())
        entry_date.delete(0, END)

    def date_field(self, posy, function, button_text):
        entry_date = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_date.place(relx=0.2 + self.button_width, rely=0.2,
                         relheight=self.button_height, relwidth=0.3)
        entry_date.insert(0, "Date: ")
        entry_date.bind("<FocusIn>",
                        lambda args: entry_date.delete(0,
                                                       END) if entry_date.get() == "Date: " else None)
        entry_date.bind("<FocusOut>",
                        lambda args: entry_date.insert(0,
                                                       "Date: ") if entry_date.get() == "" else None)

        button = tk.Button(self, text=button_text, font=50,
                           command=lambda: function(entry_date),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)


class StatisticsBusiest(tk.Frame):
    def __init__(self, parent, controller, gui, textbox):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#c48aff")
        self.controller = controller
        self.button_height = 0.05
        self.button_width = 0.25
        self.color_page = "#c48aff"
        self.color_bg = "#c48aff"
        self.color_active = "#d6adff"
        self.gui = gui
        self.textbox = textbox
        color_page = "#c48aff"
        starting_point = 0.2
        space_between = 0.06
        back_button = tk.Button(self, text="Back", font=40,
                                command=lambda: self.controller.show_frame("StartPage"),
                                bg="#adadff", activebackground="#d6adff",
                                highlightbackground=self.color_page)
        back_button.place(relx=0.03, rely=0.03, relheight=0.05, relwidth=0.1)

        self.configure(bg=color_page)
        self.controller = controller
        self.textbox = TextScrollCombo(self)
        self.textbox.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.8)
        gui.gui_create_statistic_activities_by_free_time(self.textbox)
