import os



def list_images(dataset_path: str):
    image_paths_list = []
    dataset_images_dirs = os.listdir(dataset_path)


    for dir in dataset_images_dirs:
        if not dir.startswith("."):
            dir_path = "{0}/{1}".format(dataset_path, dir)

            if os.path.isdir(dir_path):
                images_list = os.listdir(dir_path)

                for file_name in images_list:
                    file_path = dir_path + "/" + file_name

                    if os.path.isfile(file_path):
                        image_paths_list.append(file_path)


    return image_paths_list
