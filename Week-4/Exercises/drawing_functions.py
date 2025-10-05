from expyriment import design, control, stimuli
import random
from collections.abc import Iterable

def draw(stims):
    """Draw all stims once, then flip buffer and screen"""
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()

def load(stims):
    """Preload one stimulus or a list of stimuli"""
    if isinstance(stims, Iterable) and not isinstance(stims, (str, bytes)):
        for stim in stims:
            stim.preload()
    else:
        stims.preload()

def timed_draw(stims):
    t0 = exp.clock.time
    draw(stims)
    return exp.clock.time - t0

def present_for(stims, t=1000):
    draw_time = timed_draw(stims)
    wait_ms = max(0, t - draw_time)
    exp.clock.wait(wait_ms)


"""Test functions"""
exp = design.Experiment(name="Test Functions")

control.set_develop_mode()
control.initialize(exp)
control.start(subject_id=1)

#generate the fixation stim
fixation = stimuli.FixCross()
#preload the fixation stim
load(fixation)

#number of squares to present
n = 20
#generate random positions for the squares
positions = [(random.randint(-300, 300), random.randint(-300, 300)) for _ in range(n)]
#generate a list of square stims with the random positions
squares = [stimuli.Rectangle(size=(50, 50), position=pos) for pos in positions]
#preload the square stims
load(squares)

#list to store the real durations of stim presetation
durations = []

#initialize start time
t0 = exp.clock.time

#draw stims and time the presentation
for square in squares:
    if not square.is_preloaded:
        print("Preloading function not implemented correctly.")
    frame = [fixation, square]
    present_for(frame, 500)
    t1 = exp.clock.time
    durations.append(t1 - t0)
    t0 = t1

#print presentation times
print(durations)

control.end()