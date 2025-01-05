import sys
from preprocessing.tokenizer import Tokenizer
from graph.graph_builder import create_graph,close_connection,create_word_tag_relations
from one_to_one_relation_extractor.extractor import OneToOneRelationExtractor

class FSAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.tokenizer = Tokenizer()
        self.one_to_one_relation_extractor = OneToOneRelationExtractor()
        
    def analyse(self):
        x = self.tokenizer(self.text)
        create_graph(x)
        print("Graph created successfully!")
        tagger_res = self.one_to_one_relation_extractor.tag(x)
        create_word_tag_relations(tagger_res)
        close_connection()

     
def main():
    text = sys.argv[1]
    anaylzer = FSAnalyzer(text)
    anaylzer.analyse()
    
    
if __name__ == '__main__':
    main()

