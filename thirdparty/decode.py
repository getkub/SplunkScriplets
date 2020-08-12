import sys
import base64

# Decryption
def decode(key, string):
  decoded_chars = []
  string = base64.urlsafe_b64decode(string)
  for i in xrange(len(string)):
    key_c = key[ i % len(key)]
    encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
    decoded_chars.append(encoded_c)
  decoded_string = "".join(decoded_chars)
  return decoded_string
  
# Get command line arguments
try:
  key = sys.argv[1]
  epasswd = sys.argv[2]
except IndexError, e:
  print "Incorrect Arguments: Expects key and encrypted_string"
  sys.exit(1)
  
decrypted_string = decode(key,epasswd)

print "encrypted_string=" + epasswd + " ;key=" + key + " ;decrypted_string=" + decrypted_string
