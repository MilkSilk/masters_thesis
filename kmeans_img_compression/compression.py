from PIL import Image
from sklearn.cluster import KMeans
from dahuffman import HuffmanCodec
from dahuffman.huffmancodec import _EndOfFileSymbol
import json

im_source = "kmeans_img_compression/images/doggo.jpg"

def compress_image(im_source, k):
    im = Image.open(im_source)
    pixels = []
    for col in range(im.width):
        for row in range(im.height):
            pixels.append(im.getpixel((col, row)))
            
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    assigned_centroids = kmeans.predict(pixels)

    centroids = []
    for centroid in kmeans.cluster_centers_:
        centroids.append([int(x) for x in list(centroid)])

    new_image = Image.new("RGB", (im.width, im.height), color=0)
    raw_image = [centroids]
    for col in range(new_image.width):
        raw_image.append([])
        for row in range(new_image.height):
            new_pixel = assigned_centroids[col*new_image.height+row]
            raw_image[col+1].append(new_pixel)
            new_image.putpixel((col, row), tuple(centroids[new_pixel]))
    return new_image, raw_image

def huffman_enocode(im_data):
    codec = HuffmanCodec.from_data(str(im_data))
    encoded_im = codec.encode(str(im_data))
    return encoded_im, codec

def save_compressed_im(raw_im_data, n_colors):
    with open(f"kmeans_img_compression/images/{n_colors}_doggo_raw.txt", mode="w") as doggo_im_raw:
        doggo_im_raw.write(str(raw_im_data[0])+"\n")
        
        doggo_im_raw.writelines('\t'.join(str(j) for j in i) + '\n' for i in raw_im_data[1:])

    with open(f"kmeans_img_compression/images/{n_colors}_huffman_doggo_raw.txt", mode="wb") as doggo_im_raw:
        # Saves both pixel values (centroids) and pixels huffman encoded to a file
        encoded_im, codec = huffman_enocode(raw_im_data)

        codec.save(f"kmeans_img_compression/images/{n_colors}_huffman_doggo_raw.pickle")

        doggo_im_raw.write(encoded_im)

color_nums = [2, 5, 10, 20, 50, 100]

# color_nums = [2, 5]

for color_num in color_nums:
    new_image, raw_image = compress_image(im_source, color_num)
    save_compressed_im(raw_image, color_num)

    new_image.save(f"kmeans_img_compression/images/{color_num}_doggo.jpg")

