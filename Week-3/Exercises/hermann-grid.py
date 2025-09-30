import expyriment
from expyriment import design, control, stimuli, misc
from expyriment.misc import constants

#Uncomment for develop mode
control.set_develop_mode()

def hermann_grid(square_size = 50, square_colour = constants.C_BLACK, bg_colour = constants.C_WHITE, spacing = 10, num_rows = 5, num_collumns = 5):
    exp = expyriment.design.Experiment("hermann grid", background_colour = bg_colour)
    control.initialize(exp)
    expyriment.control.start(subject_id=1)

    square = stimuli.Rectangle(size = (square_size, square_size), colour = square_colour)
    total_grid_height = (square_size*num_rows) + (spacing*(num_rows-1))
    total_grid_width = (square_size*num_collumns) + (spacing*(num_collumns-1))
    position_of_first_square = ((total_grid_height/2) - (square_size/2), (-total_grid_width/2) + (square_size/2)) #top left square

    start_y = position_of_first_square[0]
    start_x = position_of_first_square[1]

    for i in range(1, num_rows + 1):
        for j in range(1, num_collumns + 1):
            x = start_x + (j - 1) * (square_size + spacing)
            y = start_y - (i - 1) * (square_size + spacing)
            square.position = (x, y)

            is_first = (i == 1 and j == 1)
            is_last  = (i == num_rows and j == num_collumns)

            # Clear once on the very first draw; update once on the very last
            square.present(clear=is_first, update=is_last)
            

    exp.keyboard.wait()
    expyriment.control.end()

hermann_grid(square_size = 100, square_colour = constants.C_BLACK, bg_colour = constants.C_WHITE, spacing = 20, num_rows = 5, num_collumns = 5)