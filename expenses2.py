#!/usr/bin/env python3

from tkinter import Tk, Button, Frame, Entry, END, Label, messagebox, filedialog, ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex, to_rgba
from matplotlib import patheffects
from matplotlib.textpath import TextToPath
import matplotlib.pyplot as plt
import pickle
from PIL import ImageTk, Image

expenses_combined_label = None
remaining_money_label = None

mexp = []
mamt = []

window = tk.Tk()
window.geometry("1100x700")

class ABC(Frame):
    def __init__(self, parent=None, mexp=None, mamt=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()
        self.menu()
        self.table()
        self.mexp = mexp
        self.mamt = mamt
        self.i = 1

    def make_widgets(self):
        self.winfo_toplevel().title("Expense calculator")

    def menu(self):
        menubar = tk.Menu(self.parent)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label='New', command=lambda: self.new())
        file_menu.add_command(label="Save as...", command=lambda: self.save_file())
        file_menu.add_command(label='Open...', command=lambda: self.open_file())
        file_menu.add_separator()
        sub_menu = tk.Menu(file_menu, tearoff=0)
        sub_menu.add_command(label='Keyboard Shortcuts')
        file_menu.add_cascade(label="Preferences", menu=sub_menu)
        color_menu = tk.Menu(sub_menu, tearoff=0)
        color_menu.add_command(label='Red', command=lambda: self.red())
        color_menu.add_command(label='Blue', command=lambda: self.blue())
        color_menu.add_command(label='Light', command=lambda: self.white())
        color_menu.add_command(label='Dark', command=lambda: self.black())
        sub_menu.add_cascade(label='Color themes', menu=color_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.parent.destroy)
        self.parent.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...', command=self.show_about_popup)
        menubar.add_cascade(label="Help", menu=help_menu)

    def change_widgets_color(self, widget):
        if isinstance(widget, (Button, Label)):
            widget.configure(highlightbackground=widget.master.cget('bg'), highlightcolor=widget.master.cget('bg'))
        for child in widget.winfo_children():
            self.change_widgets_color(child)

    def blue(self):
        window.configure(bg='blue')
        self.change_widgets_color(window)
        label1.config(bg='blue')
        label2.config(bg='blue')
        label3.config(bg='blue')
        label4.config(bg='blue')
        expenses_combined_label.config(bg='blue')
        remaining_money_label.config(bg='blue')
        label1.config(fg='white')
        label2.config(fg='white')
        label3.config(fg='white')
        label4.config(fg='white')
        expenses_combined_label.config(fg='white')
        remaining_money_label.config(fg='white')

    def red(self):
        window.configure(bg='red')
        self.change_widgets_color(window)
        label1.config(bg='red')
        label2.config(bg='red')
        label3.config(bg='red')
        label4.config(bg='red')
        expenses_combined_label.config(bg='red')
        remaining_money_label.config(bg='red')
        label1.config(fg='white')
        label2.config(fg='white')
        label3.config(fg='white')
        label4.config(fg='white')
        expenses_combined_label.config(fg='white')
        remaining_money_label.config(fg='white')

    def white(self):
        window.configure(bg='white')
        self.change_widgets_color(window)
        label1.config(bg='white')
        label2.config(bg='white')
        label3.config(bg='white')
        label4.config(bg='white')
        expenses_combined_label.config(bg='white')
        remaining_money_label.config(bg='white')
        label1.config(fg='black')
        label2.config(fg='black')
        label3.config(fg='black')
        label4.config(fg='black')
        expenses_combined_label.config(fg='black')
        remaining_money_label.config(fg='black')

    def black(self):
        window.configure(bg='black')
        self.change_widgets_color(window)
        label1.config(bg='black')
        label2.config(bg='black')
        label3.config(bg='black')
        label4.config(bg='black')
        expenses_combined_label.config(bg='black')
        remaining_money_label.config(bg='black')
        label1.config(fg='white')
        label2.config(fg='white')
        label3.config(fg='white')
        label4.config(fg='white')
        expenses_combined_label.config(fg='white')
        remaining_money_label.config(fg='white')

    def save_file(self):
        data = {
            "mexp": self.mexp,
            "mamt": self.mamt
        }
        file_path = filedialog.asksaveasfile(defaultextension=".dat")
        if file_path:
            with open(file_path.name, "wb") as file:
                pickle.dump(data, file)

    def open_file(self):
        file_path = filedialog.askopenfile(defaultextension=".dat")
        if file_path:
            with open(file_path.name, "rb") as file:
                data = pickle.load(file)
            self.mexp = data["mexp"]
            self.mamt = data["mamt"]
            label4.configure(text="Your monthly earnings: " + str(self.mamt[0]))
            print("File read:", file_path.name)
            self.update_table()
            self.update_labels()

    def plot(self): #do poprawy w przyszlosci
        label = self.mexp
        values = self.mamt[:]
        remamt = self.mamt[0] - sum(self.mamt[1:])
        values[0] = remamt
        for widget in window.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        fig, ax = plt.subplots()
        autopct_format = lambda pct: f'{pct:.1f}%\n({(pct/100)*self.mamt[0]:.2f}PLN)'
        patches, texts, autotexts = ax.pie(values, labels=label, autopct=autopct_format, startangle=90, pctdistance=0.85, labeldistance=1.3)
        for text, autotext in zip(texts, autotexts):
            text.set_color('white')
            text.set_path_effects([patheffects.withStroke(linewidth=3, foreground="black"), patheffects.Normal()])
            autotext.set_path_effects([patheffects.withStroke(linewidth=3, foreground="black"), patheffects.Normal()])
            text.set_color('white')
            text.set_path_effects([patheffects.withStroke(linewidth=3, foreground="black")])
            autotext.set_color('white')
            autotext.set_path_effects([patheffects.withStroke(linewidth=3, foreground="black")])
            text.set_ha('center')
            autotext.set_ha('center')
        bg_rgb = window.winfo_rgb(window.cget('bg'))
        bg_rgba = (bg_rgb[0] / 65535, bg_rgb[1] / 65535, bg_rgb[2] / 65535, 1.0)
        fig.patch.set_facecolor(bg_rgba)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().place(x=525, y=75, width=500, height=550)

    def table(self):
        self.table = ttk.Treeview(window, show = 'headings')
        self.table['columns'] = ('column1', 'column2', 'column3')
        self.table.column('column1', width=38)
        self.table.column('column2', width=280)
        self.table.column('column3', width=100)
        self.table.heading('column1', text='No.')
        self.table.heading('column2', text='expense name')
        self.table.heading('column3', text='value')
        self.table.pack()
        self.table.place(x=10,y=300)

    def update_table(self):
        self.table.delete(*self.table.get_children())
        for i, (expense, value) in enumerate(zip(self.mexp[1:], self.mamt[1:]), start=1):
            self.insert_row(i, expense, value)
        
    def insert_row(self, no, expense_name, value):
        self.table.insert(parent='', index='end', iid=self.i, text='', values=(no, expense_name, value))
        self.i += 1

    def delete_row(self):
        selected_items = self.table.selection()
        for item in selected_items:
            values = self.table.item(item)['values']
            if values:
                row_id = int(values[0])
                if 0 < row_id < len(self.mexp):
                    self.table.delete(item)
                    del self.mexp[row_id]
                    del self.mamt[row_id]
        self.update_table()
        self.update_labels()

    def new(self):
        self.mexp = []
        self.mamt = []
        label4.configure(text="Your monthly earnings: " + str(0))
        self.table.delete(*self.table.get_children())
        for widget in window.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        self.update_labels()

    def update_labels(self):
        total_expenses = sum(self.mamt[1:])
        if len(self.mamt) == 0:
            remaining_money = 0
        else:
            remaining_money = self.mamt[0] - total_expenses
        expenses_combined_label.configure(text=f"Expenses Combined: {total_expenses:.2f} PLN")
        remaining_money_label.configure(text=f"Remaining Money: {remaining_money:.2f} PLN")

    def add_expense(self):
        expense = entry1.get()
        value = float(entry2.get())
        self.mexp.append(expense)
        self.mamt.append(value)
        self.insert_row(self.i, expense, value)
        entry1.delete(0, END)
        entry2.delete(0, END)
        self.update_labels()

    def confirm(self):
        if float(entry3.get())>0:
            earnings = entry3.get()
        else:
            earnings = mamt[0]
        label4.configure(text="Your monthly earnings: " + str(earnings) +"PLN")
        self.update_labels()

    @staticmethod
    def show_about_popup():
        messagebox.showinfo("About", "This app was made to make monthly budget easier to comprehend and quicker to adjust. Made in just few hours by math student who never before worked with GUI programming.")

