from SeqMind import SeqMind
from eventstream_benchmark import EventStream, generate_patterns
import sty
from tqdm import tqdm

n_event_types = 26
capacity = 26 * 32

""" Generate Event Stream"""
pats = generate_patterns(
    n_patterns=3,
    pattern_length=5,
    n_types=n_event_types,
    gap_dist="uniform",  # 模板间隔的分布
    gap_base=5,  # 无效（仅用于非 uniform）
    gap_low=3,
    gap_high=9,
    seed=137,
)

stream = EventStream(
    patterns=pats,
    n_types=n_event_types,
    total_events=40_000,
    random_ratio=0.7,
    seed=137,
    # 模式间隔抖动：开 & 均匀 ±2
    pattern_jitter="uniform",
    pattern_jitter_amount=2,
    # 随机事件间隔：Poisson(base=6)，再做均匀 ±1 抖动
    rand_interval_dist="poisson",
    rand_interval_base=6,
    rand_interval_low=None,
    rand_interval_high=None,
    rand_jitter="uniform",
    rand_jitter_amount=1,
    # 密度：正弦随时间变化（把间隔除以 r(t)）
    density_mode="sin",
    density_period=8000,
    density_amp=0.6,
    density_base_rate=1.0,
    # 类型漂移（仅影响“随机事件”的类型分配）
    drift_mode="mixed",
    # 可选缓存
    cache_dir="./cache",
    regenerate=False,
)


mind = SeqMind(n_event_types=n_event_types, capacity=capacity)


for i, (t, e, is_pattern) in enumerate(stream.stream()):
    print(f"{sty.fg.yellow}{e}{sty.fg.rs}" if is_pattern else f"{sty.fg.da_grey}{e}{sty.fg.rs}", end=' ')
    mind.input_event(e)
    mind.cycle()
    if i >= 1000:
        break

sorted_sequences = sorted(list(mind.miner.sublayers[4].sequences.values()), key=lambda s: s.ror, reverse=True)

seqs_topn_ = sorted_sequences[:len(pats)]
print()
print(seqs_topn_)
print(pats.types)
print()
seqs_topn_dict = {s.components: s for s in seqs_topn_}
seqs_topn = []
for pat in pats.types:
    pat_str = tuple(pat)
    seq = seqs_topn_dict.get(pat_str, None)
    seqs_topn.append(seq)
for seq in seqs_topn:
    print(seq)
print("done.")