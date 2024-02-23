"""
.. module:: TFIDFViewer

TFIDFViewer
******

:Description: TFIDFViewer

    Receives two paths of files to compare (the paths have to be the ones used when indexing the files)

:Authors:
    bejar

:Version: 

:Date:  05/07/2017
"""
from email.mime import base
from os import walk
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

import argparse

import numpy as np

__author__ = 'bejar'

def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError(f'File [{path}] not found')
    else:
        return lfiles[0].meta.id


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get the frequency of the term in the document, and the number of documents
    # that contain the term
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = []
    for (t, w),(_, df) in zip(file_tv, file_df):
                                             # aplicar formulas:
        tfdi = w/max_freq                    # tfdi es el peso entre la max_freq
        idfi = np.log2((dcount/df))          # idfi es logaritmo base 2 de numero de documentos entre 
                                             # numero de de documentos que contiene el termino
        tfidfw.append((t,tfdi * idfi))       # anadimos el resultado a la lista

    return normalize(tfidfw)

def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    #
    # Program something here
    #
    for i in twv:       
        print(i)


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    #
    # Program something here
    #

    #obtener el modulo 
    sum = 0
    for (_, w) in tw:
        sum += w
    modulo = np.sqrt(sum)           # calculo del modulo del vector

    normal = []
    for (t, w) in tw:
        aux = w/modulo
        normal.append((t, aux))     # calculo de la normal

    return normal


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """
    indice_tw1 = 0
    indice_tw2 = 0
    
    sum = 0
    while indice_tw1 < len(tw1) and indice_tw2 < len(tw2): 

        if tw1[indice_tw1][0] == tw2[indice_tw2][0]:    # el mismo id, computamos 
            
            sum += tw1[indice_tw1][1]*tw2[indice_tw2][1]
            indice_tw1 += 1
            indice_tw2 += 1

        elif tw1[indice_tw1][1] < tw2[indice_tw2][1]:   # avanzar tw1
            indice_tw1 += 1
            
        else:                                           # avanzar tw2
            indice_tw2 += 1

    sum_tw1 = 0
    for (_, w) in tw1:                  # calculamos el modulo del primer vector
        sum_tw1 += np.square(w)
    modulo_tw1 = np.sqrt(sum_tw1)

    sum_tw2 = 0                         # calculamos el modulo del segundo vector
    for (_, w) in tw2:
        sum_tw2 += np.square(w)
    modulo_tw2 = np.sqrt(sum_tw2)


    return sum/(modulo_tw1*modulo_tw2)  # aplicamos la formula

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--files', default=None, required=True, nargs=2, help='Paths of the files to compare')
    parser.add_argument('--print', default=False, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()


    index = args.index
    

    baseball = './20_newsgroups/rec.sport.baseball'            
    baseballNames = next(walk(baseball), (None, None, []))[2]  
    baseballNames.sort()                                       # baseballNames contine todos los nombre de los ficheros 
                                                               # que estan en el path ./20_newsgroups/rec.sport.baseball                 

    hardware = './20_newsgroups/comp.sys.mac.hardware'
    hardwareNames = next(walk(hardware), (None, None, []))[2]  
    hardwareNames.sort()                                       # hardwareNames contine todos los nombre de los ficheros 
                                                               # que estan en el path ./20_newsgroups/comp.sys.mac.hardware

    for baseNames in baseballNames:
        file1 = baseball+'/'+baseNames
        sum = 0;
        for hardNames in hardwareNames:
            file2 = hardware +'/'+hardNames

            client = Elasticsearch(timeout=1000)

            try:

                # Get the files ids
                file1_id = search_file_by_path(client, index, file1)
                file2_id = search_file_by_path(client, index, file2)

                # Compute the TF-IDF vectors
                file1_tw = toTFIDF(client, index, file1_id)
                file2_tw = toTFIDF(client, index, file2_id)

                if args.print:
                    print(f'TFIDF FILE {file1}')
                    print_term_weigth_vector(file1_tw)
                    print ('---------------------')
                    print(f'TFIDF FILE {file2}')
                    print_term_weigth_vector(file2_tw)
                    print ('---------------------')
                cosinus = cosine_similarity(file1_tw, file2_tw)
                sum += cosinus      # acumulamos el valor de cosinus similarity

                #print(f"Similarity = {cosine_similarity(file1_tw, file2_tw):3.5f}")


            except NotFoundError:
                print(f'Index {index} does not exists')
        print(f"{sum/len(hardwareNames):3.5f}")             # hacemos la media
    

