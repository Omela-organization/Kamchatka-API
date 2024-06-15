import base64


def save_base64_to_file(base64_string, output_file):
    # Decode the base64 string
    image_data = base64.b64decode(base64_string)

    # Write the binary data to a file
    with open(output_file, "wb") as file:
        file.write(image_data)


def convert_file_to_base64(path_to_file):
    # Write the binary data to a file
    with open(path_to_file, "rb") as file:
        file_data = file.read()

    base64_encoded_data = base64.b64encode(file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    return base64_message
