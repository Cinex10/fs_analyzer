class NodeTypesMapper:
    def __init__(self, words_file='data/node_types.txt'):
        # Create a dictionary instead of using file mapping
        self.node_types = {}
        with open(words_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 2:
                    try:
                        node_id = int(parts[0])
                        node_type = parts[1].strip('"')
                        self.node_types[node_id] = node_type
                    except ValueError:
                        continue
    
    def get_word(self, id):
        return self.node_types.get(id)
