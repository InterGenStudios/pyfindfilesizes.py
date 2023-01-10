import urllib
from urllib.request import urlopen
import os
import math
import re
import socket
import platform
import time

def convert_size(size):
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return s, size_name[i]

def to_bytes(size, unit):
    units = {'B': 0, 'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4, 'PB': 5, 'EB': 6, 'ZB': 7, 'YB': 8}
    return int(size * math.pow(1024, units[unit]))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_directory(path, threshold):
    try:
        path = os.path.abspath(path)
        if os.path.exists(path) and os.path.isdir(path):
            files_list = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > threshold:
                        size = convert_size(file_size)
                        files_list.append(f'{file_path} - {size[0]} {size[1]}')
                        print(f'{file_path} - {size[0]} {size[1]}')
            prompt_to_save(files_list)
        else:
            print(f"{path} is not a valid directory or it does not exist")
            print()
    except Exception as e:
        print(f"An error occured {e}")
        
def prompt_to_save(files_list):
    print()
    save = input("Do you want to save the list of files to a file? (y/n): ")
    if save.lower() == 'y':
        save_to_file(files_list)
    else:
        print()
        print("List not saved to file")
        print()

def save_to_file(files_list):
    file_name = input("Enter file name to save: ")
    with open(file_name, "w") as file:
        for item in files_list:
            file.write("%s\n" % item)
    print()
    print(f"List saved to {file_name}")
    print()

if __name__ == '__main__':
    clear()
    print("PyFindFileSizes v.001")
    print()
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    d = str(urlopen('http://checkip.dyndns.com/').read())
    ext_ip =  re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    print(time.ctime())
    print("System OS:   ", platform.system())
    print("Hostname:    ",host_name)
    print("Internal IP: ",host_ip)
    print("External IP: ",ext_ip)
    print()
    while True:
        path = input('Enter the directory path to scan: ')
        path = os.path.abspath(path)
        if os.path.exists(path) and os.path.isdir(path):
            input_string = input("Enter the threshold file size (e.g. 10MB): ")
            size, unit = re.findall("([\d.]+)([A-Za-z]+)", input_string)[0]
            threshold = to_bytes(float(size), unit.upper())
            files_list = scan_directory(path, threshold)
            break
        else:
            print(f"{path} is not a valid directory or it does not exist")
            print()

