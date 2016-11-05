# -*- coding: utf-8 -*-
from __future__ import division
import string
import sys
import os
import re

# future hopes and dreams:
# Looking for proper nouns (nouns capitalized not at beginning of sentence)
# Plural pronouns without s at the end

pronouns = {"reflexive": {"singular": ["myself",
                                       "yourself",
                                       "himself",
                                       "herself",
                                       "itself"],
                          "plural": ["ourselves",
                                     "yourselves",
                                     "themselves"]},
            "relative": {"singular": ['that',
                                      'when',
                                      'which',
                                      'whichever',
                                      'whichsoever',
                                      'who',
                                      'whoever',
                                      'whosoever',
                                      'whom',
                                      'whomever',
                                      'whomsoever',
                                      'whose',
                                      'whosesoever',
                                      'whatever',
                                      'whatsoever']},
            "genderless": {"singular": ["i",
                                        "me",
                                        "you",
                                        "my",
                                        "mine",
                                        "your",
                                        "yours",
                                        "it"
                                        "its"
                                        "that"],
                           "plural": ["we",
                                      "us",
                                      "our",
                                      "ours",
                                      "their",
                                      "theirs",
                                      "they",
                                      "them"]}
            }

masculine_words = ["male",
                   "boy",
                   "man",
                   "guy",
                   "brother",
                   "father",
                   "uncle",
                   "paternal",
                   "macho",
                   "masculine"]
feminine_words = ["female",
                  "girl",
                  "woman",
                  "lady",
                  "sister",
                  "mother",
                  "aunt",
                  "maternal",
                  "feminine"]

# dictionary for each tagged anaphor - maps to it's attributes
anaphora = {}


def remove_punctuation(s):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)


def find_acronyms(phrase):
    omit = ['by', 'of', 'and']

    rules = [
        lambda p: ''.join([w[0] for w in p.split() if w not in omit]),
        lambda p: ''.join([w[0] for w in p.split()])
    ]

    return [f(phrase) for f in rules]


# intended to take the entire phrase wrapped in the coref tags and an expected gender
def gender_match(phrase, gender):
    words = phrase.split()
    for word in words:
        word = word.replace("'s", "").replace("ly", "").replace("ish", "")
        if word in masculine_words:
            return gender == "male"
        if word in feminine_words:
            return gender == "female"
    return gender == "genderless"


# looking for over 50% similarity
def overlap_similarity(phrase1, phrase2):
    phrase1 = set(remove_punctuation(phrase1).lower().split())
    phrase2 = set(remove_punctuation(phrase2).lower().split())

    return len(phrase1 & phrase2) / len(phrase1 | phrase2)


def find_coreferences(input_file, output_dir):
    contents = open(input_file).read()
    filename = os.path.basename(input_file)
    outputFile = os.path.join(output_dir, filename + '.response')

    # Do stuff here

    # weird quotes are causing the regular expression issues. ” vs "
    # is currently not matching the beginning tags such as <COREF ID=”1”>
    # also, XML parsers do not work on these files. There are foreign characters or something isn't formatted correctly
    # in her files so regex will have to do.
    # taking out the encoding declaration at the top of the file breaks this
    targets = re.split("(</?COREF( ID=(”|\")[0-9](”|\"))?>)", contents)
    # once this works, do some work to get our anaphora into the dictionary declared above???
    newContents = contents

    # Writes `newContents` to `outputFile`
    # target = open(outputFile, 'w')
    # target.write(newContents)
    # target.close()


def main():
    # Reads the input files and "finds coreferences" in them.
    # files = [f.strip() for f in open(sys.argv[1]).readlines()]
    # outputDir = sys.argv[2]

    # for file in files:
    #     find_coreferences(file, outputDir)

    # reading in example file from project description
    # find_coreferences("example_input.txt", "Coreference-Resolver")

    print(find_acronyms('John F. Kennedy'))
    print(find_acronyms('National Aeoronautics and Space Administration'))
    print()
    print(overlap_similarity('John F. Kennedy', 'John Kennedy'))
    print(overlap_similarity('Ford Motor Co.', 'Ford'))

    print(gender_match("The adult male's body", "male"))
    print(gender_match("womanly presence", "female"))
    print(gender_match("broken tree branch", "genderless"))
    print(gender_match("The motherly person", "female"))
    print(gender_match("The boyish toy", "female"))


if __name__ == '__main__':
    main()
