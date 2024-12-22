import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.binance_utils import get_valid_pairs

def test_binance():
    pairs = get_valid_pairs()
    print(f"Found {len(pairs)} valid pairs:")
    for pair in pairs[:10]:  # Show first 10 pairs
        print(f"• {pair}")

if __name__ == "__main__":
    test_binance() 