from brightics.function.sparse import sparse_encode, sparse_decode
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def tfidf_train(table, input_col, min_df=None, max_df=None, max_features=None, idf_weighting_scheme='unary'):
    _table = table.copy()
    
    _input_data = _table[input_col]
    
    if min_df is None:
        _min_df = 1
    else:
        _min_df = min_df
        
    if max_df is None:
        _max_df = 1.0
    else:
        _max_df = max_df
    
    if idf_weighting_scheme == 'idf':
        _vectorizer = TfidfVectorizer(min_df=_min_df, max_df=_max_df, max_features=max_features)
        _model = _vectorizer.fit(_input_data)        
        _tdm = _model.transform(_input_data)

    else:
        _vectorizer = CountVectorizer(min_df=_min_df, max_df=_max_df, max_features=max_features)
        _model = _vectorizer.fit(_input_data)        
        _tdm = _model.transform(_input_data)
    
    out_table = sparse_encode(_table, _tdm)['out_table']
    

    
    return {'out_table': out_table, 'fit_model': _model}

def tfidf_test(table, fit_model,input_col ):
    _table = table.copy()
    
    _input_data = _table[input_col]
    
    _transform = fit_model.transform(_input_data)
    
    out_table = sparse_encode(_table, _transform)['out_table']
    

    
    return {'out_table': out_table }