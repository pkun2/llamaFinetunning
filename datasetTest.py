from datasets import load_dataset

dataset = load_dataset("json", data_files="alphaca_formatted_dataset.jsonl", split="train")

print(dataset[0])