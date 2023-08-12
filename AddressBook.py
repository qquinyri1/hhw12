from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from info import *
import os
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts): pass

    @abstractmethod
    def display_message(self, message): pass

    @abstractmethod
    def get_user_input(self, prompt): pass

class ConsoleUserInterface(UserInterface):
    def display_contacts(self, contacts):
        if not contacts:
            print('no contacts found')
            return
        
        for contact in contacts:
            print(contact)
    
    def display_message(self, message): print(message)

    def get_user_input(self, prompt): return input(prompt).strip()

class AdressBook(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1
    
    def __str__(self) -> str:
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = ''
            if account['phones']:
                new_value = []
                for phone in account['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)
    
    def __setitem__(self, index, record):
        self.data[index] = {'name': record.name,
                            'phones': record.phones,
                            'birthday': record.birthday}

    def __getitem__(self, index):
        return self.data[index]
    
    def run(self, user_interface):
        user_interface.display_message("Welcome to Address Book Application!")

        while True:
            user_interface.display_message("Available commands:")
            user_interface.display_message("- add_contact")
            user_interface.display_message("- search_contact")
            user_interface.display_message("- remove_contact")
            user_interface.display_message("- show_all")
            user_interface.display_message("- exit")

            command = user_interface.get_user_input("Enter a command: ")

            if command == "add_contact":
                self.add_contact(user_interface)
            elif command == "search_contact":
                self.search_contact(user_interface)
            elif command == "remove_contact":
                self.remove_contact(user_interface)
            elif command == "show_all":
                self.show_all(user_interface)
            elif command == "exit":
                user_interface.display_message("Goodbye!")
                break
            else:
                user_interface.display_message("Invalid command. Please try again.")
    
    def add_contact(self, user_interface): pass

    def search_contact(self, user_interface): pass

    def remove_contact(self, user_interface): pass

    def show_all(self, user_interface):
        contacts = self.data
        user_interface.display_contacts(contacts)
    
    def load(self, file_name):
        emptyness = os.stat(file_name + '.bin')
        if emptyness.st_size != 0:
            with open(file_name + '.bin', 'rb') as file:
                self.data = pickle.load(file)
            self.log("Addressbook has been loaded!")
        else:
            self.log('Adressbook has been created!')
        return self.data
    
    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Addressbook has been saved!")
    
    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'status':
                        new_value = Status(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                             new_value.append(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False
    
    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        for account in self.data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50
