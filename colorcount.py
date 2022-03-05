import argparse
import json
import requests
from image_data import Image_Data, Color

def parse_headers(headers) -> dict:
    """
    Return parsed headers to dict
    """
    if type(headers) == dict:
        return headers

    elif type(headers) == list:
        header_parsed = {}
        for header in headers:
            # Convert each headers to "'key' : 'value'"
            header_split = header.split(':')
            key = header_split[0].replace(' ', '')
            value = header_split[1].replace(' ', '')
            header_parsed[key] = value
        
        return header_parsed

def get_request(path, headers):
    """
    Possible type of request path:
    - path to local image
    - path/url to online accessible image
    - path/url to json request
    """
    if 'http' in path:
        request = requests.get(path, headers=parse_headers(headers))
        content_type = request.headers['Content-Type']

        if 'image' in content_type:
            return path
        elif 'json' in content_type:
            return request.json()
        else:
            return Exception("Invalid Content-Type")
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
    try:
        images_path = get_images_path()
    except:
        return Exception("Can not access image_path", path_arg)

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
        response = requests.post(args.post, headers=parse_headers(args.hpost), json=output)
        print(args.post, response)

        return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help="path to image")
    parser.add_argument('-HG', '--hget', nargs='*', help="extra source of information for GET request")
    parser.add_argument('-HP', '--hpost', nargs='*', help="extra source of information for POST request")
    parser.add_argument('--plot', type=int, default=0, help="plot color data with value equal or than int")
    parser.add_argument('--save', type=str, help="save output to path")
    parser.add_argument('--post', type=str, help="send post request to url")
    args = parser.parse_args()

    response = get_response(get_request(args.path, args.hget), args.plot)
    print(response)

    send_output(response, args)

if __name__ == "__main__":
    main()