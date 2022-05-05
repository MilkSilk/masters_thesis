import os

color_nums = [2, 5, 10, 20, 50, 100]

# color_nums = [2, 5]


print("Basic image in jpg:", os.stat("kmeans_img_compression/images/doggo.jpg").st_size%1000, "KB")

for color_num in color_nums:
    print(f"Raw image {color_num} colors:", os.stat(f"kmeans_img_compression/images/{color_num}_doggo_raw.txt").st_size%1000, "KB")
    print(f"Huffman encoded all with {color_num} colors:", os.stat(f"kmeans_img_compression/images/{color_num}_huffman_naive_doggo_raw.txt").st_size%1000, "KB")
    print(f"Huffman encoded just image data with {color_num} colors:", os.stat(f"kmeans_img_compression/images/{color_num}_huffman_doggo_raw.txt").st_size%1000, "KB")
    print(f"Image with {color_num} colors:", os.stat(f"kmeans_img_compression/images/{color_num}_doggo.jpg").st_size%1000, "KB")
    print()