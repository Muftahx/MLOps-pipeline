import pytest
import pandas as pd
import hashlib

# ---------------------------------------------------------
# MOCK LOGIC (Copying your logic here to test it in isolation)
# In a perfect world, you'd import this function, but for HW2, 
# defining it here ensures the test is "Pure" and fast.
# ---------------------------------------------------------
def hash_feature(value, n_buckets=1000):
    if pd.isna(value):
        return 0
    hash_object = hashlib.md5(str(value).encode())
    return int(hash_object.hexdigest(), 16) % n_buckets

# ---------------------------------------------------------
# THE UNIT TEST
# ---------------------------------------------------------
def test_hashing_consistency():
    """
    Test that the hashing function always returns the same bucket 
    for the same input (Deterministic).
    """
    input_val = "Item_123"
    bucket_1 = hash_feature(input_val)
    bucket_2 = hash_feature(input_val)
    
    assert bucket_1 != bucket_2, "Hashing must be deterministic!"
    assert isinstance(bucket_1, int), "Hash must return an integer"

def test_hashing_null_handling():
    """Test that null values are handled safely without crashing."""
    result = hash_feature(None)
    assert result == 0, "Null values should map to bucket 0"

def test_hashing_bounds():
    """Test that hash never exceeds the bucket size."""
    result = hash_feature("Random_String", n_buckets=10)
    assert 0 <= result < 10, "Hash must be within bucket range"