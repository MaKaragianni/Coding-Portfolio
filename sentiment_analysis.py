import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# Loading spaCy & TextBlob
# Since we'll be using a spaCy model that includes word vectors,
# it's best to use en_core_web_lg instead of en_core_web_sm.
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob')

# Cleaning & preprocessing text data
def preprocess_text(text):
    doc = nlp(text)
    # Removing stopwords, punctuation & performing lowercasing
    tokens = [token.text.lower().strip() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return " ".join(tokens)

# Sentiment analysis
def analyse_sentiment(text):
    doc = nlp(text)
    polarity = doc._.blob.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Loading dataset & preprocessing the text
dataframe = pd.read_csv('amazon_product_reviews.csv', low_memory=False, encoding='utf-8')
dataframe['clean_reviews'] = dataframe['reviews.text'].dropna().apply(preprocess_text)

# Sentiment analysis on 3 product reviews for testing results
for i in range(3):
    example_review = dataframe['clean_reviews'].iloc[i]
    print(f"Cleaned Review {i+1}: {example_review}")
    sentiment = analyse_sentiment(example_review)
    print(f"Review {i+1} Sentiment: {sentiment}\n")

'''
Prints:
Cleaned Review 1: product far disappointed children love use like ability monitor control content ease
Review 1 Sentiment: negative

Cleaned Review 2: great beginner experienced person bought gift loves
Review 2 Sentiment: positive

Cleaned Review 3: inexpensive tablet use learn step nabi thrilled learn skype
Review 3 Sentiment: positive
'''

# Similarity analysis between 2 product reviews, using spacy & word vectors
def compare_similarity(review1, review2):
    doc1 = nlp(review1)
    doc2 = nlp(review2)
    return doc1.similarity(doc2)

# Selecting 2 reviews for similarity comparison
review1 = dataframe['clean_reviews'].iloc[0]
print(f"Review 1: {dataframe['reviews.text'].iloc[0]}")
review2 = dataframe['clean_reviews'].iloc[1]
print(f"Review 2: {dataframe['reviews.text'].iloc[1]}")
similarity_score = compare_similarity(review1, review2)
print(f"Similarity score between two reviews: {similarity_score}")

'''
Prints:
Review 1: This product so far has not disappointed. My children love to use it and I like the ability to monitor control what content they see with ease.
Review 2: great for beginner or experienced person. Bought as a gift and she loves it
Similarity score between two reviews: 0.6528314547670601
'''