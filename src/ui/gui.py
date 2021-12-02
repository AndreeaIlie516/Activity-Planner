import tkinter
import tkinter as tk
from tkinter import END
from tkinter import font as tkfont
from tkinter import *
from PIL import ImageTk, Image
import os

from src.service.personService import PersonService
from src.service.activityService import ActivityService


class GUI:
    def __init__(self, person_service, activity_service, undo_service):
        self._undo_service = undo_service
        self._person_service = person_service
        self._activity_service = activity_service

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
        show = "There are " + str(len(self._person_service.persons)) + " persons in the Activity Planner.\n"
        for i in self._person_service.persons:
            show += str(i) + "\n"
        textbox.txt.insert(1.0, show)

    def gui_list_activities(self, textbox):
        textbox.txt.delete(1.0, END)
        show = "There are " + str(len(self._activity_service.activities)) + " activities in the Activity Planner.\n"
        for i in self._activity_service.activities:
            show += str(i) + "\n"
        textbox.txt.insert(1.0, show)


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
        for F in (StartPage, ListPersonsPage, ListActivitiesPage, ManagePersonsActivities):
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
        self.txt.grid(row=0, column=0,  padx=0, pady=2)
        self.configure(bg="#c48aff")
        self.txt.configure(bg="#c48aff", font=("Lucida Calligraphy", 20), pady=50)
        self.txt.tag_configure("tag", justify='center')
        self.txt.insert(1.0, "Welcome to your Activity Planner!")
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
                            command=lambda: controller.show_frame("StatisticsPage"),
                            bg=color_button, activebackground=color_active, highlightbackground=color_page)
        button5.place(relx=0.33, rely=0.63, relheight=button_height, relwidth=button_width)


class TextScrollCombo(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
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
        self.id_name_field(starting_point, self.add_person_action, "Add a person")
        self.id_name_field(starting_point + space_between, self.add_activity_action, "Add an activity")
        self.id_field(starting_point + space_between * 2, self.remove_person_action, "Remove a person")
        self.id_field(starting_point + space_between * 3, self.remove_activity_action, "Remove an activity")
        self.id_name_field(starting_point + space_between * 4, self.update_person_action, "Update a person")
        self.id_name_field(starting_point + space_between * 5, self.update_activity_action, "Update an activity")
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

    def add_person_action(self, entry_id, entry_name, entry_pohone_number):
        self.gui.gui_add_person(self.textbox, entry_id.get(), entry_name.get(), entry_phone_number.get())
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        entry_phone_number.delete(0, END)
        self.controller.show_frame("StartPage")

    def add_activity_action(self, entry_id, entry_name):
        self.gui.gui_add_activity(self.textbox, entry_id.get(), entry_name.get())
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        self.controller.show_frame("StartPage")

    def remove_person_action(self, entry_id):
        self.gui.gui_remove_student(self.textbox, entry_id.get())
        entry_id.delete(0, END)
        self.controller.show_frame("StartPage")

    def remove_activity_action(self, entry_id):
        self.gui.gui_remove_activity(self.textbox, entry_id.get())
        entry_id.delete(0, END)
        self.controller.show_frame("StartPage")

    def update_person_action(self, entry_id, entry_name):
        self.gui.gui_update_person(self.textbox, entry_id.get(), entry_name.get())
        entry_id.delete(0, END)
        self.controller.show_frame("StartPage")

    def update_activity_action(self, entry_id, entry_name):
        self.gui.gui_update_activity(self.textbox, entry_id.get(), entry_name.get())
        entry_id.delete(0, END)
        entry_name.delete(0, END)
        self.controller.show_frame("StartPage")

    def undo_action(self):
        self.gui.gui_undo(self.textbox)
        self.controller.show_frame("StartPage")

    def redo_action(self):
        self.gui.gui_redo(self.textbox)
        self.controller.show_frame("StartPage")

    def id_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)
        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id),
                           bg=self.color_field, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)

    def id_name_field(self, posy, function, button_text):
        entry_id = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id.insert(0, "Id: ")
        entry_id.bind("<FocusIn>", lambda args: entry_id.delete(0, END) if entry_id.get() == "Id: " else None)
        entry_id.bind("<FocusOut>", lambda args: entry_id.insert(0, "Id: ") if entry_id.get() == "" else None)
        entry_name = tk.Entry(self, font=40, bg=self.color_field, highlightbackground=self.color_page)
        entry_name.place(relx=0.12 + self.button_width + self.id_width, rely=posy,
                         relheight=self.button_height, relwidth=0.3)
        entry_name.insert(0, "Name: ")
        entry_name.bind("<FocusIn>", lambda args: entry_name.delete(0, END) if entry_name.get() == "Name: " else None)
        entry_name.bind("<FocusOut>", lambda args: entry_name.insert(0, "Name: ") if entry_name.get() == "" else None)
        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id, entry_name),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)

    def id_id_name_field(self, posy, function, button_text):
        entry_id1 = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_id1.place(relx=0.11 + self.button_width, rely=posy, relheight=self.id_height, relwidth=self.id_width)
        entry_id1.insert(0, "Student: ")
        entry_id1.bind("<FocusIn>",
                       lambda args: entry_id1.delete(0, END) if entry_id1.get() == "Student: " else None)
        entry_id1.bind("<FocusOut>",
                       lambda args: entry_id1.insert(0, "Student: ") if entry_id1.get() == "" else None)
        entry_id2 = tk.Entry(self, font=40, bg=self.color_field, highlightbackground=self.color_page)
        entry_id2.place(relx=0.11 + self.button_width + self.id_width + 0.01, rely=posy,
                        relheight=self.id_height, relwidth=self.id_width)
        entry_id2.insert(0, "Discipline: ")
        entry_id2.bind("<FocusIn>",
                       lambda args: entry_id2.delete(0, END) if entry_id2.get() == "Discipline: " else None)
        entry_id2.bind("<FocusOut>",
                       lambda args: entry_id2.insert(0, "Discipline: ") if entry_id2.get() == "" else None)
        entry_grade = tk.Entry(self, font=40, bg=self.color_bg, highlightbackground=self.color_page)
        entry_grade.place(relx=0.13 + self.button_width + self.id_width * 2, rely=posy,
                          relheight=self.id_height, relwidth=self.id_width)
        entry_grade.insert(0, "Grade: ")
        entry_grade.bind("<FocusIn>",
                         lambda args: entry_grade.delete(0, END) if entry_grade.get() == "Grade: " else None)
        entry_grade.bind("<FocusOut>",
                         lambda args: entry_grade.insert(0, "Grade: ") if entry_grade.get() == "" else None)
        button = tk.Button(self, text=button_text, font=40,
                           command=lambda: function(entry_id1, entry_id2, entry_grade),
                           bg=self.color_bg, activebackground=self.color_active, highlightbackground=self.color_page)
        button.place(relx=0.1, rely=posy, relheight=self.button_height, relwidth=self.button_width)