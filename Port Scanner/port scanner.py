import threading  # Allows us to run multiple port checks at the same time
import socket     # Provides network tools to connect to ports

# Dictionary of common services for labeling open ports
common_services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP"
}

# Function to scan a single port
def scan_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    s.settimeout(0.5)  # Wait maximum 0.5 seconds before giving up on a port
    try:
        s.connect((host, port))  # Try to connect to the host on this port
        # If the port is open, print it
        if port in common_services:
            print(f"[+] Port {port} ({common_services[port]}) is OPEN")
        else:
            print(f"[+] Port {port} is OPEN")
    except:
        pass  # If connection fails (port closed), do nothing
    finally:
        s.close()  # Close the socket whether open or closed

# Function to scan a range of ports
def scan_ports(host, start_port, end_port):
    threads = []  # List to store threads
    # Loop over the range of ports
    for port in range(start_port, end_port + 1):
        # Create a new thread for each port
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)  # Add the thread to the list
        t.start()          # Start the thread

    # Wait for all threads to finish before ending the scan
    for t in threads:
        t.join()

# Main program execution
if __name__ == "__main__":
    print("=== Simple Port Scanner ===")
    # Ask user for the target host (IP or hostname)
    target = input("Enter target host (IP or hostname): ")
    # Ask user for start and end port numbers
    start_port = int(input("Enter start port (1-65535): "))
    end_port = int(input("Enter end port (1-65535): "))

    # Validate that start_port <= end_port
    if start_port > end_port:
        print("Error: Start port must be less than or equal to end port.")
    else:
        print(f"Scanning {target} from port {start_port} to {end_port}...")
        scan_ports(target, start_port, end_port)  # Call the scanning function
        print("Scan complete!")  # Finished scanning

