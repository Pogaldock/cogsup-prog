# Import the main modules of expyriment

from expyriment import design, control, stimuli
control.defaults.initialise_delay = 0 # No countdown
control.defaults.window_mode = True # Not full-screen
control.defaults.fast_quit = True # No goodbye message

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Circle")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

square_red = stimuli.Rectangle((50,50), colour='red', position = (-400,0))
square_green = stimuli.Rectangle((50,50), colour='green', position = (0,0))

# Start running the experiment
control.start(subject_id=1)


square_red.present(clear=True, update=False)
square_green.present(clear=False, update=True)
exp.clock.wait(1000)

square_red.move((0,0))
exp.clock.wait(square_red.move((0,0)))
square_green.move((400,0))
# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()