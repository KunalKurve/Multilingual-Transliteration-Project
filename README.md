Multilingual Transliteration Model
Objective

This project builds, optimizes, and deploys a multilingual transliteration model for Indic languages using the Aksharantar dataset.

Supported languages:

Hindi

Bengali

Tamil

The goal is to demonstrate the full NLP engineering pipeline including data preprocessing, multilingual model training, model optimization, benchmarking, and deployment.

Dataset

Dataset used: Aksharantar Transliteration Dataset

Source:
https://huggingface.co/datasets/ai4bharat/Aksharantar

The dataset contains transliteration pairs in the form:

English word

Native script word

Example:

ram → राम
namaste → नमस्ते
bharat → भारत
Language Selection

Three Indic languages were selected:

Hindi

Bengali

Tamil

These languages represent different scripts and phonetic structures, making them suitable for evaluating multilingual transliteration performance.

Preprocessing

The following preprocessing steps were performed:

Loaded language-specific JSONL files.

Selected relevant columns:

english word

native word

Converted each sample into a prompt-based format:

transliterate to hindi: ram
transliterate to bengali: ram
transliterate to tamil: ram

Combined the datasets from all three languages into one multilingual dataset.

Performed a 90/10 train-test split.

Model Training
Approach

Option B — Pretrained sequence-to-sequence model

Model used:

google/byt5-small
Why ByT5?

Transliteration is fundamentally a character-level transformation problem.
ByT5 operates at the byte level, making it well suited for handling multilingual scripts and exact string mappings.

Framework

Training was performed using:

Hugging Face Transformers

PyTorch

Training Configuration
Parameter	Value
Epochs	2
Batch size	16
Learning rate	1e-4
Max sequence length	32
Training environment	Cloud notebook with GPU
Evaluation Metrics

The model was evaluated using the following metrics:

Exact Match Accuracy

Character Error Rate (CER)

Word Error Rate (WER)

Transformers Model
Metric	Value
Accuracy	0.090
CER	0.4100
WER	0.910
CTranslate2 Model
Metric	Value
Accuracy	0.075
CER	0.4131
WER	0.925
Model Optimization with CTranslate2

The trained model was optimized using CTranslate2 with INT8 quantization.

Model Size Comparison
Model	Size
Original model	1147.40 MB
CTranslate2 optimized model	287.21 MB
Size Reduction
74.97% reduction

This significantly improves deployability in resource-constrained environments.

Inference Benchmark
Metric	Transformers	CTranslate2
Avg latency/request	0.4201 s	0.9322 s
Speed Gain
-121.88%
Observation

CTranslate2 significantly reduced model size, but in this CPU-based benchmark it did not improve latency and resulted in a small drop in quality.

However, the optimized model enables lightweight deployment for production environments.

Deployment

The optimized model was deployed using:

Gradio

Hugging Face Spaces

Live Demo

https://huggingface.co/spaces/kunalkurve219/Multilingual-Transliteration-Project

Users can enter Romanized text and obtain transliteration results for:

Hindi

Bengali

Tamil

Repository Structure
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
Challenges Faced

Several challenges were encountered during development:

Dataset loading inconsistencies when using the Hugging Face datasets loader.

Early experiments with mT5 showed unstable or poor transliteration performance.

Tokenizer compatibility issues during deployment.

CTranslate2 reduced model size significantly but did not improve latency in the current CPU benchmark environment.

Design Decisions

Key design decisions included:

Choosing Option B (pretrained seq2seq) instead of EOLE-NLP to reduce setup complexity and focus on the full pipeline.

Switching from mT5 to ByT5 for better character-level transliteration capability.

Using prompt-based multilingual training to support multiple languages within one model.

Applying CTranslate2 INT8 quantization to reduce model size and enable lightweight deployment.

Future Improvements

Possible improvements include:

Training on the full Aksharantar dataset

Increasing training epochs

Language-specific models or adapters

Improved decoding strategies

Benchmarking on different hardware environments

Author

Kunal Kurve