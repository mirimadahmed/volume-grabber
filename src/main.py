import os
import json
from datetime import datetime
from .binance_utils import get_valid_pairs
from .volume_analyzer import analyze_volumes
from .notifier import send_alert

def handler(event, context):
    """
    AWS Lambda handler function that runs every 15 minutes
    """
    try:
        # Get valid trading pairs
        pairs = get_valid_pairs()
        
        # Analyze volumes for each pair
        alerts, stats = analyze_volumes(pairs)
        
        # Send notification (always, regardless of alerts)
        send_alert(alerts, stats)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Volume analysis completed successfully',
                'timestamp': datetime.utcnow().isoformat(),
                'alerts': alerts,
                'stats': stats
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
        } 