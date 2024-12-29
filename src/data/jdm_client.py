import functools
from typing import Dict
import requests

from data.models import NodeType, RelationType


class JdmApiClient:
    def __init__(self):
        self.base_url = "https://jdm-api.demo.lirmm.fr"
        self.version = "v0"
        
        # endpoints
        self.relations_types_endpoint = "/relations_types"
        self.nodes_types_endpoint = "/nodes_types"
        self.refinements_endpoint = "/refinements/{node_name}"
        self.get_node_by_name_endpoint = "/node_by_name/{node_name}"
        self.get_node_by_id_endpoint = "/node_by_id/{node_id}"
        self.get_relation_to_endpoint = "/relations/to/{node_name}"
        self.get_relation_from_endpoint = "/relations/from/{node_name}"
        self.get_relation_from_to_endpoint = "/relations/from/{from}/to/{to}"
        
    def url(self, endpoint: str, args = {}):
        return self.base_url + f'/{self.version}' + endpoint.format(**args)
    
    @functools.cache
    def get_relation_types(self) -> Dict[int, RelationType]:
        endpoint = self.url(self.relations_types_endpoint)
        res = requests.get(endpoint)
        if res.status_code != 200:
            return {}
        res = res.json()
        result : Dict[int, RelationType] = {d['id'] : RelationType.from_dict(d) for d in res}
        return result
    
    @functools.cache
    def get_relation_types(self) -> Dict[int, NodeType]:
        endpoint = self.url(self.nodes_types_endpoint)
        res = requests.get(endpoint)
        if res.status_code != 200:
            return {}
        res = res.json()
        result : Dict[int, NodeType] = {d['id'] : NodeType.from_dict(d) for d in res}
        return result
            
            
            
    
    