abc = ABC(window, mexp, mamt)

label1 = tk.Label(window, text="expense name")
label1.place(x=100, y=150)
label2 = tk.Label(window, text="value")
label2.place(x=305, y=150)
label3 = tk.Label(window, text="monthly earnings")
label3.place(x=162.5, y=40)
entry1 = tk.Entry(window, width=20)
entry1.place(x=50, y=170)
entry2 = tk.Entry(window, width=8)
entry2.place(x=280, y=170)
entry3 = tk.Entry(window, width=15)
entry3.place(x=145, y=63)
button1 = tk.Button(window, text="add expense", command=abc.add_expense)
button1.place(x=158, y=210)
button2 = tk.Button(window, text="generate pie chart", command=abc.plot)
button2.place(x=140, y=240)
button3 = tk.Button(window, text="confirm", command=lambda: [abc.mamt.insert(0, float(entry3.get())), abc.mexp.insert(0, "remaining"), abc.confirm(), entry3.delete(0, END)])
button3.place(x=176, y=103)
button4 = tk.Button(window, text="delete", command=lambda:abc.delete_row())
button4.place(x=176, y=520)
label4 = tk.Label(window, text= "Your monthly earnings: ")
label4.place(x=100, y=10)

def switch_focus(event):
    if event.widget == entry1:
        entry2.focus_set()
    elif event.widget == entry2:
        abc.add_expense()
        entry1.focus_set()
    elif event.widget == entry3:
        abc.mamt.insert(0, float(entry3.get()))
        abc.mexp.insert(0, "remaining")
        abc.confirm()
        entry3.delete(0, END)
        entry1.focus_set()

entry1.bind("<Return>", switch_focus)
entry2.bind("<Return>", switch_focus)
entry3.bind("<Return>", switch_focus)

def delete_row(event):
    selected_items = abc.table.selection()
    if event.keysym == 'BackSpace' and selected_items:
        for item in selected_items:
            abc.table.delete(item)
            row_id = item[1:]  # Pobranie identyfikatora wiersza (bez pierwszego znaku)
            if row_id.isdigit():  # Sprawdzenie, czy identyfikator wiersza składa się tylko z cyfr
                row_id = int(row_id)
                if 0 < row_id < len(abc.mexp):
                    del abc.mexp[row_id]
                    del abc.mamt[row_id]
        abc.update_table()
        abc.update_labels()

abc.table.bind("<KeyPress>", delete_row)

expenses_combined_label = Label(window, text="Expenses Combined: 0")
expenses_combined_label.place(x=10, y=600)

remaining_money_label = Label(window, text="Remaining Money: 0")
remaining_money_label.place(x=10, y=620)

window.mainloop()