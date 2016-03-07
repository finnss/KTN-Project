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
        payload = json.loads(payload) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print('Response not valid')

    def parse_error(self, payload):
        return "Message from Server:  The following error has been encountered:  ", payload["content"]

    def parse_info(self, payload):
        return payload["content"]

    def parse_message(self, payload):
        return ("Message sent:", payload["timestamp"], " Message from user ", payload['sender'], ":", payload["content"])


    def parse_history(self, payload):
        return "All messages in this chat: ", payload["content"]
