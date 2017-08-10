'''
Created on 21.09.2016

@author: sebastian
'''

from datetime import date

def _add_month(datum):
    if datum.month < 12:
        datum = date(day=datum.day, month=(datum.month + 1), year=datum.year)
    else:
        datum = date(day=datum.day, month=1, year=datum.year + 1)
    return datum


class FrequencsFunctions:
    '''
    the frequenzfunktionen
    '''
    def __init__(self):
        funktionen = {("monatlich", _add_month)}
        self.forwardmap = {}
        self.backwardmap = {}
        for (name, funktion) in funktionen:
            self.forwardmap[name] = funktion
            self.backwardmap[funktion] = name


    def get_frequency_function_by_name(self):
        '''
        collects frequency-function out of console
        '''
        ergebnis = ""
        while ergebnis == "":
            print("Bitte geben Sie einen Rhythmus ein:")
            print("Mögliche Eingaben sind: ", self.forwardmap.keys())
            eingabe = input()
            for moeglicher_treffer in self.forwardmap.keys():
                if moeglicher_treffer == eingabe:
                    ergebnis = moeglicher_treffer
        return ergebnis

    def get_function_for_name(self, name):
        '''
        returns frequency-function for its name
        '''
        return self.forwardmap[name]
