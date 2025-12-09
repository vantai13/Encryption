"""
Mono-alphabetic Substitution Cipher Cracker
Sử dụng: Frequency Analysis + Hill Climbing + Simulated Annealing
"""

import random
import math
from collections import Counter

class MonoalphabeticCipher:
    def __init__(self):
        # Tần suất chữ cái tiếng Anh
        self.letter_freq = {
            'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
            'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25,
            'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36,
            'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29,
            'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07
        }
        
        # Tần suất bigrams phổ biến
        self.common_bigrams = [
            'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd',
            'ti', 'es', 'or', 'te', 'of', 'ed', 'is', 'it', 'al', 'ar'
        ]
        
        # Tần suất trigrams
        self.common_trigrams = [
            'the', 'and', 'ing', 'ion', 'tio', 'ent', 'her', 'for', 'tha', 'ter'
        ]
        
        # Quadgrams log-likelihood (giản lược - thực tế cần file lớn hơn)
        self.quadgram_scores = self._load_quadgrams()
    
    def _load_quadgrams(self):
        """Load quadgram frequencies - simplified version"""
        # Trong thực tế, nên load từ file quadgrams.txt
        # Đây là phiên bản đơn giản hóa
        common_quads = {
            'tion': -4.5, 'that': -5.0, 'with': -5.2, 'ther': -5.3,
            'ment': -5.4, 'atio': -6.0, 'ould': -6.1, 'this': -5.8,
            'ting': -5.9, 'here': -6.0, 'ough': -6.5, 'qual': -8.0
        }
        return common_quads
    
    def calculate_fitness(self, text):
        """Tính fitness score dựa trên quadgrams"""
        text = text.lower()
        score = 0
        default_score = -10  # Score mặc định cho quadgram không có trong dict
        
        # Quadgram scoring
        for i in range(len(text) - 3):
            quad = text[i:i+4]
            if quad.isalpha():
                score += self.quadgram_scores.get(quad, default_score)
        
        return score
    
    def create_initial_mapping(self, ciphertext):
        """Tạo mapping ban đầu dựa trên frequency analysis"""
        # Đếm tần suất trong ciphertext
        text_lower = ciphertext.lower()
        letter_count = Counter(c for c in text_lower if c.isalpha())
        
        # Sắp xếp theo tần suất
        sorted_cipher = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
        sorted_english = sorted(self.letter_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Tạo mapping ban đầu
        mapping = {}
        for i, (cipher_char, _) in enumerate(sorted_cipher):
            if i < len(sorted_english):
                plain_char = sorted_english[i][0]
                mapping[cipher_char] = plain_char
        
        # Điền các ký tự còn thiếu
        all_letters = set('abcdefghijklmnopqrstuvwxyz')
        used_plain = set(mapping.values())
        unused_plain = list(all_letters - used_plain)
        
        for cipher_char in all_letters:
            if cipher_char not in mapping and unused_plain:
                mapping[cipher_char] = unused_plain.pop(0)
        
        return mapping
    
    def apply_mapping(self, ciphertext, mapping):
        """Áp dụng mapping để giải mã"""
        result = []
        for char in ciphertext:
            if char.islower():
                result.append(mapping.get(char, char))
            elif char.isupper():
                result.append(mapping.get(char.lower(), char.lower()).upper())
            else:
                result.append(char)
        return ''.join(result)
    
    def hill_climbing(self, ciphertext, initial_mapping, max_iterations=10000):
        """Hill climbing optimization"""
        current_mapping = initial_mapping.copy()
        current_text = self.apply_mapping(ciphertext, current_mapping)
        current_score = self.calculate_fitness(current_text)
        
        best_mapping = current_mapping.copy()
        best_score = current_score
        
        letters = list('abcdefghijklmnopqrstuvwxyz')
        no_improvement = 0
        
        print(f"Initial score: {current_score:.2f}")
        
        for iteration in range(max_iterations):
            # Swap hai chữ cái ngẫu nhiên
            a, b = random.sample(letters, 2)
            
            # Tạo mapping mới
            new_mapping = current_mapping.copy()
            new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]
            
            # Tính score mới
            new_text = self.apply_mapping(ciphertext, new_mapping)
            new_score = self.calculate_fitness(new_text)
            
            # Chấp nhận nếu tốt hơn
            if new_score > current_score:
                current_mapping = new_mapping
                current_score = new_score
                no_improvement = 0
                
                if new_score > best_score:
                    best_mapping = new_mapping.copy()
                    best_score = new_score
                    
                    if iteration % 100 == 0:
                        print(f"Iteration {iteration}: Score improved to {best_score:.2f}")
            else:
                no_improvement += 1
            
            # Early stopping nếu không cải thiện sau 1000 lần
            if no_improvement > 1000:
                break
        
        return best_mapping, best_score
    
    def simulated_annealing(self, ciphertext, initial_mapping, 
                           max_iterations=50000, temp_start=20, temp_end=0.001):
        """Simulated annealing - mạnh hơn hill climbing"""
        current_mapping = initial_mapping.copy()
        current_text = self.apply_mapping(ciphertext, current_mapping)
        current_score = self.calculate_fitness(current_text)
        
        best_mapping = current_mapping.copy()
        best_score = current_score
        
        letters = list('abcdefghijklmnopqrstuvwxyz')
        
        print(f"Starting simulated annealing with score: {current_score:.2f}")
        
        for iteration in range(max_iterations):
            # Giảm nhiệt độ theo thời gian
            temperature = temp_start * ((temp_end / temp_start) ** (iteration / max_iterations))
            
            # Swap hai chữ cái
            a, b = random.sample(letters, 2)
            
            new_mapping = current_mapping.copy()
            new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]
            
            new_text = self.apply_mapping(ciphertext, new_mapping)
            new_score = self.calculate_fitness(new_text)
            
            # Chấp nhận nếu tốt hơn HOẶC theo xác suất
            delta = new_score - current_score
            
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_mapping = new_mapping
                current_score = new_score
                
                if new_score > best_score:
                    best_mapping = new_mapping.copy()
                    best_score = new_score
                    
                    if iteration % 1000 == 0:
                        print(f"Iteration {iteration}: Best score = {best_score:.2f}, Temp = {temperature:.4f}")
        
        print(f"\nFinal best score: {best_score:.2f}")
        return best_mapping, best_score
    
    def crack(self, ciphertext, use_annealing=True):
        """
        Hàm chính để crack mono-alphabetic cipher
        Returns: (mapping, plaintext, score)
        """
        print("="*60)
        print("CRACKING MONO-ALPHABETIC SUBSTITUTION")
        print("="*60)
        
        # Bước 1: Tạo mapping ban đầu
        print("\n[1] Creating initial mapping from frequency analysis...")
        initial_mapping = self.create_initial_mapping(ciphertext)
        
        # Bước 2: Optimize với hill climbing hoặc simulated annealing
        if use_annealing:
            print("\n[2] Optimizing with Simulated Annealing...")
            best_mapping, best_score = self.simulated_annealing(ciphertext, initial_mapping)
        else:
            print("\n[2] Optimizing with Hill Climbing...")
            best_mapping, best_score = self.hill_climbing(ciphertext, initial_mapping)
        
        # Bước 3: Giải mã với mapping tốt nhất
        plaintext = self.apply_mapping(ciphertext, best_mapping)
        
        return best_mapping, plaintext, best_score
    
    def format_mapping(self, mapping):
        """Format mapping để dễ đọc"""
        sorted_mapping = sorted(mapping.items())
        cipher_alpha = ''.join([k for k, v in sorted_mapping])
        plain_alpha = ''.join([v for k, v in sorted_mapping])
        return f"Cipher:    {cipher_alpha}\nPlaintext: {plain_alpha}"


def main():
    """Test function"""
    cipher = MonoalphabeticCipher()
    
    # Test với văn bản mẫu
    test_plaintext = """
    The quick brown fox jumps over the lazy dog. This is a test of the 
    monoalphabetic substitution cipher. It uses a simple substitution where 
    each letter is replaced by another letter consistently throughout the text.
    """
    
    # Tạo random mapping để mã hóa
    import string
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    encrypt_mapping = dict(zip(letters, shuffled))
    
    print("Encryption mapping:")
    print(cipher.format_mapping(encrypt_mapping))
    
    # Mã hóa
    ciphertext = cipher.apply_mapping(test_plaintext, encrypt_mapping)
    print(f"\nCiphertext:\n{ciphertext}")
    
    # Crack
    print("\n" + "="*60)
    found_mapping, decrypted, score = cipher.crack(ciphertext, use_annealing=True)
    
    print("\n" + "="*60)
    print("RESULT")
    print("="*60)
    print("\nFound mapping:")
    print(cipher.format_mapping(found_mapping))
    print(f"\nDecrypted text:\n{decrypted[:300]}...")
    print(f"\nFitness score: {score:.2f}")


