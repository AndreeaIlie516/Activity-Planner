from src.repo.personRepository import PersonRepository
from src.repo.activityRepository import ActivityRepository
from src.service.personService import PersonService
from src.service.activityService import ActivityService
from src.service.undoService import *
from src.ui.ui import UI
from src.ui.gui import GUI

if __name__ == '__main__':
    """
    The main function
    """
    person_repository = PersonRepository()
    activity_repository = ActivityRepository()
    undoController = UndoController()
    person_service = PersonService(person_repository, activity_repository, undoController, generate=True)
    activity_service = ActivityService(person_repository, activity_repository, person_service, undoController, generate=True)
    # person_service = PersonService(person_repository, activity_repository, )
    # activity_service = ActivityService(person_repository, activity_repository, person_service, undoController, generate=True)
    # person_service = PersonService(person_repository, activity_repository, activity_service, undoController, generate=True)
    ui = UI(person_service, activity_service, undoController)
    ui.create_menu()
    # gui = GUI(person_service, activity_service, undoController)
    # gui.start()

