import requests
import sys
from typing import List, Dict, Any

class AurenaAPIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    def fetch_single_page(self, offset: int = 0, limit: int = 200, language_code: str = "de_DE", 
                         province_codes: List[str] = None) -> Dict[str, Any]:
        payload = {
            "offset": offset,
            "limit": limit,
            "languageCode": language_code,
            "filter": {
                "auctions": [],
                "brands": [],
                "categories": [],
                "provinces": province_codes or []
            },
            "query": ""
        }
        
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def show_progress(self, current: int, total: int):
        percent = (current / total) * 100
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        sys.stdout.write(f'\r🔍 Fetching data: [{bar}] {percent:.1f}% ({current:,}/{total:,})')
        sys.stdout.flush()
    
    def fetch_all_data(self, limit_per_request: int = 200, language_code: str = "de_DE", 
                      province_codes: List[str] = None) -> List[Dict[str, Any]]:
        all_items = []
        offset = 0
        total_items = None
        
        if province_codes:
            print(f"🚀 Starting data fetch with province filter: {', '.join(province_codes)}")
        else:
            print(f"🚀 Starting data fetch (all provinces)")
        print(f"📦 {limit_per_request} items per request...")
        
        while True:
            try:
                data = self.fetch_single_page(offset, limit_per_request, language_code, province_codes)
                items = data.get('items', [])
                
                if total_items is None:
                    total_items = data.get('elementCount', 0)
                
                if not items:
                    break
                    
                all_items.extend(items)
                
                if total_items > 0:
                    self.show_progress(len(all_items), total_items)
                
                if len(items) < limit_per_request:
                    break
                    
                offset += limit_per_request
                
            except requests.exceptions.RequestException as e:
                print(f"\n❌ Error fetching data at offset {offset}: {e}")
                break
        
        print(f"\n✅ Fetch complete: {len(all_items):,} items retrieved")
        return all_items