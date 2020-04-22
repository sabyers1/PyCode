#forminput.py
""" Program to show how to enter information. """

import tkinter as tk

def ShowEntryFields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)

master = tk.Tk()
master.title("Form Input Demo")
tk.Label(master, text="First Name").grid(row=0)
tk.Label(master, text="Last Name").grid(row=1)


e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.insert(10, "James")
e2.insert(10, "Caan")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master, 
          text=' Quit ', highlightbackground='red',  
          command=master.quit).grid(row=3, 
                                    column=2, 
                                    sticky=tk.W, 
                                    pady=4, padx=20)
tk.Button(master, text=' Show ',highlightbackground='blue',
          command=ShowEntryFields).grid(row=3, 
                                        column=1, 
                                        sticky=tk.W, 
                                        pady=4, padx=20)

master.mainloop()
