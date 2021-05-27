from tkinter import *
# another module not a class so doesn't get caught with the *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- Search Function ------------------------------- #
def search():
    website = str(website_entry.get())
    try:
        with open("Saved_Data.json", mode="r") as data_file:
            # reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Website Found", message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
               'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]

    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)

    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]

    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)

    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    # password = ""
    # for char in password_list:
    #   password += char

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = str(website_entry.get())
    email = str(email_entry.get())
    password = str(password_entry.get())
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Error", message="whoops field empty")
    else:
        # messagebox.showinfo(title="Success", message="Done") asking user if they are happy with entered info
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                                              f" \nEmail: {email} \nPassword:"
                                                              f" {password} \n"
                                                              f"Is it ok to save?")
        # 3 types of Json method, json.dump, json.load, json.update
        if is_ok:
            try:
                with open("Saved_Data.json", mode="r") as data_file:
                    # reading old data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("Saved_Data.json", mode="w") as data_file:
                    json.load(new_data, data_file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)

                with open("Saved_Data.json", mode="w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

        else:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("password manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=18)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "skulicdamian@gmail.com")
password_entry = Entry(width=18)
password_entry.grid(row=3, column=1)

# Buttons
generate_pass_but = Button(text="Generate Password", command=generate)
generate_pass_but.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_but = Button(text="Search", command=search, width=16)
search_but.grid(row=1, column=2)

window.mainloop()
