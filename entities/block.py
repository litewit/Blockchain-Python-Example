import hashlib
import json


class Block(object):

    # index: int
    # timestamp: float
    # transactions: [Transaction]
    # proof: int
    # previous_hash: str
    # hash: str

    def __init__(self):
        """
        Create a new Empty Block object
        """
        self.index: int = 0
        self.timestamp: float = 0.0
        self.transactions: list = []
        self.proof: int = 0
        self.previous_hash: str = ""
        self.hash: str = ""

    def from_value(self, index: int, time: float, current_transactions: [], proof: int, previous_hash: str=None):
        """
        // Assign values
        :param index:
        :param time:
        :param current_transactions:
        :param proof:
        :param previous_hash:
        :return:
        """
        self.index = index
        self.timestamp = time
        self.transactions = current_transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        # self.previous_hash = previous_hash or self.hash_block(chain[-1])

    def from_dict(self, obj_dict: dict):
        self.index = int(obj_dict["index"])
        self.timestamp = float(obj_dict["timestamp"])
        self.transactions = list(obj_dict["transactions"])
        self.proof = int(obj_dict["proof"])
        self.previous_hash = str(obj_dict["previous_hash"])
        self.hash = str(obj_dict["hash"])

    def from_json(self, json_string: str):
        obj_dict = json.load(json_string)
        self.from_dict(obj_dict)

    def hash_block(self):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()