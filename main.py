from tkinter import *
from PIL import ImageTk, Image
from pandas import *
import random
import json

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = read_csv("./data/portugues_words.csv")
    to_learn = DataFrame.to_dict(original_data, orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="Portuguese", fill="black")
    canvas.itemconfig(word, text=current_card["portuguese_word"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = root.after(3000, flip_card)


def remove():
    to_learn.remove(current_card)
    df_dict_word = DataFrame.from_dict(to_learn)
    df_dict_word.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title, text="Spanish", fill="white")
    canvas.itemconfig(word, text=current_card["spanish_word"], fill="white")


root = Tk()
root.title("FlashCardApp")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = root.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
# IMAGES
card_front = ImageTk.PhotoImage(Image.open("./images/card_front.png"))
card_back = ImageTk.PhotoImage(Image.open("./images/card_back.png"))
right = ImageTk.PhotoImage(Image.open("./images/right.png"))
wrong = ImageTk.PhotoImage(Image.open("./images/wrong.png"))

canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

# TEXT
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"))

# BUTTONS
right_button = Button(image=right, highlightthickness=0, borderwidth=0, command=remove)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

root.mainloop()
