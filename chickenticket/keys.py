# MIT License

# Copyright (c) 2018 ChickenTicket

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import urandom
import ecdsa
from ecdsa.util import PRNG
from base58 import b58encode
from Cryptodome.Hash import keccak
from utils.logger import get_logger
from crypto.chickhash import chickhash

logger = get_logger()

MAGIC_BYTE = b'\x15'


def eckeys_create(secexp=None):
    """
    :param secexp:int: Secret exponent for entropy
    :return:
    """
    if secexp is None:
        secexp = int(''.join(str(o) for o in urandom(16)))

    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=PRNG(secexp), hashfunc=chickhash)
    private_key = signing_key

    verifying_key = signing_key.get_verifying_key()
    public_key = verifying_key

    return public_key, private_key


def address_create(public_key):
    """
    :param public_key:ecdsa.keys.VerifyingKey:Public key
    :return:str: A ChickenTicket address
    """
    pub_hash = chickhash(public_key)

    # create the address w/o the byte checksum and the prefix
    address_hash = pub_hash.hexdigest()[38:]

    # create the checksum of the address by hashing the address again,
    # encoding the result, and taking the last 4 of the encoding
    checksum = b58encode(address_hash.encode('ascii') + MAGIC_BYTE)[:4].upper()
    address = '0x' + address_hash + checksum.decode()
    logger.info('Generated address. Here it is; %s' % address)
    return address


def checksum_encode(address_str):
    out = ''
    addr = address_str.lower().replace('0x', '')
    addr_hash = keccak.new(data=addr.encode() + MAGIC_BYTE, digest_bits=256).hexdigest()
    for i, c in enumerate(addr):
        if int(addr_hash[i], 16) >= 8:
            out += c.upper()
        else:
            out += c

    return '0x' + out


def eth_address_create(public_key):
    address_str = keccak.new(data=public_key, digest_bits=256).hexdigest()[24:]
    return checksum_encode(address_str)

if __name__ == '__main__':
    pub_key, priv_key = eckeys_create()
    pub = pub_key.to_string().hex()

    print("Private key:", priv_key.to_string().hex())
    print("Public key: ", pub)
    print("Address:    ", eth_address_create(pub.encode()))
