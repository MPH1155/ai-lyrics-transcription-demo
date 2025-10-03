from transformers import WhisperProcessor, WhisperForConditionalGeneration
import evaluate
from datasets import load_dataset
import torch

base_processor = WhisperProcessor.from_pretrained("openai/whisper-small")
base_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

finetuned_processor = WhisperProcessor.from_pretrained("./models/whisper-small-finetuned")
finetuned_model = WhisperForConditionalGeneration.from_pretrained("./models/whisper-small-finetuned")

# Move models to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
base_model = base_model.to(device)
finetuned_model = finetuned_model.to(device)

metric = evaluate.load("wer")

from datasets import concatenate_datasets

dataset = load_dataset("MPH1155/IERG4320")
train_dataset = dataset["train"]
valid_dataset = dataset["validation"]
eval_dataset = concatenate_datasets([train_dataset, valid_dataset])

def get_transcription(audio, processor, model):
    input_features = processor(audio["array"], sampling_rate=16000, return_tensors="pt").input_features
    input_features = input_features.to(device)
    
    generated_ids = model.generate(input_features=input_features)
    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return transcription

base_predictions = []
finetuned_predictions = []
references = []

# Process eval dataset
for i, item in enumerate(eval_dataset):
    print(f"Processing sample {i+1}/{len(eval_dataset)}")
    
    # Get transcriptions from both models
    base_pred = get_transcription(item["audio"], base_processor, base_model)
    finetuned_pred = get_transcription(item["audio"], finetuned_processor, finetuned_model)
    
    # Store predictions and reference
    base_predictions.append(base_pred)
    finetuned_predictions.append(finetuned_pred)
    references.append(item["lyrics"])

# Calculate WER for both models
base_wer = metric.compute(predictions=base_predictions, references=references)
finetuned_wer = metric.compute(predictions=finetuned_predictions, references=references)

print("\nResults:")
print(f"Base Model WER: {base_wer:.4f}")
print(f"Finetuned Model WER: {finetuned_wer:.4f}")
print(f"WER Improvement: {(base_wer - finetuned_wer):.4f}")