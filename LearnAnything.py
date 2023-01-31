from random import choice
from json import load
import os
from typing import Dict, List
from sys import argv
from CommandLineTools import menu, readyUp

def q_and_a(instructions: str, prefix: str, suffix: str, question_and_answers: Dict[str, str]):
    """
    Print the instructions to standard output and repeatedly ask the user for
    the answers to the questions until they have correctly answered them all once
    """

    if instructions == "":
        print("Enter the answer to the following questions:")
    else:
        print(instructions)

    questions = list(question_and_answers.keys())
    num_got = 0
    while questions:
        question = choice(questions)
        answer = input("\n" + prefix + question + suffix)
        if answer.lower() == question_and_answers[question].lower():
            out = "Correct"
            questions.remove(question)
            num_got += 1
        else:
            out = "Incorrect, the correct answer is " + question_and_answers[question]

        print("{}, got {}/{} = {}%".format(out, num_got, len(question_and_answers), round(num_got / len(question_and_answers) * 100)))

    print("\nAll questions answered")

def get_all(instructions: str, prompt: str, things_to_get: List[str]):
    """
    Print the instructions to standard output and repeatedly ask the user for
    a thing until they have correctly inputted them all
    """

    print(instructions)
    things_to_get = [thing.lower() for thing in things_to_get]

    things = things_to_get.copy()
    num_got = 0
    while things:
        answer = input("\n" + prompt).lower()
        if answer == "":
            print("Give up, remaining things to get are: " + ", ".join(things))
            return

        if answer in things:
            out = "Correct"
            things.remove(answer)
            num_got += 1
        elif answer in things_to_get:
            out = "Already entered"
        else:
            out = "Incorrect"

        print("{}, got {}/{} = {}%".format(out, num_got, len(things_to_get), round(num_got / len(things_to_get) * 100)))

    print("\nAll correct")

def runJSON(filename: str, name: str):
    """
    Run the quiz with the given name inside the file with given name
    """

    with open(os.path.join(os.path.dirname(__file__), filename + ".json")) as f:
        data = load(f)

    # quiz names are lower case
    name = name.lower()

    assert isinstance(data, dict), "The outermost layer of JSON must be an object"
    assert name in data, "The given name does not exist"
    obj = data[name]
    assert "instructions" in obj, "Must contain an instructions field"
    assert "mode" in obj, "Must contain a mode field"

    if obj["mode"] == "q&a":
        assert "prefix" in obj, "Must contain a prefix field"
        assert "suffix" in obj, "Must contain a suffix field"
        assert "questions" in obj, "Must contain a questions field"
        q_and_a(obj["instructions"], obj["prefix"], obj["suffix"], obj["questions"])
    
    elif obj["mode"] == "get all":
        assert "prompt" in obj, "Must contain a prompt field"
        assert "things" in obj, "Must contain a things field"
        get_all(obj["instructions"], obj["prompt"], obj["things"])

    readyUp()

def fromInput():
    """
    Get input from the user for the file and name to choose
    """

    filename = input("JSON file without extension: ")

    with open(os.path.join(os.path.dirname(__file__), filename + ".json")) as f:
        data = load(f)

    # if there is only one quiz then run that automatically
    if len(data) == 1:
        for key in data:    # this loop will necessarily only run once
            runJSON(filename, key)

    # otherwise ask the user which quiz to run
    else:
        name = menu(list(data.keys()), "Which quiz would you like to play?")
        runJSON(filename, name)

def fromCommandLineArgs():
    """
    Parse command line arguments for the file and name
    """

    assert len(argv) > 2, "Must provide JSON file and name of questions"
    runJSON(argv[1], argv[2])

if __name__ == "__main__":
    try:
        if len(argv) > 1:
            fromCommandLineArgs()
        else:
            fromInput()

    except KeyboardInterrupt:
        print(f"{os.linesep}Keyboard interrupt, exiting")
