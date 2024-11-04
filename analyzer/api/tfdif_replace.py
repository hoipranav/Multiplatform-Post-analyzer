import pandas as pd

def create_tfidf_dictionary(x, transformed_file, features):
    '''
    create dictionary for each input sentence x, where each word has assigned its tfidf score
    
    inspired  by function from this wonderful article: 
    https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34
    
    x - row of dataframe, containing sentences, and their indexes,
    transformed_file - all sentences transformed with TfidfVectorizer
    features - names of all words in corpus used in TfidfVectorizer

    '''
    try:
        vector_coo = transformed_file[x].tocoo()
        vector_coo_col = features[vector_coo.col]
        dict_from_coo = dict(zip(vector_coo_col[0], vector_coo.data))
    except IndexError:
        dict_from_coo = dict(zip("xxx", [0.000000]))
    return dict_from_coo

def replace_tfidf_words(x:pd.Series, transformed_sen: pd.DataFrame, features:pd.DataFrame):
    '''
    replacing each word with it's calculated tfidf dictionary with scores of each word
    x - row of dataframe, containing sentences, and their indexes,
    transformed_file - all sentences transformed with TfidfVectorizer
    features - names of all words in corpus used in TfidfVectorizer
    '''
    dictionary = create_tfidf_dictionary(x.name, transformed_sen, features)   
    return list(map(lambda y:dictionary.get(y, 0), x.iloc[0].split()))


def replace_sentiment_words(word, sentiment_dict):
    '''
    replacing each word with its associated sentiment score from sentiment dict
    '''
    try:
        out = sentiment_dict[word]
    except KeyError:
        out = 0
    return out