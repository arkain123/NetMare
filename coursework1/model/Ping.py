import socket
import struct
import time

def calculate_checksum(source_string):
    sum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xFFFFFFFF
        count = count + 2

    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xFFFFFFFF

    sum = (sum >> 16) + (sum & 0xFFFF)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xFFFF
    answer = answer >> 8 | (answer << 8 & 0xFF00)

    return answer

def ping(target_host, packets, delay):
    icmp = socket.getprotobyname("icmp")
    socket_ping = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    packet_id = 1
    result = {}

    successes = 0
    failures = 0
    total_time = 0

    for i in range(int(packets)):
        packet = struct.pack("bbHHh", 8, 0, 0, packet_id, 1)
        packet_checksum = calculate_checksum(packet)
        packet = struct.pack("bbHHh", 8, 0, socket.htons(packet_checksum), packet_id, 1)

        start_time = time.time()

        socket_ping.sendto(packet, (target_host, 0))
        socket_ping.settimeout(1)

        try:
            received_packet, addr = socket_ping.recvfrom(1024)
            end_time = time.time()
            total_time += (end_time - start_time)
            successes += 1
        except socket.timeout:
            failures += 1

        time.sleep(delay)

        packet_id += 1

    socket_ping.close()
    if int(packets) > 0:
        success_rate = (successes / int(packets)) * 100
    else:
        success_rate = 0

    if successes > 0:
        average_time = total_time / successes
    else:
        average_time = 0

    result['successes'] = successes
    result['failures'] = failures
    result['avg'] = average_time
    result['loss'] = 100 - success_rate
    result['host'] = target_host
    result['count'] = packets
    result['delay'] = delay

    return result