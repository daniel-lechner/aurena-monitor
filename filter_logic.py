from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class AuctionFilter:
    def __init__(self, min_bids: Optional[int] = None, max_bids: Optional[int] = None, 
                 hours_before_end: Optional[int] = None, language_code: str = "de_DE"):
        self.min_bids = min_bids
        self.max_bids = max_bids
        self.hours_before_end = hours_before_end
        self.language_code = language_code
    
    def format_bid_criteria(self) -> str:
        if self.min_bids is None and self.max_bids is None:
            return "any number of bids"
        elif self.min_bids is None:
            return f"≤{self.max_bids} bids"
        elif self.max_bids is None:
            return f"≥{self.min_bids} bids"
        elif self.min_bids == self.max_bids:
            return f"exactly {self.min_bids} bids"
        else:
            return f"{self.min_bids}-{self.max_bids} bids"
    
    def format_time_criteria(self) -> str:
        if self.hours_before_end is None:
            return "any time"
        else:
            return f"within {self.hours_before_end} hours"
    
    def passes_bid_filter(self, bid_count: int) -> bool:
        if self.min_bids is not None and bid_count < self.min_bids:
            return False
        if self.max_bids is not None and bid_count > self.max_bids:
            return False
        return True
    
    def passes_time_filter(self, end_timestamp: int) -> tuple[bool, datetime, float]:
        current_time = datetime.now()
        end_time = datetime.fromtimestamp(end_timestamp / 1000)
        
        if self.hours_before_end is None:
            hours_remaining = (end_time - current_time).total_seconds() / 3600
            return True, end_time, hours_remaining
        
        cutoff_time = current_time + timedelta(hours=self.hours_before_end)
        
        if end_time <= cutoff_time and end_time > current_time:
            hours_remaining = (end_time - current_time).total_seconds() / 3600
            return True, end_time, hours_remaining
        
        return False, end_time, 0
    
    def filter_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered_items = []
        
        for item in items:
            bid_count = item.get('bc', 0)
            if not self.passes_bid_filter(bid_count):
                continue
            
            end_timestamp = item.get('et')
            if not end_timestamp:
                continue
            
            passes_time, end_time, hours_remaining = self.passes_time_filter(end_timestamp)
            if not passes_time:
                continue
                
            item['end_time_formatted'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            item['hours_remaining'] = hours_remaining
            filtered_items.append(item)
        
        filtered_items.sort(key=lambda x: x.get('et', 0))
        return filtered_items