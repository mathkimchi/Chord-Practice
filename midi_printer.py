import mido

inport = mido.open_input()

while True:
    msg = inport.receive()
    print(msg)
