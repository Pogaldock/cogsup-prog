# ——————————————————————————————————————————————————————————
# What I’m doing :
# - Classic Stroop but with COLOR-NAMING (ignore the word, answer the ink color)
# - Full balance within subjects: every WORD×COLOR pair appears once per block (16 trials)
# - 8 blocks => 128 trials total
# - Between-subject balance: I rotate which key maps to which color across subjects (4 cyclic mappings)
#   so the key mapping itself isn’t a hidden confound.
# ——————————————————————————————————————————————————————————

from expyriment import design, control, stimuli
from expyriment.misc.constants import (
    C_WHITE, C_BLACK, K_f, K_g, K_h, K_j, K_SPACE
)
import random

# Keep words and ink colors the same four labels, which makes
# congruent vs incongruent easy to compute (word == color).
WORDS  = ["red", "blue", "green", "orange"]
COLORS = ["red", "blue", "green", "orange"]

# Force a 4AFC response: left-to-right comfortable keys on one row.
RESPONSE_KEYS = [K_f, K_g, K_h, K_j]

# I want 8 identical blocks; each block is a full factorial (4×4 = 16 trials).
N_BLOCKS = 8
TRIALS_PER_BLOCK = 16  

# Instructions:
INSTR_START = (
    "TASK: Name the INK COLOR of the word, ignore what the word says.\n\n"
    "Use the keys shown on the next screen.\n\n"
    "Press SPACE to see the response mapping."
)
INSTR_MID = "Halfway. Take a short break.\nPress SPACE to continue."
INSTR_END = "Finished. Press SPACE to quit."

# Feedback is brief; I don’t want it to dominate timing or learning.
FEEDBACK_CORRECT   = "Correct"
FEEDBACK_INCORRECT = "Incorrect"

# Durations: short fixation, short feedback. (ms)
FIX_DURATION_MS = 500
FEEDBACK_MS     = 700

# Helper functions

def load(stims):
    """Preload to avoid display lag mid-experiment."""
    for s in stims:
        s.preload()

def timed_draw(*stims):
    """Batch-present stimuli in one screen update; return draw time for timing-accurate waits."""
    t0 = exp.clock.time
    exp.screen.clear()
    for s in stims:
        s.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    """Present stims and keep them on screen for exactly t ms (minus draw time)."""
    dt = timed_draw(*stims)
    exp.clock.wait(max(0, t - dt))

def present_text(text, heading=None, wait_key=True):
    """Simple wrapper for instruction screens."""
    scr = stimuli.TextScreen(heading=heading, text=text, text_justification=0)
    scr.present()
    if wait_key:
        exp.keyboard.wait([K_SPACE])

def mapping_to_text(mapping, keys_display=("F","G","H","J")):
    """Render the key to color mapping in a readable vertical list."""
    lines = [f"[{k}]  →  {c}" for k, c in zip(keys_display, mapping)]
    return "Respond with these keys:\n\n" + "\n".join(lines) + "\n\nPress SPACE to start."

def make_full_factorial_block():
    """
    Build one block with every WORDxCOLOR pair exactly once (16 trials),
    then shuffle to avoid predictable streaks.
    """
    block = [{"word": w, "color": c} for w in WORDS for c in COLORS]
    random.shuffle(block)
    return block


# Initialize experiment
exp = design.Experiment(
    name="Stroop_Balanced",
    background_colour=C_WHITE,
    foreground_colour=C_BLACK
)

# Between-subjects I rotate the color order and bind it (left to right) to [F,G,H,J].
# Over 4 subjects, each color appears once on each key.
base_colors = COLORS[:]  # copy to be explicit
cyclic_perms = [base_colors[k:] + base_colors[:k] for k in range(len(base_colors))]
exp.add_bws_factor("key_color_mapping", cyclic_perms)

# Save the columns I care about.
exp.add_data_variable_names([
    "subject_id", "block", "trial",
    "word", "ink_color", "key_pressed", "rt_ms",
    "correct", "congruent", "mapping_order"
])

# Create the backend, window, etc.
control.initialize(exp)

# Create the reusable visuals for each trial
fixation = stimuli.FixCross(); fixation.preload()
fb_correct = stimuli.TextLine(FEEDBACK_CORRECT)
fb_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([fb_correct, fb_incorrect])

# Cache all word×color TextLine objects
stims = {
    w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS}
    for w in WORDS
}
load([stims[w][c] for w in WORDS for c in COLORS])

# Run trial function
def run_trial(block_id, trial_id, word, color, key_for_color, mapping_index):
    """One trial: fixation -> stimulus -> wait valid key -> feedback -> log everything"""
    present_for(fixation, t=FIX_DURATION_MS)

    # Present the word in the specified ink color and wait for one of the 4 valid keys.
    stims[word][color].present()
    key, rt = exp.keyboard.wait(RESPONSE_KEYS)

    # Correct key is determined by the current between-subject mapping.
    correct_key = key_for_color[color]
    correct = (key == correct_key)
    congruent = (word == color)

    present_for(fb_correct if correct else fb_incorrect, t=FEEDBACK_MS)

    # Log row
    exp.data.add([
        exp.subject, block_id, trial_id,
        word, color, key, rt,
        int(correct), int(congruent), mapping_index
    ])

# Run trial
control.start(1)
subject_id = exp.subject

# Resolve the subject’s key to color mapping from the between-subject factor
mapping = exp.get_permuted_bws_factor_condition("key_color_mapping", subject_id)

# mapping is a list of colors aligned with RESPONSE_KEYS [F,G,H,J]
key_for_color = {color: key for color, key in zip(mapping, RESPONSE_KEYS)}
mapping_index = cyclic_perms.index(mapping) 

# Instructions first, then show the mapping so participants know the keys
present_text(INSTR_START, heading="Instructions", wait_key=True)
present_text(mapping_to_text(mapping, keys_display=("F","G","H","J")),
             heading="Response Mapping", wait_key=True)

# Build the 8 balanced blocks (each is a shuffled full factorial)
blocks = [make_full_factorial_block() for _ in range(N_BLOCKS)]

# Run all blocks. After block 4 (halfway), insert a break screen.
for block_id, block in enumerate(blocks, start=1):
    for trial_id, t in enumerate(block, start=1):
        run_trial(block_id, trial_id, t["word"], t["color"], key_for_color, mapping_index)
    if block_id == N_BLOCKS // 2:
        present_text(INSTR_MID, heading="Break", wait_key=True)

present_text(INSTR_END, heading="End", wait_key=True)
control.end()