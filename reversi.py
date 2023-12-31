import tkinter as tk
from tkinter import messagebox
import numpy as np
import math
import copy
import time


class ReversiGUI:
    def __init__(self, master):
        self.master = master
        master.title("Reversi Game")
        master.geometry("1200x720")
        # create a frame for the game board on the left side
        self.board_frame = tk.Frame(master)
        self.board_frame.pack(side="left", padx=0, pady=10)

        # create a canvas for the game board
        self.canvas = tk.Canvas(self.board_frame, width=600, height=600)
        self.canvas.pack()

        # create a frame for the game controls on the right side
        self.controls_frame = tk.Frame(master)
        self.controls_frame.pack(side="left", padx=0, pady=0)

        # create buttons for game mode selection
        self.game_mode = tk.StringVar(value="human_vs_ai")
        self.ai_player = tk.IntVar(value=1)

        # create buttons for Human vs Human
        self.human_vs_human_button = tk.Button(
            self.controls_frame, text="Human vs Human", command=lambda: self.select_game_mode("human_vs_human"), width=15, height=2, bg="green")
        self.human_vs_human_button.grid(row=0, column=0, padx=10, pady=10)

        # create buttons for Human vs AI
        self.human_vs_ai_button = tk.Button(
            self.controls_frame, text="Human vs AI", command=lambda: self.select_game_mode("human_vs_ai"), width=15, height=2)
        self.human_vs_ai_button.grid(row=0, column=1, padx=10, pady=10)

        # AI color selection
        self.ai_as_white_button = tk.Button(
            self.controls_frame, text="AI as White", command=lambda: self.select_ai_player(1), width=10, height=1)
        self.ai_as_black_button = tk.Button(
            self.controls_frame, text="AI as Black", command=lambda: self.select_ai_player(2), width=10, height=1)
        self.ai_level_label = tk.Label(
            self.controls_frame, text="AI Player level:", width=15, height=2)
        self.ai_level_input = tk.Scale(
            self.controls_frame, from_=1, to=11, orient="horizontal", length=200)

        self.maxDuration_label = tk.Label(
            self.controls_frame, text="AI time limit", width=20, height=2)
        self.maxDuration_input = tk.Entry(self.controls_frame, width=15)
        self.maxDuration_input.insert(0, "0.2")

        # create a button to start the game
        self.start_button = tk.Button(
            self.controls_frame, text="START GAME", command=self.start_game, width=20, height=3, bg="blue", fg="white")
        self.start_button.grid(row=12, column=0, pady=50)

        # create a button to undo the last move
        self.undo_button = tk.Button(
            self.controls_frame, text="UNDO", command=self.undo, width=20, height=3, bg="orange")
        self.undo_button.grid(row=12, column=1, pady=50)

        # create labels for player scores and current player
        self.score_label1 = tk.Label(
            self.controls_frame, text="Black: 2", width=15, height=2, font=("Arial", 14))
        self.score_label1.grid(row=14, column=0, padx=10, pady=10)

        self.score_label2 = tk.Label(
            self.controls_frame, text="White: 2", width=15, height=2, font=("Arial", 14))
        self.score_label2.grid(row=14, column=1, padx=10, pady=10)

        self.current_player_label = tk.Label(
            self.controls_frame, text="Current Player: Black", width=20, height=2,
            # make the font in the middle of the label
            anchor="center", font=("Arial", 14))
        self.current_player_label.grid(row=13, column=0, padx=0, pady=10)

        self.ai_level_label.grid(row=8, column=0)
        self.ai_level_input.grid(row=8, column=1)
        self.maxDuration_label.grid(row=9, column=0)
        self.maxDuration_input.grid(row=9, column=1)
        self.ai_as_white_button.grid(row=10, column=0)
        self.ai_as_black_button.grid(row=10, column=1)
        self.game = ReversiGame()
        self.draw_board()
        self.gameStack = []
        self.storeGame()

        # make as if human vs human button was clicked
        self.select_game_mode("human_vs_human")

    def select_game_mode(self, mode):
        self.game_mode.set(mode)
        if mode == "human_vs_human":
            self.human_vs_human_button.config(bg="green")
            self.human_vs_ai_button.config(bg=self.master.cget("bg"))

            self.ai_as_white_button.config(state="disabled")
            self.ai_as_black_button.config(state="disabled")
            self.ai_level_label.config(state="disabled")
            self.ai_level_input.config(state="disabled")
            self.maxDuration_label.config(state="disabled")
            self.maxDuration_input.config(state="disabled")
        elif mode == "human_vs_ai":
            self.human_vs_human_button.config(bg=self.master.cget("bg"))
            self.human_vs_ai_button.config(bg="green")

            self.ai_as_white_button.config(state="normal")
            self.ai_as_black_button.config(state="normal")
            self.ai_level_label.config(state="normal")
            self.ai_level_input.config(state="normal")
            self.maxDuration_label.config(state="normal")
            self.maxDuration_input.config(state="normal")

    def select_ai_player(self, player):
        self.ai_player.set(player)
        if player == 1:
            self.ai_as_white_button.config(bg="green")
            self.ai_as_black_button.config(bg=self.master.cget("bg"))
        elif player == 2:
            self.ai_as_white_button.config(bg=self.master.cget("bg"))
            self.ai_as_black_button.config(bg="green")

    def storeGame(self):
        Bcopy = self.game.get_Bcopy()
        self.gameStack.append(Bcopy)

    def undo(self, event=None):
        if len(self.gameStack) > 1:
            self.gameStack.pop()
            Bcopy = copy.deepcopy(self.gameStack[-1])
            self.game = ReversiGame()
            self.game.set_Bcopy(Bcopy)
            self.update_scores()  # update player scores
            self.draw_board()  # draw the board
            self.highlight_valid_squares()  # highlight valid squares after each move

    def draw_board(self):
        self.canvas.delete("piece")
        if self.game:
            for i in range(8):
                for j in range(8):
                    x1, y1 = j * 75, i * 75
                    x2, y2 = (j + 1) * 75, (i + 1) * 75
                    if (i+j) % 2 == 0:
                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="#00810e", outline="")
                    else:
                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="#009e12", outline="")
                    if self.game.board[i][j] == 1:
                        self.canvas.create_oval(
                            x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white", tags="piece")
                    elif self.game.board[i][j] == 2:
                        self.canvas.create_oval(
                            x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black", tags="piece")

    def start_game(self):
        if self.game:
            del self.game
        self.game = ReversiGame()

        # create ai players
        if self.game_mode.get() != "human_vs_human":
            self.level = int(self.ai_level_input.get())
            self.maxDuartion = float(self.maxDuration_input.get())
            self.ai_player_white = ReversiAI(1, self.level, self.maxDuartion)
            self.ai_player_black = ReversiAI(2, self.level, self.maxDuartion)

        # update player scores and current player label
        self.score_label1.config(text=f"Black: {self.game.score1}")
        self.score_label2.config(text=f"White: {self.game.score2}")
        if self.game.current_player == 1:
            self.current_player_label.config(text="Current Player: White")
        else:
            self.current_player_label.config(text="Current Player: Black")

        # resize canvas and draw board
        # self.canvas.config(width=400, height=400)
        self.draw_board()

        self.highlight_valid_squares()  # highlight valid squares in the first move
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)

        # change button text to "Restart"
        self.start_button.config(text="Restart", command=self.restart_game)

        # disable game mode selection
        self.disable_game_mode_selection()

        self.gameStack = []
        self.storeGame()

    def on_motion(self, event):

        if self.game_mode.get() == "ai_vs_ai":
            return
        if self.game_mode.get() == "human_vs_ai" and self.game.current_player == self.ai_player.get():
            return

        self.highlight_mouse_hover(event)

    def disable_game_mode_selection(self):
        self.human_vs_human_button.config(state="disabled")
        self.human_vs_ai_button.config(state="disabled")
        self.ai_as_white_button.config(state="disabled")
        self.ai_as_black_button.config(state="disabled")
        self.ai_level_label.config(state="disabled")
        self.ai_level_input.config(state="disabled")
        self.maxDuration_label.config(state="disabled")
        self.maxDuration_input.config(state="disabled")

    def enable_game_mode_selection(self):
        self.human_vs_human_button.config(state="normal")
        self.human_vs_ai_button.config(state="normal")
        self.ai_as_white_button.config(state="normal")
        self.ai_as_black_button.config(state="normal")
        self.ai_level_label.config(state="normal")
        self.ai_level_input.config(state="normal")
        self.maxDuration_label.config(state="normal")
        self.maxDuration_input.config(state="normal")

    def human_move(self, event):
        col = event.x // 75
        row = event.y // 75
        if self.game.make_move(row, col):

            self.update_scores()  # update player scores

            self.draw_board()
            self.check_game_over()  # check if game is over
            self.highlight_valid_squares()  # highlight valid squares after each move
            self.highlight_latest_move(row, col)  # highlight latest move
            self.storeGame()

            if self.game_mode.get() == "human_vs_ai" and self.game.current_player == self.ai_player.get():
                # Schedule AI move after a delay
                self.master.after(20, self.ai_move)
                # self.ai_move()
        else:
            # do not delete faded squares if move is invalid
            pass

    def ai_move(self):

        start = time.time()
        board = self.game.board.copy()

        if self.game_mode.get() == "human_vs_ai":
            if self.ai_player.get() == 1:
                move = self.ai_player_white.get_move(board)
            elif self.ai_player.get() == 2:
                move = self.ai_player_black.get_move(board)

        elif self.game_mode.get() == "ai_vs_ai":
            if self.game.current_player == 1:
                move = self.ai_player_white.get_move(board)
            elif self.game.current_player == 2:
                move = self.ai_player_black.get_move(board)

        dur = int((time.time() - start) * 1000)
        if dur < 400:
            # delay AI move if it is too fast
            self.master.after(400 - dur)

        row, col = move

        if self.game.make_move(row, col):
            self.update_scores()  # update player scores

            self.draw_board()
            self.check_game_over()  # check if game is over
            self.highlight_valid_squares()  # highlight valid squares after each move
            self.highlight_latest_move(row, col)  # highlight latest move
            self.storeGame()
        else:
            # do not delete faded squares if move is invalid
            pass

    def on_click(self, event):

        if self.game_mode.get() == "human_vs_human":
            self.human_move(event)

        elif self.game_mode.get() == "human_vs_ai":

            if self.game.current_player == self.ai_player.get():
                self.ai_move()
            else:
                self.human_move(event)

        elif self.game_mode.get() == "ai_vs_ai":
            self.ai_move()

    def check_game_over(self):
        if self.game.is_game_over():
            self.end_game()

    def end_game(self):
        winner = self.game.get_winner()
        if winner == 1:
            messagebox.showinfo("Game Over", "White wins!")
        elif winner == 2:
            messagebox.showinfo("Game Over", "Black wins!")
        else:
            messagebox.showinfo("Game Over", "Tie game!")

    def highlight_mouse_hover(self, event):
        self.canvas.delete("mouse_square")
        col = event.x // 75
        row = event.y // 75
        x1, y1 = col * 75 + 10, row * 75 + 10
        x2, y2 = (col + 1) * 75 - 10, (row + 1) * 75 - 10
        if self.game.current_player == 2:
            outline_color = "#000000"  # black if black to move
        else:
            outline_color = "#FFFFFF"  # white if white to move
        self.canvas.create_oval(
            x1, y1, x2, y2, fill=outline_color, outline=outline_color, tags="mouse_square")

    def highlight_valid_squares(self):
        valid_moves = self.game.get_valid_moves()
        self.canvas.delete("valid_square")
        for move in valid_moves:
            row, col = move
            x1, y1 = col * 75 + 10, row * 75 + 10
            x2, y2 = (col + 1) * 75 - 10, (row + 1) * 75 - 10
            if self.game.current_player == 2:
                outline_color = "#000000"  # black if black to move
            else:
                outline_color = "#FFFFFF"  # white if white to move
            self.canvas.create_oval(
                x1, y1, x2, y2, fill="", outline=outline_color, tags="valid_square")

    def highlight_latest_move(self, row, col):
        x, y = col * 75 + 37, row * 75 + 37
        radius = 12
        fill_color = "#808080"  # blend of black and white
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline="#000000", tags="latest_move")

    def update_scores(self):
        self.game.update_scores()
        self.score_label1.config(text=f"Black: {self.game.score2}")
        self.score_label2.config(text=f"White: {self.game.score1}")
        if self.game.current_player == 1:
            self.current_player_label.config(text="Current Player: White")
        else:
            self.current_player_label.config(text="Current Player: Black")

    def restart_game(self):

        if self.game:
            del self.game
        self.game = ReversiGame()

        # update player scores and current player label
        self.score_label1.config(text=f"Black: {self.game.score1}")
        self.score_label2.config(text=f"White: {self.game.score2}")
        if self.game.current_player == 1:
            self.current_player_label.config(text="Current Player: White")
        else:
            self.current_player_label.config(text="Current Player: Black")

        self.draw_board()

        # unbind click event
        self.canvas.unbind("<Button-1>")

        # enable game mode selection
        self.enable_game_mode_selection()

        self.start_button.config(text="Start Game", command=self.start_game)

        # select the last selected game mode
        self.select_game_mode(self.game_mode.get())

