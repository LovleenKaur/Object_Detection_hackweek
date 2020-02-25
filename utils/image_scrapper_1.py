import os
import pandas as pd
import sys
import time

from selenium import webdriver

DRIVER_PATH = '/usr/local/bin/chromedriver'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
wd.get('https://google.com')

search_query = sys.argv[1]
limit = int(sys.argv[2])


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        for _ in range(1000):
            wd.execute_script("window.scrollTo(0, 1000000);")

    # Search query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    while image_count < max_links_to_fetch:

        scroll_to_end(wd)
        actual_images = wd.find_elements_by_css_selector('img.rg_i')

        for actual_image in actual_images:
            if actual_image.get_attribute('src'):
                image_urls.add(actual_image.get_attribute('src'))

        image_count = len(image_urls)

        if len(image_urls) >= max_links_to_fetch:
            print(f"Found: {len(image_urls)} image links, done!")
            break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(1)
            load_more_button = wd.find_element_by_class_name("mye4qd")
            if load_more_button:

                wd.execute_script("document.querySelector('.mye4qd').click();")

    return image_urls


def scrapper():

    # fetch
    image_urls = list(fetch_image_urls(search_query, limit, wd))

    # create df
    df = pd.DataFrame(image_urls, columns=["image urls"])

    # Create csv

    file_path = os.path.abspath("data/scrapped_urls/")
    file_name = search_query.lower().replace(" ", "_")+'.csv'
    df.to_csv(file_path+'/'+file_name, index=False)


if __name__ == "__main__":
    scrapper()
