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
from hashlib import md5

class PeerHandler:
    def __init__(self, new_peer_callback, port=5000, peer_addrs=[]):
        self.connected_peers = {}
        self.connecting_peers = {}
        self.port = port

        self.new_peer_callback = new_peer_callback

        for peer_addr in peers:
            self.add_peer(peer_addr)

        asyncio.runcoroutine_threadsafe(asyncio.start_server, self.__call__, port=self.port)

    def add_peer(self, address):
        peer_id = md5(address.encode("utf-8")).hexdigest()

        if not self.connected_peers[peer_id]:
            reader, writer = asyncio.runcoroutine_threadsafe(asyncio.open_connection(address, self.port))

            peer_addr = writer.get_extra_info("peername")
            print("Connected to new peer: {} - {}".format(peer_addr, peer_id))

            self.connected_peers[peer_id] = {"addr": address, "reader": reader, "writer": writer}

            return peer_id

        else:
            print("Already exists")

    def remove_peer(self, peer_id):
        if not self.connected_peers[peer_id]:
            self.connected_peers[peer_id]["writer"].close()

            del self.connected_peers[peer_id]

        else:
            print("Does not exist")

    async def write_peer(self, peer_id, data):
        if self.connected_peers[peer_id]:
            try:
                self.connected_peers[peer_id]["writer"].write(data)
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    async def read_peer(self, peer_id):
        if self.connected_peers[peer_id]:
            try:
                return self.connected_peers[peer_id]["writer"].read()
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    async def writer_connecting_peer(self, peer_id, data):
        if self.connecting_peers[peer_id]:
            try:
                self.connecting_peers[peer_id]["writer"].write(data)
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    async def read_connecting_peer(self, peer_id):
        if self.connecting_peers[peer_id]:
            try:
                return self.connecting_peers[peer_id]["writer"].read()
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    def __call__(reader, writer):
        peer_addr = writer.get_extra_info("peername")
        peer_id = md5(peer_addr.encode("utf-8")).hexdigest()

        self.connecting_peers[peer_id] = {"addr": peer_addr, "reader": reader, "writer": writer}
        print("New peer connected: {} - {}".format(peer_addr, peer_id))

        self.new_peer_callback(peer_id)
