from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class NodeType:
    id: int
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from dictionary"""
        fields = ['id', 'name']
        data = {k:data[k] for k in fields}
        return cls(**data)

@dataclass
class RelationType:
    id: int
    name: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from dictionary"""
        fields = ['id', 'name']
        data = {k:data[k] for k in fields}
        return cls(**data)

