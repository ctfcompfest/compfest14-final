

from pwn import *

p = process('./asdf')

# p.sendline("asdf")
p.sendline("ラウトは難しいです")

p.interactive()