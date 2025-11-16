from dataclasses import dataclass

@dataclass
class Sequence:
    components: tuple[int, ...]
    ror: float

    def __len__(self):
        return len(self.components)
    
    def __iter__(self):
        return iter((self.components, self.ror))