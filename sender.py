import time, socket, sys, pickle

soc = socket.socket()
host = '127.0.0.1'
port = 1122
soc.bind((host, port))

soc.listen(1)
conn, addr = soc.accept()

while True:
    message = input(str("enter message :"))
    #message = 'Hey Buddy , How do you do ?'
    window_ln = len(message)
    conn.send(message.encode())
    print(message.encode())
    messagelength = str(len(message))
    conn.send(messagelength.encode())

    packet_to_send_to_receiver = 0
    window_size_c = input("Do you want to define manuall window size ? Y/N ")
    if window_size_c.lower() == "y":
        window_size = int(input("enter size of window packet: "))
    else:
        window_size = window_ln

    buffer = ""

    window_size = window_size - 1
    messagelength = int(messagelength)
    end_of_window = window_size
    while packet_to_send_to_receiver != messagelength:
        while packet_to_send_to_receiver != (messagelength - window_size):
            conn.send(message[packet_to_send_to_receiver].encode())
            print('Sending packet number {}, which is {}'.format(packet_to_send_to_receiver,
                                                                 message[packet_to_send_to_receiver]))
            buffer = conn.recv(1024)
            buffer = buffer.decode()
            if buffer != "ACK Lost":

                print('{} is received, sliding window is in the range of {} to {} '.format(buffer, str(
                    packet_to_send_to_receiver + 1)
                                                                                           , str(end_of_window + 1)))
                packet_to_send_to_receiver = packet_to_send_to_receiver + 1
                end_of_window = end_of_window + 1

            else:

                print('Ack is lost, sliding window is in the range of {} to {} '.format(
                    str(packet_to_send_to_receiver + 1)
                    , str(end_of_window + 1)))

        while packet_to_send_to_receiver != messagelength:

            conn.send(message[packet_to_send_to_receiver].encode())
            print('Sending packet number {}, which is {}'.format(packet_to_send_to_receiver,
                                                                 message[packet_to_send_to_receiver]))
            buffer = conn.recv(1024)
            buffer = buffer.decode()
            if buffer != "ACK Lost":

                print('{} is received, sliding window is in the range of {} to {} '.format(buffer, str(
                    packet_to_send_to_receiver + 1)
                                                                                           , str(end_of_window + 1)))
                packet_to_send_to_receiver = packet_to_send_to_receiver + 1

            else:

                print('Ack is lost, sliding window is in the range of {} to {} '.format(
                    str(packet_to_send_to_receiver + 1)
                    , str(end_of_window + 1)))
    exit_cond = input("Do you want to send another message ? Y/N")
    if exit_cond.lower() != "y":
        break
