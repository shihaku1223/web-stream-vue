import websockets
import asyncio
import uuid
from enum import Enum

class Peer:
    def __init__(self, client_id):
        self.session = None
        self.remote_peer = None
        self.client_id = client_id

    def __eq__(self, other):
        return self.client_id == other.client_id

class PeerSession:
    def __init__(self, peer_x: Peer, peer_y: Peer):
        self.peer_x = peer_x
        self.peer_y = peer_y
        self.peer_x.remote_peer = peer_y
        self.peer_y.remote_peer = peer_x

    def remove_peer(self, peer):
        if self.peer_x == peer:
            self.peer_x = None
        if self.peer_y == peer:
            self.peer_y = None


class ClientStatus(Enum):
    AVAILABLE = 1
    BUSY = 2

class WebRTCClient(Peer):

    HELLO_TOKEN = 'HELLO'

    WAIT_FOR_TIMEOUT = 10

    def __init__(self, websocket, client_id):
        super().__init__(client_id)
        self.websocket = websocket

        self.status = ClientStatus.AVAILABLE

    def setStatus(self, status: ClientStatus):
        self.status = status

    async def send_message(self, message):
        await self.websocket.send(message)

    async def receive_message(self):
        message = None
        while message is None:
            try:
                message = await asyncio.wait_for(
                        self.websocket.recv(),
                        timeout=WebRTCClient.WAIT_FOR_TIMEOUT)
            except (asyncio.TimeoutError):
                await self.websocket.ping()

        return message

    @staticmethod
    async def create_client(websocket):
        client_id = None
        try:
            client_id = await WebRTCClient.hello(websocket)
        except websockets.ConnectionClosedError:
            return None

        if client_id is not None:
            return WebRTCClient(websocket, client_id)

        raise Exception('Invalid client id')
        
    @staticmethod
    async def hello(websocket):
        remote_address = websocket.remote_address
        message = await websocket.recv()
        hello, client_id = message.split(maxsplit=1)

        if hello != WebRTCClient.HELLO_TOKEN:
            await websocket.close()
            raise Exception('Invalid hello.')
        try:
            client_uuid = uuid.UUID(client_id)
        except Exception:
            await websocket.close()
            raise Exception('Invalid client id.')

        await websocket.send(WebRTCClient.HELLO_TOKEN)

        return str(client_uuid)

class WebRTCServer:

    SESSION_TOKEN = 'SESSION'

    def __init__(self, loop, options):
        self.loop = loop

        self.addr = options.addr
        self.port = options.port

        self.server = None

        self.sessions = dict()

        self.clients = dict()

        self.command_handler = {
            WebRTCServer.SESSION_TOKEN: self.session_command_handler,
        }

    def create_session(self, peer_x, peer_y):
        if peer_x.session is not None or peer_y.session is not None:
            raise Exception('Client is not available.')

        session = PeerSession(peer_x, peer_y)
        peer_x.session = session
        peer_y.session = session

        return session

    async def session_command_handler(self, client, data):
        target_id = None
        try:
            target_id = str(uuid.UUID(data))
        except ValueError as e:
            print('Invalid target id {}'.format(data))
            return

        if target_id not in self.clients:
            print('Specific target id not found.')
            return

        target_client = self.get_client(target_id)
        if target_client.status != ClientStatus.AVAILABLE:
            print('Specific target is busy.')

        session = self.create_session(client, target_client)

        client.setStatus(ClientStatus.BUSY)
        target_client.setStatus(ClientStatus.BUSY)

        self.sessions[client.client_id] = session
        self.sessions[target_client.client_id] = session

        await client.websocket.send('SESSION_OK')

    def get_client(self, uuid):
        return self.clients[uuid]

    def parse_command(self, message):
        if message.startswith(WebRTCServer.SESSION_TOKEN):
            token, data = message.split(maxsplit=1)
            return WebRTCServer.SESSION_TOKEN, data
        return None

    async def handle_busy_client(self, client, message):
        remote_client = client.remote_peer
        await remote_client.send_message(message)

    async def handle_message(self, client, message):
        command, data = self.parse_command(message)
        await self.command_handler[command](client, data)

    async def client_handler(self, client):
        while True:
            message = await client.receive_message()
            if client.status == ClientStatus.BUSY:
                await self.handle_busy_client(client, message)
                continue
            try:
                await self.handle_message(client, message)
            except Exception as e:
                print(e)

    async def remove_client(self, client):
        if client.client_id in self.clients:
            del self.clients[client.client_id]
            await client.websocket.close()

        if client.client_id in self.sessions:
            self.sessions[client.client_id].remove_peer(client)
            del self.sessions[client.client_id]

    async def serve(self, stop):
        async def handler(websocket, path):
            remote_address = websocket.remote_address
            print('Connection from {}'.format(remote_address))

            try:
                client = await WebRTCClient.create_client(websocket)
            except:
                print('Create client error.')
                return

            if client is None:
                await websocket.close(code=1002)
                print('Connection from {} closed'.format(remote_address))
                return

            self.clients[client.client_id] = client

            try:
                await self.client_handler(client)
            except websockets.ConnectionClosed:
                print('Connection {} closed'.format(client.client_id))
            finally:
                await self.remove_client(client)

        self.server = websockets.serve(handler,
                self.addr, self.port)
        async with self.server:
            await stop
