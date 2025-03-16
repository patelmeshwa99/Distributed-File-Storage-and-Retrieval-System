from file_utils import chunk_file

file_path = "/Users/vigneshnatarajan/myData/PyCharm/dfsrs/bgimg.jpg"

with open(file_path, "rb") as file:
    chunks = chunk_file(file)

print(f"File split into {len(chunks)} chunks:")
for chunk in chunks:
    print(chunk)
