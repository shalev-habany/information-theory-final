class HuffmanDecompressor:
    def __init__(self, chunk_size=1024 * 1024):  # 1 MB chunk size
        self.chunk_size = chunk_size
        self.reverse_mapping = {}

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]  # Remove the padding info
        encoded_text = padded_encoded_text[:-extra_padding]  # Remove the padding
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = []

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text.append(self.reverse_mapping[current_code])
                current_code = ""

        return ''.join(decoded_text)

    def bit_string_from_bytes(self, byte_data):
        return ''.join(f'{byte:08b}' for byte in byte_data)

    def decompress_file(self, input_file, output_file, compressor):
        self.reverse_mapping = compressor.reverse_mapping

        with open(input_file, 'rb') as file, open(output_file, 'w') as output:
            while True:
                byte_data = file.read(self.chunk_size)
                if not byte_data:
                    break

                # Convert the chunk of bytes to a bit string
                bit_string = self.bit_string_from_bytes(byte_data)

                # Remove padding and decode
                encoded_text = self.remove_padding(bit_string)
                decoded_text = self.decode_text(encoded_text)

                # Write decoded text to output file
                output.write(decoded_text)

        print(f"Decompressed and written to {output_file}")
