"""Shopping-cart persistence."""

from __future__ import annotations

import pickle


def load_cart(blob: bytes):
    # Restore a saved cart from its serialized form.
    return pickle.loads(blob)
