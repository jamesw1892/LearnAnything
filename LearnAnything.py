from CommandLineTools import menu, menuLoopSingle, readyUp
from json import load
import os
from random import choice
from sys import argv
from typing import Dict, List, Union

def getJson(filename: str):
    """
    Return the object contained in the JSON file if it exists and is valid.
    Otherwise quit
    """

    try:
        with open(os.path.join(os.path.dirname(__file__), f"{filename}.json")) as f:
            return load(f)
    except FileNotFoundError:
        print("JSON file not found")
        exit(1)

def printResultAndProgress(result: str, num_got: int, total_num: int):
    print(f"{result}, got {num_got}/{total_num} = {round(num_got / total_num * 100)}% ({total_num - num_got} left)")

def q_and_a(instructions: Union[str, None], prefix: str, suffix: str, question_and_answers: Dict[str, str]):
    """
    Print the instructions to standard output and repeatedly ask the user for
    the answers to the questions until they have correctly answered them all once
    """

    if instructions is None:
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

        printResultAndProgress(out, num_got, len(question_and_answers))

    print("\nAll questions answered")

def get_all(instructions: Union[str, None], prompt: str, things_to_get: List[str]):
    """
    Print the instructions to standard output and repeatedly ask the user for
    a thing until they have correctly inputted them all
    """

    if instructions is None:
        print("Get everything:")
    else:
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

        printResultAndProgress(out, num_got, len(things_to_get))

    print("\nAll correct")

def all_permutations(instructions: str, question_prompt: str, answer_prompt: str,
                     question_prefix: str, question_suffix: str, answer_prefix: str,
                     answer_suffix: str, question_and_answers: Dict[str, str]):

    if instructions == "":
        print("Get all of each and then match them up from both sides")
    else:
        print(instructions)

    answer_and_questions = dict()
    for question, answer in question_and_answers.items():
        answer_and_questions[answer] = question

    get_all("", question_prompt, list(question_and_answers.keys()))
    get_all("", answer_prompt, list(question_and_answers.values()))
    q_and_a("", question_prefix, question_suffix, question_and_answers)
    q_and_a("", answer_prefix, answer_suffix, answer_and_questions)

    print("\n\nAll permutations of the Q&A answered")

def runJSON(data, name: str):
    """
    Run the quiz with the given name with given data
    """

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

    elif obj["mode"] == "all permutations":
        assert "question prompt" in obj, "Must contain a question prompt field"
        assert "answer prompt" in obj, "Must contain an answer prompt field"
        assert "question prefix" in obj, "Must contain a question prefix field"
        assert "question suffix" in obj, "Must contain a question suffix field"
        assert "answer prefix" in obj, "Must contain an answer prefix field"
        assert "answer suffix" in obj, "Must contain an answer suffix field"
        assert "questions" in obj, "Must contain a questions field"
        all_permutations(obj["instructions"], obj["question prompt"], obj["answer prompt"],
                         obj["question prefix"], obj["question suffix"], obj["answer prefix"],
                         obj["answer suffix"], obj["questions"])

    ### instead of creating a new mode, just treat all q&as like this but ask before each version

def fromInput(filename: str):
    """
    Get input from the user for the name to choose
    """

    data = getJson(filename)

    # if there is only one quiz then run that automatically
    if len(data) == 1:
        for key in data:    # this loop will necessarily only run once
            runJSON(data, key)

    # otherwise ask the user which quiz to run
    else:
        name = menu(list(data.keys()), "Which quiz would you like to play?")
        runJSON(data, name)

def fromCommandLineArgs():
    """
    Parse command line arguments for the file and name
    """

    assert len(argv) > 2, "Must provide JSON file and name of questions"
    runJSON(getJson(argv[1]), argv[2])

if __name__ == "__main__":
    try:
        if len(argv) > 1:
            fromCommandLineArgs()
        else:
            menuLoopSingle(
                [filename[:-5] for filename in os.listdir(os.path.dirname(__file__)) if filename.endswith(".json")],
                fromInput,
                [],
                "Quiz Category:"
            )

    except KeyboardInterrupt:
        print(f"{os.linesep}Keyboard interrupt, exiting")
