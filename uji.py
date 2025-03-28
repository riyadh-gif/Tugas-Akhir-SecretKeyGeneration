import math
from collections import Counter

def calculate_entropy(data):
    # Hitung frekuensi dari setiap karakter
    counts = Counter(data)
    total = len(data)
    
    # Hitung entropi menggunakan rumus Shannon
    entropy = 0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
        
    return entropy

# Contoh kunci dalam format heksadesimal
key = "c86a69d877ea5ecde3ccf38be9950b69"

# Menghitung entropi dari kunci
entropy = calculate_entropy(key)
print(f"Entropy dari kunci: {entropy} bit")
