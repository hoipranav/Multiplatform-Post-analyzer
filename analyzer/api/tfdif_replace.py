import pandas as pd

def create_tfidf_dictionary(x, transformed_sen, features: pd.DataFrame):
    '''
    create dictionary for each input sentence x, where each word has assigned its tfidf score
    
    inspired  by function from this wonderful article: 
    https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34
    
    x - row of dataframe, containing sentences, and their indexes,
    transformed_sen - all sentences transformed with TfidfVectorizer
    features - names of all words in corpus used in TfidfVectorizer

    '''
    # print(f"tranformed sen x name: {transformed_sen[x.name].tocoo()}")
    vector_coo = transformed_sen[x.name].tocoo()
    print(f"vector coo : {vector_coo}")
    # vector_coo_copy = vector_coo.tocsr().todense().reshape(features.shape[0], 1)
    # print(f"feature list")
    # for i in range(vector_coo.col[0]):
    #     print(features.iloc[i])
    # print(f"features shape: {features.shape}")
    # print(vector_coo.col)
    print(vector_coo.data)
    words = list(features.iloc[vector_coo.col].values)
    print(words)
    dict_from_coo = dict(zip(words[0], vector_coo.data))
    return dict_from_coo

def replace_tfidf_words(x:pd.Series, transformed_sen, features:pd.DataFrame):
    '''
    replacing each word with it's calculated tfidf dictionary with scores of each word
    x - row of dataframe, containing sentences, and their indexes,
    transformed_file - all sentences transformed with TfidfVectorizer
    features - names of all words in corpus used in TfidfVectorizer
    '''
    dictionary = create_tfidf_dictionary(x, transformed_sen, features)   
    return list(map(lambda y:dictionary.get(y, 0), x.iloc[0].split()))