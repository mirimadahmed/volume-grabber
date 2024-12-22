import os
import requests
from typing import List, Dict
from datetime import datetime, timezone

def send_alert(alerts: List[Dict], stats: Dict) -> None:
    """
    Sends grouped volume alerts via ntfy.sh push notifications
    """
    NTFY_TOPIC = os.environ['NTFY_TOPIC']
    NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
    
    try:
        # Determine overall market sentiment without emojis
        if alerts:
            up_moves = sum(1 for alert in alerts if alert['direction'] == "UP")
            down_moves = len(alerts) - up_moves
            sentiment = "Bullish" if up_moves > down_moves else "Bearish" if down_moves > up_moves else "Neutral"
        else:
            sentiment = "Quiet"
            
        # Create title
        if alerts:
            title = f"Volume Alert: {len(alerts)} pairs with high volume | {sentiment}"
        else:
            title = f"Volume Scan Complete | {sentiment}"
            
        # Create message with insights
        message = f"Market Analysis Report\n\n"
        
        # Add statistics
        message += f"Stats:\n"
        message += f"• Pairs Analyzed: {stats['pairs_analyzed']}\n"
        message += f"• Pairs with High Volume: {stats['pairs_with_volume']}\n"
        message += f"• API Calls Made: {stats['api_calls_made']}\n"
        
        if stats['highest_volume_pair']:
            message += f"\nHighest Volume Spike:\n"
            message += f"• {stats['highest_volume_pair']}: {stats['highest_volume_increase']:.1f}%\n"
            
        if stats['biggest_volume_pair']:
            message += f"\nBiggest Volume:\n"
            message += f"• {stats['biggest_volume_pair']}: {stats['biggest_volume']:,.0f}\n"
        
        # Add individual alerts if any
        if alerts:
            message += f"\nHigh Volume Pairs:\n"
            # Sort alerts by volume increase
            for alert in sorted(alerts, key=lambda x: x['percentage_increase'], reverse=True):
                message += (
                    f"• {alert['pair']} ({alert['direction']})\n"
                    f"  Volume: +{alert['percentage_increase']:.1f}% | Current: {alert['current_volume']:,.0f}\n"
                )
        
        # Add execution time
        start_time = datetime.fromisoformat(stats['start_time'])
        end_time = datetime.fromisoformat(stats['end_time'])
        execution_time = (end_time - start_time).total_seconds()
        message += f"\nExecution Time: {execution_time:.2f}s"
        
        # Send notification
        headers = {
            "Title": title,
            "Priority": "high" if alerts else "default",
            "Tags": "crypto,volume,analysis",
            "Content-Type": "text/plain; charset=utf-8"
        }

        response = requests.post(
            NTFY_URL,
            headers=headers,
            data=message.encode('utf-8'),
        )
        
        if response.status_code != 200:
            print(f"Error sending notification: {response.text}")
            print(f"Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error sending ntfy alert: {str(e)}") 