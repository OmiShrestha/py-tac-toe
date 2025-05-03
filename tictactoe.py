# Import necessary modules for GUI and message boxes
import tkinter as tk
from tkinter import messagebox

# Function to check if a player has won the game
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(cell == player for cell in board[i]):  # rows
            return True
        if all(row[i] == player for row in board):    # columns
            return True
    if all(board[i][i] == player for i in range(3)):  # main diagonal
        return True
    if all(board[i][2 - i] == player for i in range(3)):  # anti-diagonal
        return True
    return False

# Function to check if the board is full (tie condition)
def is_full(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)

# Function to handle a player's move when a button is clicked
def on_click(row, col):
    global current_player, board, buttons

    # Ensure the clicked cell is empty before proceeding
    if board[row][col] != ' ':
        return

    board[row][col] = current_player
    buttons[row][col].config(text=current_player, state="disabled")

    # Check for a winner or tie after the move
    if check_winner(board, current_player):
        messagebox.showinfo("Game Over", f"Player {current_player} wins!")
        reset_game()
    elif is_full(board):
        messagebox.showinfo("Game Over", "The game is a tie!")
        reset_game()
    else:
        current_player = 'O' if current_player == 'X' else 'X'

# Function to reset the game board and start a new game
def reset_game():
    global board, buttons, current_player
    # Reset the board and button states
    current_player = 'X'
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state="normal")

# Main function to initialize the GUI and start the game loop
def main():
    global buttons, board, current_player

    # Initialize the game state and GUI elements
    current_player = 'X'
    board = [[' ' for _ in range(3)] for _ in range(3)]

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                          command=lambda r=row, c=col: on_click(r, c))
            buttons[row][col].grid(row=row, column=col)

    # Create a reset button to restart the game
    reset_button = tk.Button(root, text="Reset", font=('Arial', 14), command=reset_game)
    reset_button.grid(row=3, column=0, columnspan=3)

    # Start the GUI event loop
    root.mainloop()

# Entry point of the script
if __name__ == '__main__':
    main()
