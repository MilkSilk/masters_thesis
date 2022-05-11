import os


# im_name = "doggo" 
im_name = "wonderland"
# im_name = "tapeta"
# im_name = "tennis"

# source_im_format = "jpg"
source_im_format = "png"

color_nums = [2, 5, 10, 20, 50, 100]

# color_nums = [2, 5]


print(f"Basic image in {source_im_format}:", os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.{source_im_format}").st_size/1000, "KB")
if source_im_format == "png":
    print(f"Png img saved as jpg size:", os.stat(f"kmeans_img_compression/images/{im_name}/{im_name}.jpg").st_size/1000, "KB")
print()

for color_num in color_nums:
    print(f"Raw {im_name} image {color_num} colors:", os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}_raw.txt").st_size/1000, "KB")
    print(f"Huffman encoded {im_name} image with {color_num} colors:", (os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.txt").st_size +
          os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_huffman_{im_name}_raw.pickle").st_size)/1000, "KB")
    print(f"Image {im_name} with {color_num} colors:", os.stat(f"kmeans_img_compression/images/{im_name}/{color_num}_{im_name}.{source_im_format}").st_size/1000, "KB")
    print()