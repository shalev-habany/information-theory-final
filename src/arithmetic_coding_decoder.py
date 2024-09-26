import struct

class Decompressor:
    def __init__(self, chunk_size=1000):
        self.chunk_size = chunk_size

    def get_symbol_ranges(self, frequencies):
        """
        Given a dictionary of symbol frequencies, return the ranges for each symbol based on probabilities.
        """
        total_count = sum(frequencies.values())
        symbol_ranges = {}
        low = 0.0
        for symbol, count in frequencies.items():
            probability = count / total_count
            high = low + probability
            symbol_ranges[symbol] = (low, high)
            low = high
        return symbol_ranges

    def decode_arithmetic(self, encoded_decimal, symbol_ranges, length):
        """
        Decode the encoded decimal value back into the original string using the symbol ranges.
        """
        decoded_string = ""
        low, high = 0.0, 1.0
        for _ in range(length):
            range_width = high - low
            for symbol, (sym_low, sym_high) in symbol_ranges.items():
                range_low = low + sym_low * range_width
                range_high = low + sym_high * range_width
                if range_low <= encoded_decimal < range_high:
                    decoded_string += symbol
                    low, high = range_low, range_high
                    break
        return decoded_string

    def decompress_file(self, input_file, output_file, original_file):
        """
        Decompress the binary file back into the original text file using arithmetic coding.
        """
        # Read the original file to get frequencies
        with open(original_file, 'r') as file:
            original_string = file.read()

        # Split original string into chunks
        original_chunks = [original_string[i:i + self.chunk_size] for i in range(0, len(original_string), self.chunk_size)]

        decompressed_data = []

        with open(input_file, 'rb') as file:  # Open in binary mode
            for i in range(len(original_chunks)):
                # Read packed binary data (8 bytes for each chunk, since it's a double)
                packed_value = file.read(8)

                # Unpack binary data to get the encoded decimal
                encoded_value = struct.unpack('>d', packed_value)[0]  # '>d' means big-endian double precision

                # Get the symbol ranges for this chunk
                chunk_frequencies = {}
                for char in original_chunks[i]:
                    chunk_frequencies[char] = chunk_frequencies.get(char, 0) + 1

                symbol_ranges = self.get_symbol_ranges(chunk_frequencies)

                # Decode the chunk
                decoded_chunk = self.decode_arithmetic(encoded_value, symbol_ranges, len(original_chunks[i]))

                decompressed_data.append(decoded_chunk)

        # Write all decoded chunks back to the output file
        with open(output_file, 'w') as file:
            for decoded_chunk in decompressed_data:
                file.write(decoded_chunk)

if __name__ == '__main__':
    decompressor = Decompressor(10)
    decompressor.decompress_file('output.bin', 'decompressed_file.txt', 'dickens.txt')