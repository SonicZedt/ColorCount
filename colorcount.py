import sys
import json
import requests
import collections
import numpy as np
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
        return dict(collections.Counter(self.color))

    @property
    def Listed_Count(self) -> list[dict]:
        """
        Return total unique color in list of dictionary
        """
        list_colors = []
        colors = dict(collections.Counter(self.color)).items()
        
        # List each dict item
        for key, val in colors:
            item = "{'%(key)s' : %(val)s}" % {'key': key, 'val': val}
            list_colors.append(eval(item))

        return list_colors

    def __init__(self, color: list):
        self.color = color

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
    image_path = sys.argv[1]

    response_status = False
    if 'http' in image_path:
        response_status = requests.get(image_path, stream=True).status_code == 200

    image = Image_Data(image_path)
    color = Color(image.Color_Hex)
    generate_response(color, response_status)

if __name__ == "__main__":
    main()