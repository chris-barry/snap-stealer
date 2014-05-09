#/bin/sh

# Clear logs.
> logs.txt

# Start proxy.
mitmproxy -s snap-intercepter.py

# Clean up our mess.
# clear
