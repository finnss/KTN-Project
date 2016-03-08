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
history_list = {}

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
            print("Listening!")
            self.timestamp = datetime.datetime.now().strftime('%H.%M %d %b')
            received_string = self.connection.recv(4096)
            if not received_string:
                print('error!')
                break
            decoded_object = json.loads(received_string.decode("utf-8"))
            request = decoded_object['request']
            content = decoded_object['content']
            print("Found something! request:",request,", content:",content)
            if request == 'login':
                self.login(content)
            elif request == 'logout':
                self.logout()
            elif request == 'names':
                self.names()
            elif request == 'help':
                self.help()
            elif request == 'msg':
                self.msg(content)
            elif request == 'history':
                self.history()

    def login(self, username):
        global clients
        self.username = username
        self.is_logged_in = True
        clients[username] = self
        self.send_response('server', 'info', 'Login successful!', False, False)

    def logout(self):
        if self.username:
            global clients
            del clients[self.username]
        self.send_response('server', 'info', 'Logout successful', False)

    def names(self):
        names = []
        for username in clients:
            names.append(username)
        strigToReturn = 'All users in this channel: ' + str(names)
        self.send_response('server', 'info', strigToReturn, False)

    def help(self):
        help_string = '\nThese are the available commands:'
        help_string += '\nlogin <username> - Logs in to the server'
        help_string += '\nlogout- Logs out'
        help_string += '\nnames - Returns a list of all the connected clients\' names'
        help_string += '\nmsg <message> - Sends the enclosed message to all connected clients'
        help_string += '\nhistory - lists all the messages posted to this server'
        self.send_response('server', 'info', help_string, False, False)

    def msg(self, message):
        if self.username:
            global history_list
            if not self.username in history_list:
                history_list[self.username] = []
            history_list[self.username].append(message)
            self.send_response(self.username, 'message', message, True)
        else:
            self.send_response('server', 'info', 'error inc', False)

    def history(self):
        history_string = ''
        if history_list:
            for username, user_history in history_list.items():
                history_string += 'User ' + username + ' has posted the following messages:\n'
                for post in user_history:
                    history_string += '\t' + post + '\n'
        else:
            history_string = 'No messages in the server\'s history.'
        self.send_response('server', 'history', history_string, False)

    def send_response(self, sender, response, message, send_to_all, must_be_logged_in = True):
        if must_be_logged_in and not self.is_logged_in:
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
        JSON_response = json.dumps(raw_respone).encode("utf-8")

        if send_to_all:
            for username, client in clients.items():
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
    HOST, PORT = '78.91.69.136', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
