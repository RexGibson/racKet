#!/usr/bin/env python

import socket, asyncore, sys
import simplejson as json

class BufferHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
    def handle_read(self):
        data = self.recv(1024)
        if data:
            events = data.split('#')
            for event in events:
                if event == '':
                    continue
                if event[:4] == 'Exit':
                    sys.exit(0)
                print event

class MockServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            handler = BufferHandler(sock)

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <configfile> [num_events]" % sys.argv[0]
        sys.exit(-1)
    configfile = sys.argv[1]
    config = json.load(open(configfile, 'r'))
    host = socket.gethostname()
    port = config['socket_port']
    server = MockServer(host, port)
    asyncore.loop(1)

if __name__ == '__main__':
    main()
