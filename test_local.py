import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.binance_utils import get_valid_pairs
from src.volume_analyzer import analyze_volumes
from src.notifier import send_alert
from dotenv import load_dotenv

TEST_MODE = False  # Set to False to use real API data

def get_test_pairs():
    """Returns a small set of test pairs"""
    return [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "AVAXUSDT"
    ]

def main():
    """
    Local test function to simulate Lambda execution
    """
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        print("🔍 Starting volume analysis...")
        
        # Get valid trading pairs
        print("📊 Fetching valid pairs...")
        if TEST_MODE:
            pairs = get_test_pairs()
            print("Using test pairs")
        else:
            pairs = get_valid_pairs()
        print(f"Found {len(pairs)} valid pairs")
        
        # Analyze volumes for each pair
        print("\n📈 Analyzing volumes...")
        alerts, stats = analyze_volumes(pairs)
        
        # Send notification
        print("\n📱 Sending notification...")
        send_alert(alerts, stats)
        
        print("\n✅ Analysis complete!")
        print(f"• Pairs analyzed: {stats['pairs_analyzed']}")
        print(f"• Pairs with high volume: {stats['pairs_with_volume']}")
        if stats['highest_volume_pair']:
            print(f"• Highest volume increase: {stats['highest_volume_pair']} ({stats['highest_volume_increase']:.1f}%)")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 