# Benchmark Results

## Model Size
- Original model size: 1147.40 MB
- CTranslate2 model size: 287.21 MB
- Reduction: 74.97%

## Inference Latency
- Transformers avg latency/request: 0.4201 s
- CTranslate2 avg latency/request: 0.9322 s
- Speed gain: -121.88% (CTranslate2 was slower in this CPU-based benchmark)

## Quality Metrics
### Transformers
- Accuracy: 0.090
- CER: 0.4100
- WER: 0.910

### CTranslate2
- Accuracy: 0.075
- CER: 0.4131
- WER: 0.925

## Observation
CTranslate2 significantly reduced model size, but in this deployment/benchmark setup it did not improve latency and slightly reduced quality.