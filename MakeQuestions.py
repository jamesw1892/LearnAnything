from sys import argv
from typing import Dict
import os
from json import load, dump

def main(filename: str, name: str, instructions: str, question_and_answers: Dict[str, str]):
    """
    Write the given instructions, questions and answers to the given file with given name.
    If the file already exists, add this quiz to it, otherwise create it with only this quiz.
    The filename should not have `.json` extension since it must be a JSON file.
    """

    filename += ".json"

    json = dict()

    if os.path.exists(filename):
        with open(filename) as f:
            json = load(f)
    
    json[name] = {
        "instructions": instructions,
        "questions": question_and_answers
    }

    with open(filename, "w") as f:
        dump(json, f)

def get_input():
    """
    Get the file, name, instructions, questions and answers to write from the user
    and write them
    """

    filename = input("Filename without extension: ")
    name = input("Name: ")
    instructions = input("Instructions: ")
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

    main(filename, name, instructions, questions_and_answers)

    print("Quiz saved")

if __name__ == "__main__":
    get_input()
