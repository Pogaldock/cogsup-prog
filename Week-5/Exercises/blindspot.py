from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_LEFT, K_RIGHT, K_1, K_2, K_SPACE
from drawing_functions import *
import os, csv  # <-- added

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

# Trial-level data (Exercise 2A)
exp.add_data_variable_names(['eye', 'final_radius', 'final_x', 'final_y'])

# Key-press data (Exercise 2B)
KEYLOG_FILE = r'C:\Users\Rowlu\Documents\Rowan\University\M1 2025-2026\Courses\Coding\Assignments\Week-5\Exercises\keypress_log.csv'
if not os.path.exists(KEYLOG_FILE):
    with open(KEYLOG_FILE, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['trial_eye', 'last_key', 'radius', 'x', 'y'])

def log_keypress(trial_eye, last_key, radius, pos):
    with open(KEYLOG_FILE, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([trial_eye, last_key, radius, pos[0], pos[1]])


input_keys = [K_LEFT, K_RIGHT, K_1, K_2, K_SPACE]


def keyboard_input(input_keys):
    key, rt = exp.keyboard.wait(keys=input_keys)
    return key

""" Stimuli helpers """
def make_circle(r, pos=(0, 0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10, colour=C_BLACK)
    c.preload()
    return c

def make_textbox(text, size, pos, text_size=22):
    """Fixed-size text container to control wrapping & placement"""
    tb = stimuli.TextBox(text=text, size=size, position=pos, text_size=text_size, text_colour=C_BLACK)
    tb.preload()
    return tb

""" Experiment """
def run_trial():
    width, height = exp.screen.size
    side_to_test = "right"  # default in case SPACE is pressed immediately

    
    title = stimuli.TextLine("Please select the eye you would like to test", text_size=30, position=(0, 120))
    hint  = stimuli.TextLine("Use LEFT/RIGHT to choose, SPACE to confirm", text_size=22, position=(0, 80))
    choice = stimuli.TextLine("", text_size=28, position=(0, 30))

    while True:
        exp.screen.clear()
        title.present(clear=False, update=False)
        hint.present(clear=False, update=False)
        choice.text = f"Current selection: {'right eye' if side_to_test=='right' else 'left eye'}"
        choice.present(clear=False, update=True)

        command = keyboard_input(input_keys)
        if command == K_SPACE:
            break
        elif command == K_LEFT:
            side_to_test = "left"
        elif command == K_RIGHT:
            side_to_test = "right"

    if side_to_test == "right":
        fixation_pos = (-(width // 2) + 300, 0)
    else:  # side_to_test == "left"
        fixation_pos = ((width // 2) - 300, 0)

    fixation = stimuli.FixCross(size=(100, 100), line_width=10, position=fixation_pos)
    fixation.preload()

    radius = 30
    circle = make_circle(radius)

    margin = 60
    box_w = int(min(width - 2 * margin, width * 0.8))
    box_h = 220
    box_pos = (0, (height // 2) - (box_h // 2) - margin)
    instructions_text = (
        f"Close your {side_to_test} eye and fixate the cross with the other.\n"
        "LEFT/RIGHT = move the circle\n"
        "1 = bigger, 2 = smaller\n"
        "Find where the circle disappears, then make it as big as possible while still invisible.\n"
        "SPACE = end"
    )
    instructions = make_textbox(instructions_text, size=(box_w, box_h), pos=box_pos, text_size=22)

    exp.screen.clear()

    while True:
        instructions.present(clear=True, update=False)
        fixation.present(clear=False, update=False)
        circle.present(clear=False, update=True)

        command = keyboard_input(input_keys)

        if command == K_SPACE:
            # log SPACE as a final keypress state too (Exercise 2B)
            log_keypress(side_to_test, 'SPACE', radius, circle.position)
            break
        elif command == K_LEFT:
            circle.move([-10, 0])
            log_keypress(side_to_test, 'LEFT', radius, circle.position)
        elif command == K_RIGHT:
            circle.move([10, 0])
            log_keypress(side_to_test, 'RIGHT', radius, circle.position)
        elif command == K_1:
            radius += 10
            circle = make_circle(radius, pos=circle.position)
            log_keypress(side_to_test, '1', radius, circle.position)
        elif command == K_2 and radius > 10:
            radius -= 10
            circle = make_circle(radius, pos=circle.position)
            log_keypress(side_to_test, '2', radius, circle.position)

    # ---- Trial-level summary row (Exercise 2A) ----
    x, y = circle.position
    exp.data.add([side_to_test, radius, x, y])

control.start(subject_id=1)
run_trial()
control.end()
