import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history

	    # More key:values pairs are needed
        }

    def parse(self, payload):
        payload = json.loads(payload.decode("utf-8")) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print('Response not valid')

    def parse_error(self, payload):
        setning = "Message from Server: \nThe following error has been encountered: " + str(payload["content"]) + "\n"
        return setning

    def parse_info(self, payload):
        setning = str(payload["content"]) + "\n"
        return setning

    def parse_message(self, payload):
        setning= "[" + str(payload["timestamp"]) + "] Message from " + str(payload['sender']) + ":\n" + str(payload["content"]) +"\n"
        return setning

    def parse_history(self, payload):
        setning= "All previous messages in this chat: \n" + str(payload["content"]) + "\n"
        return setning
