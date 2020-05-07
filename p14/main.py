#!/usr/bin/env python3

# this program is in desperate need of multithreading to handle all
# the threads independently (as it is now, the buffers fill up sometimes
# before kicking out all the alien servers, but it's good enough to keep going).

import re
import os

from threading import Thread
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from select import select
from random import choice
from time import sleep

import json

HOST = "52.49.91.111"
PORT = 2092


def parse_message(message):
    m = re.search(r"^ROUND (\d+): (\d+) -> (\S+)", message)
    if m:
        rnd = int(m.group(1))
        sender = int(m.group(2))
        cmd = m.group(3)
        args = message[m.end()+1:]
        if cmd in ("LEARN", "ACCEPTED"):
            m = re.search(r"^\{servers: \[(\d+(?:,\d+)*)\], secret_owner: (\d+)\}", args)
            args = {"servers": list(map(int,m.group(1).split(","))), "secret_owner": int(m.group(2))}
        elif cmd == "PREPARE":
            m = re.search(r"^\{(\d+),(\d+)}", args)
            args = (int(m.group(1)), int(m.group(2)))
        elif cmd == "PROMISE":
            m = re.match(r"\{(\d+),(\d+)\} (.+)", args)
            args = [(int(m.group(1)), int(m.group(2))), m.group(3)]
        return (rnd, sender, cmd, args)
    return None


class Client:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.socket.connect((HOST,PORT))
        self.sfile = self.socket.makefile("rw")
        line = next(self.sfile).strip()
        m = re.match(r"SERVER ID: (\d+)", line)
        self.id = int(m.group(1))

    def disconnect(self):
        self.sfile.close()
        self.socket.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, cls, val, tbck):
        self.disconnect()

    def read_until_round_end(self):
        messages = []
        for line in self.sfile:
            line = line.strip()
            msg = parse_message(line)
            if msg is not None:
                messages.append(msg)
            else:
                print(line)
            if line.endswith("(ROUND FINISHED)"):
                break
        return messages

    def send(self, cmd, dest):
        msg = cmd + " -> {}\n".format(dest)
        self.socket.send(msg.encode("ascii"))


def sequence_to_str(s, l="[", r="]", sep=","):
    """the server is very strict with the format and it doesn't like the 
    space after the comma in the default python representation"""
    return l+sep.join(map(str,s))+r


def accept_cmd(job, servers, secret_owner):
    cmd = "ACCEPT {{id: {job}, value: {{servers: {servers}, secret_owner: {secret_owner}}}}}".format(
            job=sequence_to_str(job, "{", "}"),
            servers=sequence_to_str(servers),
            secret_owner=secret_owner)
    return cmd


def prepare_cmd(my_id, job_id):
    cmd = "PREPARE {{{job_id},{my_id}}}".format(job_id=job_id, my_id=my_id)
    return cmd


n = 9


class ClientArray:
    def __init__(self, nclients):
        self.nclients = nclients

    def __enter__(self):
        self.clients = [Client() for _ in range(self.nclients)]
        for c in self.clients:
            c.connect()
        return self

    def __exit__(self, cls, value, tbck):
        for c in self.clients:
            c.disconnect()

    def __getitem__(self, i):
        return self.clients[i]

    def __iter__(self):
        return iter(self.clients)


with ClientArray(7) as c:
    while True:
        messages = c[0].read_until_round_end()
        for msg in messages:
            print(msg)
        round_n, sender, cmd, args = messages[-1]
        servers = args["servers"]
        secret_owner = args["secret_owner"]
        for serv in servers:
            if serv != c[0].id:
                c[0].send(prepare_cmd(c[0].id, c[0].id), serv)
        servers_after = servers.copy()
        if len(servers) < 7:
            allies_not_in_list = [client.id for client in c if client.id not in servers]
            if allies_not_in_list:
                servers_after.append(allies_not_in_list[0])
                print("Trying to add server {} (servers_after={})".format(allies_not_in_list[0], servers_after))
        else:
            alien_servers = [s for s in servers if s not in (client.id for client in c)]
            if alien_servers:
                servers_after.remove(alien_servers[0])
                secret_owner_after = alien_servers[1] if len(alien_servers) > 1 else servers_after[0] 
                print("Trying to remove server {} (servers_after={})".format(alien_servers[0], servers_after))
        for serv in servers:
            c[0].send(accept_cmd((c[0].id, c[0].id), servers_after, secret_owner_after), serv)

