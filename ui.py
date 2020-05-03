import interaction


def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    for row in board:
        print("".join(row))


def display_stats():
    stat = interaction.characters['hero']
    print(
        f'Player: {stat["name"]}  ' +
        f'Life: {stat["live"]}  ' +
        f'Attack: {stat["attack"]}  ' +
        f'Crit: {stat["chanses critical hit"]}  ' +
        f'Points: {stat["points"]}'
        )


# add display dialog box
# add display palyer stats
# add display inventory
