import nltk
from nltk.tokenize import WhitespaceTokenizer
import random as r
from re import match

class TextGenerator:
    def __init__(self, file):
        self.file = file
        self.tokens = []
        self.trigrams = []
        self.trigrams_dict = {}
        self.prediction_dict = {}

    def tokenize(self):
        with open(self.file, 'r', encoding='utf-8') as file:
            text = file.read()
        tokenizer = WhitespaceTokenizer()
        tokens = tokenizer.tokenize(text)
        self.tokens = tokens

    def corpus_statistics(self):
        print("Corpus statistics:")
        print("All tokens:", len(self.tokens))
        print("Unique tokens:", len(set(self.tokens)))
        print("Number of trigrams:", len(self.trigrams))

    def print_token(self):
        while True:
            idx = input("")
            if idx == "exit":
                break
            try:
                int_idx = int(idx)
                if int_idx >= 0 and int_idx < len(self.tokens):
                    print(self.tokens[int_idx])
                elif abs(int_idx) >= len(self.tokens):
                    print("Index Error. Please input an integer that is in the range of the corpus.")
                else:
                    int_idx = len(self.tokens) + int_idx
                    print(self.tokens[int_idx])
            except ValueError:
                print("Type Error. Please input an integer.")

    def create_trigrams(self):
        self.trigrams = list(nltk.trigrams(self.tokens))  # Use nltk.trigrams for trigrams

    def number_of_trigrams(self):
        print("Number of trigrams:", len(self.trigrams))

    def print_trigram(self):
        while True:
            head_idx = input("")
            if head_idx == "exit":
                break
            try:
                int_head_idx = int(head_idx)
                if int_head_idx >= 0 and int_head_idx < len(self.trigrams):
                    print(f"Head: {' '.join(self.trigrams[int_head_idx][:2])} Tail: {self.trigrams[int_head_idx][2]}")
                elif abs(int_head_idx) >= len(self.trigrams):
                    print("Index Error. Please input a value that is not greater than the number of all trigrams.")
                else:
                    int_head_idx = len(self.trigrams) + int_head_idx
                    print(f"Head: {' '.join(self.trigrams[int_head_idx][:2])} Tail: {self.trigrams[int_head_idx][2]}")
            except ValueError:
                print("Type Error. Please input an integer.")

    def create_trigrams_dict(self):
        for trigram in self.trigrams:
            head = ' '.join(trigram[:2])  # Combine the first two tokens into a single head
            tail = trigram[2]
            if head not in self.trigrams_dict:
                self.trigrams_dict[head] = {}
            if tail not in self.trigrams_dict[head]:
                self.trigrams_dict[head][tail] = 1
            else:
                self.trigrams_dict[head][tail] += 1

    def print_tails(self):
        while True:
            head = input("")
            if head == "exit":
                break
            if head in self.trigrams_dict:
                print(f"Head: {head}")
                for tail in self.trigrams_dict[head]:
                    print(f"Tail: {tail}      Count: {self.trigrams_dict[head][tail]}")
            if head not in self.trigrams_dict:
                print("Key Error. The requested word is not in the model. Please input another word.")

    def create_prediction_dict(self):
        most_common_count = -1
        for head, tails in self.trigrams_dict.items():
            for tail, count in tails.items():
                if count > most_common_count:
                    most_common_count = count
                    most_common_tail = tail
            self.prediction_dict[head] = most_common_tail
            most_common_count = -1

    def generate_text(self):
        sentence = []
        head = r.choice(list(self.trigrams_dict.keys()))  # Choose a random trigram head as the starting point
        while True:
            sentence.extend(head.split())  # Split the head into tokens and add to the sentence
            if head.endswith((".", "!", "?")):
                break
            last_tokens = ' '.join(sentence[-2:])  # Get the last two tokens in the sentence
            if last_tokens in self.prediction_dict:
                head = self.prediction_dict[last_tokens]  # Predict the next word based on the last two tokens
            else:
                break
        if len(sentence) < 5:
            self.generate_text()
        else:
            print(" ".join(sentence))

def main():
    file = input("Enter the path to the corpus file: ")
    corpus = TextGenerator(file)
    corpus.tokenize()
    corpus.create_trigrams()  # Change to create trigrams
    corpus.create_trigrams_dict()  # Change to create trigrams dictionary
    corpus.create_prediction_dict()
    for _ in range(10):
        corpus.generate_text()

if __name__ == "__main__":
    main()



