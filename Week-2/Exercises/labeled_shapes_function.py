from expyriment import design, control, stimuli
from expyriment.misc import geometry
import math

control.defaults.initialise_delay = 0
control.defaults.window_mode = True
control.defaults.fast_quit = True
control.defaults.window_background_colour = (0, 0, 0)

exp = design.Experiment(name="Labeled Shapes Function")
control.initialize(exp)

# --- function to generate labeled polygon + line ---
def labeled_polygon(n_sides, side_length, colour, position, label):
    """Return (polygon, line, text_label) for a labeled regular polygon."""
    polygon = stimuli.Shape(
        vertex_list=geometry.vertices_regular_polygon(n_sides, side_length),
        colour=colour
    )
    polygon.reposition(position)

    # compute top y for vertical line
    top_y = max(y for x, y in polygon.points_on_screen)

    line_height = 50
    line = stimuli.Rectangle((3, line_height), colour=(255, 255, 255))
    line.reposition((position[0], top_y + line_height / 2))

    text = stimuli.TextLine(label, text_colour=(255, 255, 255))
    text.reposition((position[0], top_y + line_height + 20))

    return polygon, line, text


# --- recreate Exercise 4A display ---
side = 50
triangle, tri_line, tri_label = labeled_polygon(3, side, "purple", (-100, 0), "triangle")

# match hexagon height to triangle height
triangle_height = side * math.sqrt(3) / 2
hex_side = triangle_height / math.sqrt(3)  # side length for hexagon with same height
hexagon, hex_line, hex_label = labeled_polygon(6, hex_side, "yellow", (100, 0), "hexagon")

# --- run experiment ---
control.start(subject_id=1)

for stim in (triangle, hexagon, tri_line, hex_line, tri_label, hex_label):
    stim.present(clear=(stim is triangle), update=False)

exp.screen.update()
exp.keyboard.wait()
control.end()
