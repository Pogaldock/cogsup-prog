import expyriment
from expyriment import design, control, stimuli

#Uncomment for develop mode
#control.set_develop_mode()

# PART 1: Global settings go here
exp = expyriment.design.Experiment("")
control.initialize(exp)

width, height = exp.screen.size
size_square = (0.05*width,0.05*width)
half_size_square = (0.05*width)//2

# PART 2: Stimuli and design (trial & block structure) go here
expyriment.control.start(subject_id=1)

square_1 = stimuli.Rectangle(size=size_square, colour = "red", line_width=1, position=((-width//2) + half_size_square,(-height//2) + half_size_square))
square_2 = stimuli.Rectangle(size=size_square, colour = "red", line_width=1, position=((width//2) - half_size_square,(-height//2) + half_size_square))
square_3 = stimuli.Rectangle(size=size_square, colour = "red", line_width=1, position=((width//2) - half_size_square,(height//2) - half_size_square))
square_4 = stimuli.Rectangle(size=size_square, colour = "red", line_width=1, position=((-width//2) + half_size_square,(height//2) - half_size_square))


# PART 3: Conducting the experiment goes here
# Loop over blocks and trials, present stimuli and get participant input

square_1.present(clear=True, update=False)
square_2.present(clear=False, update=False)
square_3.present(clear=False, update=False)
square_4.present(clear=False, update=True)


exp.keyboard.wait()
expyriment.control.end()