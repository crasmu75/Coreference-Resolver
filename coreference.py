from __future__ import division
import Document
import references
import string
import sys

# future hopes and dreams:
# Looking for proper nouns (nouns capitalized not at beginning of sentence)
# Plural pronouns without s at the end

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
        word = word.replace('\'s', '').replace('ly', '').replace('ish', '')

        if word in references.masculine_words:
            return gender == 'masculine'
            
        if word in references.feminine_words:
            return gender == 'feminine'

    return gender == 'genderless'


# looking for over 50% similarity
def overlap_similarity(phrase1, phrase2):
    phrase1 = set(remove_punctuation(phrase1).lower().split())
    phrase2 = set(remove_punctuation(phrase2).lower().split())

    return len(phrase1 & phrase2) / len(phrase1 | phrase2)


def find_coreferences(input_file, output_dir):
    doc = Document.Document(input_file, output_dir)

    # Do stuff here
    tags = doc.get_tags()
    # once this works, do some work to get our anaphora into the dictionary declared above???

    for cur in range(len(tags)):
        print 'current: {}'.format(tags[cur])

        for check in range(cur - 1, -1, -1):
            print '   {}'.format(tags[check])

            # Chekcs for either an exact match with the entire string or possible
            # acronymns of the current tag or the tag being checked.
            if (overlap_similarity(tags[cur][1], tags[check][1]) == 1 or
                    tags[check][1] in find_acronyms(tags[cur][1]) or
                    tags[cur][1] in find_acronyms(tags[check][1])):

                doc.add_coref(tags[cur][0], tags[check][0])
                break

            # If we get this far, there is no string match, so start building probabilities 
            # for each of the preceding tags and pick the highest (if over some %)

    print
    print doc.content


def main():
    # Reads the input files and 'finds coreferences' in them.
    # files = [f.strip() for f in open(sys.argv[1]).readlines()]
    # outputDir = sys.argv[2]

    # for file in files:
    #     find_coreferences(file, outputDir)

    # reading in example file from project description
    # find_coreferences('example_input.txt', 'Coreference-Resolver')


    find_coreferences('test_input.txt', 'output')

    
    # print(find_acronyms('John F. Kennedy'))
    # print(find_acronyms('National Aeoronautics and Space Administration'))
    # print(overlap_similarity('John F. Kennedy', 'John Kennedy'))
    # print(overlap_similarity('Ford Motor Co.', 'Ford'))

    # print(gender_match('The adult male\'s body', 'masculine'))
    # print(gender_match('womanly presence', 'feminine'))
    # print(gender_match('broken tree branch', 'genderless'))
    # print(gender_match('The motherly person', 'feminine'))
    # print(gender_match('The boyish toy', 'feminine'))


if __name__ == '__main__':
    main()
