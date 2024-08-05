import requests
import time
import os


def save_images(search_query: str, images: list[str]):
    for img_url in images:
        try:
            image_response = requests.get(img_url)

        except requests.RequestException:
            print("Images cannot be saved!❌")
            continue


        if image_response.status_code == 200:
            image_bytes = image_response.content

            if not os.path.exists("meals"):
                os.makedirs("meals")

            image_name = str(time.time()).replace(".", "")

            folder_path = "meals/{}".format(search_query)
            image_path = "meals/{0}/{1}.jpg".format(search_query, image_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(image_path, "wb+") as binary_file:
                binary_file.write(image_bytes)

        else:
            print("Images cannot be saved!❌")

        print("Image saved successfully!✅")

    print("Images saved successfully!✅")