class ReversiGame:
    def __init__(self):
        self.board = [[0] * 8 for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = 2
        self.current_player = 2
        self.score1 = 2
        self.score2 = 2

    def get_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0 and self.is_valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves

    def is_valid_move(self, row, col):
        if self.board[row][col] != 0:
            return False
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            if self.board[r][c] == 3 - self.current_player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - self.current_player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            if self.board[r][c] == 3 - self.current_player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - self.current_player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    r, c = row + dr, col + dc
                    while self.board[r][c] == 3 - self.current_player:
                        self.board[r][c] = self.current_player
                        r += dr
                        c += dc
        self.current_player = 3 - self.current_player
        self.update_scores()
        return True

    def update_scores(self):
        self.score1 = sum(row.count(1) for row in self.board)
        self.score2 = sum(row.count(2) for row in self.board)

    def is_game_over(self):
        return not self.get_valid_moves()

    def get_winner(self):
        if self.score1 > self.score2:
            return 1
        elif self.score2 > self.score1:
            return 2
        else:
            return 0

    def get_Bcopy(self):
        Bcopy = [self.board,
                self.current_player,
                self.score1,
                self.score2]
        return copy.deepcopy(Bcopy)

    def set_Bcopy(self, Bcopy):
        self.board = Bcopy[0]
        self.current_player = Bcopy[1]
        self.score1 = Bcopy[2]
        self.score2 = Bcopy[3]
        
class ReversiAI:

    def __init__(self, player, level=1, maxDuration=1):
        self.player = player
        self.level = level
        self.maxDuration = maxDuration

    def get_valid_moves(self, board, player):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j] == 0 and self.is_valid_move(i, j, board, player):
                    valid_moves.append((i, j))
        return valid_moves

    def is_valid_move(self, row, col, board, player):
        if board[row][col] != 0:
            return False
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            if board[r][c] == 3 - player:
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == 3 - player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    return True
        return False

    def get_corner_moves(self, valid_moves):
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for corner in corners:
            if corner in valid_moves:
                return corner
        return None

    def get_move_by_level(self, board, valid_moves, depth):
        max_eval = -math.inf
        best_move = None
        for move in valid_moves:
            board_copy = copy.deepcopy(board)
            board_copy = self.make_move(board_copy, move, self.player)
            # eval = self.minmax(board_copy, depth, 3 - self.player)
            eval = self.minmax_alpha_beta(
                board_copy, depth, 3 - self.player, -math.inf, math.inf)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def iterative_deepening(self, board, valid_moves, maxDepth):
        maxDuration = self.maxDuration
        for depth in range(1, maxDepth + 1, 1):
            startitr = time.time()
            best_move = self.get_move_by_level(board, valid_moves, depth)
            duration = time.time() - startitr
            maxDuration -= duration
            if maxDuration < 2 * duration:
                break
        return best_move

    def get_move(self, board):
        valid_moves = self.get_valid_moves(board, self.player)
        corner_move = self.get_corner_moves(valid_moves)
        if corner_move and self.level > 3:
            return corner_move

        maxDepth = max(self.level // 2, 1) if self.level <= 5 else self.level - 3
        best_move = self.iterative_deepening(board, valid_moves, maxDepth)
        return best_move

    def minmax_alpha_beta(self, board, depth, maximizing_player, alpha=-math.inf, beta=math.inf):

        valid_moves = self.get_valid_moves(board, maximizing_player)

        if depth == 0 or len(valid_moves) == 0:
            return self.evaluate(board)

        if maximizing_player == self.player:
            max_eval = -math.inf
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy = self.make_move(
                    board_copy, move, maximizing_player)
                eval = self.minmax_alpha_beta(
                    board_copy, depth - 1, 3 - self.player, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                board_copy = self.make_move(
                    board_copy, move, maximizing_player)
                eval = self.minmax_alpha_beta(
                    board_copy, depth - 1, self.player, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_move(self, board, move, player):
        row, col = move
        if not self.is_valid_move(row, col, board, player):
            return False
        board[row][col] = player
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            if not (0 <= r < 8 and 0 <= c < 8):
                continue
            if board[r][c] == 3 - player:
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == 3 - player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    r, c = row + dr, col + dc
                    while board[r][c] == 3 - player:
                        board[r][c] = player
                        r += dr
                        c += dc
        return board
    def evaluate(self, board):

            coin_parity = self.evaluate_coin_parity(board)
            mobility = self.evaluate_mobility(board)
            corners = self.evaluate_corners(board)
            stability = self.evaluate_stability(board)

            eval = coin_parity + (self.level > 2) * mobility + \
                (self.level > 3) * corners + (self.level > 4) * stability

            return eval

    def evaluate_coin_parity(self, board):

        score1 = sum(row.count(1) for row in board)
        score2 = sum(row.count(2) for row in board)
        if self.player == 1:
            return score1 - score2
        else:
            return score2 - score1

    def evaluate_mobility(self, board):
        return len(self.get_valid_moves(board, self.player)) - len(self.get_valid_moves(board, 3 - self.player))

    def evaluate_corners(self, board):
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        score = 0
        for corner in corners:
            if board[corner[0]][corner[1]] == self.player:
                score += 1
            elif board[corner[0]][corner[1]] == 3 - self.player:
                score -= 1
        return score * 25

    def evaluate_stability(self, board):
        utlMatrix = np.array([[4, -3, 2, 2, 2, 2, -3, 4],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 0, 1, 1, 0, -1, 2],
                              [2, -1, 1, 0, 0, 1, -1, 2],
                              [-3, -4, -1, -1, -1, -1, -4, -3],
                              [4, -3, 2, 2, 2, 2, -3, 4]])
        maxmat = np.array(board) == self.player
        minmat = np.array(board) == 3 - self.player
        maxscore = np.sum(utlMatrix * maxmat)
        minscore = np.sum(utlMatrix * minmat)
        return maxscore - minscore


def main():
    root = tk.Tk()
    gui = ReversiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()