import sys
import base64

# Decryption
def encode(key, string):
  encoded_chars = []
  for i in xrange(len(string)):
    key_c = key[ i % len(key)]
    encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
    encoded_chars.append(encoded_c)
  encoded_string = "".join(encoded_chars)
  return encoded_string
  
# Get command line arguments
try:
  key = sys.argv[1]
  decrypted_string = sys.argv[2]
except IndexError, e:
  print "Incorrect Arguments: Expects key and encrypted_string"
  sys.exit(1)
  
encrypted_string = encode(key,decrypted_string)

print "decrypted_string=" + decrypted_string + " ;key=" + key + " ;encrypted_string=" + encrypted_string
