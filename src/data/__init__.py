from typing import Dict

from data.models import NodeType, RelationType


class Data:
    def __init__(self):
        self.relations = Dict[int, RelationType]
        self.nodes = Dict[int, NodeType]
    
    async def load(self):
        await self.load_relations()
        await self.load_nodes()
    
    def load_relations(self):
        self.relations = ...
    
    def load_nodes(self):
        self.nodes = ...