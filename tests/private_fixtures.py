"""Absence-only guards for private replay inputs; present evidence must authenticate."""
import hashlib
import unittest


def require_private_samples(directory, samples):
    missing = []
    for sample in samples:
        path = directory / sample['file']
        if not path.exists():
            missing.append(sample['file'])
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != sample['sha256'] or len(data) != sample['size']:
            raise AssertionError('private replay integrity mismatch: ' + str(path))
    if missing:
        raise unittest.SkipTest('private replay fixtures unavailable: ' + ', '.join(missing))
