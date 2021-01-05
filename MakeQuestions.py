from sys import argv
from typing import Dict, List
import os
from json import load, dump

def write_quiz(filename: str, name: str, instructions: str, mode: str, other_fields: dict):
    """
    Write the given quiz to the given file with given name.
    If the file already exists, add this quiz to it, otherwise create it with only this quiz.
    If the file and quiz already exist, replace the old quiz with this - in this way it can
    be used to update quizes.
    The filename should not have `.json` extension since it must be a JSON file.
    """

    filename += ".json"

    json = dict()

    if os.path.exists(filename):
        with open(filename) as f:
            json = load(f)

    json[name] = {
        "instructions": instructions,
        "mode": mode,
    }

    for other_field_key in other_fields:
        other_field_value = other_fields[other_field_key]
        json[name][other_field_key] = other_field_value

    with open(filename, "w") as f:
        dump(json, f)

def q_and_a(filename: str, name: str, instructions: str, question_and_answers: Dict[str, str]):
    """
    Write the given instructions, questions and answers to the given file with given name.
    If the file already exists, add this quiz to it, otherwise create it with only this quiz.
    If the file and quiz already exist, replace the old quiz with this - in this way it can
    be used to update quizes.
    The filename should not have `.json` extension since it must be a JSON file.
    """

    other_fields = dict()
    other_fields["questions"] = question_and_answers

    write_quiz(filename, name, instructions, "q&a", other_fields)

def get_all(filename: str, name: str, instructions: str, prompt: str, things: List[str]):
    """
    Write the given instructions, prompt and things to the given file with given name.
    If the file already exists, add this quiz to it, otherwise create it with only this quiz.
    If the file and quiz already exist, replace the old quiz with this - in this way it can
    be used to update quizes.
    The filename should not have '.json' extension since it must be a JSON file.
    """

    other_fields = dict()
    other_fields["prompt"] = prompt
    other_fields["things"] = things

    write_quiz(filename, name, instructions, "get all", other_fields)

def get_input_q_and_a(filename: str, name: str, instructions: str):

    print("Input blank for a question when done:")
    questions_and_answers = dict()
    count = 1
    while True:
        question = input("Question {}: ".format(count))
        if question == "":
            break
        answer = input("Answer {}: ".format(count))
        questions_and_answers[question] = answer
        count += 1

    q_and_a(filename, name, instructions, questions_and_answers)

def get_input_get_all(filename: str, name: str, instructions: str):

    prompt = input("Prompt to display to the user before they enter each thing: ")

    print("Input blank for a thing when done:")
    things = []
    count = 1
    while True:
        thing = input("Thing {}: ".format(count))
        if thing == "":
            break
        things.append(thing)
        count += 1

    get_all(filename, name, instructions, prompt, things)

def get_input():
    """
    Get the file, name, instructions, questions and answers to write from the user
    and write them
    """

    filename = input("Filename without extension: ")
    name = input("Name: ")
    instructions = input("Instructions: ")

    mode = input("Mode: ")
    if mode == "q&a":
        get_input_q_and_a(filename, name, instructions)

    elif mode == "get all":
        get_input_get_all(filename, name, instructions)

    else:
        print("Invalid mode, try again")
        exit(1)

    print("Quiz saved")

if __name__ == "__main__":
    get_input()
