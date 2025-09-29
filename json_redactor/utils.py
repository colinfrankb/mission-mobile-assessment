import re

import ijson # type: ignore


def key_matcher(keys):
    def _key_matcher(value):
        return value in keys
    
    return _key_matcher
    

def regex_key_matcher(keys_regex):
    def _key_matcher(value):
        return re.search(keys_regex, value)
    
    return _key_matcher


def mask_redactor(value):
    return "***REDACTED***"


def hash_redactor(value):
    return "hashed"


def redact_json(file, keys, redactor):
    objects = ijson.items(file, 'item')
    for obj in objects:
        for k, v in obj.items():
            if keys(k):
                obj[k] = redactor(v)
        print(obj)
