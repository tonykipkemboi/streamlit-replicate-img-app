import requests

API_URL = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.1"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

def query(payload):
	try:
		response = requests.post(API_URL, headers=headers, json=payload)
		return response.content
	except Exception as e:
		print("error", e)
