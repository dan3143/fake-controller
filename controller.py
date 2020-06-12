import bluetooth as bt
import tkinter as tk
from os import system
from tkinter import ttk

class Device:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Controller:
    def __init__(self):
        self.socket = None
        self.service_uuid = "00001101-0000-1000-8000-00805F9B34FB"
        self.devices = []

    def search_devices(self):
        self.devices.clear()
        print ("Searching for devices...")
        devices = bt.discover_devices(lookup_names=True)
        print ("Search finished")
        if not devices:
            print ("No devices found")
        else:
            for address, name in devices:
                self.devices.append(Device(name, address))
        
    def connect(self, device: Device) -> bool:
        if self.socket != None:
            return False
        services = bt.find_service(uuid=self.service_uuid, address=device.address)
        if len(services) == 0:
            print ("Could not find service")
            return False
        else:
            service = services[0]
            port = service["port"]
            name = service["name"]
            print ("Connecting to",device.name,"'s ",name,"service...")
            self.socket = bt.BluetoothSocket(bt.RFCOMM)
            try:
                self.socket = self.socket.connect((device.address, port))
                print ("Successful connection")
                return True
            except:
                print ("The connection failed")
                return False

    def disconenct(self):
        if self.socket == None:
            return False
        print ("Closing connection...")
        self.socket.close()
        print ("Connection closed")
        return True
    
    def send(self, message: str):
        if self.socket == None:
            return
        try:
            self.socket.send(message)
        except:
            self.disconenct()