import sys
from preprocessing.tokenizer import Tokenizer
from graph.graph_builder import create_graph,close_connection

class FSAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.tokenizer = Tokenizer()
        
    def analyse(self):
        x = self.tokenizer(self.text)
        print(x)
        create_graph(x)
        print("Graph created successfully!")
        close_connection()

     
def main():
    text = sys.argv[1]
    anaylzer = FSAnalyzer(text)
    anaylzer.analyse()
    
    
if __name__ == '__main__':
    main()

