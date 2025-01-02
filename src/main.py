import sys
from preprocessing.tokenizer import Tokenizer
from graph.graph_builder import create_graph,close_connection
from src.pos_tagger.pos_tagger import PosTagger
from src.relation_extraction.extractor import RelationExtractor

class FSAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.tokenizer = Tokenizer()
        self.relation_extractor = RelationExtractor()
        self.pos_tagger = PosTagger()
        
    def analyse(self):
        x = self.tokenizer(self.text)
        create_graph(x)
        print("Graph created successfully!")
        from_relation = self.relation_extractor.extract_from_relation(x)
        tagger_res = self.pos_tagger.tag(from_relation)
        close_connection()

     
def main():
    text = sys.argv[1]
    anaylzer = FSAnalyzer(text)
    anaylzer.analyse()
    
    
if __name__ == '__main__':
    main()

