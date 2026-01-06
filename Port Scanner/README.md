# Port Scanner

## This project is a simple port scanner written in Python. It scans a range of TCP ports with a target host to determine which ports are open and labels common services.

## How it Works
* Creates TCP socket for each port in given range
* Attempts to connect to target host on each port
* Uses multithreaded ports to scan multiple ports
* Prints open ports and labels common services

## Concepts
* Multithreaded ports using import threading
* Network ports and common services
* Input validation
* Exception handling
* Sockets

## Requirements
* Python 3.9+
