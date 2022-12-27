from transformers import BertTokenizer, BertModel
from torch.nn import CosineSimilarity as cosine_similarity
import torch
import Levenshtein
from typing import List, Tuple, Callable, TextIO


class WriteData:
    def __init__(self, out_strem: TextIO, test_data_fn: Callable = None) -> None:
        self.out_strem = out_strem
        if test_data_fn is not None:
            self.test_data = test_data_fn

    def write(self, data: str):
        if self.test_data and not self.test_data(data):
            raise ValueError("test data failed")
        self.out_strem.write(data)


def get_close_sentences(name, sentences):
    # Create a list of tuples, where each tuple consists of a sentence and its Levenshtein distance to the name
    sentence_distances = [(sentence, Levenshtein.distance(
        name, sentence)) for sentence in sentences]

    # Sort the list of tuples by the Levenshtein distance in ascending order
    sorted_sentences = sorted(sentence_distances, key=lambda x: x[1])

    # Extract the sorted list of sentences from the tuples
    close_sentences = [t[0] for t in sorted_sentences]

    return close_sentences


class similarity:
    def __init__(self, sentences):
        # Load the BERT tokenizer and model
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        self.model = BertModel.from_pretrained('bert-base-cased')
        self.sentences = sentences
        self.tokenizer()

    def tokenizer(self):
        # Tokenize and encode the sentences using BERT
        self.encoded_sentences = [self.tokenizer.encode(
            sentence, return_tensors='pt') for sentence in self.sentences]

    def similarity(self, sentence):
# Calculate the similarity between the vectors
        similarity = []
        for i, encoded_sentence in enumerate(self.encoded_sentences):
            with torch.no_grad():
                output = self.model(encoded_sentence)[0]
            similarity.append(cosine_similarity(dim=1)(output[0], self.encoded_sentences[0][0]))

