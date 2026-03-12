import time
import torch
import ctranslate2
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def benchmark_hf():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained("final_model")
    model = AutoModelForSeq2SeqLM.from_pretrained("final_model").to(device)
    model.eval()

    def hf_transliterate(text, lang):
        prompt = f"transliterate to {lang}: {text}"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=64)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=20, num_beams=4)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    samples = [
        ("ram", "hindi"),
        ("namaste", "hindi"),
        ("krishna", "hindi"),
        ("bharat", "bengali"),
        ("aatchiyaalargalin", "tamil"),
    ] * 10

    start = time.time()
    for text, lang in samples:
        _ = hf_transliterate(text, lang)
    total = time.time() - start
    print("HF total time:", total)
    print("HF avg latency per request:", total / len(samples))

def benchmark_ct2():
    tokenizer = AutoTokenizer.from_pretrained("final_model")
    translator = ctranslate2.Translator("ct2_model", device="cpu")

    def ct2_transliterate(text, lang):
        prompt = f"transliterate to {lang}: {text}"
        input_ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=64)["input_ids"][0]
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        results = translator.translate_batch([tokens], max_decoding_length=20, beam_size=4)
        output_tokens = results[0].hypotheses[0]
        return tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens), skip_special_tokens=True)

    samples = [
        ("ram", "hindi"),
        ("namaste", "hindi"),
        ("krishna", "hindi"),
        ("bharat", "bengali"),
        ("aatchiyaalargalin", "tamil"),
    ] * 10

    start = time.time()
    for text, lang in samples:
        _ = ct2_transliterate(text, lang)
    total = time.time() - start
    print("CT2 total time:", total)
    print("CT2 avg latency per request:", total / len(samples))

if __name__ == "__main__":
    benchmark_hf()
    benchmark_ct2()