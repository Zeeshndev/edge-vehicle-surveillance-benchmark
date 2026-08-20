import os
import json
import pytest

def test_split_manifest_exists():
    """Verify that split_manifest.json exists if generated."""
    manifest_path = "dataset/split_manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            data = json.load(f)
        assert "train" in data and "val" in data and "test" in data

def test_zero_split_leakage():
    """Ensure absolute sequence non-overlap across train, val, and test splits."""
    manifest_path = "dataset/split_manifest.json"
    if not os.path.exists(manifest_path):
        pytest.skip("Manifest not generated in CI environment.")

    with open(manifest_path, "r") as f:
        splits = json.load(f)

    train_set = set(splits.get("train", []))
    val_set = set(splits.get("val", []))
    test_set = set(splits.get("test", []))

    assert train_set.isdisjoint(val_set), "Leakage detected between train and val splits!"
    assert train_set.isdisjoint(test_set), "Leakage detected between train and test splits!"
    assert val_set.isdisjoint(test_set), "Leakage detected between val and test splits!"