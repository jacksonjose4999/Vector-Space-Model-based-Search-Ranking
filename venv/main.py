import glob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os.path
import math
import re

stop_words = set(stopwords.words('english'))

# Number of documents to be indexed
documents_in_consideration = 2

# Make this true if you wish to use lemmatization
use_lemmatization = False

source_files_pathname = '/Users/mohith/PycharmProjects/Vector-Space-Model-based-Search-Ranking/venv/corpus/Document'

lemmatizer = WordNetLemmatizer()
document_all_words = []
document_unique_words = []

if use_lemmatization:
    print("Using Lemmatization")
else:
    print("Not using lemmatization")

for document_counter in range(1, documents_in_consideration + 1):
    document_path = source_files_pathname + str(document_counter) + '.txt'
    print("Extracting from document " + str(document_counter))
    final_split_text = []
    words_in_current_email = []
    with open(document_path, 'r') as current_document:
        text_in_document = current_document.read()
        split_text = re.split("[\!\"\?\;\:\\n\,\.\ ]", text_in_document)
        for unique_word in split_text:
            if stop_words.__contains__(unique_word) == False:
                if document_unique_words.__contains__(unique_word) == False:
                    document_unique_words.append(unique_word)
                if use_lemmatization:
                    lemmatized_word = lemmatizer.lemmatize(unique_word.lower())
                    if final_split_text.__contains__(lemmatized_word) == False:
                        final_split_text.append(lemmatized_word)
                else:
                    final_split_text.append(unique_word)
        document_all_words.append(final_split_text)
        print(len(final_split_text))
        # document_unique_words.append(words_in_current_email)

#tf-idf of all the words in the document
complete_array_with_count = dict()

#number of documents the word has occured in, DOCUMENT FREQUENCY
document_frequency = dict()

# for document in document_unique_words:
for unique_word in document_unique_words:
    # calculates the tf-idf values of all the words in the respective documents
    document_wise_words_count = []
    for document_counter in range(0,documents_in_consideration):
        has_occured_in_current_document = False
        current_word_count = 0
        current_document = document_all_words[document_counter]
        for all_words in current_document:
            if unique_word == all_words:
                current_word_count += 1
                if has_occured_in_current_document == False:
                    has_occured_in_current_document = True
                    if unique_word not in document_frequency:
                        document_frequency[unique_word] = 1
                    else:
                        document_frequency[unique_word] += 1
        if current_word_count == 0:
            document_wise_words_count.append(0)
        else:
            document_wise_words_count.append((1 + math.log(current_word_count, 10))*(math.log(documents_in_consideration/document_frequency[unique_word],10)))
    complete_array_with_count[unique_word] = document_wise_words_count

# print(complete_array_with_count)
# print(len(complete_array_with_count))

ranking_values_query = dict()

user_query = input("Search the novels : ")
user_query = user_query.split(" ")
unique_words_in_query = dict()
for words in user_query:
    if words not in unique_words_in_query:
        unique_words_in_query[words] = 1
    else:
        unique_words_in_query[words] += 1

for words_in_query in unique_words_in_query:
    unique_words_in_query[words_in_query] = (1+math.log(unique_words_in_query[words_in_query]))

for documents in range(0,documents_in_consideration):
    result = 0.0
    for words_in_query in unique_words_in_query:
        if complete_array_with_count.__contains__(words_in_query):
            result = result + (complete_array_with_count[words_in_query][documents]*unique_words_in_query[words_in_query])
        ranking_values_query[documents] = result

for i in sorted(ranking_values_query.values()):
    print(i)

# print(ranking_values_query)
