import socket
import select
import json
from datetime import datetime


def turn(pills):
    print(pills)
    #https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/

def receive_udp_non_blocking(host, port):
    # Create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    udp_socket.setblocking(False)  # Set socket to non-blocking mode

    scetuals = []

    while True:
        # Use select to check for readable sockets
        ready_sockets, _, _ = select.select([udp_socket], [], [], 1.0)  # Timeout 1 second
        
        if ready_sockets:
            # If there is data available, receive it
            data, addr = udp_socket.recvfrom(1024)  # Buffer size of 1024 bytes
            print(f"-----Received message: {data} from {addr}")
            data = json.loads(data)
            if type(data[0]) is str:
                date = data.pop(0)
                date = date.replace("T", " ")
                
                target_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M")
                log = {
                    "time":target_datetime,
                    "piller":data
                    }
                scetuals.append(log)
            else:
                turn(data)

            

        else:
            # No data received, can perform other tasks
            now = datetime.now()
            i=0
            for scetual in scetuals:
                if now >= scetual["time"]:
                    scetuals.pop(i)
                    turn(scetual["piller"])
                i += 1
            # You can add more code here to do something else while waiting for UDP packets

# Example usage
receive_udp_non_blocking('', 12000)
