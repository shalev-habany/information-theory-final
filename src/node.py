
class Node:
    def __init__(self, char, freq):
        self.char = char  # Character
        self.freq = freq  # Frequency of the character
        self.left = None  # Left child
        self.right = None  # Right child

    def __lt__(self, other):
        return self.freq < other.freq
