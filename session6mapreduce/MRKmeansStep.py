"""
.. module:: MRKmeansDef

MRKmeansDef
*************

:Description: MRKmeansDef

    

:Authors: bejar
    
    
:Version: 

:Created on: 17/07/2017 7:42 

"""

from mrjob.job import MRJob
from mrjob.step import MRStep

__author__ = 'bejar'


class MRKmeansStep(MRJob):
    prototypes = {}

    def jaccard(self, prot, doc):
        """
        Compute here the Jaccard similarity between  a prototype and a document
        prot should be a list of pairs (word, probability)
        doc should be a list of words
        Words must be alphabeticaly ordered

        The result should be always a value in the range [0,1]
        """

        sum = 0
        for i in range(len(prot)):
            sum += prot[i][1]**2  
        sum += len(doc)                 #puesto que 1^2 = 1  

        prod = 0
        i = 0
        j = 0
        while (i < len(prot) and j < len(doc)):
            if (prot[i][0] < doc[j]):
                i += 1
            elif (prot[i][0] > doc[j]):
                j += 1
            else:
                prod += prot[i][1]
                i += 1
                j += 1
        
        return float(prod)/float(sum - prod)


    def configure_args(self):
        """
        Additional configuration flag to get the prototypes files

        :return:
        """
        super(MRKmeansStep, self).configure_args()
        self.add_file_arg('--prot')


    def load_data(self):
        """
        Loads the current cluster prototypes

        :return:
        """
        f = open(self.options.prot, 'r')
        for line in f:
            cluster, words = line.split(':')
            cp = []
            for word in words.split():
                cp.append((word.split('+')[0], float(word.split('+')[1])))
            self.prototypes[cluster] = cp

    def assign_prototype(self, _, line):
        """
        This is the mapper it should compute the closest prototype to a document

        Words should be sorted alphabetically in the prototypes and the documents

        This function has to return at list of pairs (prototype_id, document words)

        You can add also more elements to the value element, for example the document_id
        """

        # Each line is a string doc_id  :   wor1 word2 ... wordn
        doc, words = line.split(':')
        lwords = words.split()      # lista de palabras en words
            
        #
        # Compute map here
        #
        assignedPrototype = next(iter(self.prototypes))                 
        minDistance = 1-self.jaccard(self.prototypes[assignedPrototype], lwords)     # diatancia = (1-similitud)

        for prot in self.prototypes:
            auxDistance = 1-self.jaccard(self.prototypes[prot],lwords)
            if(auxDistance < minDistance):
                minDistance = auxDistance
                assignedPrototype = prot
            
        # Return pair key, value
        yield assignedPrototype, (doc,lwords)




    def aggregate_prototype(self, key, values):
        """
        input is cluster and all the documents it has assigned
        Outputs should be at least a pair (cluster, new prototype)

        It should receive a list with all the words of the documents assigned for a cluster

        The value for each word has to be the frequency of the word divided by the number
        of documents assigned to the cluster

        Words are ordered alphabetically but you will have to use an efficient structure to
        compute the frequency of each word

        :param key:
        :param values:
        :return:
        """


        nextPrototype = dict()      #diccionario de palabra-fracuencia
        nextDocList = []
        docsNum = 0

        for doc in values:      # (direccion_docu, lista_palabras)
            docsNum += 1
            nextDocList.append(doc[0])
            for token in doc[1]:
                if token in nextPrototype:       # si la palabra esta en nextPrototype
                    nextPrototype[token] += 1       #incrementamos la frecuencia
                else:
                    nextPrototype[token] = 1     # si no esta lo inicializamos a 1
        
        rProt = []
        for token in nextPrototype:      #normalizar
            rProt.append((token,nextPrototype[token]/float(docsNum)))

        sortedDocList = sorted(nextDocList)
        sortedProt = sorted(rProt, key=lambda x: x[0])
    
        yield key, (sortedDocList, sortedProt)


    def steps(self):
        return [MRStep(mapper_init=self.load_data, mapper=self.assign_prototype,
                       reducer=self.aggregate_prototype)
            ]


if __name__ == '__main__':
    MRKmeansStep.run()