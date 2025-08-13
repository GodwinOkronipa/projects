import hashlib
import datetime

class GodwinCoinBlock:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        # Add a timestamp to the block's data for a more realistic blockchain
        self.timestamp = datetime.datetime.now()

        # Concatenate block data and previous hash to create a unique data string
        self.block_data = "+".join(self.transaction_list) + "-" + str(self.timestamp) + "-" + self.previous_block_hash
        
        # Calculate the hash for the block
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

# Create the first block (genesis block)
t1 = "Godwin sends 2 GC to Rex"
t2 = "Rex sends 4 GC to Opoku"
t3 = "Opoku sends 1 GC to Fiifi"
t4 = "Rex sends 3 GC to Godwyn"

# The genesis block has an empty string for the previous hash
block_one = GodwinCoinBlock(" ", [t1, t2])

# Print the hash of the genesis block
print("Block 1 Hash:", block_one.block_hash)

# Create the second block, which uses the hash of the first block
block_two = GodwinCoinBlock(block_one.block_hash, [t3, t4])

# Print the hash of the second block
print("Block 2 Hash:", block_two.block_hash)

# Create the third block, which uses the hash of the second block
t5 = "Opoku sends 1 GC to Fiifi"
t6 = "Fiifi sends 3 GC to Godwin"

block_three = GodwinCoinBlock(block_two.block_hash, [t5, t6])

# Print the hash of the third block
print("Block 3 Hash:", block_three.block_hash)

# Checking blockchain Integrity
block_list = [block_one, block_two, block_three]

def check_chain_integrity(chain):
    # We loop through the chain, starting from the second block (index 1)
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i-1]

        # We check two things:
        # 1. Does the current block's hash match its own calculated hash?
        # 2. Does the current block's previous_block_hash match the previous block's hash?
        
        # A simple check to recalculate the hash of the current block
        recalculated_hash = hashlib.sha256(current_block.block_data.encode()).hexdigest()

        if recalculated_hash != current_block.block_hash or \
           current_block.previous_block_hash != previous_block.block_hash:
            print(f"Blockchain integrity compromised at block #{i}!")
            return False

    print("Blockchain integrity check passed! The chain is secure.")
    return True

# Testing
print("\n--- Running Integrity Check ---")
check_chain_integrity(block_list)
