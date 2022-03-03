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
| --path   | str  | path or url to image (required) |
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
    "total_scanned_color" : 4,
    "unique_color_count" : [
        {"#ffffff" : 2},
        {"#000000" : 1},
        {"#dabeef" : 1}
    ]
}
```

#### 2nd Example:
Count color on online accessible image and plot the data with count equal or more than 1000:

Image source (https://avatars.githubusercontent.com/u/83224221?v=4):

![Image_Source](https://avatars.githubusercontent.com/u/83224221?v=4)
```
python colorcount.py --path https://avatars.githubusercontent.com/u/83224221?v=4 --plot 1000
```
Output:
![Color_Distribution_Plot](https://user-images.githubusercontent.com/83224221/156562301-639a35ef-e7c9-444e-bea1-9453ab0feee5.png)

```
{
    "ok": true,
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
