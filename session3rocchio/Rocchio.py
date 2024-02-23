
import math
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch.client import CatClient
import argparse
import operator
import numpy as np

def normalize(d):
   
    s = sum(d.values())     #suma valor vector
    r = np.sqrt(s)      #raiz cuadrada
    norm = {t: d.get(t, 0)/r for t in set(d)}       #dividir cada elemento por la raiz cuadada
    return norm



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

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

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
    tfidfw = {}
    for (t, w),(_, df) in zip(file_tv, file_df):
                                               # aplicar formulas:
        tfdi = w/max_freq                      # tfdi es el peso entre la max_freq
        idfi = np.log2((dcount/df))            # idfi es logaritmo base 2 de numero de documentos entre 
                                               # numero de de documentos que contiene el termino
        tfidfw[t] = (tfdi * idfi) # añadimos el resultado a la lista normalizandolo respecto al tamaño del documento
    return normalize(tfidfw)

if __name__ == '__main__':
    #Parsear la entrada
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)
    nhits = args.nhits


    nrounds = 5
    k = args.nhits
    alpha = 1
    beta = 0
    R = 6

    datos = []
    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            for i in range(0,nrounds):
                #Obtener la query
                q = Q('query_string',query=query[0])
                for i in range(1, len(query)):
                    q |= Q('query_string',query=query[i])

                s = s.query(q)
                #print(query)
                response = s[0:nhits].execute()
                # computar palabra-peso

                palabra_peso = {}
                for q in query:
                    if '^' in q:
                        aux = q.split('^')
                        palabra_peso[aux[0]] = float(aux[1])
                    else:
                        aux = q 
                        palabra_peso[aux[0]] = 1.0
                    
                #print(palabra_peso);
                # Calculo Rocchio Rule
                # Calculo del TFIDF de cada documento
                sumDocs = {}
                for r in response:
                    file_tw = toTFIDF(client, index, r.meta.id) #computo tf-idf de cada documento
                    sumDocs = {t: sumDocs.get(t,0) + file_tw.get(t,0) for t in set(file_tw) | set(sumDocs)} #suma de valores de los docs

                sumDocs = {t: beta*sumDocs.get(t,0)/nhits for t in set(sumDocs)} #beta * vector de documents / K
                oldQuery = {t: alpha*palabra_peso.get(t,0) for t in set(palabra_peso)} #alpha * query
                newQuery = {t: sumDocs.get(t,0) + oldQuery.get(t,0) for t in set(oldQuery)|set(sumDocs)} #newquery = sumDocs + oldquery

                #
                newQuery = sorted(newQuery.items(), key=operator.itemgetter(1), reverse=True)
                newQuery = newQuery[:R]
                # Cálculo token-peso de la query
                query = []
                for (term, value) in newQuery:
                    query.append(term + '^' + str(value))

                
                #print(query)
                # imprimir resultados
                #response = s[0:nhits].execute()
                
                for r in response:  # only returns a specific number of results
                    datos.append(r.meta.score)
                    print(f'ID= {r.meta.id} SCORE={r.meta.score}')
                    print(f'PATH= {r.path}')
                    print(f'TEXT: {r.text[:50]}')
                    print('-----------------------------------------------------------------')
                print (f"{response.hits.total['value']} Documents")
            

        else:
            print('No query parameters passed')

        print (f"{response.hits.total['value']} Documents")
        print(query)
        print(datos)
    except NotFoundError:
        print(f'Index {index} does not exists')





