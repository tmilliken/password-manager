from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    entry_password.insert(0, password)

    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = entry_url.get().title()
    email = entry_user.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(message="You have empty fields")
    else:
        try:
            with open("data.json", mode="r") as f:
                # read data from file
                data = json.load(f)
                # update json file
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as f:
                # write to file
                json.dump(new_data, f, indent=4)
        else:
            with open("data.json", mode="w") as f:
                # write to file
                json.dump(data, f, indent=4)
        finally:
            entry_url.delete(0, END)
            entry_password.delete(0, END)


# -------------------------SEARCH FUNCTION ---------------------------- #


def search_file():
    website = entry_url.get().title()
    try:
        f = open("data.json", mode="r")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data file not found")
    else:
        data = json.load(f)
        if website in data:
            message = f"{website}\nUsername= {data[website]['email']}\nPassword= {data[website]['password']}\n" \
                      f"\nYour password has been copied to your clipboard"
            messagebox.showinfo(title="Search Results", message=message)
            pyperclip.copy(data[website]["password"])
        else:
            messagebox.showinfo(title="Not Found", message=f"No Details for {website} not found")
    finally:
        f.close()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=240, height=240, )
lock_img = PhotoImage(file="logo.png")
canvas.create_image(120, 120, image=lock_img)
canvas.grid(column=1, row=0)

label_url = Label(text="Website: ")
label_url.grid(column=0, row=1, pady=5)

entry_url = Entry(width=21)
entry_url.grid(column=1, row=1, columnspan=2, pady=5, sticky="w")
entry_url.focus()

button_search = Button(text="Search", width=15, command=search_file)
button_search.grid(column=2, row=1, pady=5, sticky="w")

label_user = Label(text="Email/Username: ")
label_user.grid(column=0, row=2, pady=5)

entry_user = Entry(width=39)
entry_user.grid(column=1, row=2, columnspan=2, pady=5, sticky="w")
entry_user.insert(0, "tmilliken@gmail.com")
label_password = Label(text="Password: ")
label_password.grid(column=0, row=3, pady=5)

entry_password = Entry(width=21)
entry_password.grid(column=1, row=3, pady=5, sticky="w")

button_password = Button(text="Generate Password", command=generate_password)
button_password.grid(column=2, row=3, pady=5, sticky="w")

button_add = Button(text="Add", width=37, command=save_data)
button_add.grid(column=1, row=4, columnspan=2, pady=5, sticky="w")

window.mainloop()
