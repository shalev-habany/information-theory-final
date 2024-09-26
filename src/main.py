from tqdm import tqdm

from src.arithmetic_coding_decoder import Decompressor
from src.arithmetic_coding_encoder import Compressor
from src.huffman_coding_decoder import HuffmanDecompressor
from src.huffman_coding_encoder import HuffmanCompressor

# if __name__ == '__main__':
#     with tqdm(total=2, desc="Compression and Decompression", colour="green") as pbar:
#         compressor = Compressor(32, 15)
#         compressor.compress_file('./data/dickens.txt', './data/compressed.bin')
#         pbar.update(1)
#
#         decompressor = Decompressor(15)
#         decompressor.decompress_file('./data/compressed.bin', './data/decompressed.txt', './data/dickens.txt')
#         pbar.update(1)
#

if __name__ == "__main__":
    input_text_file = "./data/dickens.txt"
    compressed_file = "./data/huffman_compressed.bin"
    decompressed_text_file = "./data/huffman_decompressed.txt"

    compressor = HuffmanCompressor(chunk_size=1000)
    decompressor = HuffmanDecompressor(chunk_size=1024*1024)

    # Compress the input text file
    compressor.compress_file(input_text_file, compressed_file)

    # Decompress the compressed binary file
    decompressor.decompress_file(compressed_file, decompressed_text_file, compressor)
