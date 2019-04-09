# PyOUI

A utils to compress and lookup mac vendor locally.

# How to use

First, download/update ouis.gz. By default, run `make`.

Then you are free to query vendor by `python macs.py {mac}`.

We accept '00:00:00:00:00:00' or '00-00-00-00-00-00', or even '000000000000'. They look same when you comma-blindness or dash-blindness.

Read `macs.py` if you want to use API. I won't explain too much when my code can do better.

# What is base64-ed MAC

Oh. It's not important to user. This is a way I used to compress MAC. All prefix in OUI records are at least 24 bits long. So I cut those prefix, transfer to binary, base64 encoding them, and put them back to where they were. It saves 2 bytes for each MAC, and won't effect search.

# Why it's so slow

Because PyOUI are designed for an embedded system at the beginning. So I mostly focused on how to make database smaller, and how to reduce memory usage. (It's sounds pretty weird, when you are using python and manifesto you want to save memory at the same time) So I restore all MAC prefixes together (yes, so I can save some space from vendor's name), didn't use binary search.

You can try `MacIndex` if you want to run a batch query in python. It will load everything into memory and took 10M memory under 64 bits python3. Then it's much faster than lookup.

# Cool, what can I do

I don't want you donate, I don't want you promise. Please try you best, don't do evil with it.
