impot hashlib

class GodwinCoinBlock:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = '+'.join(transation_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        
# Create the first block (genesis block)
t1 = "Godwin sends 2 NC to Rex"
t2 = "Rex sends 4 NC to Opoku"
t3 = "Opoku sends 1 NC to Fiifi"
t4 = "Rex sends 3 NC to Godwyn"

# The genesis block has an empty string for the previous hash
block_one = GodwinCoinBlock(" ", [t1, t2])

# Print the hash of the genesis block
print(block_one.block_hash)

# Create the second block, which uses the hash of the first block
block_two = GodwinCoinBlock(block_one.block_hash, [t3, t4])

# Print the hash of the second block
print(block_two.block_hash)

# Create the third block, which uses the hash of the second block
t5 = "Opoku sends 1 NC to Fiifi"
t6 = "Fiifi sends 3 NC to Godwyn"

block_three = NeuralCoinBlock(block_two.block_hash, [t5, t6])

# Print the hash of the third block
print(block_three.block_hash)
