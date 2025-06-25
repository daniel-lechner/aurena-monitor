# Aurena Auction Monitor

A Python script that monitors aurena.at auctions to find items with specific bid counts ending within a specified timeframe.

## Features

- **Automatic Monitoring**: Scans auctions 1-2 times daily
- **Flexible Filtering**: Filter by bid count (0 bids, ranges, etc.)
- **Time-based Alerts**: Find items ending within X hours
- **Data Export**: Save results as JSON with timestamps
- **Progress Tracking**: Visual progress bars during data fetching

## Quick Start

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file:**

   ```bash
   API_URL=https://webplatform-facade.cluster.prod.aurena.services/api/v1/package/2485524364
   BASE_URL=https://www.aurena.at/posten

   HOURS_BEFORE_END=3

   MIN_BIDS=
   MAX_BIDS=0

   LIMIT_PER_REQUEST=200
   LANGUAGE_CODE=de_DE

   SAVE_RESULTS=true
   ```

3. **Run the montior:**

   ```bash
   python3 main.py
   ```

   Results will be located at `results/`, eg.:

   **Example Output**

   ```txt
    🏆 Aurena Auction Monitor
    🔎 Searching for items with exactly 0 bids ending within 24 hours

    🚀 Starting data fetch with 200 items per request...
    🔍 Fetching data: [████████████████████████████████████████] 100.0% (6,397/6,397)
    ✅ Fetch complete: 6,397 items retrieved

    📊 Results Summary:
      Total items fetched: 6,397
      Items matching filter: 142
      ✅ Found 142 matching items!
      💾 Results saved to: results/auction_results_20250625_143052.json
   ```

   **Result Example**

   ```json
   {
     "timestamp": "2025-06-25T14:30:52.123456",
     "filter_criteria": {
       "hours_before_end": 24,
       "min_bids": 0,
       "max_bids": 0,
       "bid_criteria": "exactly 0 bids",
       "time_criteria": "within 24 hours"
     },
     "total_items": 142,
     "items": [
       {
         "lid": 12345678,
         "aid": 987654,
         "seq": 1,
         "bc": 0,
         "sp": 25.5,
         "hib": {
           "val": null,
           "id": null
         },
         "et": 1719331852000,
         "ts": 2,
         "ld": {
           "ti": {
             "de_DE": "Vintage Kamera Set"
           },
           "de": {
             "de_DE": "<p>Beschreibung der Artikel...</p>"
           }
         },
         "im": [
           "https://images.aurena.at/image1.jpg",
           "https://images.aurena.at/image2.jpg"
         ],
         "cat": 1001,
         "brd": 2002,
         "end_time_formatted": "2025-06-25 16:30:52",
         "hours_remaining": 2.5
       }
     ]
   }
   ```

   **Key fields explanation:**

   - Item Identification:
     - `lid` - Listing ID (for URL construction)
     - `aid` - Auction ID
     - `seq` - Position in auction
   - **Bidding Info:**
     - `bc` - Bid count
     - `sp` - Starting price (Rufpreis)
     - `hib.val` - Highest bid value (null if no bids)
     - `hib.id` - Highest bid ID
   - **Timing:**
     - `et` - End timestamp (milliseconds)
     - `end_time_formatted` - Human-readable end time (added by filter)
     - `hours_remaining` - Hours until auction ends (added by filter)
   - **Item Details:**
     - `ld.ti.de_DE` - German title
     - `ld.de.de_DE` - German description (HTML)
     - `im[]` - Array of image URLs
     - `cat` - Category ID
     - `brd` - Brand ID

## Configuration

Set environment variables or modify defaults:

- `MIN_BIDS` / `MAX_BIDS`: Filter by bid count range
- `HOURS_BEFORE_END`: Items ending within X hours
- `LIMIT_PER_REQUEST`: API pagination size (default: 200)
- `SAVE_RESULTS`: Save to JSON files (default: true)

## Requirements

- Python 3.7+
- requests - HTTP requests
- python-dotenv - Environment variable management
