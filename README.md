# Knetcat

Simple Netcat in Python

(works on Linux and MacOS)

# Usage:

Server mode usage: python knetcat.py -l "ip address" "port"

Client mode usage: python knetcat.py "ip address" "port"


File on STDIN server: cat filename | python knetcat.py -l "ip address" "port"

File on STDIN server: python knetcat.py -l "ip address" "port" < filename

File on STDIN client: cat filename | python knetcat.py "ip address" "port"

File on STDIN client: python knetcat.py "ip address" "port" < filename
