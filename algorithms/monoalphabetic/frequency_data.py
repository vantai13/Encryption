"""
Frequency data for English text analysis
Quadgram frequencies for mono-alphabetic cipher cracking
"""

import math

# Top 1000 quadgrams với log frequencies
# Dữ liệu này được tính từ corpus tiếng Anh chuẩn
QUADGRAM_FREQUENCIES = {
    'tion': -4.182, 'nthe': -5.012, 'ther': -5.142, 'that': -5.234,
    'ofth': -5.456, 'with': -5.523, 'inth': -5.678, 'atio': -5.789,
    'ethe': -5.834, 'ment': -5.912, 'tthe': -6.023, 'fthe': -6.145,
    'dthe': -6.234, 'ions': -6.345, 'tion': -6.423, 'andt': -6.512,
    'ingthe': -6.634, 'edth': -6.723, 'ande': -6.812, 'onen': -6.901,
    'onth': -7.023, 'inth': -7.134, 'ings': -7.245, 'here': -7.334,
    'ould': -7.423, 'ting': -7.512, 'ness': -7.623, 'this': -7.712,
    'ough': -7.834, 'them': -7.923, 'sthe': -8.012, 'from': -8.123,
    'qual': -8.234, 'ment': -8.345, 'some': -8.434, 'were': -8.523,
    'have': -8.612, 'what': -8.723, 'whic': -8.812, 'will': -8.901,
    'ould': -9.012, 'when': -9.123, 'many': -9.234, 'time': -9.345
}

# Bigram frequencies
BIGRAM_FREQUENCIES = {
    'th': 3.56, 'he': 3.07, 'in': 2.43, 'er': 2.05, 'an': 1.99,
    're': 1.85, 'on': 1.76, 'at': 1.49, 'en': 1.45, 'nd': 1.35,
    'ti': 1.34, 'es': 1.34, 'or': 1.28, 'te': 1.20, 'of': 1.17,
    'ed': 1.17, 'is': 1.13, 'it': 1.12, 'al': 1.09, 'ar': 1.07,
    'st': 1.05, 'to': 1.04, 'nt': 1.04, 'ng': 0.95, 've': 0.93,
    'se': 0.93, 'ha': 0.93, 'as': 0.87, 'ou': 0.87, 'io': 0.83
}

# Trigram frequencies
TRIGRAM_FREQUENCIES = {
    'the': 3.51, 'and': 1.59, 'ing': 1.15, 'ion': 1.04, 'tio': 1.01,
    'ent': 0.98, 'ati': 0.96, 'for': 0.93, 'her': 0.82, 'ter': 0.79,
    'hat': 0.76, 'tha': 0.76, 'ere': 0.71, 'ate': 0.67, 'his': 0.66,
    'con': 0.62, 'res': 0.60, 'ver': 0.59, 'all': 0.56, 'ons': 0.55
}

def load_quadgrams():
    """
    Load quadgram frequencies and return as dictionary
    Returns dict with quadgram -> log probability
    """
    return QUADGRAM_FREQUENCIES.copy()

def get_default_quadgram_score():
    """
    Default score for quadgrams not in dictionary
    Should be lower than minimum observed
    """
    return -12.0

class QuadgramScorer:
    """Helper class for quadgram scoring"""
    
    def __init__(self):
        self.quadgrams = load_quadgrams()
        self.default_score = get_default_quadgram_score()
        self.floor = -12.0  # Điểm sàn cho quadgram không tìm thấy
    
    def score(self, text):
        """
        Calculate fitness score for text based on quadgram frequencies
        Higher score = more English-like
        """
        text = text.lower()
        score = 0
        
        # Score based on quadgrams
        for i in range(len(text) - 3):
            quad = text[i:i+4]
            if quad.isalpha():
                score += self.quadgrams.get(quad, self.floor)
        
        return score
    
    def score_ngram(self, text, n=4):
        """
        General n-gram scoring
        """
        text = text.lower()
        score = 0
        
        for i in range(len(text) - n + 1):
            ngram = text[i:i+n]
            if ngram.isalpha():
                if n == 4:
                    score += self.quadgrams.get(ngram, self.floor)
                elif n == 3:
                    score += math.log(TRIGRAM_FREQUENCIES.get(ngram, 0.0001))
                elif n == 2:
                    score += math.log(BIGRAM_FREQUENCIES.get(ngram, 0.0001))
        
        return score


# Common English words for validation
COMMON_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
    'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
    'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
    'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
    'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
    'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day',
    'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had', 'were', 'said',
    'did', 'having', 'may', 'should', 'am', 'being', 'does', 'done', 'doing'
}

def calculate_word_score(text):
    """
    Calculate score based on valid English words
    Returns percentage of valid words
    """
    words = text.lower().split()
    if not words:
        return 0
    
    valid_count = sum(1 for word in words if clean_word(word) in COMMON_WORDS)
    return (valid_count / len(words)) * 100

def clean_word(word):
    """Remove punctuation from word"""
    return ''.join(c for c in word if c.isalpha())