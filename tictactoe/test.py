import tictactoe as ttt

board = ttt.initial_state()
print(ttt.player(board))
print(ttt.actions(board))
# print(ttt.result(board, (1, 2)))
print(ttt.winner(board))
print(ttt.terminal(board))
print(ttt.utility(board))
