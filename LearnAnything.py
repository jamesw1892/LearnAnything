from random import choice
from json import load
from typing import Dict, List
from sys import argv

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
    while questions:
        question = choice(questions)
        answer = input("\n" + prefix + question + suffix)
        if answer.lower() == question_and_answers[question].lower():
            print("Correct!")
            questions.remove(question)
        else:
            print("Incorrect, the correct answer is " + question_and_answers[question])

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
        if answer in things:
            print("Correct! ", end="")
            things.remove(answer)
            num_got += 1
        elif answer in things_to_get:
            print("Already entered. ", end="")
        else:
            print("Incorrect. ", end="")

        print("Got {}/{} = {}%".format(num_got, len(things_to_get), round(num_got / len(things_to_get) * 100)))

    print("\nAll correct")

def runJSON(filename: str, name: str):
    """
    Run the quiz with the given name inside the file with given name
    """

    with open(filename + ".json") as f:
        data = load(f)

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

def fromInput():
    """
    Get input from the user for the file and name to choose
    """

    filename = input("JSON file without extension: ")
    name = input("Name of questions within JSON file: ")
    runJSON(filename, name)

def fromCommandLineArgs():
    """
    Parse command line arguments for the file and name
    """

    assert len(argv) > 2, "Must provide JSON file and name of questions"
    runJSON(argv[1], argv[2])

if __name__ == "__main__":
    if len(argv) > 1:
        fromCommandLineArgs()
    else:
        fromInput()
