from SeqMiner import SeqMiner
import numpy as np
from Sequence import Sequence


class SeqMind:
    def __init__(self, n_event_types: int, capacity: int):
        self.capacity = capacity
        self.miner = SeqMiner(capacity)
        for i in range(n_event_types):
            self.miner.sublayers[0].sequences[(i, )] = Sequence((i,), 0)

        self.ts: int = 1
        self.current_event: int = -1

        self.receptors = np.zeros(n_event_types, dtype=np.int64) - 1000

    def cycle(self):
        self.miner.decay_ror()
        new_compound_events = self.observe_compound_event()
        if len(new_compound_events) > 0 and self.current_event >= 0:
            self.build_hypotheses(self.current_event, new_compound_events)
        self.ts += 1
        self.current_event = -1

    def input_event(self, event_id: int):
        if event_id < 0 or event_id >= len(self.receptors):
            raise ValueError("Invalid event_id")
        self.receptors[event_id] = self.ts
        self.current_event = event_id

    def observe_compound_event(self):
        new_compound_events = []
        for sublayer in self.miner.sublayers[:-1]:
            seq: Sequence
            for seq in sublayer.sequences.values():
                timestamps = [dt - len(seq) for dt in range(len(seq))]
                occur_time = self.receptors[list(seq.components)] - self.ts
                if np.all(occur_time == timestamps):
                    new_compound_events.append(seq.components)
                    seq.ror += 1
        return new_compound_events

    def build_hypotheses(self, current_event: int, past_events_list: list[tuple[int, ...]]):
        for past_events in past_events_list:
            new_sequence = Sequence(tuple((*past_events, current_event)), 1)
            self.miner.add_sequence(new_sequence)
