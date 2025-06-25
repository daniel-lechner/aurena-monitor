import requests

def test_limits():
    api_url = "https://webplatform-facade.cluster.prod.aurena.services/api/v1/package/2485524364"
    
    for limit in [96, 200, 250, 300, 350, 400, 500, 1000]:
        payload = {
            "offset": 0,
            "limit": limit,
            "languageCode": "de_DE",
            "filter": {
                "auctions": [],
                "brands": [],
                "categories": [],
                "provinces": []
            },
            "query": ""
        }
        
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                element_count = data.get('elementCount', 0)
                print(f"Limit {limit}: Got {len(items)} items (total: {element_count})")
            else:
                print(f"Limit {limit}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"Limit {limit}: Error - {e}")

if __name__ == "__main__":
    test_limits()