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

__all__ = ["Ledger", "Wallet", "DB"]

from utils.logger import get_logger

from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = get_logger(level=0) # NOTSET: all messages

Base = declarative_base()

class Ledger(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    height = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    address = Column(String(length=64), nullable=False)
    recipient = Column(String(length=64), nullable=False)
    amount = Column(Integer, nullable=False)
    signature = Column(String, nullable=False)
    public_key = Column(String(length=88), nullable=False)
    block_hash = Column(String, nullable=False, unique=True)
    fee = Column(Integer, nullable=False)
    reward = Column(Integer, nullable=False)
    openfield = Column(String, nullable=False)

    def __repr__(self):
        return "<Transaction(id={0.id}, height={0.height}, timestamp={0.timestamp}, address='{0.address}', recipient='{0.recipient}', amount={0.amount}, signature='{0.signature}', public_key='{0.public_key}', block_hash='{0.block_hash}', fee={0.fee}, reward={0.reward}, openfield='{0.openfield}')>".format(self)

class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(length=64), nullable=False, unique=True)
    public_key = Column(String(length=88), nullable=False, unique=True)
    private_key = Column(String(length=64), nullable=False, unique=True)

    def __repr__(self):
        return "<Wallet(id={0.id}, address='{0.address}', public_key='{0.public_key}', private_key='{0.private_key}')>".format(self)

# adapter class
class DB:
    def __init__(self, *args, **kwargs):
        db_name = kwargs.get("db_name", "pychickenticket")
        self.engine = create_engine("sqlite:///{}.db".format(db_name))
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        logger.debug("Created database engine")

    @contextmanager # allows to cleanly open and close sessions, automatically rolling back any errors
    def get_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.critical("{0.name}: {0!s}".format(e))
            session.rollback()
        finally:
            session.close()

# To use DB class elsewhere:
#
# from db import DB
#
# database = DB()
# with DB.get_session() as session:
#   session.query/insert...