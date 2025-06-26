from dataclasses import dataclass, asdict
import json

@dataclass
class RuleBelief:
    name: str
    description: str
    last_rationale: str

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, name, data):
        return cls(name=name, **data)

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, name, json_str):
        return cls.from_dict(name, json.loads(json_str))