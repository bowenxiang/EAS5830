import requests
import json

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    
    # --- Load key from a secure file ---
    try:
        with open('pinata_key.txt', 'r') as f:
            jwt_token = f.read().strip()
    except FileNotFoundError:
        print("Error: 'pinata_key.txt' file not found.")
        print("Please create this file and paste your Pinata JWT into it.")
        return None
    # ---------------
		
    endpoint = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    # Set the headers for authentication
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }
    
    # Send the data in the 'pinataContent' key, as required by the Pinata API
    payload = {
        "pinataContent": data,
        "pinataOptions": {
            "cidVersion": 1  # Use CIDv1
        }
    }

    try:
        # Make the POST request with the JSON payload and headers
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Get the CID from the response
        cid = response.json()['IpfsHash']
        return cid

    except requests.exceptions.RequestException as e:
        print(f"Error pinning to Pinata: {e}")
        return None


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    
    # Use a public gateway as shown in the instructions
    # Use the cloudflare-ipfs.com gateway
    gateway_url = f"https://cloudflare-ipfs.com/ipfs/{cid}"

    try:
        response = requests.get(gateway_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # The instructions state to assume the content is valid JSON
        data = response.json()

        assert isinstance(data, dict), f"get_from_ipfs should return a dict"
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting from IPFS: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Content for CID {cid} is not valid JSON.")
        return None