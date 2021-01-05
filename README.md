# Learn Anything

Simple command-line tool that can be used to learn anything by repeatedly answering questions until every question has been answered correctly.

# How it Works

It is not case-sensitive, but the answers do have to be otherwise spelt correctly.

There are two modes that quizes can take:

## Q&A

Questions are chosen randomly from those that have not yet been answered correctly. The correct answer is shown if an incorrect answer is given.

## Get All

The user must repeatedly input a 'thing' until they have all been entered. The progress is shown at each step.

# Usage

## Users

### Learning

Run `python LearnAnything.py` to be asked for the filename and quiz name to run, or provide them as command line inputs, for example: `python LearnAnything.py Examples "Phonetic Alphabet"`. The filename should not include the `.json` extension since it must be a JSON file.

### Creating Questions

Run `python MakeQuestions.py` to be asked for the filename, quiz name, instructions, mode and anything else the quiz requires.

## Programs

### Learning

#### With JSON file

Call the `runJSON` function of `LearnAnything.py` to run the quiz in the JSON file. The first argument is the filename without `.json` extension and the second argument is the quiz name which is case sensitive.

#### Without JSON File

##### Q&A Mode

Call the `q_and_a` function of `LearnAnything.py` with first argument the instructions as a string, second argument the string prefix, third argument the string suffix, and fourth argument a dictionary with string keys and values where each key, value pair is a question and answer.

##### Get All Mode

Call the `get_all` function of `LearnAnything.py` with the first argument the instructions as a string, second argument the prompt before they input each thing as a string and third argument a list of strings representing the things.

### Creating Questions

#### Q&A Mode

Call the `q_and_a` function of `MakeQuestions.py` with arguments:

- filename (str): The filename without .json extension
- name (str): The quiz name within the file, this is case sensitive
- instructions (str): The instructions to show the user before the questions
- prefix (str): Prefix to question to display to the user
- suffix (str): Suffix to question to display to the user
- questions_and_answers (Dict[str, str]): The questions and their corresponding answers

#### Get All Mode

Call the `get_all` function of `MakeQuestions.py` with arguments:

- filename (str): The filename without .json extension
- name (str): The quiz name within the file, this is case sensitive
- instructions (str): The instructions to show the user before the questions
- prompt (str): The prompt to show the user before they enter each thing
- things (List[str]): The things the user needs to enter

# JSON Files

The questions are read from a JSON file which has the following structure. The outer structure is an object with a key equal to each quiz name. Each quiz is another object containing a string field `instructions` which is displayed to the user before they start answering the questions, a string field `mode` that determines the quiz's mode and other fields depending on the mode:

## Q&A Mode

Includes the additional string fields prefix and suffix for text to display to the user around the question and the object field `questions` with string fields for each question and answer. Example JSON file:

```json
{
    "q&a 1 name": {
        "instructions": "q&a 1 instructions",
        "mode": "q&a",
        "prefix": "q&a 1 prefix",
        "suffix": "q&a 1 suffix",
        "questions": {
            "q&a 1 question 1": "q&a 1 answer 1",
            "q&a 1 question 2": "q&a 1 answer 2"
        }
    },
    "Logical NOT": {
        "instructions": "In terms of 1s and 0s, what is the logical NOT of the following:",
        "mode": "q&a",
        "prefix": "What is the logical NOT of ",
        "suffix": "? ",
        "questions": {
            "0": "1",
            "1": "0"
        }
    }
}
```

## Get All Mode

Includes the additional string field `prompt` to display to the user before they input each thing and an array field `things` with string entries for each thing to get. Example JSON file:

```json
{
    "get all 1 name": {
        "instructions": "get all 1 instructions",
        "mode": "get all",
        "prompt": "get all 1 prompt",
        "things": [
            "get all 1 thing 1",
            "get all 1 thing 2"
        ]
    },
    "Boolean Values": {
        "instructions": "In terms of numbers, enter all the boolean values",
        "mode": "get all",
        "prompt": "Boolean value: ",
        "things": [
            "0",
            "1"
        ]
    }
}
```