# Server-only teaching data. No API exposes the answer list.
ANSWERS = {1: 'Toy Story', 2: 'Finding Nemo', 3: 'The Lion King'}

def check_guess(clue_id, title):
    return title.strip().casefold() == ANSWERS[clue_id].casefold()
