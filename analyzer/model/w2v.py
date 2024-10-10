from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
import multiprocessing
import pandas as pd
import joblib


def w2v_model(df: pd.DataFrame) -> None:
    """
    Train a word2vec model from a DataFrame of comments.

    The model is saved to a file named './model/w2v_model.pkl'.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame with a single column 'comment' containing the text
        comments.
    """
    sent = [row.split() for row in df['comment']]
    cores = multiprocessing.cpu_count() 
    phrases = Phrases(sent, min_count=10, progress_per=10000)
    bigram = Phraser(phrases)
    sentences = bigram[sent]

    w2v_model = Word2Vec(
        min_count=20,
        window=2,
        vector_size=300,
        sample=6e-5,
        alpha=0.03,
        min_alpha=0.0007,
        negative=20,
        workers=cores-1
    )
    w2v_model.build_vocab(sentences, progress_per=10000)
    w2v_model.train(
        sentences,
        total_examples=w2v_model.corpus_count,
        epochs=30,
        report_delay=1
    )
    joblib.dump(w2v_model, './analyzer/model/w2v_model.pkl')

