from PIL import Image
from sklearn.cluster import KMeans
from dahuffman import HuffmanCodec

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
            raw_image[col+1].append(assigned_centroids[col*new_image.height+row])
            new_image.putpixel((col, row), tuple(centroids[assigned_centroids[col*new_image.height+row]]))
    return new_image, raw_image

def huffman_enocode(im_data):
    codec = HuffmanCodec.from_data(str(im_data))
    print(str(im_data[:100]))
    codec_table = codec.get_code_table()
    print(codec_table)
    codec.print_code_table()
    encoded_im = codec.encode(str(im_data))
    return encoded_im, codec_table

def save_compressed_im(raw_im_data, n_colors):
    with open(f"kmeans_img_compression/images/{n_colors}_doggo_raw.txt", mode="w") as doggo_im_raw:
        doggo_im_raw.write(str(raw_im_data[0])+"\n")
        
        doggo_im_raw.writelines('\t'.join(str(j) for j in i) + '\n' for i in raw_im_data[1:])
    with open(f"kmeans_img_compression/images/{n_colors}_huffman_naive_doggo_raw.txt", mode="wb") as doggo_im_raw:
        # Saves both pixel values (centroids) and pixels huffman encoded to a file
        encoded_im, codec_table = huffman_enocode(raw_im_data)
        codec_table_bytes = str.encode(codec_table)

        doggo_im_raw.write(codec_table_bytes)
        doggo_im_raw.write(encoded_im)

    with open(f"kmeans_img_compression/images/{n_colors}_huffman_doggo_raw.txt", mode="wb") as doggo_im_raw:
        # Saves both pixel values (centroids) raw and pixels huffman encoded to a file
        doggo_im_raw.write(str.encoderaw_im_data[0])
        encoded_im, codec_table = huffman_enocode(raw_im_data[1:])
        codec_table_bytes = str.encode(codec_table)
        
        doggo_im_raw.write(codec_table_bytes)
        doggo_im_raw.write(encoded_im)


# color_nums = [2, 5, 10, 20, 50, 100]


color_nums = [2, 5]

for color_num in color_nums:
    new_image, raw_image = compress_image(im_source, color_num)
    save_compressed_im(raw_image, color_num)

    new_image.save(f"kmeans_img_compression/images/{color_num}_doggo.jpg")

