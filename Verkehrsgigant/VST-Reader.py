import tkinter as tk
from tkinter import filedialog

input_entries = []
input_values = []

def save_file():
    data = bytearray()

    for entry in input_entries:
        value = int(entry.get())
        data.extend(value.to_bytes(4, byteorder="little", signed=True))

    path = filedialog.asksaveasfilename(
        defaultextension=".vst"
    )
    with open(path, 'wb') as file:
        file.write(data)

def select_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    file_path.delete(0, tk.END)
    file_path.insert(0, path)

    with open(path, "rb") as f:
        data = f.read()

    # Data
    for i in range(0, len(data), 4):
        value = int.from_bytes(data[i:i+4], byteorder="little", signed=True)
        input_values.append(value)

    movements = input_values[0]

    # Labels
    labels = ["X offset", "Y offset", "Sprite position"]
    input_labels = []
    input_labels.append("Movements: ")
    input_labels.extend(
        f"{label} {i}"
        for i in range(1, movements + 1)
        for label in labels
    )

    remaining = len(input_values) - len(input_labels)

    input_labels.extend(
        f"Unknown {i}"
        for i in range(1, remaining + 1)
    )   
   
    # Placing
    

    # movements
    label = tk.Label(root, text=input_labels[0])
    label.grid(row=1, column=0)
    entry = tk.Entry(root)
    entry.grid(row=1, column=1)
    entry.insert(0, movements)
    input_entries.append(entry)

    # offset + sprite
    place_column = 0
    place_row = 2
    for index, i in enumerate(range(1, 3 * movements + 1)):
        if (index % 3 == 0):
            place_row += 1
            place_column = 0
        label = tk.Label(root, text=input_labels[i])
        label.grid(row=place_row+1, column=place_column)
        entry = tk.Entry(root)
        entry.grid(row=place_row+1, column=place_column + 1)
        entry.insert(0, input_values[i])
        input_entries.append(entry)
        place_column += 2

    # unknown
    place_column = 0
    place_row = movements + 3
    for index, i in enumerate(range(3 * movements + 1,len(input_values))):
        if (index % 2 == 0):
            place_row += 1
            place_column = 0
        label = tk.Label(root, text=input_labels[i])
        label.grid(row=place_row+1, column=place_column)
        entry = tk.Entry(root)
        entry.grid(row=place_row+1, column=place_column + 1)
        entry.insert(0, input_values[i])
        input_entries.append(entry)
        place_column += 2


    # Save button
    save_button = tk.Button(root, text="Save", bg="gray", fg="white", command=save_file)
    save_button.grid(row=movements * 3 + 4, column=1, pady=10)

## GUI

root = tk.Tk()
root.title("VST Reader")

# Set window size
window_width = 800
window_height = 900
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))


# Filepath
file_label = tk.Label(root, text="Filepath (.vst):")
file_label.grid(row=0, column=0)
file_path = tk.Entry(root)
file_path.grid(row=0, column=1)
file_button = tk.Button(root, text="Search", command=select_file)
file_button.grid(row=0, column=2)

root.mainloop()