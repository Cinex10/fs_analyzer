import re
from typing import List, Dict, Any

class Tokenizer:
    def __init__(self):
        self.abbreviations = set(['M.', 'Mme.', 'Mlle.', 'Dr.', 'Prof.', 'etc.'])
        self.contractions = {
            "l'": "le ", 
            "c'": "ce ", 
            "d'": "de ", 
            "j'": "je ", 
            "m'": "me ", 
            "n'": "ne ", 
            "qu'": "que ",
            "s'": "se ", 
            "t'": "te ",
        }

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes French text into a list of tokens.
        """
        text = text.lower()

        for contraction, replacement in self.contractions.items():
            text = text.replace(contraction, replacement)

        tokens = re.findall(r'\b\w+\b', text)
        
        return tokens