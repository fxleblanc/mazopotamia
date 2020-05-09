from pwn import *

connection = remote('challenges2.france-cybersecurity-challenge.fr', 6002)

content = connection.recvuntil(b'Press a key when you are ready...')

connection.send(b'\n')

content = connection.recvuntil(b'>>>')

print(content)
