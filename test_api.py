import requests
import json

def test_api_call():
    api_url = "https://webplatform-facade.cluster.prod.aurena.services/api/v1/package/2485524364"
    
    payload = {
        "offset": 0,
        "limit": 96,
        "languageCode": "de_DE"
    }
    
    print("Testing API call...")
    print(f"URL: {api_url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(api_url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if 'data' in data:
                print(f"Data keys: {list(data['data'].keys())}")
                items = data.get('data', {}).get('items', [])
                print(f"Items found: {len(items)}")
                
                if items:
                    print(f"First item keys: {list(items[0].keys())}")
                    print(f"First item sample: {json.dumps(items[0], indent=2)[:500]}...")
            else:
                print(f"Full response: {json.dumps(data, indent=2)[:1000]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    test_api_call()