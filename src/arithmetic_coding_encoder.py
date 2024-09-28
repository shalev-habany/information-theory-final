import struct

class Compressor:
    def __init__(self, chunk_size):
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

    def encode_arithmetic(self, input_string, symbol_ranges):
        low, high = 0.0, 1.0
        for symbol in input_string:
            range_width = high - low
            sym_low, sym_high = symbol_ranges[symbol]
            high = low + range_width * sym_high
            low = low + range_width * sym_low
        return (low + high) / 2

    def compress_file(self, input_file, output_file):
        with open(input_file, 'r') as file:
            input_string = file.read()
        chunks = [input_string[i:i + self.chunk_size] for i in range(0, len(input_string), self.chunk_size)]
        with open(output_file, 'wb') as file:
            for chunk in chunks:
                frequencies = {}
                for char in chunk:
                    frequencies[char] = frequencies.get(char, 0) + 1
                symbol_ranges = self.get_symbol_ranges(frequencies)
                encoded_value = self.encode_arithmetic(chunk, symbol_ranges)
                packed_value = struct.pack('>d', encoded_value)
                file.write(packed_value)