import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

keyword = input("enter search keyword: ")
search_item = keyword.replace(" ", "+")
folder_name = f"images_{keyword.replace(' ', '_')}"
os.makedirs(folder_name, exist_ok=True)

search_url = f"http://www.google.com/search?tbm=isch&q={search_item}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = requests.get(search_url, headers=headers)                                        
soup = BeautifulSoup(response.text, "html.parser")
img_tags = soup.find_all("img")

img_urls = []
for img in img_tags:
    if 'src' in img.attrs:
        img_urls.append(img['src'])
    elif 'data-src' in img.attrs:
        img_urls.append(img['data-src'])

for i, img_urls in enumerate(tqdm(img_urls, desc="Downloading Images")):
    try:
        img_data = requests.get(img_urls).content
        with open(f"{folder_name}/{keyword.replace(' ', '_')}_{i}.jpg", "wb") as f:
            f.write(img_data)
    except:
        pass
print(f"Downloaded {len(img_urls)} images into {folder_name}")                         