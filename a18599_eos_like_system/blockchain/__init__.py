import hashlib
from blockchain.block import Block
from blockchain.transaction import Transaction

from termcolor import colored, cprint
import time


class Blockchain:

    def __init__(self):
        self.__current_transactions = []
        self.__chain = []
        # Create genesis block
        self.create_genesis()

    def create_genesis(self):

        genesis_block = Block(0, self.__current_transactions, 0, '00')
        self.__chain.append(genesis_block)

    def add_block(self, block):

        if self.validate_block(block, self.last_block):
            self.__chain.append(block)

            # Remove transactions from the list
            self.__current_transactions = []

            return True

        return False

    def create_transaction(self, sender, recipient, amount):

        transaction = Transaction(sender, recipient, amount)
        text = colored(
            "----- Creates a new transaction to go into the next block------",
            "red",
            attrs=["reverse", "blink"],
        )
        print(text)
        if transaction.validate():
            self.__current_transactions.append(transaction)

            return transaction, True

        return None, False

    def mine(self, reward_address):

        last_block = self.last_block
        index = last_block.index + 1
        previous_hash = last_block.hash

        # Let's start with the heavy duty, generating the proof of work
        nonce = self.generate_proof_of_work(last_block)

        # In the next step we will create a new transaction to reward the miner
        # In this particular case, the miner will receive coins that are just "created", so there is no sender
        self.create_transaction(
            sender="0",
            recipient=reward_address,
            amount=1,
        )

        # Add the block to the new chain
        block = Block(index, self.__current_transactions, nonce, previous_hash)

        if self.add_block(block):
            return block

        return None

    @staticmethod
    def validate_proof_of_work(last_nonce, last_hash, nonce):

        sha = hashlib.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())

        print('validate_proof_of_work hash is ->', sha.hexdigest()[:4])
        time.sleep(0.00001)
        return sha.hexdigest()[:4] == '0000'

    def generate_proof_of_work(self, block):

        last_nonce = block.nonce
        last_hash = block.hash

        nonce = 0
        while not self.validate_proof_of_work(last_nonce, last_hash, nonce):
            nonce += 1

        return nonce

    def validate_block(self, current_block, previous_block):
        print('validate_block')
        if current_block.index != previous_block.index + 1:
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

        if current_block.hash != current_block.hash_block():
            return False

        if not self.validate_proof_of_work(previous_block.nonce, previous_block.hash, current_block.nonce):
            return False

        return True

    def validate_chain(self, chain_to_validate):

        if chain_to_validate[0].hash_block() != self.__chain[0].hash_block():
            return False

        # Then we compare each block with its previous one
        for x in range(1, len(chain_to_validate)):
            if not self.validate_block(chain_to_validate[x], chain_to_validate[x - 1]):
                return False

        return True

    def replace_chain(self, new_chain):

        if len(new_chain) <= len(self.__chain):
            return False

        # Validate the new chain
        if not self.validate_chain(new_chain):
            return False

        new_blocks = new_chain[len(self.__chain):]
        for block in new_blocks:
            self.add_block(block)

    @property
    def last_block(self):
        return self.__chain[-1]

    @property
    def last_transaction(self):
        return self.__current_transactions[-1]

    @property
    def pending_transactions(self):
        return self.__current_transactions

    @property
    def full_chain(self):
        return self.__chain
