from tqdm import tqdm

from src.arithmetic_coding_decoder import Decompressor
from src.arithmetic_coding_encoder import Compressor
from src.huffman_coding_decoder import HuffmanDecompressor
from src.huffman_coding_encoder import HuffmanCompressor

def arithmetic_coding():
    input_text_file = "./data/dickens.txt"
    compressed_file = "./data_demo/arithmetic_coding_compressed.bin"
    decompressed_text_file = "./data_demo/arithmetic_coding_decompressed.txt"
    with tqdm(total=2, desc="Compression and Decompression arithmetic coding", colour="green") as pbar:
        compressor = Compressor(15)
        decompressor = Decompressor(15)
        compressor.compress_file(input_text_file, compressed_file)
        pbar.update(1)
        decompressor.decompress_file(compressed_file, decompressed_text_file, input_text_file)
        pbar.update(1)

def huffman_coding():
    input_text_file = "./data/dickens.txt"
    compressed_file = "./data_demo/huffman_compressed.bin"
    decompressed_text_file = "./data_demo/huffman_decompressed.txt"
    with tqdm(total=2, desc="Compression and Decompression huffman coding", colour="green") as pbar:
        compressor = HuffmanCompressor(chunk_size=1000)
        decompressor = HuffmanDecompressor(chunk_size=1024 * 1024)
        compressor.compress_file(input_text_file, compressed_file)
        pbar.update(1)
        decompressor.decompress_file(compressed_file, decompressed_text_file, compressor)
        pbar.update(1)

if __name__ == '__main__':
    arithmetic_coding()
    huffman_coding()