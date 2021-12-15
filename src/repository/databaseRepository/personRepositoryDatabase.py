from src.domain.person import Person
from src.repository.baseRepository.personRepository import PersonRepository
import mysql.connector


class PersonRepositoryDatabase(PersonRepository):
    def __init__(self, file_name):
        PersonRepository.__init__(self)
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            port='3306',
            database=file_name
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS persons (person_id INTEGER PRIMARY KEY, name VARCHAR(30), '
            'phone_number VARCHAR(11))')

    @property
    def persons(self):
        self.cursor.execute('SELECT * FROM persons;')
        persons = self.cursor.fetchall()
        return [Person(x[0], x[1], x[2]) for x in persons]

    def find_person_by_id(self, person_id):
        self.cursor.execute('SELECT * FROM persons WHERE person_id=%s;', (person_id,))
        persons = self.cursor.fetchall()
        if len(persons) == 0:
            return None
        self._person_list = [Person(x[0], x[1], x[2]) for x in persons]
        return [Person(x[0], x[1], x[2]) for x in persons][0]

    def add_person(self, person):
        self.cursor.execute(
            "INSERT INTO `activity_planner_database`.`persons` (`person_id`,`name`,`phone_numbers`) VALUES (%s, %s, "
            "%s);",
            (person.person_id, person.name, person.phone_number))
        PersonRepository.add_person(self, person)
        self.connection.commit()

    def remove_person(self, person):
        self.cursor.execute('DELETE FROM persons WHERE person_id=%s;', (person.person_id,))
        PersonRepository.remove_person(self, person)
        self.connection.commit()

    def update_person(self, person_id, name, phone_number):
        self.cursor.execute('UPDATE `activity_planner_database`.`persons` SET `name`= %s, `phone_numbers`= %s'
                            ' WHERE `person_id`= %s;', (name, phone_number, person_id))
        PersonRepository.update_person(self, person_id, name, phone_number)
        self.connection.commit()
