from utils.file_utils import create_mapped_file

class WordsMapper:
    def __init__(self, words_file= 'data/words.txt'):
        self.mapped_file = create_mapped_file(words_file)
    
    def get_word(self, id):
        lookup_id = f'{id};'
        position = self.mapped_file.find(lookup_id.encode("utf-8"))  # Must use bytes for searching
        self.mapped_file.seek(position)
        line = self.mapped_file.readline().decode('utf-8')
        word = line.split(';')[1].strip('"')
        return word
