import bluetooth as bt
import threading
import select

class Device:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

class ControllerConnection:
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
        return len(self.devices)
        
    def connect(self, device: Device) -> bool:
        if self.socket != None:
            return False
        print ("Searching service",self.service_uuid,"in",device.address)
        services = bt.find_service(uuid=self.service_uuid, address=device.address)
        if len(services) == 0:
            print ("Could not find service")
            return False
        else:
            service = services[0]
            port = service["port"]
            name = service["name"]
            print ("Connecting to",device.name+"'s ",name,"service...")
            self.socket = bt.BluetoothSocket(bt.RFCOMM)
            #self.socket.setblocking(0)
            try:
                self.socket.connect((device.address, port))
                print ("Successful connection")
                return True
            except:
                print ("The connection failed")
                return False

    def disconnect(self):
        if self.socket == None:
            return False
        print ("Closing connection...")
        self.socket.close()
        self.socket = None
        self.stop_receiving()
        while self.receiving:
            pass
        print ("Connection closed")
        return True
    
    def send(self, message: str):
        print("Sending",message)
        if self.socket == None:
            return
        try:
            self.socket.send(message)
        except:
            self.disconnect()

    def start_receiving(self, callback):
        if self.socket is None:
            return
        print ("Recieving...")
        self.stop = False
        self.receive_thread = threading.Thread(target=self._receive, args=(callback,))
        self.receive_thread.start() 
        self.receiving = True

    def stop_receiving(self):
        print("Stopping receive thread...")
        self.stop = True

    def _receive(self, callback):
        while not self.stop:
            ready = select.select([self.socket], [], [], 5)
            if ready[0]:
                data = self.socket.recv(1024)
                if data:
                    callback(data)
            else:
                print("Did not receive data")
        self.receiving = False
        print("Stopped receiving")


if __name__ == '__main__':
    from sys import argv
    blt = ControllerConnection()
    print(blt.search_devices())

