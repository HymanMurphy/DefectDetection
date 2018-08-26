import sys
sys.path.append("..")

import interface.model_interface as mi
import tensorflow as tf


class EnsembleModel:

    def __init__(self):

        self.model_inception = mi.ModelInterface('Inception')
        #self.model_mobilenet = mi.ModelInterface('Mobilenet')

    def predict(self, filename, sess1):

        label1, prob1 = self.model_inception.predict(filename, sess1)
        #label2, prob2 = self.model_mobilenet.predict(filename, sess2)

        #return self.ensemble_predict([label1, prob1], [label2, prob2])
        return self.ensemble_predict([label1, prob1])


    def ensemble_predict(self, pre1, pre3=None):
        # probability larger than 60% is judged as unnormal
        threshold = 0.50
        print(pre1)
        if pre3 == None:
            #if pre1[1][pre1[0].index('normal')] > threshold:
            if pre1[0] == 'normal':
                return False
            else:
                return True
        else:
            if pre1[1][pre1[0].index('normal')] > threshold  and pre3[1][pre3[0].index('normal')] > threshold:
                return False
            else:
                return True
