import time
import random
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
#thank you to this person for the words
#https://github.com/dwyl/english-words/blob/master/words_alpha.txt
word = ""
guessed_letters = []
lives = 6
stage = 1
word_length = 5

image_width = 400
image_height = 400


def choose_word():
    with open("allWords.txt", "r") as file:
        word_list = file.read().splitlines()

    filtered_words = [w for w in word_list if len(w) == word_length]

    if filtered_words:
        word = random.choice(filtered_words)
        print("The chosen word is:", word)
        return word
    else:
        print(f"No words found with length {word_length}.")
        return ""


def display_word(word, guessed_letters):
    display = " ".join([letter if letter in guessed_letters else "_ " for letter in word])
    return display


def display_image(image_name):
    image_path = f"images/{image_name}.png"
    img = Image.open(image_path)
    img = img.resize((image_width, image_height), Image.BILINEAR)
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img


def guess_letter():
    global guessed_letters, lives, stage
    letter = letter_entry.get().lower()

    if letter.isalpha() and len(letter) == 1:
        if letter in guessed_letters:
            display_image("alreadyGuessed")
        elif letter in word:
            guessed_letters.append(letter)
            if display_word(word, guessed_letters) == word:
                display_image("win")
                new_game()
            else:
                update_display()
        else:
            guessed_letters.append(letter)
            lives -= 1
            stage += 1
            update_display()
    else:
        display_image("invalidLetter")


def update_display():
    word_display.config(text=display_word(word, guessed_letters))
    guessed_display.config(text="Guessed Letters: " + " ".join(guessed_letters))
    lives_display.config(text=f"Lives: {lives - 1}")

    if stage <= 6:
        image_path = f"images/stage{stage}.png"
        img = Image.open(image_path)
        img = img.resize((image_width, image_height), Image.BILINEAR)
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img

    if lives == 0 or (stage > 6 and lives != 1):
        new_game()


def new_game():
    global word, guessed_letters, lives, stage
    word = choose_word()
    guessed_letters = []
    lives = 6
    stage = 1
    update_display()


def set_difficulty():
    global word_length
    word_length = simpledialog.askinteger("Difficulty", "Drag slider to pick difficulty", initialvalue=5, minvalue=3,
                                          maxvalue=10)
    new_game()


root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x700")  # Enlarged the window

# Button styles
new_game_style = ttk.Style()
new_game_style.configure(
    "NewGame.TButton",
    background="red",
    foreground="white",
    font=("Arial", 16),
)

guess_style = ttk.Style()
guess_style.configure(
    "Guess.TButton",
    background="blue",  # Changed guess button color
    foreground="white",
    font=("Arial", 16),
)

# New Game button
new_game_button = ttk.Button(root, text="New Game", command=new_game, style="NewGame.TButton")
new_game_button.pack(pady=10)

# Set Difficulty button
set_difficulty_button = ttk.Button(root, text="Set Difficulty", command=set_difficulty, style="NewGame.TButton")
set_difficulty_button.pack(pady=10)

# Word display
word_display = tk.Label(root, text="", font=("Helvetica", 32))  # Increased font size
word_display.pack(pady=20)

# Guessed Letters
guessed_display = tk.Label(root, text="Guessed Letters:", font=("Helvetica", 24))  # Increased font size
guessed_display.pack()

# Lives
lives_display = tk.Label(root, text="", font=("Helvetica", 24))  # Increased font size
lives_display.pack(pady=10)

# Letter Entry
letter_entry = tk.Entry(root, font=("Helvetica", 20))  # Increased font size
letter_entry.pack(pady=10)

# Guess Button
guess_button = ttk.Button(root, text="Guess", command=guess_letter, style="Guess.TButton")
guess_button.pack(pady=10)

# Image Label
image_label = tk.Label(root)
image_label.pack()

new_game()  # Start a new game

root.mainloop()
