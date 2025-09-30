from expyriment import design, control, stimuli

#Uncomment for develop mode
control.set_develop_mode()

# PART 1: Global settings go here
exp = expyriment.design.Experiment("")
control.initialize(exp)

# PART 2: Stimuli and design (trial & block structure) go here
expyriment.control.start(subject_id=1)

# PART 3: Conducting the experiment goes here
# Loop over blocks and trials, present stimuli and get participant input
expyriment.control.end()