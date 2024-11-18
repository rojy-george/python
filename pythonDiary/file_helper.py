import ast
import os
import json
import datetime

FILE_PATH = './Diary'


def validate(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return False


def create_file(filename, new_dict):
    try:
        with open(os.path.join(FILE_PATH, filename), 'w') as fp:
            write_file = json.dumps(new_dict, indent=4, sort_keys=True)
            fp.write(write_file)
            print("File " + filename + " created successfully.")
    except IOError:
        print("Error: could not create file " + filename)


def print_data(key, json_data):
    print(f"\tId : {key}.")
    print(f"\t\tTask : {json_data.get('task')}")
    print(f"\t\tNote : {json_data.get('note')}")
    print(f"\t\tStatus : {json_data.get('status')}")


def read_file(filename):
    try:
        with open(os.path.join(FILE_PATH, filename), 'r') as f:
            data = f.read()
            dict_entry = ast.literal_eval(data)
            for key, value in dict_entry.items():
                json_data = json.loads(value)
                print_data(key, json_data)

    except IOError:
        print("Error: could not read file " + filename)


def append_file(filename, new_dict):
    dict_entry = {}
    try:
        with open(os.path.join(FILE_PATH, filename), 'r') as f:
            data = f.read()
            dict_entry = ast.literal_eval(data)

        with open(os.path.join(FILE_PATH, filename), 'w') as fp:
            dict_entry.update(new_dict)
            fp.write(str(dict_entry))

        print("Entry appended to file " + filename + " successfully.")
    except IOError:
        print("Error: could not append to file " + filename)


def edit_file(filename, id, new_val):
    dict_entry = {}
    try:
        with open(os.path.join(FILE_PATH, filename), 'r') as f:
            data = f.read()
            dict_entry = ast.literal_eval(data)
            for key, value in dict_entry.items():
                print(f"id= {id}")
                if key == id:
                    dict_entry[key] = new_val

        with open(os.path.join(FILE_PATH, filename), 'w') as fp:
            fp.write(str(dict_entry))

        print("Entry edited to file " + filename + " successfully.")
    except IOError:
        print("Error: could not edit the entry " + filename)


def search_contains(json_data,search_word):
    if search_word in json_data.get('task'):
        return True
    elif search_word in json_data.get('note'):
        return True
    elif search_word in json_data.get('status'):
        return True
    else:
        return False


def search_file(search_word):
    dict_entry = {}
    try:
        for file_name in os.listdir(FILE_PATH):
            found = False
            if file_name.endswith(".txt"):
                with open(os.path.join(FILE_PATH, file_name), 'r') as f:
                    data = f.read()
                    dict_entry = ast.literal_eval(data)
                    for key, value in dict_entry.items():
                        json_data = json.loads(value)
                        if search_contains(json_data,search_word):
                            print_data(key, json_data)
                            found = True
                    if not found:
                        print(f"{search_word} not found ")

    except IOError:
        print("Could not find " + search_word)

