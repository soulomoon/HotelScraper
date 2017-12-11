import os
import shutil
import re
from names import FOLDER


def save_file(name, text):
    os.makedirs(FOLDER, exist_ok=True)
    file_path = os.path.join(FOLDER, name)
    print("saving: {}".format(file_path))
    with open(file_path, "w+", encoding='utf-8') as textfile:
        textfile.write(text)
    print("file saved:{}".format(file_path))


def delete_all():
    delete_file("")


def action_to_files(pattern, func):
    folder = FOLDER
    p = re.compile("^{}\d+".format(pattern))
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and p.match(the_file):
                func(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
            raise


def delete_file(pattern):
    action_to_files(pattern, os.unlink)


def retrieve_files_path(pattern):
    paths = []
    action_to_files(pattern, paths.append)
    print(paths)
    return paths


if __name__ == "__main__":
    retrieve_files_path("BookingScraper")
