import expyriment
from expyriment import design, control, stimuli, misc

#Uncomment for develop mode
control.set_develop_mode()

# PART 1: Global settings go here
exp = expyriment.design.Experiment("", background_colour=misc.constants.C_GREY)
control.initialize(exp)

width, height = exp.screen.size
size_square = (0.25*width,0.25*width)
half_size_square = (0.25*width) /2.0
size_circle = 0.05*width

# PART 2: Stimuli and design (trial & block structure) go here
expyriment.control.start(subject_id=1)

circle_b_left = stimuli.Circle(radius=size_circle, colour = "black", position = (-half_size_square,half_size_square))
circle_b_right = stimuli.Circle(radius=size_circle, colour = "black", position = (half_size_square,half_size_square))
circle_w_left = stimuli.Circle(radius=size_circle, colour = "white", position = (-half_size_square,-half_size_square))
circle_w_right = stimuli.Circle(radius=size_circle, colour = "white", position = (half_size_square,-half_size_square))
square = stimuli.Rectangle(size=size_square, colour = misc.constants.C_GREY)


# PART 3: Conducting the experiment goes here
# Loop over blocks and trials, present stimuli and get participant input

circle_b_left.present(clear=True, update=False)
circle_b_right.present(clear=False, update=False)
circle_w_left.present(clear=False, update=False)
circle_w_right.present(clear=False, update=False)
square.present(clear=False,update=True)

exp.keyboard.wait()
expyriment.control.end()