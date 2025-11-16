from SeqSublayer import SeqSublayer
from Sequence import Sequence

class SeqMiner:
    def __init__(self, capacity: int):
        self.sublayers = [SeqSublayer(capacity) for _ in range(7)]
    
    def add_sequence(self, sequence: Sequence):
        sublayer: SeqSublayer = self.sublayers[len(sequence) - 1]
        sublayer.add_sequence(sequence)

    def decay_ror(self):
        for sublayer in self.sublayers:
            sublayer.decay_ror()
