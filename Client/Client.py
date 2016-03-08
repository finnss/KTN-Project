# -*- coding: utf-8 -*-
import sys
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
import socket

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
        receiver = MessageReceiver(self, self.connection)
        receiver.start()

        while True:
            command = input("> ")
            if len(command.split(" ")) > 1: # It's a command with content
                command = command.split(" ")

                if command[0] == "login":
                    raw_message = {
                        'request': 'login',
                        'content': command[1]
                    }

                elif command[0] == "msg":
                    messageString = ""
                    for i in command[1:]:
                        messageString += i + ' '
                    messageString = messageString[:-1]
                    raw_message = {
                        'request': 'msg',
                        'content': messageString
                    }
                else:
                    print("Unknown command! Please try again.")
                    continue
            else: # It's a command without content
                if command == 'logout' or command == 'help' or command == 'history' or command == 'names':
                    raw_message = {
                        'request': command,
                        'content': None
                    }
                else:
                    print("Unknown command! Please try again.")
                    continue
            JSON_message = json.dumps(raw_message)
            self.send_payload(JSON_message.encode("utf-8"))

    def disconnect(self):
        print("Bye!")
        self.connection.close()
        sys.exit()

    def receive_message(self, message):
        parser = MessageParser()
        parsed_message = parser.parse(message)
        print(parsed_message,'\n> ',end='')

    def send_payload(self, data):
        self.connection.sendto(data, (self.host, self.server_port))

    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    ip = input("Which IP do you want to connect to?")
    print('Client is running...')
    client = Client(ip, 9998)
