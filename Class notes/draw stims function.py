def draw(stims):
    """
    Takes an ordered list of stimuli 
    """

    #clear back buffer
    exp.screen.clear()

    #draw stims
    for stim in stims:
        stim.present(clear=False, update=False)

    #update screen (swap buffer)
    exp.screen.update()

