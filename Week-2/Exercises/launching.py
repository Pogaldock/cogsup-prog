from expyriment import design, control, stimuli

control.defaults.initialise_delay = 0
control.defaults.window_mode = True
control.defaults.fast_quit = True

exp = design.Experiment(name="Moving Square")
control.initialize(exp)

# start at left side
square_red = stimuli.Rectangle((50, 50), colour='red', position=(-400, 0))
square_green = stimuli.Rectangle((50, 50), colour='green', position=(0, 0))

control.start(subject_id=1)

# Present both once initially
square_green.present(clear=True, update=False)
square_red.present(clear=False, update=True)

# Move red square step by step to center
target_x_red = -50 
target_x_green = 400 # final position of the green square
step = 5  # pixels per frame

while square_red.position[0] < target_x_red:
    # update position
    x, y = square_red.position
    square_red.position = (x + step, y)

    # redraw both squares
    square_green.present(clear=True, update=False)
    square_red.present(clear=False, update=True)

while square_green.position[0] < target_x_green:
    # update position
    x, y = square_green.position
    square_green.position = (x + step, y)

    # redraw both squares
    square_green.present(clear=True, update=False)
    square_red.present(clear=False, update=True)

# Leave on screen until a key is pressed
exp.keyboard.wait()
control.end()