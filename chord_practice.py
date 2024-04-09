import random
import sys

notes = [
    str(chr(note_index)) + accidental
    for accidental in ["", "b", "#"]
    for note_index in range(ord("A"), ord("G") + 1)
]

# print(notes)

chord_types = ["", "-", "7", "maj7", "-7", "-7b5"]

if len(sys.argv) > 1:  # first argument is file name, second will be num practice
    for i in range(int(sys.argv[1])):
        print(f"{random.choice(notes)}{random.choice(chord_types)}")
else:
    while True:
        print(f"{random.choice(notes)}{random.choice(chord_types)}")
        if input() != "":
            break
