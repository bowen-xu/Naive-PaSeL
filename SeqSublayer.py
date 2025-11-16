from Sequence import Sequence


class SeqSublayer:
    def __init__(self, capacity: int = 100):
        self.capacity: int = capacity
        self.sequences: dict[tuple, Sequence] = {}

    def add_sequence(self, sequence: Sequence):
        if sequence.components in self.sequences:
            existing_seq = self.sequences[sequence.components]
            existing_seq.ror += sequence.ror
            return
        if len(self.sequences) < self.capacity:
            self.sequences[sequence.components] = sequence
            return
        
        min_seq = min(self.sequences.values(), key=lambda seq: seq.ror)
        if sequence.ror > min_seq.ror:
            del self.sequences[min_seq.components]
            self.sequences[sequence.components] = sequence

    def decay_ror(self):
        for seq in self.sequences.values():
            seq.ror *= 0.999
        

    def __len__(self):
        return len(self.sequences)
