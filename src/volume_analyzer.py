import os
import requests
from typing import List, Dict, Tuple
import statistics
from datetime import datetime
import time

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def analyze_volumes(pairs: List[str]) -> Tuple[List[Dict], Dict]:
    """
    Analyzes volume for given pairs using taapi.io
    Returns tuple of (alerts, insights)
    Returns top 3 alerts with highest volume increase
    """
    TAAPI_API_KEY = os.environ['TAAPI_API_KEY']
    VOLUME_THRESHOLD = 1.5  # 150% of median volume
    RATE_LIMIT_DELAY = 3  # 3 seconds between requests to stay under 400/minute
    BASE_URL = "https://api.taapi.io/volume"
    MAX_ALERTS = 3  # Maximum number of alerts to return
    
    all_alerts = []  # Store all potential alerts
    stats = {
        'pairs_analyzed': 0,
        'pairs_with_volume': 0,
        'highest_volume_increase': 0,
        'highest_volume_pair': None,
        'biggest_volume': 0,
        'biggest_volume_pair': None,
        'start_time': datetime.utcnow().isoformat(),
        'api_calls_made': 0
    }
    
    for pair in pairs:
        try:
            # Respect rate limits
            if stats['api_calls_made'] > 0:
                time.sleep(RATE_LIMIT_DELAY)
            
            # Convert pair format from BTCUSDT to BTC/USDT
            base = pair[:-4]  # Remove USDT
            formatted_pair = f"{base}/USDT"
            
            # Get volumes (current and historical)
            params = {
                "secret": TAAPI_API_KEY,
                "exchange": "binancefutures",
                "symbol": formatted_pair,
                "interval": "5m",
                "results": "51"  # Changed from 50 to 51 to maintain 49 historical candles
            }
            
            print(f"\nFetching volumes for {BOLD}{pair}{RESET}...")
            response = requests.get(BASE_URL, params=params)
            stats['api_calls_made'] += 1
            
            if response.status_code != 200:
                print(f"{RED}API Error for {pair}: {response.text}{RESET}")
                continue
                
            volumes = response.json()['value']
            
            # Use the second-to-last value (last closed candle) as current
            current_volume = abs(float(volumes[-2]))
            direction_color = GREEN if float(volumes[-2]) > 0 else RED
            print(f"Current volume for {pair}: {current_volume:,.0f} (Direction: {direction_color}{'DOWN' if float(volumes[-2]) < 0 else 'UP'}{RESET})")
            
            # Historical volumes are all except the last two candles
            historical_volumes = [abs(float(v)) for v in volumes[:-2]]
            
            stats['pairs_analyzed'] += 1
            
            # Calculate median and direction using absolute values
            median_volume = abs(statistics.median(historical_volumes))
            direction = "DOWN" if float(volumes[-2]) < 0 else "UP"
            
            # Calculate threshold value and volume increase using absolute values
            threshold_value = median_volume * VOLUME_THRESHOLD
            volume_increase = abs((current_volume / median_volume - 1) * 100) if median_volume > 0 else 0
            
            print(f"Median volume for {pair}: {median_volume:,.0f}")
            print(f"Threshold ({VOLUME_THRESHOLD}x median) for {pair}: {threshold_value:,.0f}")
            
            # Color the volume increase based on whether it exceeds threshold
            if current_volume > threshold_value:
                print(f"{GREEN}Volume increase: +{volume_increase:,.1f}% (ALERT!){RESET}")
            else:
                print(f"Volume increase: +{volume_increase:,.1f}%")
            
            print("------------------------")
            
            # Track statistics
            if volume_increase > stats['highest_volume_increase']:
                stats['highest_volume_increase'] = volume_increase
                stats['highest_volume_pair'] = pair
            
            # Check if current volume exceeds threshold
            if current_volume > (median_volume * VOLUME_THRESHOLD):
                stats['pairs_with_volume'] += 1
                all_alerts.append({
                    'pair': pair,
                    'median_volume': median_volume,
                    'current_volume': current_volume,
                    'percentage_increase': volume_increase,
                    'direction': direction,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
        except Exception as e:
            print(f"{RED}Error processing {pair}: {str(e)}{RESET}")
            continue
    
    # Sort all alerts by volume increase and take top 3
    alerts = sorted(all_alerts, key=lambda x: x['percentage_increase'], reverse=True)[:MAX_ALERTS]
    
    if len(all_alerts) > MAX_ALERTS:
        print(f"\n{YELLOW}Found {len(all_alerts)} pairs with high volume, selecting top {MAX_ALERTS} for alerts:{RESET}")
        for alert in alerts:
            print(f"{GREEN}• {alert['pair']}: +{alert['percentage_increase']:.1f}%{RESET}")
    
    stats['end_time'] = datetime.utcnow().isoformat()
    return alerts, stats