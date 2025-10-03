from datasets import load_dataset, Audio, DatasetDict
from huggingface_hub import login
from huggingface_api import huggingface_api_write_key

dataset = load_dataset('csv', data_files='original_data/dataset.csv')

dataset = dataset.cast_column("audio", Audio())

login(token=huggingface_api_write_key)

print(dataset)

# Split into 80% train and 20% validation
train_valid = dataset["train"].train_test_split(test_size=0.2, seed=4320)
train_dataset = train_valid["train"]
validation_dataset = train_valid["test"]

final_dataset = DatasetDict({
    "train": train_dataset,
    "validation": validation_dataset
})

print(final_dataset)
final_dataset.push_to_hub("MPH1155/IERG4320")