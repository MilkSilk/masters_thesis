import os
import json

im_names = [
    "doggo.jpg",
    "wonderland.png",
    "tapeta.png",
    "tennis.png",
]

color_nums = [2, 5, 10, 20, 50, 100]

# color_nums = [2, 5]

im_sizes = {}

for im_name in im_names:
    im_name, source_im_format = im_name.split(".")
    im_sizes.update({im_name: {}})

    im_sizes[im_name].update({"Basic image": str(os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.{source_im_format}").st_size/1000) + "KB"})
    # print(f"Basic image in {source_im_format}:", os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.{source_im_format}").st_size/1000, "KB")
    if source_im_format == "png":
        im_sizes[im_name].update({"Png saved as jpg": str(os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.jpg").st_size/1000) + "KB"})
        # print(f"Png img saved as jpg size:", os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.jpg").st_size/1000, "KB")
    # print()

    for color_num in color_nums:
        im_sizes[im_name].update({f"Raw {color_num} colors": str(os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}_raw.txt").st_size/1000) + "KB"})
        im_sizes[im_name].update({f"Huffman raw {color_num} colors": str((os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.txt").st_size +
            os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.pickle").st_size)/1000) + "KB"})
        im_sizes[im_name].update({f"Compressed {source_im_format} {color_num} colors": str(os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}.{source_im_format}").st_size/1000) + "KB"})

        # print(f"Raw {im_name} image {color_num} colors:", os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}_raw.txt").st_size/1000, "KB")
        # print(f"Huffman encoded {im_name} image with {color_num} colors:", (os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.txt").st_size +
        #     os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.pickle").st_size)/1000, "KB")
        # print(f"Image {im_name} with {color_num} colors:", os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}.{source_im_format}").st_size/1000, "KB")
        # print()

print(im_sizes)
with open('kmeans_img_compression/im_size.json', 'w') as json_writer:
    json.dump(im_sizes, json_writer)
