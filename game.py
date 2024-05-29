import tkinter as tk
from PIL import Image, ImageTk
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.current_level = 1
        self.score = Score(self.root)
        self.start_screen = StartScreen(self.root, self.start_game)
        self.game_window = None
        self.game_over_screen = None

    def start_game(self):
        self.start_screen.hide()
        self.load_level(self.current_level)

    def load_level(self, level):
        self.game_window = GameWindow(self.root, level, self.end_game, self.score)
        self.game_window.start()

    def end_game(self):
        self.game_window.hide()
        self.game_over_screen = GameOverScreen(self.root, self.restart_game)

    def restart_game(self):
        self.game_over_screen.hide()
        self.current_level = 1
        self.score.reset()
        self.start_game()

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.grid_size = 5 + level_number  # Increase grid size with level
        self.words = self.generate_words()

    def generate_words(self):
        # List of possible words
        possible_words = ["PYTHON", "JAVA", "RUBY", "JAVASCRIPT", "SWIFT", "C", "C++", "HTML", "CSS", "PHP", "PYTHONIC", "JAVAEE", "SQL"]

        # Randomly select words based on level
        num_words = min(5 + self.level_number, len(possible_words))  
        words = random.sample(possible_words, num_words)
        return words

class Grid:
    def __init__(self, canvas, level):
        self.canvas = canvas
        self.level = level
        self.size = self.level.grid_size
        self.grid = self.create_grid()  
        self.selected_letters = []
        self.selected_positions = []

    def create_grid(self):
        grid = [['' for _ in range(self.size)] for _ in range(self.size)]
        for word in self.level.words:
            placed = False
            while not placed:
                direction = random.choice(['horizontal', 'vertical'])
                if direction == 'horizontal':
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, max(0, self.size - len(word)))  # Ensure non-negative range
                    if all(grid[row][col + i] in ('', letter) for i, letter in enumerate(word)):
                        for i, letter in enumerate(word):
                            grid[row][col + i] = letter
                        placed = True
                else:
                    row = random.randint(0, max(0, self.size - len(word)))  # Ensure non-negative range
                    col = random.randint(0, self.size - 1)
                    if all(grid[row + i][col] in ('', letter) for i, letter in enumerate(word)):
                        for i, letter in enumerate(word):
                            grid[row + i][col] = letter
                        placed = True
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == '':
                    grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return grid

    def display(self):
        for i, row in enumerate(self.grid):
            for j, letter in enumerate(row):
                self.canvas.create_text(50 + j * 30, 50 + i * 30, text=letter, font=('Helvetica', 20), fill='white')

    def select_letter(self, x, y):
        row, col = (y - 35) // 30, (x - 35) // 30
        if 0 <= row < self.size and 0 <= col < self.size and (row, col) not in self.selected_positions:
            self.selected_positions.append((row, col))
            self.selected_letters.append(self.grid[row][col])
            self.canvas.create_rectangle(35 + col * 30, 35 + row * 30, 65 + col * 30, 65 + row * 30, outline='yellow', tags="selection")
            return ''.join(self.selected_letters)
        return ''

class WordList:
    def __init__(self, canvas, level):
        self.canvas = canvas
        self.words = level.words
        self.found_words = []
        self.display()

    def display(self):
        for i, word in enumerate(self.words):
            self.canvas.create_text(400, 50 + i * 30, text=word, font=('Arial', 20), tags=word, fill='white')

    def mark_word_found(self, word):
        if word in self.words and word not in self.found_words:
            self.found_words.append(word)
            self.canvas.itemconfig(word, fill='yellow') 

class GameWindow:
    def __init__(self, root, level, end_game_callback, score):
        self.root = root
        self.level = Level(level)
        self.end_game_callback = end_game_callback
        self.canvas = tk.Canvas(self.root, width=800, height=600)  # Fixed dimensions
        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((500, 300)))  
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.grid = Grid(self.canvas, self.level)
        self.word_list = WordList(self.canvas, self.level)
        self.score = score

        self.canvas.bind('<Button-1>', self.on_click)

    def start(self):
        self.canvas.pack()
        self.grid.display()

    def on_click(self, event):
        word = self.grid.select_letter(event.x, event.y)
        if word:
            self.check_word(word)

    def check_word(self, word):
        if word in self.level.words and word not in self.word_list.found_words:
            self.word_list.mark_word_found(word)
            self.score.increase()
            self.grid.selected_letters = []
            self.grid.selected_positions = []
            self.canvas.delete("selection")

        if set(self.word_list.found_words) == set(self.level.words):
            self.end_game_callback()

    def hide(self):
        self.canvas.pack_forget()


class StartScreen:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        self.frame = tk.Frame(self.root)
        self.label = tk.Label(self.frame, text="Word Finder Game", font=('Helvetica', 24))
        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game_callback)

        self.label.pack()
        self.start_button.pack()
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

class GameOverScreen:
    def __init__(self, root, restart_game_callback):
        self.root = root
        self.restart_game_callback = restart_game_callback
        self.frame = tk.Frame(self.root)
        self.label = tk.Label(self.frame, text="Game Over", font=('Helvetica', 24))
        self.restart_button = tk.Button(self.frame, text="Restart Game", command=self.restart_game_callback)

        self.label.pack()
        self.restart_button.pack()
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

class Score:
    def __init__(self, root):
        self.score = 0
        self.label = tk.Label(root, text=f"Score: {self.score}", font=('Helvetica', 16))
        self.label.pack()

    def increase(self):
        self.score += 10
        self.label.config(text=f"Score: {self.score}")

    def reset(self):
        self.score = 0
        self.label.config(text=f"Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
