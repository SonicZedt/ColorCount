import argparse
import json
import requests
from image_data import Image_Data, Color

def get_request(path):
    """
    Possible type of request path:
    - path to local image
    - path/url to online accessible image
    - path/url to json request
    """

    if 'http' in path:
        request = requests.get(path)

        content_type = request.headers['Content-Type']
        if 'image' in content_type:
            return path
        elif 'json' in content_type:
            return request.json()
    else:
        return path

def get_response(path_arg, plot: bool = False):
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

    def get_images_path() -> list[str]:
        if type(path_arg) == str:
            if not path_arg.endswith('.json'):
                return [path_arg]

            with open(path_arg, 'r') as j:
                return json.loads(j.read())["image_path"]

        elif type(path_arg) == dict:
            return path_arg["image_path"]

    response = []
    images_path = get_images_path()
    for image_path in images_path:
        image = Image_Data(image_path)
        color = Color(image.Color_Hex)
        
        if plot:
            color.plot()

        response.append(generate(image_path, color))

    response = response[0] if len(response) == 1 else response
    response = json.dumps(response, indent=4)

    return response

def send_output(output, args):
    if args.save:
        # Save output to args.save (path)
        with open(args.save, 'w') as file:
            file.write(output)
    
    elif args.post:
        # Send request post to args.post (url)
        response = requests.post(args.post, json=output)
        print(args.post, response)

        return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help="path to image")
    parser.add_argument('--plot', type=int, default=0, help="int, plot color data")
    parser.add_argument('--save', type=str, help="path, save output to path")
    parser.add_argument('--post', type=str, help="send post request to url")
    args = parser.parse_args()

    image_path = get_request(args.path)
    plot_data = args.plot

    response = get_response(image_path, plot_data)
    print(response)

    send_output(response, args)

if __name__ == "__main__":
    main()