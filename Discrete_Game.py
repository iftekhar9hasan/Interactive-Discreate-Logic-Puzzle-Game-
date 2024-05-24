import tkinter as tk
from tkinter import messagebox  # Correct import statement
import random

possible_clues = [
    "The killer used a knife and a gun.",
    "The killer used a knife or a gun.",
    "Melkor or Saruman were suspected",
    "Sauron and Gollum were suspected",
    "The killer has money and jealousy as a motive.",
    "The killer has money or jealousy as a motive."
]

# The game logic functions
def generate_puzzle(size):
    puzzle = []
    for _ in range(size):
        row_list = []
        for _ in range(size):
            num = random.choice([0, 1])
            row_list.append(num)
        puzzle.append(row_list)
    return puzzle

def check_rows(puzzle):
    for i in range(len(puzzle)):
        row = puzzle[i]
        if all(row):
            return i
    return -1

def display_puzzle(puzzle_frame, symbols, puzzle, names, motives, size):
    # Clear the existing puzzle display
    for widget in puzzle_frame.winfo_children():
        widget.destroy()

    # Display the top labels for each column
    for j in range(size):
        top_label = tk.Label(puzzle_frame, text=motives[j], font=("Helvetica", 14), width=6, height=2, relief="ridge")
        top_label.grid(row=0, column=j + 1, padx=2, pady=2)

    # Display puzzle as a table with names and symbols
    for i in range(size):
        # Display the name on the left side
        name_label = tk.Label(puzzle_frame, text=names[i], font=("Helvetica", 14), width=16, height=2, relief="ridge", anchor='w')
        name_label.grid(row=i + 1, column=0, padx=2, pady=2)

        for j in range(size):
            # Display the symbol with color
            value = puzzle[i][j]
            color = "red" if value == 0 else "green"
            label = tk.Label(puzzle_frame, text=symbols[value], font=("Helvetica", 14), width=6, height=2, relief="ridge", fg=color)
            label.grid(row=i + 1, column=j + 1, padx=2, pady=2)

def update_puzzle(root, puzzle_frame, symbols, puzzle, names, motives, size, row_input, col_input, value_input, correct_killer):
    try:
        row = int(row_input.get())
        col = int(col_input.get())
        value = int(value_input.get())

        if 0 <= row < size and 0 <= col < size and value in [0, 1]:
            puzzle[row][col] = value
            display_puzzle(puzzle_frame, symbols, puzzle, names, motives, size)
            killer_index = check_rows(puzzle)
            if killer_index != -1:
                selected_killer = names[killer_index]
                if selected_killer == correct_killer:
                    messagebox.showinfo("Game Over", f"Congratulations! The killer is {correct_killer}.")
                    root.destroy()
                else:
                    messagebox.showinfo("Game Over", f"Wrong choice! The real killer is {correct_killer}.")

            # Clear the input fields
            row_input.delete(0, tk.END)
            col_input.delete(0, tk.END)
            value_input.delete(0, tk.END)

        else:
            messagebox.showerror("Error", "Invalid input. Row and Column should be between 0 and 3, and Value should be 0 or 1.")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def start_game(root):
    # Destroy the welcome frame
    welcome_frame.destroy()

    # Initialize game variables
    size = 4
    puzzle = generate_puzzle(size)
    names = ["Melkor", "Sauron", "Saruman", "Gollum"]
    motives = ["🔫", "🔪", "💸", "😏"]
    symbols = {0: "❌", 1: "✔️"}

    # Select a random killer based on clues
    correct_killer_index = random.randint(0, size - 1)
    correct_killer = names[correct_killer_index]

    def reset_game():
        # Restart the game in a new screen
        new_root = tk.Tk()
        new_root.title("Logic Puzzle Challenge")
        new_root.geometry(root.geometry())  # Maintain the window size
        welcome_screen(new_root)

    # Create a frame for clues
    clues_frame = tk.Frame(root)
    clues_frame.pack()

    # Display "Clues" label
    clues_label_title = tk.Label(clues_frame, text="Clues", font=("Helvetica", 12, "bold"))
    clues_label_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=3)

    # Randomly select three clues
    random_clues = random.sample(possible_clues, 3)

    # Display clues in a rectangular shape
    for i, clue_text in enumerate(random_clues):
        clue_box = tk.Frame(clues_frame, bd=2, relief="ridge")
        clue_box.grid(row=1, column=i, padx=5, pady=5, sticky="w")

        clue_label = tk.Label(clue_box, text=clue_text, font=("Helvetica", 12), wraplength=400, anchor="w")
        clue_label.pack(padx=5, pady=5)

    # Create a frame for puzzle display
    puzzle_frame = tk.Frame(root)
    puzzle_frame.pack()

    # Display the puzzle
    display_puzzle(puzzle_frame, symbols, puzzle, names, motives, size)

    # Create a frame for game rules
    rules_frame = tk.Frame(root)
    rules_frame.pack()

    # Display game rules
    rules_title_label = tk.Label(rules_frame, text="Game Rules", font=("Helvetica", 12, "bold"))
    rules_title_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="n", padx=5)
 
    rules_text = "1. The puzzle consists of a 4x4 grid. Each cell in the grid can be filled with either ❌ (0) or ✔️ (1).\n" \
                 "2. Your goal is to identify the row where all cells are filled with ✔️ (1).\n" \
                 "3. Enter the row, column, and value (0 or 1) to fill a cell.\n" \
                 "4. Click the 'Submit' button to update the puzzle.\n" \
                 "5. Solve the puzzle and find the killer!\n"
    
    rules_label = tk.Label(rules_frame, text=rules_text, font=("Helvetica", 12), anchor="w", justify="left")
    rules_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    

    # Create a frame for user inputs
    input_frame = tk.Frame(root)
    input_frame.pack()

    # Row input
    row_label = tk.Label(input_frame, text="Row (0-3):")
    row_label.grid(row=0, column=0)
    row_input = tk.Entry(input_frame)
    row_input.grid(row=0, column=1)

    # Column input
    col_label = tk.Label(input_frame, text="Column (0-3):")
    col_label.grid(row=1, column=0)
    col_input = tk.Entry(input_frame)
    col_input.grid(row=1, column=1)

    # Value input
    value_label = tk.Label(input_frame, text="Value (0 or 1):")
    value_label.grid(row=2, column=0)
    value_input = tk.Entry(input_frame)
    value_input.grid(row=2, column=1)

    # Submit button
    submit_button = tk.Button(
        input_frame,
        text="Submit",
        command=lambda: update_puzzle(
            root,
            puzzle_frame,
            symbols,
            puzzle,
            names,
            motives,
            size,
            row_input,
            col_input,
            value_input,
            correct_killer,
        ),
    )
    submit_button.grid(row=3, column=0, columnspan=2)

    # Reset button
    reset_button = tk.Button(input_frame, text="Reset Game", command=reset_game)
    reset_button.grid(row=4, column=0, columnspan=2, pady=10)

def welcome_screen(root):
    global welcome_frame
    welcome_frame = tk.Frame(root)
    welcome_frame.pack()

    welcome_msg = "Welcome to Logic Puzzle Challenge!\n" \
                  "Solve the puzzle to find the killer!"
    welcome_label = tk.Label(welcome_frame, text=welcome_msg, font=("Helvetica", 16, "bold"))
    welcome_label.pack()

    start_button = tk.Button(welcome_frame, text="Start Game", command=lambda: start_game(root))
    start_button.pack(pady=120)

# Create the Tkinter window
root = tk.Tk()
root.title("Logic Puzzle Challenge")

# Welcome screen
welcome_screen(root)

root.mainloop()