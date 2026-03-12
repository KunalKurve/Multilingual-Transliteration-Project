# Multilingual Transliteration Model

## Objective
This project builds, optimizes, and deploys a multilingual transliteration model for Indic languages using the Aksharantar dataset.

Supported languages:
- Hindi
- Bengali
- Tamil

The goal is to create an end-to-end NLP pipeline including data preprocessing, model training, optimization, benchmarking, and deployment.

## Sample Outputs

Input: Bharat
Hindi: भरत
Bengali: ভারতে
Tamil: பரத்

Input: namaste
Hindi: नमस्ते
Bengali: নমস্তে
Tamil: நமஸ்டே

Input: Krishna
Hindi: क्रिश्
Bengali: ক্রিশ্
Tamil: கிரிஷ்

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

## Data Preprocessing
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

Advantages:

- Byte-level tokenization
- Handles multilingual scripts naturally
- Good for exact string transformations

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
CTranslate2 significantly reduced model size, but in this CPU-based benchmark it did not improve latency and showed a small quality drop in accuracy.

## Deployment
The optimized model was deployed using:
- Gradio
- Hugging Face Spaces

Live demo:
https://huggingface.co/spaces/kunalkurve219/Multilingual-Transliteration-Project

Users can input Romanized text and obtain transliterations in:
- Hindi
- Bengali
- Tamil

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
```

## Challenges Faced
Several challenges were encountered during development:
- Dataset loading inconsistencies when using the Hugging Face datasets loader.
- Early experiments with mT5 showed unstable or poor transliteration performance.
- Tokenizer compatibility issues during deployment.
- CTranslate2 reduced model size significantly but did not improve latency in the current CPU benchmark environment.

## Design Decisions
Key design decisions included:
- Choosing Option B (pretrained seq2seq) instead of EOLE-NLP to reduce setup complexity and focus on the full pipeline.
- Switching from mT5 to ByT5 for better character-level transliteration capability.
- Using prompt-based multilingual training to support multiple languages within one model.
- Applying CTranslate2 INT8 quantization to reduce model size and enable lightweight deployment.

## Future Improvements

Potential improvements include:
- Training on the full Aksharantar dataset
- Increasing training epochs
- Language-specific models or adapters
- Improved decoding strategies
- Benchmarking on different hardware environments

## Author

Kunal Kurve