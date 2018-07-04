import hashlib

from urllib.parse import urlparse

from time import time

import requests

from entities.block import Block
from entities.transaction import Transaction


class Blockchain(object):

    # current_transactions: [dict]
    # chain: [dict]

    def __init__(self):
        self.current_transactions: [dict] = []
        self.chain: [dict] = []
        self.nodes = set()

        # Create the genesis block
        genesis_block = Block()
        genesis_block.from_value(1, time(), current_transactions=[], proof=100, previous_hash=1)
        self.chain.append(genesis_block.__dict__)
        # self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None) -> Block:
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        self.resolve_conflicts()

        block = Block()
        block.from_value(len(self.chain) + 1, time(), self.current_transactions, proof,
                         previous_hash or self.chain[-1].hash)

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block.__dict__)
        return block

    def total_amount(self, node_id) -> int:

        self.resolve_conflicts()

        current_index = 1
        total_amount = 0

        while current_index < len(self.chain):
            block = Block()
            block.from_dict(self.chain[current_index])

            for transaction in block.transactions:
                if transaction['recipient'] == node_id:
                    total_amount += transaction['amount'];
                elif transaction['sender'] == node_id:
                    total_amount -= transaction['amount']

            current_index += 1

        return total_amount

    def valid_transaction(self, sender, recipient, amount) -> bool:
        total_amount = self.total_amount(sender);
        if amount > total_amount:
            return False
        else:
            return True

    def new_transaction(self, sender, recipient, amount) -> int:
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction.__dict__)

        return self.last_block.index + 1

    @property
    def last_block(self) -> Block:
        # last_block_dict = self.chain[-1]
        last_block = Block()
        last_block.from_dict(self.chain[-1])
        return last_block

    # @staticmethod
    # def hash(block):
    #     """
    #     Creates a SHA-256 hash of a Block
    #     :param block: <dict> Block
    #     :return: <str>
    #     """
    #
    #     # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    #     block_string = json.dumps(block, sort_keys=True).encode()
    #     return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address: str):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: []) -> bool:
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = Block()
        last_block.from_dict(chain[0])
        current_index = 1

        while current_index < len(chain):
            # block_dict = chain[current_index]
            block = Block()
            block.from_dict(chain[current_index])

            print(f'{last_block.__dict__}')
            print(f'{block.__dict__}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block.previous_hash != last_block.hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


