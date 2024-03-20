import socket
import paramiko
from getpass import getpass
from threading import Thread
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Adjust timeout as needed

    result = sock.connect_ex((ip, port))
    sock.close()

    if result == 0:
        return True  # Port is open
    else:
        return False  # Port is closed

def get_hostname(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=22, username=username, password=password, timeout=5)

        stdin, stdout, stderr = client.exec_command('hostname')
        hostname = stdout.read().decode().strip()

        client.close()

        return hostname
    except (paramiko.AuthenticationException, paramiko.SSHException, paramiko.ssh_exception.NoValidConnectionsError) as e:
        print(f"Failed to connect to {ip}: {str(e)}")
        return None

def scan_ips(start_ip, end_ip, username, password):
    print(start_ip)
    for ip in range(start_ip, end_ip + 1):
        ip_address = f"10.20.{ip // 256}.{ip % 256}"

        if check_port(ip_address, 22):
            hostname = get_hostname(ip_address, username, password)
            if hostname:
                print(f"{ip_address} - {hostname}\n")
# Define the range of IP addresses to scan
start_ip = 0
end_ip = 8 * 256 + 255

# Set your SSH credentials
print(f'Username: ')
username = input()
password = getpass()
t1 = Thread(target=scan_ips, args=[0,1*256,username,password])
t2 = Thread(target=scan_ips, args=[1*256,2*256,username,password])
t3 = Thread(target=scan_ips, args=[2*256,3*256,username,password])
t4 = Thread(target=scan_ips, args=[3*256,4*256,username,password])
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()

