import tkinter as tk
import math

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    return None

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(best_score, score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        
        # Game board and controls
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        
        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.tie_score = 0
        
        self.create_start_screen()

    def create_start_screen(self):
        # Create a frame for the start screen
        start_frame = tk.Frame(self.window)
        start_frame.grid(row=0, column=0)

        # Add a label prompting the user to choose
        tk.Label(start_frame, text="Who should start?", font=("Arial", 18)).grid(row=0, column=0, columnspan=2)

        # Add buttons for player or AI to start
        tk.Button(start_frame, text="Player", font=("Arial", 14),
                  command=lambda: self.start_game(True, start_frame)).grid(row=1, column=0)
        tk.Button(start_frame, text="AI", font=("Arial", 14),
                  command=lambda: self.start_game(False, start_frame)).grid(row=1, column=1)

    def start_game(self, player_starts, start_frame):
        # Destroy the start screen
        start_frame.destroy()

        # Set who starts
        self.player_turn = player_starts

        # Create the score display
        self.create_score_display()

        # Create the game buttons
        self.create_buttons()

        # If AI starts, make the first move
        if not self.player_turn:
            self.ai_move()

    def create_score_display(self):
        # Create labels for the scores
        self.player_score_label = tk.Label(self.window, text=f"Player: {self.player_score}", font=("Arial", 14))
        self.player_score_label.grid(row=0, column=0)
        
        self.ai_score_label = tk.Label(self.window, text=f"AI: {self.ai_score}", font=("Arial", 14))
        self.ai_score_label.grid(row=0, column=1)
        
        self.tie_score_label = tk.Label(self.window, text=f"Ties: {self.tie_score}", font=("Arial", 14))
        self.tie_score_label.grid(row=0, column=2)

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text=" ", font=("Arial", 24), height=2, width=5,
                                               command=lambda row=i, col=j: self.player_move(row, col))
                self.buttons[i][j].grid(row=i+1, column=j)

    def player_move(self, row, col):
        if self.board[row][col] == " " and self.player_turn:
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X")
            self.player_turn = False
            self.check_game_state()
            if not self.player_turn:
                self.ai_move()

    def ai_move(self):
        move = best_move(self.board)
        if move:
            row, col = move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
        self.player_turn = True
        self.check_game_state()

    def check_game_state(self):
        winner = check_winner(self.board)
        if winner:
            if winner == "X":
                self.player_score += 1
                self.update_score_display()
                self.end_game("Player wins!")
            elif winner == "O":
                self.ai_score += 1
                self.update_score_display()
                self.end_game("AI wins!")
        elif is_full(self.board):
            self.tie_score += 1
            self.update_score_display()
            self.end_game("It's a tie!")

    def update_score_display(self):
        # Update the score labels
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.ai_score_label.config(text=f"AI: {self.ai_score}")
        self.tie_score_label.config(text=f"Ties: {self.tie_score}")

    def end_game(self, message):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)
        
        # Display the game result
        tk.Label(self.window, text=message, font=("Arial", 18)).grid(row=4, column=0, columnspan=3)
        
        # Add a Restart button
        restart_button = tk.Button(self.window, text="Restart", font=("Arial", 14), command=self.restart_game)
        restart_button.grid(row=5, column=0, columnspan=3)

    def restart_game(self):
        # Reset the board and player turn
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player_turn = True  # Reset to default or ask again who starts

        # Clear the buttons and enable them
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state=tk.NORMAL)

        # Remove any result messages or restart button
        for widget in self.window.grid_slaves():
            if int(widget.grid_info()["row"]) > 3:  # Remove elements in rows 4 and 5
                widget.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
