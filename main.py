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
    word_length = simpledialog.askinteger("Difficulty", " pick difficulty (enter a num 3 to 15)", initialvalue=5, minvalue=3,
                                          maxvalue=15)
    new_game()


root = tk.Tk()
root.title("Hangman Game")
root.geometry("800x700")

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
    background="blue",
    foreground="white",
    font=("Arial", 16),
)

new_game_button = ttk.Button(root, text="New Game", command=new_game, style="NewGame.TButton")
new_game_button.pack(pady=10)

set_difficulty_button = ttk.Button(root, text="Set Difficulty", command=set_difficulty, style="NewGame.TButton")
set_difficulty_button.pack(pady=10)

word_display = tk.Label(root, text="", font=("Helvetica", 32))
word_display.pack(pady=20)

guessed_display = tk.Label(root, text="Guessed Letters:", font=("Helvetica", 24))
guessed_display.pack()

lives_display = tk.Label(root, text="", font=("Helvetica", 24))
lives_display.pack(pady=10)

letter_entry = tk.Entry(root, font=("Helvetica", 20))
letter_entry.pack(pady=10)

guess_button = ttk.Button(root, text="Guess", command=guess_letter, style="Guess.TButton")
guess_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

new_game()

root.mainloop()
