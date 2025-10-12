
from collections.abc import Iterable
import math

FPS = 60 # frames per second
MSPF = 1000 / FPS # milliseconds per frame (more robust than using 16.67)

def to_frames(t):
    return math.ceil(t / MSPF) # Make sure you use consistent rounding

def to_time(num_frames):
    return num_frames * MSPF


def draw(exp, stims):
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

def timed_draw(exp, stims):
    t0 = exp.clock.time # Initial time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
        exp.screen.update()
    elapsed = exp.clock.time - t0 # Time after drawing
    return elapsed

def present_for(exp, stims, num_frames):
    if num_frames == 0: # If num_frames = 0 → No need to present anything
        return
    dt = timed_draw(exp, stims) # Get time needed for correction
    if dt > 0:
        t = to_time(num_frames) # Convert frames to time
        exp.clock.wait(t - dt) # Adjust waiting time by dt

