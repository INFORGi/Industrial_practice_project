import tkinter as tk

# Создание главного окна
root = tk.Tk()
root.title("Пример с grid()")

# Создание и размещение виджетов с использованием grid()
label1 = tk.Label(root, text="Label 1", bg="red")
label1.grid(row=0, column=0)

label2 = tk.Label(root, text="Label 2", bg="green")
label2.grid(row=0, column=1)

label3 = tk.Label(root, text="Label 3", bg="blue")
label3.grid(row=1, column=0, columnspan=2)

button = tk.Button(root, text="Button", bg="yellow")
button.grid(row=2, column=0, columnspan=2, sticky="ew")

# Запуск основного цикла обработки событий
root.mainloop()
