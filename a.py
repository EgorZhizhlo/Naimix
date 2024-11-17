import requests


headers = {'User-Agent': 'Namix project'}
print(requests.get('https://2ed5-79-139-222-136.ngrok-free.app/', headers=headers).json())