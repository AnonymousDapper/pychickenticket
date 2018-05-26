class InvalidTransaction(Exception):
    pass


class UnsignedTransaction(InvalidTransaction):
    pass


class InsufficiantBalance(InvalidTransaction):
    pass
