import re
import os

class Tag(object):
    """docstring for Tag"""
    def __init__(self, id, ref, content):
        super(Tag, self).__init__()
        self.id = id
        self.ref = ref
        self.content = content
        
    def __str__(self):
        return '<COREF ID="{}" REF="{}">{}</COREF>'.format(self.id, self.ref, self.content)
        
class Document(object):
    """docstring for Document"""
    def __init__(self, input_file, output_dir):
        super(Document, self).__init__()

        filename = os.path.splitext(os.path.basename(input_file))[0]
        self.output_file = os.path.join(output_dir, filename + '.response')
        
        self.content = open(input_file).read()
        self.tags = self.extract_tags()

    def extract_tags(self):
        TAG_RE = r'<COREF ID="([\w\d]+)"(?: REF="([\w\d]+)")?>([^<]+)</COREF>'

        matches = re.findall(TAG_RE, self.content)

        if matches:
            return [Tag(*x) for x in matches]

    # def add_coref(self, anaphor, antecedent):
    #     anaphor.ref = antecedent.id
    #     self.matched_tags.append(anaphor)

    def save(self):
        target = open(self.output_file, 'w')

        output = '<TXT>{}</TXT>'.format(''.join(map(str, self.tags)))

        target.write(output)
        target.close()