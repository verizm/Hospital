def start():
    print("Start and let's go")

def stop():
    print("Stop and done")

def unknown():
    print("Command is unknown")

class Controller:

    def __init__(self, id):
        self.id = id

    def handle(self):
        print("id: ", self.id)


controller = Controller(1)

factory = {}
factory["start"] = start
factory["stop"]  = stop
factory["handle"] = lambda: controller.handle()

name = input("Type a command please: ")

cmd = factory.get(name)
if cmd is None:
    cmd = unknown

cmd()
