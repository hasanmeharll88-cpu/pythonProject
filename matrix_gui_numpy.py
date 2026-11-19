
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# ================= WINDOW =================

root = tk.Tk()
root.title("Matrix Calculator Pro")
root.geometry("1100x750")
root.state("zoomed")
root.configure(bg="#0F172A")
root.minsize(850, 600)

# ================= COLORS =================

BG = "#0F172A"
CARD = "#1E293B"
INPUT = "#334155"
TEAL = "#14B8A6"
WHITE = "#FFFFFF"

# ================= SCROLLABLE MAIN AREA =================

container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(
    container,
    bg=BG,
    highlightthickness=0
)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

content = tk.Frame(canvas, bg=BG)

window_id = canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def update_content_width(event):
    canvas.itemconfigure(window_id, width=event.width)


content.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", update_content_width)


def mouse_scroll(event):
    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all("<MouseWheel>", mouse_scroll)

# ================= TITLE =================

title = tk.Label(
    content,
    text="MATRIX CALCULATOR",
    font=("Arial", 27, "bold"),
    bg=BG,
    fg=WHITE
)
title.pack(pady=(15, 3))

subtitle = tk.Label(
    content,
    text="POWERFUL 3 x 3 MATRIX OPERATIONS",
    font=("Arial", 11, "bold"),
    bg=BG,
    fg=TEAL
)
subtitle.pack(pady=5)

# ================= MATRIX INPUTS =================

main_frame = tk.Frame(content, bg=BG)
main_frame.pack(pady=12)

matrix_a_entries = []
matrix_b_entries = []


def create_matrix(parent, title, entries):

    card = tk.Frame(
        parent,
        bg=CARD,
        padx=20,
        pady=12
    )
    card.pack(side="left", padx=15)

    tk.Label(
        card,
        text=title,
        font=("Arial", 17, "bold"),
        bg=CARD,
        fg=TEAL
    ).pack(pady=7)

    grid = tk.Frame(card, bg=CARD)
    grid.pack()

    for i in range(3):

        row = []

        for j in range(3):

            entry = tk.Entry(
                grid,
                width=7,
                font=("Arial", 16, "bold"),
                justify="center",
                bg=INPUT,
                fg=WHITE,
                insertbackground=WHITE,
                relief="flat"
            )

            entry.grid(
                row=i,
                column=j,
                padx=5,
                pady=5,
                ipady=8
            )

            row.append(entry)

        entries.append(row)


create_matrix(main_frame, "MATRIX A", matrix_a_entries)
create_matrix(main_frame, "MATRIX B", matrix_b_entries)

# ================= MATRIX FUNCTIONS =================

def get_matrix(entries):

    try:
        return np.array([
            [float(entries[i][j].get()) for j in range(3)]
            for i in range(3)
        ])

    except ValueError:
        raise ValueError(
            "Please enter valid numbers in all required matrix cells."
        )


def load_example():

    a = [
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ]

    b = [
        [2, 0, 1],
        [1, 3, 2],
        [4, 1, 0]
    ]

    for i in range(3):
        for j in range(3):

            matrix_a_entries[i][j].delete(0, tk.END)
            matrix_a_entries[i][j].insert(0, str(a[i][j]))

            matrix_b_entries[i][j].delete(0, tk.END)
            matrix_b_entries[i][j].insert(0, str(b[i][j]))


def swap_matrices():

    for i in range(3):
        for j in range(3):

            a = matrix_a_entries[i][j].get()
            b = matrix_b_entries[i][j].get()

            matrix_a_entries[i][j].delete(0, tk.END)
            matrix_a_entries[i][j].insert(0, b)

            matrix_b_entries[i][j].delete(0, tk.END)
            matrix_b_entries[i][j].insert(0, a)


# ================= BUTTON FUNCTION =================

def make_button(parent, text, command, color):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=18,
        pady=11,
        cursor="hand2",
        activebackground=color,
        activeforeground=WHITE
    )


# ================= BUTTON SECTION =================

button_frame = tk.Frame(content, bg=BG)
button_frame.pack(pady=10)

make_button(
    button_frame,
    "LOAD EXAMPLE",
    load_example,
    "#2563EB"
).pack(side="left", padx=7)

make_button(
    button_frame,
    "SWAP MATRICES",
    swap_matrices,
    "#7C3AED"
).pack(side="left", padx=7)


# ================= OPERATION SECTION =================

operation_card = tk.Frame(
    content,
    bg=CARD,
    padx=25,
    pady=15
)

operation_card.pack(
    fill="x",
    padx=35,
    pady=12
)

tk.Label(
    operation_card,
    text="SELECT OPERATION",
    font=("Arial", 14, "bold"),
    bg=CARD,
    fg=WHITE
).pack(anchor="w", pady=5)

operations = [
    "Addition (A + B)",
    "Subtraction (A - B)",
    "Matrix Multiplication (A x B)",
    "Element-wise Multiplication",
    "Scalar Multiplication (A)",
    "Transpose A",
    "Transpose B",
    "Determinant A",
    "Determinant B",
    "Inverse A",
    "Inverse B",
    "Trace A",
    "Trace B",
    "Square A"
]

control_frame = tk.Frame(operation_card, bg=CARD)
control_frame.pack(fill="x", pady=8)

operation_var = tk.StringVar(
    value=operations[2]
)

operation_menu = ttk.Combobox(
    control_frame,
    textvariable=operation_var,
    values=operations,
    state="readonly",
    width=32,
    font=("Arial", 11)
)

operation_menu.pack(side="left", padx=5, ipady=5)

tk.Label(
    control_frame,
    text="Scalar:",
    bg=CARD,
    fg=WHITE,
    font=("Arial", 11)
).pack(side="left", padx=(15, 5))

