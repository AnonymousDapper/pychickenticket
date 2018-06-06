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

# QaD peer management system

import asyncio

class PeerHandler:
    def __init__(self, port=5000, peers={}):
        self.peers = {}
        self.port = port

        for peer in peers:
            self.add_peer(peer[0], peer[1], peer[2])

        asyncio.runcoroutine_threadsafe(self.start_server)

    def add_peer(self, address, port, nickname):
        if not self.peers[nickname]:
            reader, writer = asyncio.runcoroutine_threadsafe(asyncio.open_connection(address, port))

            self.peers[nickname] = {"addr": address, "port": port, "reader": reader, "writer": writer}

        else:
            print("Already exists")

    def remove_peer(self, nickname):
        if not self.peers[nickname]:
            self.peers[nickname]["writer"].close()

            del self.peers[nickname]

        else:
            print("Does not exist")

    async def write_peer(self, nickname, data):
        if self.peers[nickname]:
            try:
                self.peers[nickname]["writer"].write(data)
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    async def read_peer(self, nickname):
        if self.peers[nickname]:
            try:
                return self.peers[nickname]["writer"].read()
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    def __call__()