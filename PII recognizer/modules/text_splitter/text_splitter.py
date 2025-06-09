from abc import ABCMeta, abstractmethod

class Splitter(metaclass=ABCMeta):
    """
    Abstract base class for splitting raw text into segments.  
    Input: raw text  
    Output: segmented text
    """
    def __init__(self):
        self.texts = []

    @abstractmethod
    def split(self, raw_text) -> list:
        pass

class Reddit_Splitter(Splitter):
    """
    A concrete class inheriting from Splitter, designed to split Reddit conversations.
    """
    def __init__(self):
        super().__init__()

    def split(self, raw_text) -> list:
        conversation = ""
        for line in raw_text.split('\n'):
            # new conversation
            if line == '' or line == "[deleted]":
                continue
            elif line.startswith('Conversation ID'):
                self.texts.append(conversation)
                conversation = ""
            else:
                conversation += line + ' '
        return self.texts

class Wikipeople_Splitter(Splitter):
    """
    each line is a new record
    """
    def __init__(self):
        super().__init__()

    def split(self, raw_text) -> list:
        for line in raw_text.split('\n'):
            self.texts.append(line)
        return self.texts