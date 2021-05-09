# Menu to send client
def mp_print_menu(first_mv):
    menu = "*"*20 + "\n TIC TAC TOE MENU " + "\n" + "*"*20 + "\n" +\
            "All players get circles.\n" + \
            "The algo will get crosses. \n" \
            "To place a move on the board, first type the row letter\n" \
            "then the column number, e.g. a1, c3, etc...\n" \
            "After you make your move, the algo will make " \
            "one in response. \n"

    if first_mv == b'-c':
        menu += "!! since it was indicated that the client starts first, then please make a move.\n"
    else:
        menu += "!! since it was not indicated that the client starts first, " \
                                "then the AI will make the first " \
                                "move.\n "
    return menu.encode()
