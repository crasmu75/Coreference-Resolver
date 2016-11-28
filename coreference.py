from __future__ import division
import Document
import references
import string
import sys
import re

# future hopes and dreams:
# Looking for proper nouns (nouns capitalized not at beginning of sentence)
# Plural pronouns without s at the end


def remove_punctuation(s):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)


def find_acronyms(phrase):
    phrase = phrase.lower()

    omit = ['by', 'of', 'and']

    rules = [
        lambda p: ''.join([w[0] for w in p.split() if w not in omit]),
        lambda p: ''.join([w[0] for w in p.split()])
    ]

    return set([f(phrase) for f in rules])


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
        word = word.replace('\'s', '').replace('ly', '').replace('ish', '').replace('grand', '').replace('.', '')

        if word in references.masculine_words:
            return 'masculine'
            
        if word in references.feminine_words:
            return 'feminine'

        return 'genderless'


def guess_plurality(phrase):
    # naive approach to singularity
    return 'plural' if phrase.endswith('s') else 'singular'


def get_phrase_attributes(phrase):
    gender = guess_gender(phrase)
    attribute = guess_plurality(phrase)

    return [attribute, gender]


# phrase 1 is a pronoun, phrase 2 will not be a pronoun (since we have already checked
# for exact string matching for pronouns)
def pronoun_attribute_match(phrase1, phrase2):
    phrase1_attrs = references.pronouns[phrase1]

    if phrase1_attrs[1] != "genderless":
        phrase2_attrs = get_phrase_attributes(phrase2.lower())
        if phrase2_attrs[1] == phrase1_attrs[1]:
            return True

    return False


def find_coreferences(input_file, output_dir):
    doc = Document.Document(input_file, output_dir)
    tags = doc.tags

    for anaphor_idx in range(len(tags)):

        # Finding string matches
        if tags[anaphor_idx].content.lower() not in references.pronouns:
            for antecedent_idx in range(anaphor_idx -1, -1, -1):
                if (head_word_match(tags[anaphor_idx].content, tags[antecedent_idx].content) or
                    overlap_similarity(tags[anaphor_idx].content, tags[antecedent_idx].content) >= .5 or
                    tags[anaphor_idx].content.lower() in find_acronyms(tags[antecedent_idx].content) or
                    tags[antecedent_idx].content.lower() in find_acronyms(tags[anaphor_idx].content)):
                    tags[anaphor_idx].ref = tags[antecedent_idx].id

                    if not tags[antecedent_idx].ref:
                        tags[antecedent_idx].ref = tags[anaphor_idx].id

                    break

        # Look for pronouns
        else:
            for antecedent_idx in range(anaphor_idx - 1, max(-1, anaphor_idx - 10), -1):
                if tags[anaphor_idx].content.lower() == tags[antecedent_idx].content.lower():
                    tags[anaphor_idx].ref = tags[antecedent_idx].id
                    if not tags[antecedent_idx].ref:
                        tags[antecedent_idx].ref = tags[anaphor_idx].id
                elif pronoun_attribute_match(tags[anaphor_idx].content.lower(), tags[antecedent_idx].content.lower()):
                    tags[anaphor_idx].ref = tags[antecedent_idx].id
                    if not tags[antecedent_idx].ref:
                        tags[antecedent_idx].ref = tags[anaphor_idx].id

    unmatched_tags = [t for t in doc.tags if not t.ref]
    counter = 0
    for tag in unmatched_tags:
        TAG_RE = re.compile('(?:^|[\s])(' + re.escape(tag.content.lower().split()[-1]) + ')(?:$|[\.\s\,\!\?])')

        matches = re.findall(TAG_RE, doc.content)

        if matches:
            for match in matches:
                new_id = 'A' + str(counter)
                doc.tags.append(Document.Tag(new_id, tag.id, match))
                tag.ref = new_id
                counter += 1

    doc.save()


def main():
    # Reads the input files and 'finds coreferences' in them.
    files = [f.strip() for f in open(sys.argv[1]).readlines()]
    outputDir = sys.argv[2]

    for f in files:
        find_coreferences(f, outputDir)


if __name__ == '__main__':
    main()
