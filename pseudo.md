1. Display current score at the top during gameplay
2. clear the board consistently
3. Extract some of the responsibilities from TicTacToe class
ex) smart_choices and find_winning_square -> Computer class?
ex) display and input methods could be extracted to a helper module or mxin
4. consider eliminating duplication in play_one_game for human_first and computer_first
5. join_or function doesn't handle the single0item case correclty(it will cause an IndexError)
6. Implement ask_play_again
7. score_reset method is commented out. will use or not?


current_player_moves(human)
current_player_moves(computer)
