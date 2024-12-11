from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import bigrams

nltk.download('punkt_tab')

def get_ngrams(comments:pd.DataFrame):
	tokens = comments.comment.apply(word_tokenize)
	bigrammed = ["".join(map(str, bigram)) for bigram in bigrams(tokens)]
	vectorizer = TfidfVectorizer(min_df=1)
	dat = pd.DataFrame(bigrammed, columns=["comment"])
	return pd.DataFrame(data=vectorizer.fit_transform(dat.comment).toarray(), columns=vectorizer.get_feature_names_out())


def generate_bigrams(comments: pd.DataFrame):
    # Tokenize the comments
    tokens = comments.comment.apply(word_tokenize)
    
    # Generate bigrams for each tokenized comment and join them into strings
    bigrammed = [
        " ".join("".join(map(str, bigram)) for bigram in bigrams(token_list))
        for token_list in tokens
    ]
    
    # Vectorize the bigrams using TfidfVectorizer
    vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = vectorizer.fit_transform(bigrammed)
    
    # Convert the matrix to a DataFrame
    return pd.DataFrame(
        data=tfidf_matrix.toarray(), 
        columns=vectorizer.get_feature_names_out()
    )


def count_vectorizer_bigram(comments:pd.DataFrame):
    tokens = pd.DataFrame(comments.comment.apply(word_tokenize), columns=["comment"])
    vectorizer = CountVectorizer(min_df=5, ngram_range=(2, 2))
    bigrammed = vectorizer.fit_transform(tokens.comment)
    return pd.DataFrame(bigrammed, columns=vectorizer.get_feature_names_out())