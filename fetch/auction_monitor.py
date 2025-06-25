import os
import json
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
from .api_client import AurenaAPIClient
from .filter_logic import AuctionFilter

load_dotenv()

class AurenaMonitor:
    def __init__(self):
        self.api_url = os.getenv('API_URL', 'https://webplatform-facade.cluster.prod.aurena.services/api/v1/package/2485524364')
        self.base_url = os.getenv('BASE_URL', 'https://www.aurena.at/posten')
        self.limit_per_request = int(os.getenv('LIMIT_PER_REQUEST', '200'))
        self.language_code = os.getenv('LANGUAGE_CODE', 'de_DE')
        
        self.api_client = AurenaAPIClient(self.api_url)
        self.filter = AuctionFilter(
            min_bids=self._parse_int_env('MIN_BIDS'),
            max_bids=self._parse_int_env('MAX_BIDS'),
            hours_before_end=self._parse_int_env('HOURS_BEFORE_END'),
            locations=self._parse_locations_env('LOCATION'),
            language_code=self.language_code
        )
        
        os.makedirs('results', exist_ok=True)
    
    def _parse_int_env(self, env_var: str) -> Optional[int]:
        value = os.getenv(env_var, '').strip()
        if value == '':
            return None
        try:
            return int(value)
        except ValueError:
            print(f"⚠️  Warning: Invalid value for {env_var}: '{value}'. Ignoring.")
            return None
    
    def _parse_locations_env(self, env_var: str) -> List[str]:
        value = os.getenv(env_var, '').strip()
        if value == '':
            return []
        return [loc.strip().upper() for loc in value.split(',') if loc.strip()]
    
    def save_results(self, items) -> None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"results/auction_results_{timestamp}.json"
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'filter_criteria': {
                'hours_before_end': self.filter.hours_before_end,
                'min_bids': self.filter.min_bids,
                'max_bids': self.filter.max_bids,
                'locations': self.filter.locations,
                'bid_criteria': self.filter.format_bid_criteria(),
                'time_criteria': self.filter.format_time_criteria(),
                'location_criteria': self.filter.format_location_criteria()
            },
            'total_items': len(items),
            'items': items
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
    
    def run(self):
        bid_criteria = self.filter.format_bid_criteria()
        time_criteria = self.filter.format_time_criteria()
        location_criteria = self.filter.format_location_criteria()
        
        print("🏆 Aurena Auction Monitor")
        print(f"🔎 Searching for items with {bid_criteria} ending {time_criteria}")
        if self.filter.locations:
            print(f"📍 Filtering by {location_criteria}")
        print()
        
        province_codes = self.filter.get_province_codes_for_api()
        all_items = self.api_client.fetch_all_data(self.limit_per_request, self.language_code, province_codes)
        
        if not all_items:
            print("❌ No data fetched. Exiting.")
            return
        
        print(f"🔍 Filtering {len(all_items):,} items by bid count and time...")
        filtered_items = self.filter.filter_items(all_items, self.base_url)
        
        print()
        print("📊 Results Summary:")
        print(f"   Total items fetched: {len(all_items):,}")
        print(f"   Items matching filter: {len(filtered_items):,}")
        
        if len(filtered_items) == 0:
            criteria_parts = [f"{bid_criteria} ending {time_criteria}"]
            if self.filter.locations:
                criteria_parts.append(f"in {location_criteria}")
            print(f"   ❌ No items found with {' '.join(criteria_parts)}")
        else:
            print(f"   ✅ Found {len(filtered_items):,} matching items!")
            
            save_results = os.getenv('SAVE_RESULTS', 'true').lower() == 'true'
            if save_results:
                self.save_results(filtered_items)
            else:
                print("   📝 Results not saved (SAVE_RESULTS=false)")
        
        input("\n⏸️  Press Enter to return to main menu...")