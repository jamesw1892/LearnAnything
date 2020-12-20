from random import choice
from json import load
from typing import Dict
from sys import argv

def main(instructions: str, question_and_answers: Dict[str, str]):
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
        answer = input("\n" + question + "    ")
        if answer.lower() == question_and_answers[question].lower():
            print("Correct!")
            questions.remove(question)
        else:
            print("Incorrect, the correct answer is " + question_and_answers[question])

    print("\nAll questions answered")

def runJSON(filename: str, name: str):
    """
    Run the quiz with the given name inside the file with given name
    """

    with open(filename + ".json") as f:
        data = load(f)

    assert isinstance(data, dict), "The outermost layer of JSON must be an object"
    assert name in data, "The given name does not exist"
    obj = data[name]
    assert "questions" in obj, "Must contain a questions field"
    assert "instructions" in obj, "Must contain an instructions field"

    main(obj["instructions"], obj["questions"])

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
