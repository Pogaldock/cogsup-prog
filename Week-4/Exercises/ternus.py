from expyriment import design, control, stimuli, misc
from expyriment.misc.constants import K_SPACE
from drawing_functions import *

""" Stimuli """
RADIUS = 50; DISTANCE = RADIUS * 3; SPREAD = RADIUS * 9

def make_circles(radius=RADIUS):
    positions = range(-SPREAD // 2, SPREAD // 2, DISTANCE) # x-positions: [-225, -75, 75]
    circles = [stimuli.Circle(radius=radius, position=(x_pos, 0)) for x_pos in positions]
    return circles

def add_tags(circles, tag_radius):
    tag_colors = [misc.constants.C_YELLOW, misc.constants.C_RED, misc.constants.C_BLUE]
    tag_circles = [stimuli.Circle(radius=tag_radius, colour=col) for col in tag_colors]
    for circle, tag in zip(circles, tag_circles):
        tag.plot(circle)


def run_trial(circle_frames=12, ISI=0, tags=False):
    # Create circles
    circles = make_circles()

    if tags: add_tags(circles, tag_radius=RADIUS // 5)
    load(circles)
    while True:
        for dx in (SPREAD, -SPREAD):
            present_for(exp, circles, num_frames=circle_frames)
            present_for(exp, [], num_frames=ISI)
            circles[0].move((dx, 0))
        if exp.keyboard.check(K_SPACE):
            break



control.set_develop_mode()

bg = misc.constants.C_WHITE
fg = misc.constants.C_BLACK

exp = design.Experiment("Ternus", background_colour=bg, foreground_colour=fg)
control.initialize(exp)
control.start(subject_id=1)
trials = [{'ISI': 0}, {'ISI': 18}, {'ISI': 18, 'tags': True}]
for trial_params in trials:
    run_trial(**trial_params)
control.end()