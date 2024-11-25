import os
import json
import csv
import datetime
import pandas as pd

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp

class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.note_id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print('Заметка успешно добавлена')

    def list_notes(self):
        if not self.notes:
            print('Список заметок пуст')
            return
        for note in self.notes:
            print(f'{note.note_id}. {note.title} (дата: {note.timestamp})')
        
    def get_note_by_id(self, note_id) -> Note:
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f'Заголовок: {note.title}')
            print(f'Содержимое: {note.content}')
            print(f'Дата последнего изменения: {note.timestamp}')
        else:
            print('Заметка не найдена')

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_notes()
            print('Заметка успешно отредактирована')
        else:
            print('Заметка не найдена')

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print('Заметка успешно удалена')
        else:
            print('Заметка не найдена')
    
    def export_notes_to_csv(self):
        if not self.notes:
            print('Список заметок пуст')
            return
        file_name = 'notes.csv'
        with open(file_name, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['ID', 'Заголовок', 'Содержимое', 'Дата'])
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    'ID': note.note_id,
                    'Заголовок': note.title,
                    'Содержимое': note.content,
                    'Дата': note.timestamp
                })
        print( f'Заметки успешно экспортированы в файл {file_name}')

    def import_notes_from_csv(self):
        file_name = input('Введите имя CSV-файла: ')
        if not os.path.exists(file_name):
            print(f'Файл {file_name} не найден')
            return
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                note_id = max([note.note_id for note in self.notes], default=0) + 1
                title = row.get['Заголовок', '']
                content = row.get['Содержимое', '']
                timestamp = row.get['Дата', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                new_note = Note(note_id, title, content, timestamp)
                self.notes.append(new_note)
            self.save_notes()
        print(f'Заметки успешно импортированы из файла {file_name}')

def notes_menu():
    manager = NoteManager()
    while True:
        print('Управление заметками:')
        print('1. Добавить новую заметку')
        print('2. Просмотреть список заметок')
        print('3. Посмотреть заметку')
        print('4. Редактировать заметку')
        print('5. Удалить заметку')
        print('6. Экспорт заметок в CSV')
        print('7. Импорт заметок из CSV')
        print('8. Назад')

        choise = int(input('Введите номер действия: '))

        if choise == 1:
            title = input('Введите заголовок заметки: ')
            content = input('Введите содержание заметки: ')
            manager.add_note(title, content)
        elif choise == 2:
            manager.list_notes()
        elif choise == 3:
            try:
                note_id = int(input('Введите ID заметки: '))
                manager.view_note(note_id)
            except ValueError:
                print('ID заметки не корректен')
        elif choise == 4:
            try:
                note_id = int(input('Введите ID заметки: '))
                new_title = input('Введите новый заголовок заметки: ')
                new_content = input('Введите новое содержание заметки: ')
                manager.edit_note(note_id, new_title, new_content)
            except ValueError:
                print('ID заметки не корректен')
        elif choise == 5:
            try:
                note_id = int(input('Введите ID заметки: '))
                manager.delete_note(note_id)
            except ValueError:
                print('ID заметки не корректен')
        elif choise == 6:
            manager.export_notes_to_csv()
        elif choise == 7:
            manager.import_notes_from_csv()
        elif choise == 8:
            break
        else:
            print('Неверный номер действия, попробуйте снова')

class Task:
    def __init__(self, task_id, title, description, done=False, priority="Средний", due_date=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data(TASKS_FILE, [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data(TASKS_FILE, data)

    def add_task(self, title, description, priority="Средний", due_date=None):
        valid_priorities = ['Низкий', 'Средний', 'Высокий']
        if priority not in valid_priorities:
            print("Ошибка: Некорректное значение приоритета. Выберите из: Низкий, Средний, Высокий.")
            return
        try:
            datetime.datetime.strptime(due_date, '%d-%m-%Y')  # Проверка формата ДД-ММ-ГГГГ
        except ValueError:
            print("Ошибка: Некорректный формат даты. Укажите дату в формате ДД-ММ-ГГГГ.")
            return
        task_id = max([task.task_id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, title, description, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print('Задача успешно добавлена')

    def list_tasks(self):
        if not self.tasks:
            print('Список задач пуст')
            return
        for task in self.tasks:
            print(f"{task.task_id}. {task.title} (Статус: {'Выполнено' if task.done else 'Не выполнено'}, Приоритет: {task.priority}, Срок: {task.due_date})")
            print(f"   Содержимое: {task.description}")


    def mark_task_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print('Задача успешно выполнена')
        else:
            print('Задача не найдена')

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def edit_task(self, task_id, new_title=None, new_description=None, new_priority=None, new_due_date=None):
        task = self.get_task_by_id(task_id)
        if task:
            task.title = new_title or task.title
            task.description = new_description or task.description
            task.priority = new_priority or task.priority
            task.due_date = new_due_date or task.due_date
            self.save_tasks()
            print('Задача успешно отредактирована')
        else:
            print('Задача не найдена')

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print('Задача успешно удалена')
        else:
            print('Задача не найдена')

    def export_tasks_to_csv(self):
        if not self.tasks:
            print('Список задач пуст')
            return
        file_name = 'tasks.csv'
        with open(file_name, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['ID', 'Заголовок', 'Описание', 'Статус', 'Приоритет', 'Срок'])
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'ID': task.task_id,
                    'Заголовок': task.title,
                    'Описание': task.description,
                    'Статус': 'Выполненo' if task.done else 'Не выполненo',
                    'Приоритет': task.priority,
                    'Срок': task.due_date
                })
        print( f'Задачи успешно экспортированы в файл {file_name}')

    def import_tasks_from_csv(self):
        file_name = input('Введите имя CSV-файла: ')
        if not os.path.exists(file_name):
            print(f'Файл {file_name} не найден')
            return
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task_id = max([task.task_id for task in self.tasks], default=0) + 1
                title = row.get('Заголовок', '')
                description = row.get('Описание', '')
                done = row.get('Статус', 'Не выполненo') == 'Выполненo'
                priority = row.get('Приоритет', 'Средний')
                due_date = row.get('Срок', None)
                new_task = Task(task_id, title, description, done, priority, due_date)
                self.tasks.append(new_task)
            self.save_tasks()
        print(f'Задачи успешно импортированы из файла {file_name}')

    def import_tasks_from_csv(self):
        file_name = input('Введите имя CSV-файла: ')

def tasks_menu():
    manager = TaskManager()
    while True:
        print('Управление задачами:')
        print('1. Добавить новую задачу')
        print('2. Просмотреть список задач')
        print('3. Отметить задачу как выполненную')
        print('4. Редактировать задачу')
        print('5. Удалить задачу')
        print('6. Экспортировать задачи в CSV')
        print('7. Импортировать задачи из CSV')
        print('8. Назад')

        choise = int(input('Введите номер действия: '))

        if choise == 1:
            title = input('Введите заголовок задачи: ')
            description = input('Введите описание задачи: ')
            priority = input('Введите приоритет задачи (Низкий, Средний, Высокий): ').strip()
            due_date = input('Введите срок выполнения задачи (ДД-ММ-ГГГГ): ').strip()
            manager.add_task(title, description, priority, due_date)
            if priority in ['Низкий', 'Средний', 'Высокий'] and is_valid_date(due_date):
                break
        elif choise == 2:
            manager.list_tasks()
        elif choise == 3:
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.mark_task_done(task_id)
            except ValueError:
                print('ID задачи не корректен')
        elif choise == 4:
            try:
                task_id = int(input('Введите ID задачи: '))
                new_title = input('Введите новый заголовок задачи: ')
                new_description = input('Введите новое описание задачи: ')
                new_priority = input('Введите новый приоритет задачи (Низкий, Средний, Высокий): ') 
                new_due_date = input('Введите новый срок выполнения задачи (ДД-ММ-ГГГГ): ')
                manager.edit_task(task_id, new_title, new_description, new_priority, new_due_date)
            except ValueError:
                print('ID задачи не корректен')
        elif choise == 5:
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.delete_task(task_id)
            except ValueError:
                print('ID задачи не корректен')
        elif choise == 6:
            manager.export_tasks_to_csv()
        elif choise == 7:
            manager.import_tasks_from_csv()
        elif choise == 8:
            break
        else:
            print('Неверный номер действия, попробуйте снова')

def main_menu():
    while True:
        print ('Добро пожаловать в Персональный помощник!')
        print('Выберите действие:')
        print('1. Управление заметками')
        print('2. Управление задачами')
        print('3. Управление контактами')
        print('4. Управление финансовыми записями')
        print('5. Калькулятор')
        print('6. Выход')

        choise = int(input('Введите номер действия: '))

        if choise == 1:
            notes_menu()
        elif choise == 2:
            tasks_menu()
        elif choise == 6:
            print('До свидания!')
            break
        else:
            print('Неверный номер действия, попробуйте снова')

if __name__ == '__main__':
    main_menu()
