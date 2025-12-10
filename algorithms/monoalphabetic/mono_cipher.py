"""
Mono-alphabetic Substitution Cipher Cracker
Sử dụng: Frequency Analysis + Hill Climbing + Simulated Annealing
"""

import random
import math
from collections import Counter
from .frequency_data import QuadgramScorer, calculate_word_score

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
        
        # Quadgram scorer
        self.scorer = QuadgramScorer()
    
    def calculate_fitness(self, text):
        """Tính fitness score dựa trên quadgrams"""
        return self.scorer.score(text)
    
    def create_initial_mapping(self, ciphertext):
        """Tạo mapping ban đầu dựa trên frequency analysis"""
        # Đếm tần suất trong ciphertext (chỉ chữ thường)
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
                # Giữ nguyên chữ hoa hoặc chuyển theo đề bài
                result.append(mapping.get(char.lower(), char.lower()))
            else:
                result.append(char)
        return ''.join(result)
    
    def simulated_annealing(self, ciphertext, initial_mapping, 
                           max_iterations=50000, temp_start=20, temp_end=0.001,
                           callback=None):
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
                        if callback:
                            callback(iteration, best_score)
        
        print(f"\nFinal best score: {best_score:.2f}")
        return best_mapping, best_score
    
    def crack(self, ciphertext, callback=None):
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
        
        # Bước 2: Optimize với simulated annealing
        print("\n[2] Optimizing with Simulated Annealing...")
        best_mapping, best_score = self.simulated_annealing(
            ciphertext, initial_mapping, callback=callback
        )
        
        # Bước 3: Giải mã với mapping tốt nhất
        plaintext = self.apply_mapping(ciphertext, best_mapping)
        
        return best_mapping, plaintext, best_score
    
    def format_mapping(self, mapping):
        """Format mapping để dễ đọc - theo yêu cầu output"""
        sorted_mapping = sorted(mapping.items())
        # Format: a->e, b->t, c->a, ...
        mapping_str = ', '.join([f"{k}->{v}" for k, v in sorted_mapping])
        return mapping_str


def crack_from_file(input_file, output_file):
    """
    Crack cipher từ file và ghi kết quả
    Theo đúng format yêu cầu của Lab06
    """
    # Đọc ciphertext
    with open(input_file, 'r', encoding='utf-8') as f:
        ciphertext = f.read()
    
    # Crack
    cipher = MonoalphabeticCipher()
    mapping, plaintext, score = cipher.crack(ciphertext)
    
    # Ghi kết quả theo format yêu cầu
    with open(output_file, 'w', encoding='utf-8') as f:
        # Dòng 1: điểm
        f.write(f"{score:.4f}\n")
        # Dòng 2: mapping
        f.write(cipher.format_mapping(mapping) + "\n")
        # Dòng 3+: plaintext
        f.write(plaintext)
    
    print(f"\n✓ Results saved to: {output_file}")
    return mapping, plaintext, score