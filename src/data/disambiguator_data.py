
import html

class DisambiguatorData:
    def __init__(self, words_file='data/disambiguator.txt'):
        # Create a dictionary instead of using file mapping
        self.r_raff_sem = {}
        with open(words_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = html.unescape(line).lower()
                parts = line.strip().split(';')
                if len(parts) < 3:
                    continue
                word, ref, weight = parts[0].strip(), parts[1].strip(), float(parts[2].strip())
                if weight <= 0:
                    continue
                self.r_raff_sem[word] = self.r_raff_sem.get(word, []) + [{"ref" : ref, "w" : weight}]
    
    def get_raff(self, word):
        matches = []
        search_key = word.lower()        
        for key in self.r_raff_sem:
            if key.startswith(search_key):
                matches += self.r_raff_sem[key]
        return matches

