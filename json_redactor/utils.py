import json
import sys

import ijson # type: ignore


def redact_json(file, keys, redactor):
    objects = ijson.items(file, 'item')
    sys.stdout.write("[")
    for i, obj in enumerate(objects):
        redactor(keys, obj)
        if i != 0:
            sys.stdout.write(",")    
        json.dump(obj, sys.stdout)
        sys.stdout.flush()
    sys.stdout.write("]\n")
