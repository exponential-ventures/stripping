import pickle

import numpy as np


def to_bytes(attribute) -> bytes:
    if isinstance(attribute, np.ndarray):
        result = attribute.tobytes()
    else:
        result = pickle.dumps(attribute)

    if not isinstance(result, bytes):
        raise TypeError(f"Unable to convert tye: '{type(attribute)} to bytes.'")

    return result
