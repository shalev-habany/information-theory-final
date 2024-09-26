from tqdm import tqdm

from src.arithmetic_coding_decoder import Decompressor
from src.arithmetic_coding_encoder import Compressor

if __name__ == '__main__':
    with tqdm(total=2, desc="Compression and Decompression", colour="green") as pbar:
        compressor = Compressor(32, 15)
        compressor.compress_file('dickens.txt', 'compressed.bin')
        pbar.update(1)

        decompressor = Decompressor(15)
        decompressor.decompress_file('compressed.bin', 'decompressed.txt', 'dickens.txt')
        pbar.update(1)