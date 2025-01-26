import pdb
import sys
from preprocessing.tokenizer import Tokenizer
from graph.graph_builder import apply_rules, create_graph,close_connection,create_word_tag_relations,compound_words,resolve_anaphora,resolve_determiner_anaphora
from one_to_one_relation_extractor.extractor import OneToOneRelationExtractor
from disambiguation.disambiguator import Disambiguator
from rule_engine.rule_engine import RuleEngine

class FSAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.tokenizer = Tokenizer()
        self.one_to_one_relation_extractor = OneToOneRelationExtractor()
        self.disambiguator = Disambiguator()
        self.rule_engine = RuleEngine()
        
    def analyse(self):
        x = self.tokenizer(self.text)
        create_graph(x)
        print("Graph created successfully!")
        tagger_res, compound_words_res = self.one_to_one_relation_extractor.tag(x)
        compound_words(compound_words_res)
        create_word_tag_relations(tagger_res)
        disambiguator_res = self.disambiguator.disambiguate_all(x)
        create_word_tag_relations(disambiguator_res)
        rules = self.rule_engine.get_rules()
        apply_rules(rules)
        resolve_anaphora()
        close_connection()
        resolve_determiner_anaphora()
       
     
def main():
    text = sys.argv[1]
    anaylzer = FSAnalyzer(text)
    anaylzer.analyse()
    
    
if __name__ == '__main__':
    # use this example "frégate ancien coule"
    main()

