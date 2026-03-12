import os
import zipfile
import gradio as gr
import ctranslate2
from transformers import AutoTokenizer

# Extract optimized model
if not os.path.exists("ct2_model"):
    with zipfile.ZipFile("ct2_model.zip", "r") as zip_ref:
        zip_ref.extractall()

# Extract tokenizer
if not os.path.exists("tokenizer_only"):
    with zipfile.ZipFile("tokenizer_only.zip", "r") as zip_ref:
        zip_ref.extractall()

# Load the exact tokenizer used during training/conversion
tokenizer = AutoTokenizer.from_pretrained("tokenizer_only")

# Load optimized CTranslate2 model
translator = ctranslate2.Translator("ct2_model", device="cpu")


def transliterate_one(text, lang):
    if not text or not text.strip():
        return ""

    prompt = f"transliterate to {lang}: {text.strip()}"

    input_ids = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=64
    )["input_ids"][0].tolist()

    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    results = translator.translate_batch(
        [tokens],
        beam_size=4,
        max_decoding_length=20
    )

    output_tokens = results[0].hypotheses[0]
    output_ids = tokenizer.convert_tokens_to_ids(output_tokens)

    if isinstance(output_ids, int):
        output_ids = [output_ids]

    return tokenizer.decode(output_ids, skip_special_tokens=True)


def transliterate_all(text):
    hindi = transliterate_one(text, "hindi")
    bengali = transliterate_one(text, "bengali")
    tamil = transliterate_one(text, "tamil")
    return hindi, bengali, tamil


demo = gr.Interface(
    fn=transliterate_all,
    inputs=gr.Textbox(
        label="Enter Romanized text",
        placeholder="e.g. namaste, bharat"
    ),
    outputs=[
        gr.Textbox(label="Hindi"),
        gr.Textbox(label="Bengali"),
        gr.Textbox(label="Tamil"),
    ],
    title="Multilingual Transliteration Model",
    description="Enter Romanized text and get transliteration in Hindi, Bengali, and Tamil."
)

if __name__ == "__main__":
    demo.launch()