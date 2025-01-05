import sys
from preprocessing.tokenizer import Tokenizer
from graph.graph_builder import create_graph,close_connection,create_word_tag_relations
from pos_tagger.pos_tagger import PosTagger
from relation_extraction.extractor import RelationExtractor

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
        create_word_tag_relations(tagger_res)
        close_connection()

     
def main():
    text = sys.argv[1]
    anaylzer = FSAnalyzer(text)
    anaylzer.analyse()
    
    
if __name__ == '__main__':
    main()

