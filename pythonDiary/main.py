import json
import os
import sys
import time

from entry import Entry
from file_helper import create_file, read_file, validate, edit_file, append_file, FILE_PATH, search_file


def create():
    file_name = input("Enter file name in (YYYY-MM-DD) format : ")
    while not validate(file_name):
        file_name = input("Enter file name in (YYYY-MM-DD) format : ")
        validate(file_name)
    path = f'./Diary/{file_name}.txt'
    if os.path.exists(path):
        overwrite = input("Do you want to Overwrite?(yes/no) :")
        if overwrite == 'yes':
            create_entry(False, f"{file_name}.txt")
        elif overwrite == 'no':
            create_entry(True, f"{file_name}.txt")
    else:
        create_entry(False, f"{file_name}.txt")


def create_entry(append, file_name):
    task = input("Enter Task : ")
    note = input("Enter note : ")
    status = input("Enter status : ")
    entry = Entry(file_name, task, note, status)
    time_mills = str(time.time_ns())
    length = len(time_mills)
    t_mills = time_mills[length - 4:]
    dict_entry = {t_mills: json.dumps(entry.__dict__)}
    if append:
        append_file(file_name, dict_entry)
    else:
        create_file(file_name, dict_entry)


def view():
    while True:
        try:
            view_date = input("Enter date, should be in YYYY-MM-DD format : ")
            if validate(view_date):
                read_file(f"{view_date}.txt")
            else:
                continue
        except ValueError:
            print("An value error occurred")
            continue
        else:
            break


def print_file_names():
    print("File List ................")
    for file_name in os.listdir(FILE_PATH):
        if file_name.endswith(".txt"):
            print(file_name)
    #files = [file_name for file_name in os.listdir(FILE_PATH) if file_name.endswith(".txt")]
    #print(files)


def edit():
    files = [file_name for file_name in os.listdir(FILE_PATH) if file_name.endswith(".txt")]
    if len(files) <= 0:
        print("No files found")
        return

    print_file_names()
    view_date = input("Enter a date from above : ")
    read_file(f"{view_date}.txt")
    edit_entry = input("Enter an id of entry to edit : ")
    task = input("Enter Task : ")
    note = input("Enter note : ")
    status = input("Enter status : ")
    entry = Entry("file_name", task, note, status)
    edit_file(f"{view_date}.txt", edit_entry, json.dumps(entry.__dict__))


def start_diary(rules=None):
    if rules is None:
        rules = ("1. Add a new entry \n"
                 "2. View an entry\n"
                 "3. Edit an entry\n"
                 "4. Search entries\n"
                 "5. List all entries\n"
                 "6. Exit\n")
    select = ["1", "2", "3", "4", "5", "6"]

    while True:
        user_choice = input(f"\n\nWelcome to your Personal Diary! Choose an option : \n{rules} ")
        if user_choice in select:
            break
        print("That is not a valid choice.")

    if user_choice == select[0]:
        create()

    elif user_choice == select[1]:
        view()

    elif user_choice == select[2]:
        edit()

    elif user_choice == select[3]:
        search_word = input("Enter word to search : ")
        search_file(search_word)

    elif user_choice == select[4]:
        print_file_names()

    elif user_choice == select[5]:
        sys.exit(0)


while True:
    if not os.path.exists('Diary'):
        os.makedirs('Diary')
    start_diary()
    enter_again = input("Do you want to try again? (yes/no) : ")
    if enter_again != 'yes':
        break
