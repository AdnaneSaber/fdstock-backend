import requests
from bs4 import BeautifulSoup
import json


def get_tags(id: str | int) -> str:
    url = f"https://stock.adobe.com/ma/images/worker-service-eazeor-electric/{id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    json_data = soup.find('script', {'id': 'image-detail-json'}).string
    data = json.loads(json_data)
    return data[str(id)]['title']
