# Import the main modules of expyriment

from expyriment import design, control, stimuli
from expyriment.misc import geometry
import math

control.defaults.initialise_delay = 0 # No countdown
control.defaults.window_mode = True # Not full-screen
control.defaults.fast_quit = True # No goodbye message

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Circle")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

side = 50
triangle = stimuli.Shape(
    vertex_list=geometry.vertices_regular_polygon(3, side),
    colour="purple"
)

triangle.reposition((-100, 0))

hexagon = stimuli.Shape(
    vertex_list=geometry.vertices_regular_polygon(6, side/2),
    colour="yellow"
)

hexagon.reposition((100, 0))

def top_y(shape): return max(y for x, y in shape.points_on_screen)

line_height = 50
line_width = 3
tri_line = stimuli.Rectangle((line_width, line_height), colour=(255, 255, 255))
tri_line.reposition((triangle.position[0], top_y(triangle) + line_height / 2))
hex_line = stimuli.Rectangle((line_width, line_height), colour=(255, 255, 255))
hex_line.reposition((hexagon.position[0], top_y(hexagon) + line_height / 2))

offset = 20
tri_label = stimuli.TextLine("triangle", text_colour=(255, 255, 255))
tri_label.reposition((triangle.position[0], top_y(triangle) + line_height + offset))
hex_label = stimuli.TextLine("hexagon", text_colour=(255, 255, 255))
hex_label.reposition((hexagon.position[0], top_y(hexagon) + line_height + offset))

# Start running the experiment
control.start(subject_id=1)

for stim in (triangle, hexagon, tri_line, hex_line, tri_label, hex_label):
    stim.present(clear=(stim is triangle), update=False)

exp.screen.update()
exp.keyboard.wait()
control.end()