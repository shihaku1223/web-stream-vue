#!/usr/bin/env python3

import sys
import websockets
import asyncio
import argparse
import signal

from webrtc_server import WebRTCServer

is_running = True
server = None

def handler(stop):
    stop.set_result(None)

def start(server):
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM,
            handler, stop)
    loop.add_signal_handler(signal.SIGINT,
            handler, stop)

    print('Starting server', options)
    server.loop.run_until_complete(server.serve(stop))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', default='')
    parser.add_argument('--port', default=8443)

    options = parser.parse_args()

    loop = asyncio.get_event_loop()
    server = WebRTCServer(loop, options)

    start(server)
    print('server closed')
