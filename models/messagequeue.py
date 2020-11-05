
class MessageQueue:
    """
    This class provides a basic custom messaging system to interact with the user
    """
    def __init__(self):
        self.messages = []

    def add(self, msg):
        self.messages.append(msg)

    def get(self):
        msg_list = self.messages.copy()
        self.clear()
        return msg_list

    def is_empty(self):
        return (len(self.messages) <= 0)

    def clear(self):
        self.messages.clear()
