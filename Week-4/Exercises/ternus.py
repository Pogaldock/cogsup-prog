from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE

exp = design.Experiment(background_colour=(255,255,255))
control.set_develop_mode()
control.initialize(exp)


def load(stims):
    for stim in stims:
        stim.preload()


def make_circles(stims):
    canvas = stimuli.Canvas(size=exp.screen.size)
    for stim in stims:
        stim.plot(canvas)
    canvas.present(clear=True, update=True)

def present_for(stims, nb_frames):
    make_circles(stims)
    exp.clock.wait(nb_frames * 16.67) 

# --- Trial function ---
def run_trials(rad, isi, col_tags=False):
    while True:
        positions = [(-165,0),(-55,0),(55,0),(165,0)]
        circles = [stimuli.Circle(radius=rad, position=pos, colour=(0,0,0)) for pos in positions]

        # define colour tags
        overlays = [
            stimuli.Circle(radius=10, position=positions[0], colour=(255,222,33)),
            stimuli.Circle(radius=10, position=positions[1], colour=(255,0,0)),
            stimuli.Circle(radius=10, position=positions[2], colour=(0,255,0)),
            stimuli.Circle(radius=10, position=positions[3], colour=(255,222,33))
        ]

        load(circles)


        if exp.keyboard.check(K_SPACE):
            break

        nb_frames = 25  # Hardcode number of frames

        if isi == 0:
            #low isi
            present_for([circles[0], circles[1], circles[2]] +
                        (overlays[0:3] if col_tags else []), nb_frames)
            present_for([circles[1], circles[2], circles[3]] +
                        (overlays[1:4] if col_tags else []), nb_frames)
        else:
            #high isi
            present_for([circles[0], circles[1], circles[2]] +
                        (overlays[0:3] if col_tags else []), nb_frames)
            exp.clock.wait(isi * 16.67)
            canvas = stimuli.Canvas(size=exp.screen.size, colour=exp.background_colour)
            canvas.present(clear=True, update=True)
            exp.clock.wait(isi * 16.67)
            present_for([circles[1], circles[2], circles[3]] +
                        (overlays[1:4] if col_tags else []), nb_frames)
            canvas.present(clear=True, update=True)
            exp.clock.wait(int(isi * 16.67))

           

#press space between each run of the function
run_trials(rad=50, isi=3, col_tags=False)
run_trials(rad=50, isi=20, col_tags=False)
run_trials(rad=50, isi=0, col_tags=True)

control.end()