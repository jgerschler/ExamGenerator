import simplecrypt
from binascii import hexlify


test = 'bbbbbbbbbbcdabcdabcdabcdabcdab'


cipher_text = hexlify(simplecrypt.encrypt('ChangeThisKeyHere!', test))

print(cipher_text)
