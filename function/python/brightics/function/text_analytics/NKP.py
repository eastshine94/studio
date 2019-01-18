from brightics.common.report import ReportBuilder, strip_margin, pandasDF2MD
from brightics.function.utils import _model_dict
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from twkorean import TwitterKoreanProcessor

import MeCab
import pandas as pd
import numpy as np
import re


def twitter_tokenizer(table, input_col, token_col_name = 'tokens', pos_col_name = 'pos',stemming=False, normalization=False, morpheme=None) :
    processor = TwitterKoreanProcessor(stemming=stemming, normalization=normalization)
    out_table = table.copy()
    tokens_col_data = []
    pos_col_data = []
    for i in out_table.index :
        try:
            sentence = out_table.at[i,input_col]
            tokenize = processor.tokenize(sentence)
            tokens_list = []
            pos_list = []
            for token in tokenize:
                if(morpheme is None or token.pos in morpheme):
                    tokens_list.append(token.text)
                    pos_list.append(token.pos)

            if (tokens_list == []) :
                out_table.drop(i,inplace=True)
            else :
                tokens_col_data.append(tokens_list)
                pos_col_data.append(pos_list)
        except:
            out_table.drop(i,inplace=True)
    out_table[token_col_name] = tokens_col_data
    out_table[pos_col_name] = pos_col_data

    return {'out_table': out_table} 
    
def analyzer(table,input_col,id_col = None) :
    input_table = table.copy()
    tagger = MeCab.Tagger()
    data_list = []
    
    for document_id, table_index in enumerate(input_table.index):
        try:
            parse = tagger.parseToNode(input_table.at[table_index,input_col])
            index = 0
            while parse:
                if(parse.surface != ""):
                    word = parse.surface
                    feature = parse.feature.split(",")
                    pos = feature[0]
                    start = index
                    index += len(word)
                    end = index
                    if(id_col is None):
                        data_list.append([document_id,word,pos,feature,start,end])
                    else : 
                        data_list.append([input_table.at[table_index,id_col],word,pos,feature,start,end])
                parse = parse.next
        except:
            None
    out_table = pd.DataFrame(data=data_list,columns=['id','word','pos','feature','start','end'])
    return {'out_table': out_table}


def mecab_tokenizer(table, input_col,token_col_name = 'tokens', pos_col_name = 'pos', morpheme=None):
    out_table = table.copy()
    tagger = MeCab.Tagger()

    tokens_col_data = []
    pos_col_data = []

    for i in out_table.index:
        tokens_list = []
        pos_list = []

        try:
            parse = tagger.parseToNode(out_table.at[i,input_col])
            while parse:
                if(parse.surface != ""):
                    word = parse.surface
                    feature = parse.feature.split(",")
                    pos = feature[0]
                    if(morpheme is None or pos in morpheme):
                        tokens_list.append(word)
                        pos_list.append(pos)     
                parse = parse.next
            if tokens_list == []:
                out_table.drop(i,inplace=True)
            else :
                tokens_col_data.append(tokens_list)
                pos_col_data.append(pos_list)
        except:
            out_table.drop(i,inplace=True)
    out_table[token_col_name] = tokens_col_data
    out_table[pos_col_name] = pos_col_data

    return {'out_table': out_table}


def doc_to_vec_train(table, tokens_col, label_col = None, vector_size = 100, window = 5, min_count = 5, workers = 3, epochs = 5):

    out_table = table.copy()
    if label_col is None :
        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(out_table[tokens_col])]
    else :
        documents = [TaggedDocument(doc, [i]) for i, doc in zip(out_table[label_col],out_table[tokens_col])]

    model = Doc2Vec(documents, vector_size = vector_size, window = window, min_count = min_count, workers = workers, epochs = epochs)
    model.train(documents, total_examples=len(documents), epochs=model.epochs)

    vectors = [model.infer_vector(tokens) for tokens in out_table[tokens_col]]


    array_vectors = np.array(vectors)
    for i in range(model.vector_size) :
        col_name = 'vectors_' + str(i)
        out_table[col_name] = array_vectors[:,i]

    return {'out_table': out_table, 'model': model}


def doc_to_vec_infer_vector(table, model, tokens_col):

    out_table = table.copy()
    
    vectors = [model.infer_vector(tokens) for tokens in out_table[tokens_col]]

    array_vectors = np.array(vectors)
    for i in range(model.vector_size) :
        col_name = 'vectors_' + str(i)
        out_table[col_name] = array_vectors[:,i]
    
    return {'out_table': out_table}


def remove_stopwords(table, input_col, stopwords, output_col_name='removed'):
    out_table = table.copy()
    
    def _remove_stopwords(str_list):
        return [_ for _ in str_list if _ not in stopwords]
    
    out_table[output_col_name] = table[input_col].apply(_remove_stopwords)
    
    return {'out_table': out_table}