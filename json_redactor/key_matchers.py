import re


def exact_key_matcher(keys):
    def _key_matcher(value):
        return value in keys
    
    return _key_matcher
    

def regex_key_matcher(keys_regex):
    def _key_matcher(value):
        return re.search(keys_regex, value)
    
    return _key_matcher