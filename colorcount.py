import argparse
import json
import requests
from image_data import Image_Data, Color

def get_response(path_arg: str, plot: bool = False):
    def check_status_code(url: str, status_code = 200) -> bool:
        if 'http' in url:
            return requests.get(url, stream=True).status_code == status_code
        else:
            return False

    def generate(image_path: str, color_data: Color):
        response = {
            "ok" : False,
            "image_path" : '',
            "total_scanned_color" : 0,
            "unique_color_count" : []
        }

        response["ok"] = check_status_code(image_path)
        response["image_path"] = image_path
        response["total_scanned_color"] = color_data.Total
        response["unique_color_count"] = color_data.Listed_Count

        return response

    def get_images_path():
        with open(path_arg, 'r') as j:
            return json.loads(j.read())["image_path"]

    response = []
    images_path = get_images_path() if path_arg.endswith('.json') else [path_arg]
    for image_path in images_path:
        image = Image_Data(image_path)
        color = Color(image.Color_Hex)
        
        if plot:
            color.plot()

        response.append(generate(image_path, color))

    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help="path to image")
    parser.add_argument('--plot', type=int, default=0, help="plot color data")
    args = parser.parse_args()

    image_path = args.path
    plot_data = args.plot

    response = get_response(image_path, plot_data)
    print(response)

if __name__ == "__main__":
    main()