# ColorCount
Count color on a image

## Usage
Execute from terminal:
```
python colorcount.py --path <str> --plot <int>
```
### Arguments:
| Argument | Type | description |
| :--      | :--  | :--         |
| --path   | str  | path or url to image or to json request file (required) |
| --plot   | int  | plot color data with count equal or more than defined argument. _default: 0_ (opt) |

#### 1st Example:
Count color on local image without plot the data:
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