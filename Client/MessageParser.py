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
        setning = "Message from Server: \nThe following error has been encountered: ", payload["content"], "\n"
        return ''.join(setning)

    def parse_info(self, payload):
        setning = payload["content"], "\n"
        return ''.join(setning)

    def parse_message(self, payload):
        setning= "Message sent: ", payload["timestamp"], "\nMessage from user ", payload['sender'],":\n", payload["content"],"\n"
        return ''.join(setning)

    def parse_history(self, payload):
        setning= "All previous messages in this chat: \n", payload["content"], "\n"
        return ''.join(setning)
