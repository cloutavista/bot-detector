### This script will be responsible for building a model, optionally leveraging a training set ###

from abc import ABC


class Model(ABC):

    def train(self):
        return NotImplemented

    def predict(self, profile):
        return NotImplemented