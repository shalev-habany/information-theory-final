import struct

class Compressor:
    def __init__(self, precision, chunk_size):
        self.precision = precision
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

    def encode_arithmetic(self, input_string, symbol_ranges):
        """
        Perform arithmetic encoding of the input string.
        """
        low, high = 0.0, 1.0
        for symbol in input_string:
            range_width = high - low
            sym_low, sym_high = symbol_ranges[symbol]
            high = low + range_width * sym_high
            low = low + range_width * sym_low
        return (low + high) / 2  # Final encoded value

    def compress_file(self, input_file, output_file):
        """
        Compress a text file using finite precision arithmetic coding and save the result as a binary file.
        """
        with open(input_file, 'r') as file:
            input_string = file.read()

        # Split input string into chunks
        chunks = [input_string[i:i + self.chunk_size] for i in range(0, len(input_string), self.chunk_size)]

        with open(output_file, 'wb') as file:  # Open in binary mode
            for chunk in chunks:
                # Calculate frequencies for this chunk
                frequencies = {}
                for char in chunk:
                    frequencies[char] = frequencies.get(char, 0) + 1

                # Get symbol ranges based on frequencies
                symbol_ranges = self.get_symbol_ranges(frequencies)

                # Encode the chunk
                encoded_value = self.encode_arithmetic(chunk, symbol_ranges)

                # Pack the encoded value as a double-precision float (8 bytes)
                packed_value = struct.pack('>d', encoded_value)  # '>d' means big-endian double precision

                # Write packed binary data to the file
                file.write(packed_value)

if __name__ == '__main__':
    compressor = Compressor(64, 10)
    compressor.compress_file('dickens.txt', 'output.bin')