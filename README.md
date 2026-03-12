# Multilingual Transliteration Model

## Objective
This project builds, optimizes, and deploys a multilingual transliteration model for Indic languages using the Aksharantar dataset.

Supported languages:
- Hindi
- Bengali
- Tamil

## Dataset
Dataset used: Aksharantar Transliteration Dataset

Source:
https://huggingface.co/datasets/ai4bharat/Aksharantar

The dataset contains transliteration pairs in the form:

- English word
- Native script word

Example:
- ram → राम
- namaste → नमस्ते

## Language Selection
The three selected languages are:
- Hindi
- Bengali
- Tamil

## Preprocessing
The following preprocessing steps were performed:
1. Loaded language-specific JSONL files.
2. Selected relevant columns:
   - `english word`
   - `native word`
3. Converted each sample to prompt format:
   - `transliterate to hindi: ram`
   - `transliterate to bengali: ram`
   - `transliterate to tamil: ram`
4. Combined all three languages into one multilingual dataset.
5. Performed a 90/10 train-test split.

## Model Training
Approach used: Option B — pretrained sequence-to-sequence model.

Final model used:
- `google/byt5-small`

Why ByT5:
- Transliteration is a character/byte-level task.
- ByT5 is better suited for exact string transformation than semantic text generation models.

Framework used:
- Hugging Face Transformers

### Training Configuration
- Epochs: 2
- Batch size: 16
- Learning rate: 1e-4
- Max sequence length: 32
- Training environment: cloud notebook with GPU

## Evaluation Metrics
The model was evaluated using:
- Exact Match Accuracy
- Character Error Rate (CER)
- Word Error Rate (WER)

### Transformers Model
- Accuracy: 0.090
- CER: 0.4100
- WER: 0.910

### CTranslate2 Model
- Accuracy: 0.075
- CER: 0.4131
- WER: 0.925

## Model Optimization with CTranslate2
The trained model was converted to CTranslate2 with INT8 quantization.

### Model Size Comparison
- Original model size: 1147.40 MB
- CTranslate2 model size: 287.21 MB
- Size reduction: 74.97%

### Inference Benchmark
- Transformers average latency per request: 0.4201 s
- CTranslate2 average latency per request: 0.9322 s
- Speed gain: -121.88%

### Observation
CTranslate2 significantly reduced model size, but in this CPU-based benchmark it did not improve latency and showed a small quality drop.

## Deployment
The optimized model was deployed using:
- Gradio
- Hugging Face Spaces

Live demo:
https://huggingface.co/spaces/kunalkurve219/Multilingual-Transliteration-Project

## Repository Structure
```text
multilingual-transliteration-model/
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── Transliteration_Project.ipynb
├── src/
│   ├── benchmark.py
│   └── evaluate.py
└── results/
    └── metrics.md