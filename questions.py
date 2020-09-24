import nltk
#nltk.download('stopwords')
import sys
import math
import os
import string

from nltk.tokenize import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    corpus_dict = {}
    for dir in os.listdir(directory):
        with open(os.path.join(directory, dir)) as f:
            corpus_dict[dir] = f.read()

    #print(corpus_dict['python.txt'])

    return corpus_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    token_document = word_tokenize(document)

    #print (token_document)

    document_words = []

    for word in token_document:
        if word not in string.punctuation and \
        word not in nltk.corpus.stopwords.words('english'):

            word = word.lower()

            document_words.append(word)


    #print(document_words)

    return document_words
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """


    num_documents = len(documents)

    words = set()

    for filename in documents:
        words.update(documents[filename])

    #print(words)
    idf_dict = {}

    for word in words:

        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(num_documents / f)
        idf_dict[word] = idf


    #print(idf_dict)

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """


    files_td_idf = {}


    for file in files:

        match_words = list([word for word in query if word in files[file]])

        frequencies = dict()

        word_idfs = dict()

        for word in match_words:


            word_idfs[word] = idfs[word]

            frequencies[word] = files[file].count(word)

        files_td_idf[file] = sum(word_idfs[word] * frequencies[word] for word in match_words)

    print(files_td_idf)
    sorted_files = {k: v for k, v in sorted(files_td_idf.items(),
                key=lambda item: item[1], reverse = True)}


    print(sorted_files)

    top_files = list([file for file in sorted_files])



    print(top_files[:n])

    return top_files[:n]




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


#def get_tf(word, file):


if __name__ == "__main__":
    main()
