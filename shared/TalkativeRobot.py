class TalkativeRobot:
    """
    A class to represent a robot with say_hello() and say_goodbye() methods.
    Should not be implemented directly. Instead, should be inherited by another class.
    """
    def __init__(self, name):
        self.name = name
    
    def say_hello(self):
        raise NotImplementedError
    
    def say_goodbye(self):
        raise NotImplementedError