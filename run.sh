#/bin/sh

# Clear logs.
> logs.txt

# Start proxy.
mitmproxy -s snap-logger.py

# Clean up our mess.
clear
