
class Transaction(object):

    # sender: str
    # recipient: str
    # amount: int

    def __init__(self, sender: str, recipient: str, amount: int):
        """
        Create a new object of Transaction
        :param sender: str
        :param recipient: str
        :param amount: int
        """
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: int = amount
