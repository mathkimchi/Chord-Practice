import mido
import atexit
import random
import time

chords: list[tuple[str, set[int]]] = [
    ("MAJOR", {0, 4, 7}),
    ("MINOR", {0, 3, 7}),
    ("DOM7", {0, 4, 7, 10}),
    ("MAJ7", {0, 4, 7, 11}),
    ("MIN7", {0, 3, 7, 10}),
]
# chord_notes_to_name = {
#     {0, 4, 7}: "MAJOR",
#     {0, 3, 7}: "MINOR",
#     {0, 4, 7, 10}: "DOM7",
#     {0, 4, 7, 11}: "MAJ7",
#     {0, 3, 7, 10}: "MIN7",
# }
# I will stop here because that is all I want to practice for now

# sharp mode
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def num_to_note(note_num: int) -> tuple[str, int]:
    note_name = note_names[note_num % 12]
    octave = note_num // 12

    return note_name, octave


# no inversions
def notes_to_chord(notes: set[int]) -> tuple[str, int, str] | None:
    "note name, note octave, chord name"
    if len(notes) == 0:
        return None

    lowest_note = min(notes)
    shifted_notes = {note_num - lowest_note for note_num in notes}

    for chord_name, chord_notes in chords:
        if shifted_notes == chord_notes:
            return *num_to_note(lowest_note), chord_name

    return None


def chord_recognize_demo():
    import mido
    import rtmidi

    inport = mido.open_input()  # type: ignore
    currently_active_notes = set()

    print("msg=")
    print(f"{currently_active_notes=}")
    print(f"Chord: {notes_to_chord(currently_active_notes)}")

    while True:
        msg = inport.receive()
        note_num = msg.note
        if msg.type == "note_on":
            currently_active_notes.add(note_num)
        elif msg.type == "note_off":
            currently_active_notes.remove(note_num)

        LINE_UP = "\033[1A"  # https://itnext.io/overwrite-previously-printed-lines-4218a9563527
        LINE_CLEAR = "\x1b[2K"
        for _ in range(3):
            print(LINE_UP, end=LINE_CLEAR)

        print(f"{msg=}")
        print(f"{currently_active_notes=}")
        print(f"Chord: {notes_to_chord(currently_active_notes)}")


class ChordPractice:
    def __init__(self) -> None:
        self.inport = mido.open_input()  # type: ignore
        self.currently_active_notes: set[int] = set()
        current_chord: str | None = None


def chord_practice():
    inport = mido.open_input()  # type: ignore
    currently_active_notes: set[int] = set()
    current_chord: tuple[str, int, str] | None = None

    print("\033[?47h")  # save the screen
    atexit.register(lambda: print("\033[?47l"))  # restore the screen on exit

    goal_note_name: str = random.choice(note_names)
    goal_chord_name: str = random.choice(chords)[0]

    # doesn't work, makes sense because ppl woul usually use OOP instead of fn in fn.
    # def set_goal():
    #     global goal_note_name
    #     goal_note_name = random.choice(note_names)
    #     global goal_chord_name
    #     goal_chord_name = random.choice(chords)[0]

    def log():
        print("\033[2J")

        print(f"Goal: {goal_note_name} {goal_chord_name}")
        print(f"{currently_active_notes=}")
        print(f"Chord: {current_chord}")

    def is_goal_met() -> bool:
        if current_chord == None:
            return False

        # inversion matters but octave doesn't matter
        return (
            current_chord[0] == goal_note_name and current_chord[2] == goal_chord_name
        )

    log()

    while True:
        msg = inport.receive()
        note_num = msg.note

        # update currently_active_notes
        if msg.type == "note_on":
            currently_active_notes.add(note_num)
        elif msg.type == "note_off":
            currently_active_notes.remove(note_num)

        # update current chord
        current_chord = notes_to_chord(currently_active_notes)

        log()

        if is_goal_met():
            print("Goal met!")
            time.sleep(1)

            # new goals
            goal_note_name = random.choice(note_names)
            goal_chord_name = random.choice(chords)[0]


if __name__ == "__main__":
    chord_practice()
