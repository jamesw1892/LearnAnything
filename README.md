# Learn Anything

Simple command-line tool that can be used to learn anything by repeatedly answering questions until every question has been answered correctly.

# How it Works

Questions are chosen randomly from those that have not yet been answered correctly. The correct answer is shown if an incorrect answer is given. It is not case-sensitive, but the answers do have to be otherwise spelt correctly.

# Usage

## Users

### Learning

Run `python LearnAnything.py` to be asked for the filename and quiz name to run, or provide them as command line inputs, for example: `python LearnAnything.py Examples "Phonetic Alphabet"`. The filename should not include the `.json` extension since it must be a JSON file.

### Creating Questions

Run `python MakeQuestions.py` to be asked for the filename, quiz name and for each question and answer.

## Programs

### Learning

#### With JSON file

Call the `runJSON` function of `LearnAnything.py` to run the quiz in the JSON file. The first argument is the filename without `.json` extension and the second argument is the quiz name which is case sensitive.

#### Without JSON File

Call the `main` function of `LearnAnything.py` with first argument the instructions as a string and second argument a dictionary with string keys and values where each key, value pair is a question and answer.

### Creating Questions

Call the `main` function of `MakeQuestions.py` with arguments:

- filename (str): The filename without .json extension
- name (str): The quiz name within the file, this is case sensitive
- instructions (str): The instructions to show the user before the questions
- questions_and_answers (Dict[str, str]): The questions and their corresponding answers

# JSON Files

The questions are read from a JSON file which has the following structure. The outer structure is an object with a key equal to each quiz name. Each quiz is another object containing a string field `instructions` which is displayed to the user before they start answering the questions, and an object field `questions` with string fields for each question and answer. Example JSON file:

```json
{
    "quiz 1 name": {
        "instructions": "quiz 1 instructions",
        "questions": {
            "quiz 1 question 1": "quiz 1 answer 1",
            "quiz 1 question 2": "quiz 1 answer 2"
        }
    },
    "logical NOT": {
        "instructions": "In terms of 1s and 0s, what is the logical NOT of the following:",
        "questions": {
            "0": "1",
            "1": "0"
        }
    }
}
```