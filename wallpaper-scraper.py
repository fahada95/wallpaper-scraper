import os
import requests
from urllib.parse import urlparse


def remove_existing_images():
  wd = os.getcwd()
  file_list = os.listdir(wd)
  items_removed = []
  for item in file_list:
    if item.lower().endswith(('.png', 'jpg', 'jpeg')):
      items_removed.append(item)
      os.remove(os.path.join(wd, item))
  return items_removed



def get_response():
  url = "https://www.reddit.com/r/wallpapers/top.json"
  payload = {}
  headers= {
    'User-Agent': 'wallpaper-scraper'
  }
  response = requests.request("GET", url, headers=headers, data = payload)
  response_json = response.json()
  return response_json


def get_image(image_url):
  image_filename = urlparse(image_url)
  if os.path.basename(image_filename.path).lower().endswith(('.png', '.jpg', '.jpeg')):
    image_res = requests.request("GET", image_url, headers={'User-Agent': 'wallpaper-scraper'}, data = {}, stream=True)
    if image_res.status_code >= 200 and image_res.status_code < 300:
      with open(os.path.basename(image_filename.path), 'wb') as f:
        for chunk in image_res.iter_content(1024):
          f.write(chunk)


def get_image_url_list(response_json):
  post_list = response_json['data']['children']
  image_url_list = []
  for post in post_list:
    image_url_list.append(post['data']['url'])
  return image_url_list


if __name__ == "__main__":
  # TODO Add ability to read json or yaml of links and endpoints to get images from file
  removed_files = remove_existing_images()
  response_json = get_response()
  image_url_list = get_image_url_list(response_json)
  for url in image_url_list:
    get_image(url)
  print("Updated wallpaper repository")

