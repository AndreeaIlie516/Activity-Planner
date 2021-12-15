from configparser import ConfigParser
from src.repository.baseRepository.personRepository import PersonRepository
from src.repository.baseRepository.activityRepository import ActivityRepository
from src.services.undoService import UndoController
from src.repository.CSVRepository.personRepositoryCSV import PersonRepositoryCSV
from src.repository.CSVRepository.activityRepositoryCSV import ActivityRepositoryCSV
from src.repository.binaryRepository.personRepositoryBinary import PersonRepositoryBinary
from src.repository.binaryRepository.activityRepositoryBinary import ActivityRepositoryBinary
from src.repository.jsonRepository.personRepositoryJson import PersonRepositoryJson
from src.repository.jsonRepository.activitiesRepositoryJson import ActivityRepositoryJson
from src.repository.databaseRepository.personRepositoryDatabase import PersonRepositoryDatabase
from src.repository.databaseRepository.activityRepositoryDatabase import ActivityRepositoryDatabase
from src.services.personService import PersonService
from src.services.activityService import ActivityService
from src.ui.ui import UI
from src.ui.gui import GUI


class Settings:
    def __init__(self):
        parser = ConfigParser()
        parser.read("settings.properties")
        self.ui = None
        self.ui = UI
        ui_style = parser.get("options", "ui")
        if ui_style == "console":
            self.ui = UI
        elif ui_style == "gui":
            self.ui = GUI
        repo_style = parser.get("options", "repository")
        if repo_style == "inmemory":
            person_repository = PersonRepository()
            activity_repository = ActivityRepository()
            undo_controller = UndoController()
            person_service = PersonService(person_repository, activity_repository, undo_controller, generate=True)
            activity_service = ActivityService(person_repository, activity_repository, person_service, undo_controller,
                                               generate=True)
            self.ui = self.ui(person_service, activity_service, undo_controller)
        elif repo_style == "csv":
            person_repository_csv = PersonRepositoryCSV(parser.get("options", "persons"))
            activity_repository_csv = ActivityRepositoryCSV(parser.get("options", "activities"))
            undo_controller = UndoController()
            person_service = PersonService(person_repository_csv, activity_repository_csv, undo_controller,
                                           generate=False)
            activity_service = ActivityService(person_repository_csv, activity_repository_csv, person_service,
                                               undo_controller, generate=False)
            self.ui = self.ui(person_service, activity_service, undo_controller)
        elif repo_style == "binary":
            person_repository_binary = PersonRepositoryBinary(parser.get("options", "persons"))
            activity_repository_binary = ActivityRepositoryBinary(parser.get("options", "activities"))
            undo_controller = UndoController()
            person_service = PersonService(person_repository_binary, activity_repository_binary, undo_controller,
                                           generate=False)
            activity_service = ActivityService(person_repository_binary, activity_repository_binary, person_service,
                                               undo_controller, generate=False)
            self.ui = self.ui(person_service, activity_service, undo_controller)
        elif repo_style == "json":
            person_repository_json = PersonRepositoryJson(parser.get("options", "persons"))
            activity_repository_json = ActivityRepositoryJson(parser.get("options", "activities"))
            undo_controller = UndoController()
            person_service = PersonService(person_repository_json, activity_repository_json, undo_controller,
                                           generate=False)
            activity_service = ActivityService(person_repository_json, activity_repository_json, person_service,
                                               undo_controller, generate=False)
            self.ui = self.ui(person_service, activity_service, undo_controller)
        elif repo_style == "database":
            person_repository_database = PersonRepositoryDatabase(parser.get("options", "persons"))
            activity_repository_database = ActivityRepositoryDatabase(parser.get("options", "activities"))
            undo_controller = UndoController()
            person_service = PersonService(person_repository_database, activity_repository_database, undo_controller,
                                           generate=False)
            activity_service = ActivityService(person_repository_database, activity_repository_database, person_service,
                                               undo_controller, generate=False)
            self.ui = self.ui(person_service, activity_service, undo_controller)

    def get_ui(self):
        return self.ui
