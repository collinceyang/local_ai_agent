import requests
import json

user_input = input("Please enter your questions to AI agent: ")
# print("You entered:", user_input)

url = "http://localhost:11434/api/chat"
payload = {
    "model": "llama3.2",
    "messages": [
        {"role": "user", "content": user_input}
    ]
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Check for HTTP errors


    raw_response = response.text.strip()
    json_parts = raw_response.split('\n')  # Assuming each line is a separate JSON object
    output=[]
    for part in json_parts:
        try:
            json_data = json.loads(part)
            # print("Parsed JSON:", json_data)
            # print(json_data["message"]["content"])
            output.append(json_data["message"]["content"])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    
    result = ''.join(output)
    print(result)

    

    
except requests.exceptions.RequestException as e:
    print(f"HTTP Request failed: {e}")
except ValueError as e:
    print(f"Error parsing JSON response: {e}")