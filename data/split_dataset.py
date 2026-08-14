import os
import json
import random
from pathlib import Path

def generate_split_manifest(sequence_list, output_path, seed=42):
    """
    Splits video sequences into 70% Train, 15% Val, 15% Test to prevent frame-leakage.
    """
    random.seed(seed)
    
    # Sort for deterministic behavior before shuffling
    sequence_list.sort()
    random.shuffle(sequence_list)
    
    num_seq = len(sequence_list)
    train_end = int(num_seq * 0.70)
    val_end = train_end + int(num_seq * 0.15)
    
    splits = {
        "train": sequence_list[:train_end],
        "val": sequence_list[train_end:val_end],
        "test": sequence_list[val_end:]
    }
    
    # Write the reproducibility manifest
    with open(output_path, "w") as f:
        json.dump(splits, f, indent=4)
        
    print(f"Manifest written to {output_path}")
    print(f"Train: {len(splits['train'])} seqs | Val: {len(splits['val'])} seqs | Test: {len(splits['test'])} seqs")
    return splits

if __name__ == "__main__":
    print("Sequence Splitter Initialized. (Will be executed on Colab once data is downloaded).")
    # execution logic will follow here in the Colab notebook...