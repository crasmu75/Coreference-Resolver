import re
import os


class Document(object):
    """docstring for DocumentHandler"""
    def __init__(self, input_file, output_dir):
        super(Document, self).__init__()

        filename = os.path.basename(input_file)
        output_file = os.path.join(output_dir, filename + '.response')

        self.input_file = input_file
        self.output_file = output_file
        self.content = open(input_file).read()
        
    def get_tags(self):
        TAG_RE = r'<COREF ID="([\w\d]+)">([^<]+)</COREF>'

        matches = re.findall(TAG_RE, self.content)

        if matches:
            return matches

    def add_coref(self, tag_id, coref_id):
        tag = '<COREF ID="{}">'.format(tag_id)
        new_tag = '<COREF ID="{}" REF="{}">'.format(tag_id, coref_id)
        self.content = self.content.replace(tag, new_tag)

    def save(self):
        # Writes `newContents` to `outputFile`
        target = open(self.output_file, 'w')
        target.write(self.content)
        target.close()