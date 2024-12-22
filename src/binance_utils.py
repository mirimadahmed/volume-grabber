import os
import requests
from typing import List

def get_valid_pairs() -> List[str]:
    """
    Fetches and filters valid futures trading pairs from Binance
    Returns only pairs with significant volume
    """
    try:
        response = requests.get('https://fapi.binance.com/fapi/v1/ticker/24hr')
        data = response.json()
        
        # Filter pairs based on minimum volume and price
        MIN_VOLUME_USD = 1000000  # $1M daily volume
        MIN_PRICE = 0.00001  # Minimum price to filter out inactive pairs
        
        valid_pairs = []
        for pair in data:
            if (float(pair['volume']) * float(pair['lastPrice']) >= MIN_VOLUME_USD and
                float(pair['lastPrice']) >= MIN_PRICE):
                valid_pairs.append(pair['symbol'])
                
        return valid_pairs
        
    except Exception as e:
        raise Exception(f"Error fetching Binance pairs: {str(e)}") 