#!/usr/bin/env python

########################################################################
#
#   Author: Michele Berselli
#       University of Padova
#       berselli.michele@gmail.com
#
#   Objects and functions to work with rest api
########################################################################


########################################################################
#   Libraries
########################################################################
import sys
import requests
import json


########################################################################
#   Global Variables
########################################################################
HEADERS_json = {'accept': 'application/json'}


########################################################################
#   Classes
########################################################################
class Entry(object):
    ''' Class to model a general object, accepts any number of attributes
    as a python dictionary. Attributes are stored as str '''

    def __init__(self, dct):
        for key, val in dct.items():
            self.__dict__[str(key)] = str(val)
        #end for
    #end def __init__

    def header_to_tsv(self):
        ''' Method to return all keys in a tsv format '''
        s, c, l = '', 0, len(self.__dict__)-1
        for key in sorted(self.__dict__):
            s += key + '\t' if c < l else key + '\n'
            c += 1
        #end for
        return s
    #end def header_to_tsv

    def values_to_tsv(self):
        ''' Method to return all attributes in a tsv format '''
        s, c, l = '', 0, len(self.__dict__)-1
        for _, val in sorted(self.__dict__.items()):
            s += val + '\t' if c < l else val + '\n'
            c += 1
        #end for
        return s
    #end def values_to_tsv
#end Entry


########################################################################
#   Functions
########################################################################
def GET_json(url):
    ''' Requests a json from the url and check for errors '''
    r = requests.get(url, headers=HEADERS_json)
    #Check errors
    if r.status_code == 200: #OK
        return r.json(), 0
    else:
        return None, 1
    #end if
#end def GET_json

def dict_structure(dct, expand=False, levels=[0,-1]):
    ''' Return the structure of the keys for a dictionary dct '''
    #expand: allows to expand values that are lists of dictionaries,
    #        returns the structure of first dictionary (OBJECT).
    #levels: allows to specify the range of levels to return [min, max],
    #       [.., -1] removes maximum depth limit.
    s, l, o = [''], 0, 0 #l = level, o = current object
    if len(levels) != 2 or (levels[0] > levels[1] and levels[1] != -1):
        raise ValueError("levels error, provide levels=[min, max]")
    else:
        min, max = levels[0], levels[1]
    #end if
    routine_iter_keys(dct, s, l, o, expand, min, max)
    return s[0]
#end def dict_structure

def routine_iter_keys(dct, s, l, o, expand, min, max):
    '''  '''
    if l <= max or max == -1:
        for key, val in sorted(dct.items()):
            if l >= min:
                s[0] += '\t'*(l-min) + '[%d|%s]'% (l, type(val).__name__.upper()) + str(key) + '\n'
            #end if
            if isinstance(val, dict):
                routine_iter_keys(val, s, l+1, o, expand, min, max)
            elif isinstance(val, list):
                if expand and len(val) > 0 and isinstance(val[0], dict):
                    if (l+1 <= max or max == -1) and l+1 >= min:
                        s[0] += '\t'*(l-min+1) + '*[%d]-OBJECT-*'% (o) + '\n'
                        routine_iter_keys(val[0], s, l+1, o+1, expand, min, max)
                        s[0] += '\t'*(l-min+1) + '*[%d]--------*'% (o) + '\n'
                    else:
                        routine_iter_keys(val[0], s, l+1, o+1, expand, min, max)
                    #end if
                #end if
            #end if
        #end for
    #end if
#end def routine_iter_keys


########################################################################
#   Main
########################################################################
def main(args): # use as args['name']

    pass

# end def main

if __name__ == '__main__':

    main(args)

# end if
