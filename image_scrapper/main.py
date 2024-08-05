import time
import argparse
from get_images import get_images
from save_images import save_images
import http.client


conn = http.client.HTTPSConnection("google.serper.dev")

def batch_save(search: str):
    SEARCH_ENGINES = {"google": 1, "yandex": 1, "yahoo": 1, "bing": 1}

    for engine, page in SEARCH_ENGINES.items():
        page_exists = True
        page = page

        while page_exists:
            if page == 10:
                print("1000 images from {0} saved successfully!✅".format(engine))
                print("Skip engine!➡️")
                page_exists = False
                break

            images = get_images(conn, search, page, engine)

            if len(images) == 0:
                print("Images not found:\n{0} From:\n{1}\nPage number: {2} ❌".format(search, engine, page))
                print("Skip engine!➡️")
                page_exists = False
                break

            print("Images parsed for: {0}\nFrom: {1}\nPage number: {2}✅".format(search, engine, page))

            save_images(search, images)

            page += 1

    print("Images for '{}' saved successfully!✅✅✅✅✅".format(search))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--search", required=True, help="search param to find images")

    args = ap.parse_args()

    batch_save(args.search)



if __name__ == "__main__":
    main()