scalar_entry = tk.Entry(
    control_frame,
    width=8,
    font=("Arial", 12),
    justify="center"
)

scalar_entry.insert(0, "2")
scalar_entry.pack(side="left", ipady=5)


# ================= RESULT SECTION =================

result_card = tk.Frame(
    content,
    bg=CARD,
    padx=20,
    pady=15
)

result_card.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=10
)

tk.Label(
    result_card,
    text="RESULT",
    font=("Arial", 17, "bold"),
    bg=CARD,
    fg=TEAL
).pack(anchor="w", pady=8)


# Result heading

result_heading = tk.Label(
    result_card,
    text="Your result will appear here.",
    font=("Arial", 12, "bold"),
    bg=CARD,
    fg=WHITE
)

result_heading.pack(anchor="w", pady=5)


# Result text and scrollbar

result_frame = tk.Frame(
    result_card,
    bg="#111827"
)

result_frame.pack(
    fill="both",
    expand=True,
    pady=5
)

result_scrollbar = ttk.Scrollbar(
    result_frame,
    orient="vertical"
)

result_scrollbar.pack(side="right", fill="y")

result_box = tk.Text(
    result_frame,
    height=10,
    font=("Consolas", 16, "bold"),
    bg="#111827",
    fg="#34D399",
    insertbackground=WHITE,
    relief="flat",
    padx=15,
    pady=12,
    wrap="none",
    yscrollcommand=result_scrollbar.set
)

result_box.pack(
    side="left",
    fill="both",
    expand=True
)

result_scrollbar.config(
    command=result_box.yview
)

result_box.insert(
    tk.END,
    "Your result will appear here."
)


# ================= CALCULATE FUNCTION =================

def calculate():

    operation = operation_var.get()

    try:

        A = None
        B = None

        if operation in [
            "Addition (A + B)",
            "Subtraction (A - B)",
            "Matrix Multiplication (A x B)",
            "Element-wise Multiplication"
        ]:

            A = get_matrix(matrix_a_entries)
            B = get_matrix(matrix_b_entries)

        elif operation in [
            "Transpose A",
            "Determinant A",
            "Inverse A",
            "Trace A",
            "Square A",
            "Scalar Multiplication (A)"
        ]:

            A = get_matrix(matrix_a_entries)

        elif operation in [
            "Transpose B",
            "Determinant B",
            "Inverse B",
            "Trace B"
        ]:

            B = get_matrix(matrix_b_entries)

        # Perform calculations

        if operation == "Addition (A + B)":

            answer = np.add(A, B)

        elif operation == "Subtraction (A - B)":

            answer = np.subtract(A, B)

        elif operation == "Matrix Multiplication (A x B)":

            answer = np.matmul(A, B)

        elif operation == "Element-wise Multiplication":

            answer = np.multiply(A, B)

        elif operation == "Scalar Multiplication (A)":

            scalar = float(scalar_entry.get())
            answer = A * scalar

        elif operation == "Transpose A":

            answer = np.transpose(A)

        elif operation == "Transpose B":

            answer = np.transpose(B)

        elif operation == "Determinant A":

            answer = np.linalg.det(A)

        elif operation == "Determinant B":

            answer = np.linalg.det(B)

        elif operation == "Inverse A":

            if np.isclose(np.linalg.det(A), 0):
                raise ValueError(
                    "Matrix A has no inverse because determinant is zero."
                )

            answer = np.linalg.inv(A)

        elif operation == "Inverse B":

            if np.isclose(np.linalg.det(B), 0):
                raise ValueError(
                    "Matrix B has no inverse because determinant is zero."
                )

            answer = np.linalg.inv(B)

        elif operation == "Trace A":

            answer = np.trace(A)

        elif operation == "Trace B":

            answer = np.trace(B)

        elif operation == "Square A":

            answer = np.matmul(A, A)

        else:

            raise ValueError("Please select an operation.")

        # Display result

        result_box.delete("1.0", tk.END)

        if isinstance(answer, np.ndarray):

            output = np.array2string(
                answer,
                precision=4,
                suppress_small=True
            )

            result_heading.config(
                text=f"RESULT: {operation}"
            )

        else:

            output = f"{answer:.6g}"

            result_heading.config(
                text=f"RESULT: {operation}"
            )

        result_box.insert(tk.END, output)

        result_box.see("1.0")

        update_scroll_region()

    except ValueError as error:

        messagebox.showerror(
            "Calculation Error",
            str(error)
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )


# ================= CALCULATE BUTTON =================

make_button(
    control_frame,
    "CALCULATE  →",
    calculate,
    TEAL
).pack(side="right", padx=5)


# ================= COPY RESULT =================

def copy_result():

    text = result_box.get("1.0", tk.END).strip()

    if not text or text == "Your result will appear here.":
        messagebox.showinfo(
            "Copy Result",
            "Please calculate a result first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(text)

    messagebox.showinfo(
        "Copied",
        "Result copied successfully!"
    )


make_button(
    result_card,
    "COPY RESULT",
    copy_result,
    "#2563EB"
).pack(anchor="e", pady=8)


# ================= RESET ALL =================

def reset_all():

    for matrix in [
        matrix_a_entries,
        matrix_b_entries
    ]:

        for row in matrix:

            for entry in row:
                entry.delete(0, tk.END)

    result_box.delete("1.0", tk.END)

    result_box.insert(
        tk.END,
        "Your result will appear here."
    )

    result_heading.config(
        text="RESULT"
    )

    operation_var.set(operations[2])
    scalar_entry.delete(0, tk.END)
    scalar_entry.insert(0, "2")


make_button(
    button_frame,
    "RESET ALL",
    reset_all,
    "#DC2626"
).pack(side="left", padx=7)


# ================= START PROGRAM =================

load_example()

root.mainloop()
