import argparse
import json
import requests
import collections
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

class Image_Data:
    image = None

    @property
    def Array(self) -> np.ndarray:
        """
        Return image array (R, G, B)
        """
        return self.image

    @property
    def Color_Hex(self) -> list:
        hex = []

        def convert_RGB2HEX(color):
            return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

        image = self.image        
        image_height = len(image)
        for y in range(image_height):
            for x in image[y]:
                hex.append(convert_RGB2HEX(x))

        return hex

    def __init__(self, image_path: str):
        if 'http' in image_path:
            # Online image
            image_req = requests.get(image_path, stream=True)
            if image_req.status_code == 200:
                self.image = np.array(Image.open(BytesIO(image_req.content)))

        else:
            # Local image
            self.image = np.array(Image.open(image_path))

    def show(self):
        Image.fromarray(self.image, 'RGB').show()

class Color:
    color = []

    @property
    def Total(self) -> int:
        return len(self.color)

    @property
    def Count(self) -> dict:
        """
        Return total unique color
        """
        color_count = dict(collections.Counter(self.color))
        
        # Sort dict by highest value
        color_count = {
            key: value for key, value in sorted(color_count.items(), key=lambda x: x[1], reverse=True)
        }

        return color_count

    @property
    def Listed_Count(self) -> list[dict]:
        """
        Return total unique color in list of dictionary
        """
        list_colors = []
        colors = self.Count.items()
        
        # List each dict item
        for key, val in colors:
            item = "{'%(key)s' : %(val)s}" % {'key': key, 'val': val}
            list_colors.append(eval(item))

        return list_colors

    def __init__(self, color: list):
        self.color = color

    def plot(self, min_value = 1):
        """
        Plot color data with value more than min_value
        """
        color_count = self.Count
        color_count = {key : value for key, value in color_count.items() if value >= min_value}
    
        color = list(color_count.keys())
        count = list(color_count.values())
        bar_colors = color

        figure = plt.figure('Color Distribution')
        plt.barh(color, count, color=bar_colors, edgecolor='#aaaaaa')
        plt.title('Color Distribution')
        plt.ylabel('Color')
        plt.xlabel('Count')
        plt.show()

        return figure

def generate_response(color_data: Color, response_status: bool):
    response = {
        "ok" : False,
        "total_scanned_color" : 0,
        "unique_color_count" : []
    }

    response["ok"] = response_status
    response["total_scanned_color"] = color_data.Total
    response["unique_color_count"] = color_data.Listed_Count

    return json.dumps(response) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help="path to image")
    parser.add_argument('--plot', type=int, default=0, help="plot color data")
    args = parser.parse_args()

    image_path = args.path
    plot_data = args.plot
    response_status = False

    if 'http' in image_path:
        response_status = requests.get(image_path, stream=True).status_code == 200

    image = Image_Data(image_path)
    color = Color(image.Color_Hex)

    if plot_data:
        color.plot(plot_data)

    response = generate_response(color, response_status)
    print(response)
    return response

if __name__ == "__main__":
    main()