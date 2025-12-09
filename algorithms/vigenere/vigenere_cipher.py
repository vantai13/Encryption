"""
Vigenère Cipher Cracker
Sử dụng: Kasiski Examination + Index of Coincidence + Frequency Analysis
"""

from collections import Counter
import math

class VigenereCipher:
    def __init__(self):
        # Tần suất chữ cái tiếng Anh
        self.english_freq = {
            'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270,
            'f': 0.0223, 'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015,
            'k': 0.0077, 'l': 0.0403, 'm': 0.0241, 'n': 0.0675, 'o': 0.0751,
            'p': 0.0193, 'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
            'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015, 'y': 0.0197,
            'z': 0.0007
        }
        
        self.IC_ENGLISH = 0.0686  # Index of Coincidence cho tiếng Anh
        self.IC_RANDOM = 0.0385   # IC cho text ngẫu nhiên
    
    def clean_text(self, text):
        """Chỉ giữ lại chữ cái"""
        return ''.join(c.lower() for c in text if c.isalpha())
    
    def find_repeated_sequences(self, ciphertext, min_length=3, max_length=5):
        """Tìm các chuỗi lặp lại (Kasiski Examination)"""
        text = self.clean_text(ciphertext)
        sequences = {}
        
        for length in range(min_length, max_length + 1):
            for i in range(len(text) - length):
                seq = text[i:i+length]
                
                # Tìm các vị trí khác của chuỗi này
                positions = []
                for j in range(i + length, len(text) - length + 1):
                    if text[j:j+length] == seq:
                        positions.append(j)
                
                if positions:
                    if seq not in sequences:
                        sequences[seq] = [i]
                    sequences[seq].extend(positions)
        
        return sequences
    
    def calculate_spacings(self, sequences):
        """Tính khoảng cách giữa các vị trí xuất hiện"""
        spacings = []
        
        for seq, positions in sequences.items():
            if len(positions) < 2:
                continue
            
            for i in range(len(positions) - 1):
                spacing = positions[i+1] - positions[i]
                spacings.append(spacing)
        
        return spacings
    
    def find_factors(self, number):
        """Tìm ước số"""
        factors = []
        for i in range(2, min(number, 30)):  # Giới hạn key length <= 30
            if number % i == 0:
                factors.append(i)
        return factors
    
    def kasiski_examination(self, ciphertext, top_n=10):
        """Kasiski Examination - ước lượng độ dài khóa"""
        print("\n[Kasiski Examination]")
        
        sequences = self.find_repeated_sequences(ciphertext)
        
        if not sequences:
            print("No repeated sequences found!")
            return []
        
        print(f"Found {len(sequences)} repeated sequences")
        
        # In ra một số ví dụ
        sorted_seqs = sorted(sequences.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        for seq, positions in sorted_seqs:
            print(f"  '{seq}' appears at positions: {positions[:5]}...")
        
        spacings = self.calculate_spacings(sequences)
        
        if not spacings:
            print("No spacings found!")
            return []
        
        # Đếm tần suất các ước số
        factor_count = Counter()
        for spacing in spacings:
            factors = self.find_factors(spacing)
            for factor in factors:
                factor_count[factor] += 1
        
        # Lấy các ước số phổ biến nhất
        likely_keylengths = [k for k, v in factor_count.most_common(top_n)]
        
        print(f"\nMost common factors (likely key lengths):")
        for length, count in factor_count.most_common(top_n):
            print(f"  Length {length}: appears {count} times")
        
        return likely_keylengths
    
    def calculate_IC(self, text):
        """Tính Index of Coincidence"""
        text = self.clean_text(text)
        n = len(text)
        
        if n <= 1:
            return 0
        
        freq = Counter(text)
        ic = sum(count * (count - 1) for count in freq.values())
        ic /= (n * (n - 1))
        
        return ic
    
    def ic_test_keylength(self, ciphertext, key_length):
        """Test độ dài khóa bằng IC"""
        text = self.clean_text(ciphertext)
        
        # Chia thành các subset
        subsets = ['' for _ in range(key_length)]
        for i, char in enumerate(text):
            subsets[i % key_length] += char
        
        # Tính IC trung bình
        ic_values = [self.calculate_IC(subset) for subset in subsets]
        avg_ic = sum(ic_values) / len(ic_values)
        
        return avg_ic
    
    def find_key_length_ic(self, ciphertext, max_key_length=20):
        """Tìm độ dài khóa bằng IC"""
        print("\n[Index of Coincidence Analysis]")
        
        ic_results = []
        
        for key_length in range(1, max_key_length + 1):
            avg_ic = self.ic_test_keylength(ciphertext, key_length)
            ic_results.append((key_length, avg_ic))
        
        # Sắp xếp theo IC gần với tiếng Anh nhất
        ic_results.sort(key=lambda x: abs(x[1] - self.IC_ENGLISH))
        
        print(f"\nTop 10 key lengths by IC score:")
        for i, (length, ic) in enumerate(ic_results[:10], 1):
            diff = abs(ic - self.IC_ENGLISH)
            print(f"  #{i} Length {length:2d}: IC = {ic:.4f} (diff = {diff:.4f})")
        
        return [length for length, _ in ic_results[:10]]
    
    def chi_squared_score(self, text):
        """Tính chi-squared statistic"""
        text = self.clean_text(text)
        n = len(text)
        
        if n == 0:
            return float('inf')
        
        freq = Counter(text)
        
        chi2 = 0
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            observed = freq.get(letter, 0) / n
            expected = self.english_freq[letter]
            chi2 += ((observed - expected) ** 2) / expected
        
        return chi2
    
    def crack_caesar_subset(self, subset):
        """Crack một subset như Caesar cipher"""
        best_key = 0
        best_score = float('inf')
        
        for key in range(26):
            decrypted = ''.join(
                chr((ord(c) - ord('a') - key) % 26 + ord('a'))
                for c in subset
            )
            
            score = self.chi_squared_score(decrypted)
            
            if score < best_score:
                best_score = score
                best_key = key
        
        return best_key
    
    def find_key(self, ciphertext, key_length):
        """Tìm khóa với độ dài đã biết"""
        text = self.clean_text(ciphertext)
        
        # Chia thành các subset
        subsets = ['' for _ in range(key_length)]
        for i, char in enumerate(text):
            subsets[i % key_length] += char
        
        # Crack từng subset
        key = []
        for i, subset in enumerate(subsets):
            char_key = self.crack_caesar_subset(subset)
            key.append(chr(char_key + ord('a')))
            print(f"  Position {i}: key = '{chr(char_key + ord('a'))}' (shift = {char_key})")
        
        return ''.join(key)
    
    def decrypt_vigenere(self, ciphertext, key):
        """Giải mã Vigenère với khóa đã biết"""
        result = []
        key_index = 0
        key = key.lower()
        
        for char in ciphertext:
            if char.isalpha():
                is_upper = char.isupper()
                char = char.lower()
                
                shift = ord(key[key_index % len(key)]) - ord('a')
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                
                if is_upper:
                    decrypted = decrypted.upper()
                
                result.append(decrypted)
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def crack(self, ciphertext):
        """
        Hàm chính để crack Vigenère cipher
        Returns: (key, plaintext)
        """
        print("="*60)
        print("CRACKING VIGENÈRE CIPHER")
        print("="*60)
        
        # Bước 1: Kasiski Examination
        kasiski_lengths = self.kasiski_examination(ciphertext, top_n=10)
        
        # Bước 2: IC Analysis
        ic_lengths = self.find_key_length_ic(ciphertext, max_key_length=20)
        
        # Bước 3: Kết hợp kết quả
        # Ưu tiên các độ dài xuất hiện trong cả 2 phương pháp
        common_lengths = [l for l in kasiski_lengths if l in ic_lengths[:5]]
        
        if not common_lengths:
            common_lengths = ic_lengths[:3]
        
        print(f"\n[Combined Analysis]")
        print(f"Most likely key lengths: {common_lengths[:5]}")
        
        # Bước 4: Thử các độ dài khóa
        best_key = ""
        best_plaintext = ""
        best_score = float('inf')
        
        print(f"\n[Testing Key Lengths]")
        
        for key_length in common_lengths[:3]:  # Test top 3
            print(f"\nTrying key length = {key_length}:")
            
            key = self.find_key(ciphertext, key_length)
            plaintext = self.decrypt_vigenere(ciphertext, key)
            score = self.chi_squared_score(plaintext)
            
            print(f"  Found key: '{key}'")
            print(f"  Chi-squared score: {score:.4f}")
            print(f"  Preview: {plaintext[:100]}...")
            
            if score < best_score:
                best_score = score
                best_key = key
                best_plaintext = plaintext
        
        print("\n" + "="*60)
        print("FINAL RESULT")
        print("="*60)
        print(f"Key: {best_key}")
        print(f"Score: {best_score:.4f}")
        
        return best_key, best_plaintext


def main():
    """Test function"""
    cipher = VigenereCipher()
    
    # Test với văn bản dài
    test_plaintext = """
    The Vigenère cipher is a method of encrypting alphabetic text by using a series 
    of interwoven Caesar ciphers based on the letters of a keyword. It is a form of 
    polyalphabetic substitution. The Vigenère cipher has been reinvented many times. 
    The method was originally described by Giovan Battista Bellaso in his 1553 book 
    La cifra del. Sig. Giovan Battista Bellaso. However, the scheme was later 
    misattributed to Blaise de Vigenère in the 19th century, and is now widely known 
    as the Vigenère cipher. This cipher is well known because while it is easy to 
    understand and implement, for three centuries it resisted all attempts to break it.
    """ * 3  # Lặp lại để đủ dài
    
    test_key = "SECRET"
    
    print(f"Original plaintext length: {len(test_plaintext)}")
    print(f"Encryption key: '{test_key}'")
    
    # Mã hóa
    encrypted = cipher.decrypt_vigenere(test_plaintext, test_key)  # Dùng decrypt để encrypt (reverse)
    # Thực ra cần hàm encrypt riêng, nhưng với Vigenère, ta có thể dùng decrypt với key ngược
    
    # Mã hóa đúng cách
    result = []
    key_index = 0
    for char in test_plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            shift = ord(test_key[key_index % len(test_key)]) - ord('a')
            encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            if is_upper:
                encrypted_char = encrypted_char.upper()
            result.append(encrypted_char)
            key_index += 1
        else:
            result.append(char)
    
    ciphertext = ''.join(result)
    print(f"\nCiphertext preview:\n{ciphertext[:200]}...\n")
    
    # Crack
    found_key, decrypted = cipher.crack(ciphertext)
    
    print(f"\nDecrypted preview:\n{decrypted[:200]}...")
    print(f"\nKey match: {'✓' if found_key.upper() == test_key.upper() else '✗'}")

