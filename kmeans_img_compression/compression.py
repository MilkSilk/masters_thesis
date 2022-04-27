from PIL import Image
from sklearn.cluster import KMeans
from dahuffman import HuffmanCodec

codec = HuffmanCodec.from_frequencies({'e': 100, 'n':20, 'x':1, 'i': 40, 'q':3})
encoded = codec.encode('exeneeeexniqneieini')
encoded
# b'\x86|%\x13i@'
len(encoded)
# 6
codec.decode(encoded)
# 'exeneeeexniqneieini'
codec.print_code_table()
# bits  code       (value)  symbol
#    5  00000      (    0)  _EOF
#    1  1          (    1)  'e'
#    2  01         (    1)  'i'
#    3  001        (    1)  'n'
#    4  0001       (    1)  'q'
#    5  00001      (    1)  'x'

codec = HuffmanCodec.from_data('hello world how are you doing today foo bar lorem ipsum')
codec.encode('do lo er ad od')
# b'^O\x1a\xc4S\xab\x80'
len(_)
# 7

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

def save_compressed_im(raw_im_data, n_colors):
    with open(f"kmeans_img_compression/images/{n_colors}_doggo_raw.txt", mode="w") as doggo_im_raw:
        doggo_im_raw.write(str(raw_im_data[0])+"\n")
        
        doggo_im_raw.writelines('\t'.join(str(j) for j in i) + '\n' for i in raw_im_data[1:])


color_nums = [2, 5, 10, 20, 50, 100]

for color_num in color_nums:
    new_image, raw_image = compress_image(im_source, color_num)
    save_compressed_im(raw_image, color_num)

    new_image.save(f"kmeans_img_compression/images/{color_num}_doggo.jpg")