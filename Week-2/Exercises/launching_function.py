from expyriment import design, control, stimuli

def run_launching_experiments(temporal_gap_ms=200, spatial_gap_px=80, speedup_factor=3.0):
    control.defaults.initialise_delay = 0
    control.defaults.window_mode = True
    control.defaults.fast_quit = True

    exp = design.Experiment("Launching")
    control.initialize(exp)
    control.start(subject_id=1)

    # Initial parameters
    SIZE = 50
    RED_START = -400
    CENTER = 0
    GREEN_START = CENTER
    GREEN_END = 400
    RED_TOUCH = CENTER - SIZE
    step = 5
    frame = 20

    def draw(r, g):
        g.present(clear=True, update=False)
        r.present(clear=False, update=True)

    def move_x(sq, target, sp, other):
        dx = sp if sq.position[0] < target else -sp
        while (dx > 0 and sq.position[0] < target) or (dx < 0 and sq.position[0] > target):
            x, y = sq.position
            sq.position = (x + dx, y)
            draw(r=sq, g=other)
            exp.clock.wait(frame)

    def reset_pos():
        r = stimuli.Rectangle((SIZE, SIZE), colour="red",   position=(RED_START, 0))
        g = stimuli.Rectangle((SIZE, SIZE), colour="green", position=(GREEN_START, 0))
        draw(r, g)
        exp.clock.wait(250)
        return r, g
    
    def show_label(text):
        stimuli.TextLine(text, position=(0, 0)).present(clear=True, update=True)
        exp.clock.wait(600)

    # Michotte
    show_label("Michottean launching")
    red, green = reset_pos()
    move_x(red, RED_TOUCH, step, green)
    move_x(green, GREEN_END, step, red)
    exp.clock.wait(300)

    # Temporal gap
    show_label("Temporal gap")
    red, green = reset_pos()
    move_x(red, RED_TOUCH, step, green)
    exp.clock.wait(temporal_gap_ms)
    move_x(green, GREEN_END, step, red)
    exp.clock.wait(300)

    # Spatial gap
    show_label("Spatial gap")
    red, green = reset_pos()
    move_x(red, RED_TOUCH - spatial_gap_px, step, green)
    move_x(green, GREEN_END, step, red)
    exp.clock.wait(300)

    # Triggering
    show_label("Triggering")
    red, green = reset_pos()
    move_x(red, RED_TOUCH, step, green)
    move_x(green, GREEN_END, int(step * speedup_factor), red)

    stimuli.TextLine("Press any key to exit.").present(clear=True, update=True)
    exp.keyboard.wait()
    control.end()

run_launching_experiments(1000,100,5)