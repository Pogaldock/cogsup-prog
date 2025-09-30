# kanizsa-rectangle.py
import expyriment
from expyriment import design, control, stimuli, misc



def kanizsa_rectangle(aspect_ratio=1.5, rectangle_scaling=0.25, circle_scaling=0.05):

    # Uncomment for develop mode
    control.set_develop_mode()

    # PART 1: Global settings go here
    exp = design.Experiment("", background_colour=misc.constants.C_GREY)
    control.initialize(exp)

    width, height = exp.screen.size

    # Rectangle geometry
    rect_w = rectangle_scaling * width
    rect_h = rect_w / aspect_ratio
    size_rectangle = (rect_w, rect_h)

    # Corner offsets (use half sizes of the rectangle)
    half_rect_w = rect_w / 2.0
    half_rect_h = rect_h / 2.0

    # Circles scale from screen width (your style)
    size_circle = circle_scaling * width  # used as radius

    # PART 2: Stimuli and design (trial & block structure) go here
    control.start(subject_id=1)

    # Four circles at rectangle corners
    circle_b_left  = stimuli.Circle(radius=size_circle, colour="black", position=(-half_rect_w,  half_rect_h))  # top-left
    circle_b_right = stimuli.Circle(radius=size_circle, colour="black", position=( half_rect_w,  half_rect_h))  # top-right
    circle_w_left  = stimuli.Circle(radius=size_circle, colour="white", position=(-half_rect_w, -half_rect_h))  # bottom-left
    circle_w_right = stimuli.Circle(radius=size_circle, colour="white", position=( half_rect_w, -half_rect_h))  # bottom-right

    # Occluder
    rectangle = stimuli.Rectangle(size=size_rectangle, colour=misc.constants.C_GREY)

    # Draw stimuli
    circle_b_left.present(clear=True,  update=False)
    circle_b_right.present(clear=False, update=False)
    circle_w_left.present(clear=False,  update=False)
    circle_w_right.present(clear=False, update=False)
    rectangle.present(clear=False,      update=True)

    exp.keyboard.wait()
    control.end()

# Run 
kanizsa_rectangle(
    aspect_ratio=1.8, 
    rectangle_scaling=0.30,
    circle_scaling=0.05
)
