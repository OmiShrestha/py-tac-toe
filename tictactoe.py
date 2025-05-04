# Author: Omi Shrestha

# Imports
import tkinter as tk
from tkinter import messagebox

# Global variables for scores
score_x = 0
score_o = 0

# Function to check if a player has won the game
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(cell == player for cell in board[i]):        # rows
            return True
        if all(row[i] == player for row in board):          # columns
            return True
    if all(board[i][i] == player for i in range(3)):        # main diagonal
        return True
    if all(board[i][2 - i] == player for i in range(3)):    # anti-diagonal
        return True
    return False

# Function to check if the board is full (TIE)
def is_full(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)

# Function for the AI to make a move
def ai_move():
    global current_player, board, buttons, status_label

    # Simple AI logic: prioritize winning, blocking, or random moves
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':  # Check empty cell
                # Simulate AI move
                board[row][col] = 'O'
                if check_winner(board, 'O'):
                    buttons[row][col].config(text='O', state="disabled", disabledforeground="red")
                    return
                board[row][col] = ' '  # Undo move

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':  # Check empty cell
                # Simulate blocking move
                board[row][col] = 'X'
                if check_winner(board, 'X'):
                    board[row][col] = 'O'
                    buttons[row][col].config(text='O', state="disabled", disabledforeground="red")
                    return
                board[row][col] = ' '  # Undo move

    # If no winning or blocking move, pick the first available cell
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                buttons[row][col].config(text='O', state="disabled", disabledforeground="red")
                return

# Modify the on_click function to include AI's turn
def on_click(row, col):
    global current_player, board, buttons, status_label, score_x, score_o, score_label

    # Ensure the clicked cell is empty before proceeding
    if board[row][col] != ' ':
        return

    board[row][col] = current_player
    buttons[row][col].config(text=current_player, state="disabled",
                             disabledforeground="blue" if current_player == 'X' else "red")

    # Check for a winner or tie after the move
    if check_winner(board, current_player):
        if current_player == 'X':
            score_x += 1
        else:
            score_o += 1
        score_label.config(text=f"> X: {score_x} | O: {score_o}")
        messagebox.showinfo("Game Over", f"Player {current_player} wins!")
        reset_game()
    elif is_full(board):
        messagebox.showinfo("Game Over", "The game is a tie!")
        reset_game()
    else:
        current_player = 'O' if current_player == 'X' else 'X'
        status_label.config(text=f"Player {current_player}'s Turn")

        # If it's AI's turn, make the AI move
        if current_player == 'O':
            ai_move()
            if check_winner(board, 'O'):
                score_o += 1
                score_label.config(text=f"> X: {score_x} | O: {score_o}")
                messagebox.showinfo("Game Over", "Player O wins!")
                reset_game()
            elif is_full(board):
                messagebox.showinfo("Game Over", "The game is a tie!")
                reset_game()
            else:
                current_player = 'X'
                status_label.config(text=f"Player {current_player}'s Turn")

# Function to reset the game board and start a new game
def reset_game():
    global board, buttons, current_player, status_label
    # Reset the board and button states
    current_player = 'X'
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state="normal", bg="lightgray")
    status_label.config(text="Player X's Turn")

# Function to reset the scores
def reset_scores():
    global score_x, score_o, score_label
    score_x = 0
    score_o = 0
    score_label.config(text=f"Score -> X: {score_x} | O: {score_o}")

# Main function to initialize the GUI and start the game loop
def main():
    global buttons, board, current_player, status_label, score_label

    # Initialize the game state and GUI elements
    current_player = 'X'
    board = [[' ' for _ in range(3)] for _ in range(3)]

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    # Center the window on the screen
    window_width, window_height = 400, 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Add a title label
    title_label = tk.Label(root, text="Tic-Tac-Toe", font=('Arial', 24, 'bold'), pady=10)
    title_label.pack()

    # Add a status label to show the current player's turn
    status_label = tk.Label(root, text="Player X's Turn", font=('Arial', 14))
    status_label.pack()

    # Add a score label to display the scores
    score_label = tk.Label(root, text=f"Score -> X: {score_x} | O: {score_o}", font=('Arial', 14))
    score_label.pack()

    # Create a frame for the game board
    board_frame = tk.Frame(root)
    board_frame.pack(pady=20)

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(board_frame, text='', font=('Arial', 24), width=5, height=2,
                                          bg="lightgray", command=lambda r=row, c=col: on_click(r, c))
            buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

    # Create a reset button to restart the game
    reset_button = tk.Button(root, text="Reset Game", font=('Arial', 14), command=reset_game)
    reset_button.pack(pady=5)

    # Create a reset scores button
    reset_scores_button = tk.Button(root, text="Reset Scores", font=('Arial', 14), command=reset_scores)
    reset_scores_button.pack(pady=5)

    # Start the GUI event loop
    root.mainloop()

# Entry point of the script
if __name__ == '__main__':
    main()
