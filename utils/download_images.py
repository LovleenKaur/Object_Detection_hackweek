import hashlib
import os
import sys
import requests
import pickle
import pandas as pd
import io

from PIL import Image

DRIVER_PATH = '/usr/local/bin/chromedriver'
search_query = sys.argv[1]
limit = int(sys.argv[2])


def persist_image(folder_path: str, url: str):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


if __name__ == "__main__":
    file_name = search_query.lower().replace(" ", "_")
    target_folder = os.path.abspath("data/scrapped_urls")
    final_folder = os.path.abspath("data/train/{}".format(file_name))
    urls = pd.read_csv(target_folder+'/{}.csv'.format(file_name))
    urls = urls['image urls'].to_list()
    for image in urls:
        persist_image(final_folder, image)
