# done with refernce to https://colab.research.google.com/github/sanchit-gandhi/notebooks/blob/main/fine_tune_whisper.ipynb
from datasets import load_dataset, DatasetDict, Audio
from huggingface_hub import login
from huggingface_api import huggingface_api_write_key
import torch

# Centralized directory name for fine-tuned model artifacts
FINETUNED_DIR = "./models/whisper-small-finetuned"  # unified path

dataset = DatasetDict()
login(token=huggingface_api_write_key)

# load dataset from huggingface
# login(token=huggingface_api_write_key)
# dataset["train"] = load_dataset("MPH1155/IERG4320", token=huggingface_api_write_key)
# dataset["validation"] = load_dataset("MPH1155/IERG4320", token=huggingface_api_write_key)

# load my own local dataset
# dataset = load_dataset('csv', data_files='data/dataset.csv')

# dataset = dataset.cast_column("audio", Audio())

# print(dataset)

# load dataset from slt-lyrics-audio dataset (https://huggingface.co/datasets/gmenon/slt-lyrics-audio)
# it have audio and transcription columns
dataset = load_dataset("gmenon/slt-lyrics-audio")

# Split into 80% train and 20% testing for around 9.6k row of data
train_valid = dataset["train"].train_test_split(test_size=0.2, seed=4320)
train_dataset = train_valid["train"]
test_dataset = train_valid["test"]
# 500 row of data for evaluation
eval_dataset = dataset["eval"]

final_dataset = DatasetDict({
    "train": train_dataset,
    "test": test_dataset,
    "validation": eval_dataset
})

print(final_dataset)

from transformers import WhisperFeatureExtractor
from transformers import WhisperTokenizer
from transformers import WhisperProcessor
from transformers import WhisperForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer

feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-small")
tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small", language="English", task="transcribe")
processor = WhisperProcessor.from_pretrained("openai/whisper-small", language="English", task="transcribe")

print(final_dataset["train"][0])

final_dataset = final_dataset.cast_column("audio", Audio(sampling_rate=16000))


def prepare_dataset(batch):
    # load and resample audio data from 48 to 16kHz
    audio = batch["audio"]

    # compute log-Mel input features from input audio array
    batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]

    # encode target text to label ids
    batch["labels"] = tokenizer(batch["transcription"]).input_ids
    return batch


processed_dataset = final_dataset.map(prepare_dataset, remove_columns=["audio", "transcription"])

processed_dataset.set_format(type="torch", columns=["input_features", "labels"])

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model.generation_config.language = "English"
model.generation_config.task = "transcribe"

model.generation_config.forced_decoder_ids = None

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

######################################################################################################################
######################################################################################################################
import torch
from dataclasses import dataclass
from typing import Any, Dict, List, Union

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # Split inputs and labels since they have different lengths and need different padding methods

        # a) Process and pad input audio features
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

        # b) Process and pad label sequences (lyrics)
        label_features = [{"input_ids": feature["labels"]} for feature in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

        # c) Replace padding token ids with -100 to ignore them in loss computation
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        # d) Remove the beginning-of-sequence (BOS) token if present
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]

        # e) Add the processed labels to the batch
        batch["labels"] = labels

        return batch

data_collator = DataCollatorSpeechSeq2SeqWithPadding(
    processor=processor,
    decoder_start_token_id=model.config.decoder_start_token_id,
)
######################################################################################################################
######################################################################################################################

#Evaluation Metrics
import evaluate

metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids

    # replace -100 with the pad_token_id
    label_ids[label_ids == -100] = tokenizer.pad_token_id

    # we do not want to group tokens when computing the metrics
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}

training_args = Seq2SeqTrainingArguments(
    output_dir=FINETUNED_DIR,  # unified output directory
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,  # increase by 2x for every 2x decrease in batch size
    num_train_epochs=3, 
    learning_rate=5e-5,
    warmup_steps=500,
    # max_steps=4000,
    gradient_checkpointing=True,
    fp16=True,
    evaluation_strategy="steps",
    per_device_eval_batch_size=8,
    predict_with_generate=True,
    generation_max_length=225,
    save_steps=100,
    eval_steps=100,
    logging_dir="./logs",
    logging_steps=25,
    report_to=["tensorboard"],
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    push_to_hub=True,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=processed_dataset["train"],
    eval_dataset=processed_dataset["test"],
    tokenizer=processor.feature_extractor,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.push_to_hub("MPH1155/IERG4320")
# Use the unified directory constant for saving final artifacts
trainer.save_model(FINETUNED_DIR)
processor.save_pretrained(FINETUNED_DIR)


val_metrics = trainer.evaluate(eval_dataset=processed_dataset["validation"])
print("Validation metrics:", val_metrics)