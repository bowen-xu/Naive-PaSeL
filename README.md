# **Naïve-PaSeL: a Naïve Passive Sequence Learning Method**

**Naïve-PaSeL** is a lightweight, proof-of-concept approach for *passive*, *online* sequence learning.
It incrementally scans an event stream and extracts frequently occurring event sequences ("patterns") without supervision.

This implementation is intentionally **naïve** and serves as a conceptual prototype.

---

## 🚀 **Motivation**

Learning sequential patterns is almost the most fundamental capability of intelligent systems.
Naïve-PaSeL explores the simplest possible approach for learning such patterns in a streaming setting:

* Events arrive one by one in **discrete time**
* Patterns are **sequences of event types**, but the event types are non-repeating in a pattern.
* The system passively observes the stream
* Frequent sequences gradually accumulate higher scores
* Infrequent ones fade due to temporal decay and capacity limits

No prediction or inference is performed (yet):
Naïve-PaSeL currently focuses only on **pattern discovery**.
Note that the assumptions are too idealized to be applied in designing a comprehensive sequence learning system.

---

## 🧠 **Concept Overview**

Naïve-PaSeL maintains a hierarchy of "sublayers", each responsible for sequences of a specific length:

```
Length 1 → Sublayer 0
Length 2 → Sublayer 1
Length 3 → Sublayer 2
...
```

Each sublayer functions as a small memory store with limited capacity.
Whenever the system detects that a known sequence has just re-occurred, its score increases.
Whenever a new potential sequence appears (based on observed consecutive events), the system forms a new hypothesis and inserts it into the appropriate sublayer.

### Core ideas

* **Online processing**: one event at a time
* **Passive detection**: no active prediction
* **Recurrence score (`ror`)**: measures frequency
* **Exponential decay**: recent events matter more
* **Capacity constraints**: enforce competition
* **Hypothesis expansion**: longer sequences arise from shorter ones

This creates a simple but emergent mechanism for discovering repeated event structures.

---

## 📦 **Repository Structure**

```
main.py            # Example usage + event stream generation
SeqMind.py         # High-level temporal processing module
SeqMiner.py        # Manages sublayers and sequence storage
SeqSublayer.py     # Fixed-capacity memory for sequences of a given length
Sequence.py        # Data structure for sequences (components + ror)
```

External helper:

* `eventstream_benchmark` is used for generating synthetic patterned event streams.

---

## 🏗️ **How It Works**

### 1. **Event ingestion**

Each new event updates a per-type "receptor" that stores its most recent occurrence time.

### 2. **Decay**

All sequence scores (`ror`, representing *Recent Occurrence Rate*) decay slightly every cycle:

```python
ror *= 0.999
```

This favors frequently repeating patterns over the long term.

### 3. **Pattern detection**

The system checks whether any known sequence has just occurred *consecutively* in the last `L` timesteps.

> Current design&implementation only supports *strictly consecutive* matches
> (no gaps allowed).

### 4. **Hypothesis building**

If a past sequence `S` has just occurred, and the current event is `e`, a new candidate sequence `(S, e)` is created and added (with capacity-based competition) to the next sublayer.

---

## 🔬 **Limitations (Intended for the Prototype)**

This project is for experimentation and proof-of-concept.
Known limitations include:

* Only detects **strictly consecutive** sequences (no gaps)
* Only supports **non-repeating event types within a sequence pattern**
* Memory is simple; eviction is naïve
* No prediction or forecasting
* Sensitive to timestamp collisions (last-occurrence model)

---

## 🧪 **Example**

Running `main.py` generates a synthetic event stream containing hidden patterns and feeds it into Naïve-PaSeL:

```python
mind = SeqMind(n_event_types=26, capacity=26 * 32)

for t, e, is_pattern in stream.stream():
    mind.input_event(e)
    mind.cycle()
```

After processing, top recurring sequences in a specific sublayer can be inspected:

```python
sorted_sequences = sorted(
    mind.miner.sublayers[4].sequences.values(),
    key=lambda s: s.ror,
    reverse=True
)
```

---

## 📄 **License**

MIT License

