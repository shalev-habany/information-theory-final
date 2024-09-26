def get_frequency_table(text):
    frequency_table = {}
    for char in text:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

def get_sections(frequency_table):
    sections = {}
    low = 0
    for char, freq in frequency_table.items():
        high = low + freq
        sections[char] = (low, high)
        low = high
    return sections

def normalize_sections(sections):
    total = sum(high - low for low, high in sections.values())
    normalized_sections = {}
    for char, (low, high) in sections.items():
        normalized_low = low / total
        normalized_high = high / total
        normalized_sections[char] = (normalized_low, normalized_high)
    return normalized_sections

def get_normalized_sections(text):
    frequency_table = get_frequency_table(text)
    sections = get_sections(frequency_table)
    normalized_sections = normalize_sections(sections)
    return normalized_sections

def encode(text, normalized_sections):
    low = 0
    high = 1
    for char in text:
        low, high = (
            low + (high - low) * normalized_sections[char][0],
            low + (high - low) * normalized_sections[char][1],
        )
    return (low + high) / 2