# This is a simple demo of how to calculate and verify bitcoin hash algorithm
import hashlib

def result_hash(attempt_hex):
   attempt_bin = attempt_hex.decode('hex')
   attempt_hash = hashlib.sha256(hashlib.sha256(attempt_bin).digest()).digest()
   hash_hex = attempt_hash.encode('hex_codec')
   return hash_hex[::-1]

def zero_padded_hex(int_val, num_zeros=8):
   return hex(int_val)[2:].zfill(num_zeros)

def is_correct(attempt_hash, num_zeros=2):
   return attempt_hash[0:num_zeros] == '0'*num_zeros

if __name__ == "__main__":
   previous_block = "deadbeef" # This is hex
   num_zeros = 3
   attempts = 10000

   for nonce in xrange(attempts):
      nonce_hex = zero_padded_hex(nonce)
      next_block_attempt = previous_block + nonce_hex
      block_hash = result_hash(next_block_attempt)
      print "NONCE = %d, HASH = %s" % (nonce, block_hash)

      if is_correct(block_hash, num_zeros):
         print "(Nonce = %d): FOUND SOLUTION: %s" % (nonce, block_hash)
         break

