# & 'C:\Program Files\Git\mingw64\bin\curl.exe' -X POST http://127.0.0.1:5000/predict -F file=@C:\Users\yzvor\docker_exc\final_project\cat_1.jpg

import argparse
import requests


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client for recognizing pets')
    parser.add_argument('path_to_file', type=str, help='path to the image you want to recognize')

    args = parser.parse_args()

    files = {
        "file": open(args.path_to_file, "rb")
    }

    res = requests.post(url='http://localhost:5000/predict',
                        files=files)
    print(res.json()["message"])
