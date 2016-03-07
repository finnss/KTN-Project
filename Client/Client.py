# -*- coding: utf-8 -*-
import socket
from .MessageReceiver import MessageReceiver
from .MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port

        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        reciever = MessageReceiver(self, self.connection)
        reciever.run()
        while True:
            command = input("> ")
            if len(command.split(" ")) > 1: # It's a command with content

                if command[0] == "login":
                    raw_message = {
                        'request': 'login',
                        'content': command[1]
                    }

                elif command[0] == "msg":
                    messageString = ""
                    for i in command[1:]:
                        messageString += i
                    raw_message = {
                        'request': 'msg',
                        'content': messageString
                    }
            else: # It's a command without content
                raw_message = {
                    'request': command[0],
                    'content': None
                }
            JSON_message = json.dumps(raw_message)
            self.send_payload(JSON_message)
        
    def disconnect(self):
        print("Bye!")
        self.connection.close()

    def receive_message(self, message):
        parser = MessageParser()
        parsed_message = parser.parse(message)
        print(parsed_message)

    def send_payload(self, data):
        self.connection.sendto(data, self.host, self.server_port)
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
