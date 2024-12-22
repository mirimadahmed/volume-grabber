import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.volume_analyzer import analyze_volumes
from dotenv import load_dotenv

def test_volume_analyzer():
    load_dotenv()
    
    # Test with a small set of pairs
    test_pairs = [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "AVAXUSDT"
    ]
    
    print("Testing volume analyzer...")
    print(f"Testing with {len(test_pairs)} pairs: {', '.join(test_pairs)}")
    
    try:
        alerts, stats = analyze_volumes(test_pairs)
        
        print("\nAnalysis Results:")
        print(f"• Pairs analyzed: {stats['pairs_analyzed']}")
        print(f"• Pairs with high volume: {stats['pairs_with_volume']}")
        print(f"• API calls made: {stats['api_calls_made']}")
        
        if stats['highest_volume_pair']:
            print(f"\nHighest Volume Increase:")
            print(f"• Pair: {stats['highest_volume_pair']}")
            print(f"• Increase: {stats['highest_volume_increase']:.1f}%")
        
        if stats['biggest_volume_pair']:
            print(f"\nBiggest Volume:")
            print(f"• Pair: {stats['biggest_volume_pair']}")
            print(f"• Volume: {stats['biggest_volume']:,.0f}")
        
        if alerts:
            print("\nAlerts Generated:")
            for alert in alerts:
                print(f"\n• {alert['pair']} ({alert['direction']})")
                print(f"  Current Volume: {alert['current_volume']:,.0f}")
                print(f"  Median Volume: {alert['median_volume']:,.0f}")
                print(f"  Increase: {alert['percentage_increase']:.1f}%")
        else:
            print("\nNo alerts generated")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_volume_analyzer() 