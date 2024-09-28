import struct

class Decompressor:
    def __init__(self, chunk_size=1000):
        self.chunk_size = chunk_size

    def get_symbol_ranges(self, frequencies):
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
        with open(original_file, 'r') as file:
            original_string = file.read()

        original_chunks = [original_string[i:i + self.chunk_size] for i in range(0, len(original_string), self.chunk_size)]

        decompressed_data = []

        with open(input_file, 'rb') as file:
            for i in range(len(original_chunks)):
                packed_value = file.read(8)
                encoded_value = struct.unpack('>d', packed_value)[0]
                chunk_frequencies = {}
                for char in original_chunks[i]:
                    chunk_frequencies[char] = chunk_frequencies.get(char, 0) + 1
                symbol_ranges = self.get_symbol_ranges(chunk_frequencies)
                decoded_chunk = self.decode_arithmetic(encoded_value, symbol_ranges, len(original_chunks[i]))
                decompressed_data.append(decoded_chunk)
        with open(output_file, 'w') as file:
            for decoded_chunk in decompressed_data:
                file.write(decoded_chunk)

if __name__ == '__main__':
    decompressor = Decompressor(10)
    decompressor.decompress_file('output.bin', 'decompressed_file.txt', 'dickens.txt')