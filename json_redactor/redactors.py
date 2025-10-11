import hashlib
from concurrent.futures import ThreadPoolExecutor


def mask_redactor(keys, obj):
    for k, v in obj.items():
        if keys(k):
            obj[k] = "***REDACTED***"


def hash_redactor(keys, obj):
    def hash_value(key):
        obj[key] = hashlib.sha256(obj[key].encode()).hexdigest()

    matched_keys = [k for k, v in obj.items() if keys(k)]
    with ThreadPoolExecutor() as executor:
        executor.map(hash_value, matched_keys)