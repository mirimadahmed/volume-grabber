import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.notifier import send_alert
from dotenv import load_dotenv

def test_notification():
    load_dotenv()
    
    # Test data
    test_alerts = [{
        'pair': 'BTCUSDT',
        'median_volume': 100,
        'current_volume': 250,
        'percentage_increase': 150,
        'direction': 'UP',
        'price_change': 2.5,
        'timestamp': '2024-01-01T00:00:00'
    }]
    
    test_stats = {
        'pairs_analyzed': 5,
        'pairs_with_volume': 1,
        'highest_volume_increase': 150,
        'highest_volume_pair': 'BTCUSDT',
        'biggest_price_move': 2.5,
        'biggest_price_move_pair': 'BTCUSDT',
        'start_time': '2024-01-01T00:00:00',
        'end_time': '2024-01-01T00:00:10',
        'api_calls_made': 1
    }
    
    print("Testing notification system...")
    print(f"NTFY_TOPIC: {os.getenv('NTFY_TOPIC')}")
    
    send_alert(test_alerts, test_stats)
    print("Notification test complete!")

if __name__ == "__main__":
    test_notification() 