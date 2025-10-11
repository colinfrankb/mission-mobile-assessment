import json
import sys

import ijson # type: ignore


class JsonRedactor():
    def __init__(self, key_matcher, redactor):
        self.key_matcher = key_matcher
        self.redactor = redactor
    
    def redact(self, file):
        objects = ijson.items(file, 'item')
        sys.stdout.write("[")
        for i, obj in enumerate(objects):
            self.redactor(self.key_matcher, obj)
            if i != 0:
                sys.stdout.write(",")    
            json.dump(obj, sys.stdout)
            sys.stdout.flush()
        sys.stdout.write("]\n")
