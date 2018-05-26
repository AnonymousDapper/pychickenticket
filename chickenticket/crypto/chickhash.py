from Cryptodome.Hash import keccak


def chickhash(data: bytes):
    """
    :param data: bytes-like data to be hashed
    :return: Cryptodome.Hash.keccak object
    """
    return keccak.new(data=data, digest_bits=256)