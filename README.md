# ColorCount
Count color on a image

## Table of Content
1. [Usage](#Usage)
2. [Arguments](#Arguments)
3. [Output](#Output)
4. [Example](#Example)
    - [Count color on local image](#Count-color-on-local-image)
    - [Count color on online accessible image](#Count-color-on-online-accessible-image)
    - [Count color on multiple images](#Count-color-on-multiple-images)
    - [Plot data](#Plot-data)
    - [Post request](#Post-request)

## Usage
Execute from terminal:
```
python colorcount.py --path <str> --hget <str> --plot <int> --save <str> --post <str> --hpost <str>
```
### Arguments:
| Argument | Type | Required | Description |
| :--      | :--  | :--      |:--          |
| --path   | str  | yes | path or url to image or to json request |
| -HG, --hget |str| opt | headers for GET request if require to access given path/url |
| -HP, --hpost|str| opt | headers for POST request if require to access url |
| --plot   | int  | opt | plot color data with count equal or more than defined argument. _default: 1_ |
| --save   | str  | opt | save output to path |
| --post   | str  | opt | send POST request contain json output to url |

### Output:
Output is a json.
| Key                 | Type | Description |
| :--                 | :--  | :--         |
| ok                  | bool | response 200 of given path or url to image, produce false if local path |
| image_path          | str  | path or url to image |
| total_scanned_color | int  | total scanned color, sum of image resolution, or how many pixel the image has |
| unique_color_count  | dict | total unique color. Key is color in hex, value is number of occurrences of color in image . `{"#ffffff": 3}` means there are 3 occurrences of exact white in an image|

### Example:
#### Count color on local image:
This will count color on `image.jpg` which is stored in D: drive
Command:
```
python colorcount.py --path D:\image.jpg
```
Output:
```
{
    "ok": false,
    "image_path": "D:\image.jpg",
    "total_scanned_color" : 4,
    "unique_color_count" : [
        {"#ffffff" : 2},
        {"#000000" : 1},
        {"#dabeef" : 1}
    ]
}
```

#### Count color on online accessible image:
This will count color on online accessible image where url is contains `http`
Command:
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4
```
Output:
```
{
    "ok": true,
    "image_path": "https://avatars.githubusercontent.com/u/83224221?v=4"
    "total_scanned_color" : 211600,
    "unique_color_count" : [
        {"#ffffff": 180063},
        {"#ff8017": 29509},
        {"#ffbf8b": 88},
        {"#fffdfb": 83},
        {"#ff811a": 72}
        ...
    ]
}
```

#### Count color on multiple images
To count color on multiple local and/or online accessible images, a json as a request is needed
request.json:
```
{
    "image_path" : [
        "path/to/image.jpg",
        "https://path.to.image.png"
    ]
}
```
Command:
```
python colorscan.py --path request.json
```
Output:
```
[
    {
        "ok": false,
        "image_path": "path/to/image.jpg"
        "total_scanned_color" : 5,
        "unique_color_count" : [
            {"#ffffff": 2},
            {"#000000": 2}.
            {"babeef": 1}
        ]
    },
    {
        "ok": true,
        "image_path": "https://path.to.image.png"
        "total_scanned_color" : 4,
        "unique_color_count" : [
            {"#ffffff": 3},
            {"#000000": 1}
        ]
    }
]
```

This will get path of images from online private json, to read it require a secret key and it's can be passed in header called `X-Master-Key` as well as other extra information such as `X-Bin-Meta`
Command:
```
python colorcount.py --path https://api.jsonbin.io/b/62235e8d06182767436dca2a --hget 'X-Master-Key: <key>' 'X-Bin-Meta: true'
```

#### Plot data:
**UNDER RECONSTRUCTION**. Currently `color.plot()` returning image in 3D numpy array of plot figure<br/>
This will plot color data of github avatar that has number of occurrences equal or more than 1000
<br/>
Image source (https://avatars.githubusercontent.com/u/83224221?v=4):<br/>
![Image_Source](https://avatars.githubusercontent.com/u/83224221?v=4)<br/>
Command:
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4 --plot 1000
```
Output:
![Color_Distribution_Plot](https://user-images.githubusercontent.com/83224221/156562301-639a35ef-e7c9-444e-bea1-9453ab0feee5.png)

#### Post request:
This will send post request contains json output to https://httpbin.org/post
Command:
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4 --post https://httpbin.org/post
```

Suppose if POST request require headers contains `id` and `key`:
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4 --post https://httpbin.org/post --hpost 'id: 00' 'key: rndmky'
```
