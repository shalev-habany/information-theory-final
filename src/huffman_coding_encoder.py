import heapq
from collections import defaultdict

from src.node import Node


class HuffmanCompressor:
    def __init__(self, chunk_size=1000):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.chunk_size = chunk_size

    def frequency_table(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency

    def build_heap(self, frequency):
        for key in frequency:
            node = Node(key, frequency[key])
            heapq.heappush(self.heap, node)

    def build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def build_codes(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.build_codes(root.left, current_code + "0")
        self.build_codes(root.right, current_code + "1")

    def generate_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.build_codes(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            byte_array.append(int(byte, 2))
        return byte_array

    def compress_file(self, input_file, output_file):
        with open(input_file, 'r') as file:
            input_string = file.read()
        frequency = self.frequency_table(input_string)
        self.build_heap(frequency)
        self.build_tree()
        self.generate_codes()
        with open(output_file, 'wb') as output:
            for i in range(0, len(input_string), self.chunk_size):
                chunk = input_string[i:i + self.chunk_size]
                encoded_text = self.get_encoded_text(chunk)
                padded_encoded_text = self.pad_encoded_text(encoded_text)
                byte_array = self.get_byte_array(padded_encoded_text)
                output.write(bytes(byte_array))
