import os

color_nums = [2, 5, 10, 20, 50, 100]

print("Basic image in jpg size:", os.stat("kmeans_img_compression/images/doggo.jpg").st_size)

for color_num in color_nums:
    print(f"Raw image size with {color_num} colors size:", os.stat(f"kmeans_img_compression/images/{color_num}_doggo_raw.txt").st_size)
    print(f"Image with {color_num} colors size:", os.stat(f"kmeans_img_compression/images/{color_num}_doggo.jpg").st_size)