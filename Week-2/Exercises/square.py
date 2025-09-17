# Import the main modules of expyriment

from expyriment import design, control, stimuli
control.defaults.initialise_delay = 0 # No countdown
control.defaults.window_mode = True # Not full-screen
control.defaults.fast_quit = True # No goodbye message

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Circle")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# Create a fixation cross (color, size, and position will take on default values)
fixation = stimuli.FixCross() # At this stage the fixation cross is not yet rendered

square = stimuli.Rectangle((50,50), colour='blue')

# Start running the experiment
control.start(subject_id=1)


square.present(clear=True, update=False)
fixation.present(clear=False, update=True)

# Leave it on-screen
exp.clock.wait(500)

square.present(clear=True, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()