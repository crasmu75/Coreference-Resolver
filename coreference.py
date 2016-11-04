from __future__ import division
import string
import sys
import os


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


def overlap_similarity(phrase1, phrase2):
    phrase1 = set(remove_punctuation(phrase1).lower().split())
    phrase2 = set(remove_punctuation(phrase2).lower().split())

    return len(phrase1 & phrase2)/len(phrase1 | phrase2)


def find_coreferences(inputFile, outputDir):
    contents = open(inputFile).read()
    filename = os.path.basename(inputFile)
    outputFile = os.path.join(outputDir, filename + '.response')

    # Do stuff here
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



    print find_acronyms('John F. Kennedy')
    print find_acronyms('National Aeoronautics and Space Administration')
    print
    print overlap_similarity('John F. Kennedy', 'John Kennedy')
    print overlap_similarity('Ford Motor Co.', 'Ford')

if __name__ == '__main__':
    main()