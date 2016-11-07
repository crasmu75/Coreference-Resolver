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


# intended to take the entire phrase wrapped in the coref tags
# intended for use when phrase is not a pronoun.
def fetch_phrase_gender(phrase):
    words = phrase.split()

    for word in words:
        word = word.replace('\'s', '').replace('ly', '').replace('ish', '').replace('grand', '')

        if word in references.masculine_words:
            return 'masculine'
            
        if word in references.feminine_words:
            return 'feminine'

    return 'genderless'


# looking for over 50% similarity
def overlap_similarity(phrase1, phrase2):
    phrase1 = set(remove_punctuation(phrase1).lower().split())
    phrase2 = set(remove_punctuation(phrase2).lower().split())

    return len(phrase1 & phrase2) / len(phrase1 | phrase2)


def attribute_similarity(phrase1, phrase2):
    phrase1 = phrase1.lower()
    phrase2 = phrase2.lower()

    if phrase1 in references.pronouns:
        p1plurality = references.pronouns[phrase1][0]
        p1gender = references.pronouns[phrase1][1]
    else:
        # naive approach to singularity
        p1plurality = ('plural' if phrase1.endswith('s') else 'singular')
        p1gender = fetch_phrase_gender(phrase1)

    if phrase2 in references.pronouns:
        p2plurality = references.pronouns[phrase2][0]
        p2gender = references.pronouns[phrase2][1]
    else:
        p2plurality = ('plural' if phrase2.endswith('s') else 'singular')
        p2gender = fetch_phrase_gender(phrase2)

    return ((1 if p1gender == p2gender else 0) +
            (1 if p1plurality == p2plurality else 0)) / 2


def find_coreferences(input_file, output_dir):
    doc = Document.Document(input_file, output_dir)

    tags = doc.get_tags()

    for cur in range(len(tags)):
        print('current: {}'.format(tags[cur]))

        for check in range(cur - 1, -1, -1):
            print('   {}'.format(tags[check]))

            # Chekcs for either an exact match with the entire string or possible
            # acronymns of the current tag or the tag being checked.
            if (overlap_similarity(tags[cur][1], tags[check][1]) == 1 or
                    tags[check][1] in find_acronyms(tags[cur][1]) or
                    tags[cur][1] in find_acronyms(tags[check][1])):

                doc.add_coref(tags[cur][0], tags[check][0])
                break

            # If we get this far, there is no string match, so start building probabilities 
            # for each of the preceding tags and pick the highest (if over some %)

            if attribute_similarity(tags[cur][1], tags[check][1]) == 1:
                doc.add_coref(tags[cur][0], tags[check][0])
                break



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


    find_coreferences('example_files/example_input.txt', 'output')

    
    # print(find_acronyms('John F. Kennedy'))
    # print(find_acronyms('National Aeoronautics and Space Administration'))
    # print(overlap_similarity('John F. Kennedy', 'John Kennedy'))
    # print(overlap_similarity('Ford Motor Co.', 'Ford'))

    print(fetch_phrase_gender('The adult male\'s body'))
    print(fetch_phrase_gender('womanly presence'))
    print(fetch_phrase_gender('broken tree branch'))
    print(fetch_phrase_gender('The motherly person'))
    print(fetch_phrase_gender('The boyish toy'))


if __name__ == '__main__':
    main()
