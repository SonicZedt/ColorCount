# ColorCount
Count color on a image

## Usage
Execute from terminal:
```
python colorcount.py --path <str> --plot <int>
```
### Arguments:
| Argument | Type | Description |
| :--      | :--  | :--         |
| --path   | str  | path or url to image or to json request file (required) |
| --plot   | int  | plot color data with count equal or more than defined argument. _default: 0_ (opt) |
| --save   | str  | save output to path (opt) |

#### 1st Example:
Count color on local image without plot the data and save output:</br>
this will count color on `image.jpg` and save the output to `image_color_count,json`
```
python colorcount.py --path D:\image.jpg --save D:\image_color_count.json
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

#### 2nd Example:
Count color on online accessible image and plot the data with count equal or more than 1000: </br>
Image source (https://avatars.githubusercontent.com/u/83224221?v=4):</br>
![Image_Source](https://avatars.githubusercontent.com/u/83224221?v=4)
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4 --plot 1000
```
Output:
![Color_Distribution_Plot](https://user-images.githubusercontent.com/83224221/156562301-639a35ef-e7c9-444e-bea1-9453ab0feee5.png)

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
#### 3rd Example:
Count color on multiple local image without plot the data: </br>
to count color on multiple local and/or online accessible image, a json is needed</br>
request.json:
```
{
    "image_path" : [
        "path/to/image.jpg",
        "https://path.to.image.png"
    ]
}
```
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

### Output:
Output is a json.
| Key                 | Type | Description |
| :--                 | :--  | :--         |
| ok                  | bool | Response 200 of given path or url to image, produce false if local path |
| image_path          | str  | Path or url to image |
| total_scanned_color | int  | Total scanned color, sum of image resolution, or how many pixel the image has |
| unique_color_count  | dict | Total unique color. Key is color in hex, value is count how many time that color appear in image. `{"#ffffff": 3}` |