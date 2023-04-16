import json as JSON
from json import JSONEncoder
import numpy as np

class Custom_Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def open_cache():
    '''
    Reads the cache file 'cache.json' and returns its contents as a dictionary.

    If the cache file does not exist or cannot be read, an empty dictionary is returned.

    Parameters
    ----------
    None

    Returns
    -------
    dictionary: A dictionary containing the contents of the cache file.

    '''
    try:
        cache_file = open('cache.json', 'r')
        cache_contents = cache_file.read()
        cache_dict = JSON.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    '''
    saves the current state of the cache as a dictionary object to a JSON file on disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = JSON.dumps(cache_dict, cls=Custom_Encoder)
    fw = open('cache.json',"w")
    fw.write(dumped_json_cache)
    fw.close()

def if_entry_in_cache(cache_dict, new_entry):
    '''
    Check whether a new entry is already present within a cache dictionary.

    PARAMETERS
    ==============================
    cache_dict : dict
    A dictionary object representing the cache.

    new_entry : dict or list
    An object that needs to be searched for within the cache. It should have
    the same structure as the items in the cache_dict.


    RETURNS
    =============================
    bool
        True if the new entry is found in the cache_dict, False otherwise.


    '''
    if new_entry not in cache_dict.items():
        return False
    return True