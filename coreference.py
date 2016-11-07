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


# looking for over 50% similarity
def overlap_similarity(phrase1, phrase2):
    phrase1 = set(remove_punctuation(phrase1).lower().split())
    phrase2 = set(remove_punctuation(phrase2).lower().split())

    return len(phrase1 & phrase2) / len(phrase1 | phrase2)


def head_word_match(phrase1, phrase2):
    return phrase1.lower().split()[-1] == phrase2.lower().split()[-1]


# intended to take the entire phrase wrapped in the coref tags
# intended for use when phrase is not a pronoun.
def guess_gender(phrase):
    words = phrase.split()

    for word in words:
        word = word.replace('\'s', '').replace('ly', '').replace('ish', '').replace('grand', '')

        if word in references.masculine_words:
            return 'masculine'
            
        if word in references.feminine_words:
            return 'feminine'

    return 'genderless'

def guess_plurality(phrase):
    # naive approach to singularity
    return 'plural' if phrase.endswith('s') else 'singular'


def get_phrase_attributes(phrase):
    if phrase in references.pronouns:
        return set(references.pronouns[phrase])
    else:
        return set([guess_gender(phrase), guess_plurality(phrase)])


def attribute_similarity(phrase1, phrase2):
    phrase1_attrs = get_phrase_attributes(phrase1.lower())
    phrase2_attrs = get_phrase_attributes(phrase2.lower())

    return len(phrase1_attrs & phrase2_attrs) / len(phrase1_attrs | phrase2_attrs)


def find_coreferences(input_file, output_dir):
    doc = Document.Document(input_file, output_dir)
    tags = doc.get_tags()

    for cur in range(len(tags)):
        print('current: {}'.format(tags[cur]))
        possibilities = []

        for check in range(cur - 1, -1, -1):
            print('   {}'.format(tags[check]))

            # Chekcs for either an exact match with the entire string or possible
            # acronymns of the current tag or the tag being checked.
            if (head_word_match(tags[cur][1], tags[check][1]) or
                    overlap_similarity(tags[cur][1], tags[check][1]) >= .75 or
                    tags[check][1] in find_acronyms(tags[cur][1]) or
                    tags[cur][1] in find_acronyms(tags[check][1])):

                doc.add_coref(tags[cur][0], tags[check][0])
                break

            # Find the score for these two tags and just add it to a list of all scores.
            score = attribute_similarity(tags[cur][1], tags[check][1])
            possibilities.append((score, tags[check][0]))

        # Coref the highest scoring tag if it's over a 75% match
        if possibilities and max(possibilities)[0] >= .75:
            doc.add_coref(tags[cur][0], max(possibilities)[1])


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

    print(guess_gender('The adult male\'s body'))
    print(guess_gender('womanly presence'))
    print(guess_gender('broken tree branch'))
    print(guess_gender('The motherly person'))
    print(guess_gender('The boyish toy'))


if __name__ == '__main__':
    main()
