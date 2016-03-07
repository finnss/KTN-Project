# -*- coding: utf-8 -*-
import datetime
import json
import socketserver

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

# Dictionary
clients = {}
history_list = []

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    username = ""
    timestamp = ""
    is_logged_in = False

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            selftimestamp = str(datetime.datetime.now())
            received_string = self.connection.recv(4096)
            decoded_object = json.loads(received_string)
            request = decoded_object['request']
            content = decoded_object['content']
            if request == 'login':
                self.login(content)
            elif request == 'logout':
                self.logout()
            elif request == 'names':
                self.names()
            elif request == 'help':
                self.help()
            elif request == 'msg':
                self.logout()
            elif request == 'history':


    def login(self, username):
        global clients
        self.username = username
        self.is_logged_in = True
        clients[username] = self
        self.send_respone('server', 'info', 'Login successful!', False)

    def logout(self):
        global clients
        del clients[self.username]
        self.send_respone('server', 'info', 'Logout successful', False)

    def names(self):
        names = []
        for username in clients:
            names.append(username)
        strigToReturn = 'All users in this channel: ', names
        self.send_respone('server', 'info', strigToReturn, False)

    def help(self):
        pass

    def msg(self, message):
        self.send_response(self.username, 'message', message, True)

    def history(self):
        self.send_response('server', 'history', history_list, False)

    def send_respone(self, sender, response, message, send_to_all):

        if response != 'help' and response != 'login' and not self.is_logged_in:
            raw_respone = {
                'timestamp': self.timestamp,
                'sender': 'server',
                'response': 'error',
                'content': 'You need to log in!'
            }
        else:
            raw_respone = {
                'timestamp': self.timestamp,
                'sender': sender,
                'response': response,
                'content': message
            }
        JSON_response = json.dumps(raw_respone)

        if response == 'message':
            global history_list
            history_list.append(JSON_response)
        if send_to_all:
            for username, client in clients:
                client.connection.send(JSON_response)
        else:
            self.connection.send(JSON_response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
