
import tkinter as tk
from tkinter import ttk, messagebox

class MatrixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("3 x 3 Matrix Operations")
        self.root.geometry("900x690")
        self.root.minsize(820, 620)
        self.entries_a = []
        self.entries_b = []
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        heading = ttk.Label(self.root, text="3 x 3 MATRIX CALCULATOR",
                            font=("Segoe UI", 19, "bold"))
        heading.pack(pady=(14, 4))
        ttk.Label(self.root, text="Enter values in Matrix A and Matrix B, then select an operation.",
                  font=("Segoe UI", 10)).pack(pady=(0, 12))

        matrices = ttk.Frame(self.root, padding=10)
        matrices.pack()
        self.entries_a = self._make_matrix(matrices, "Matrix A", 0)
        self.entries_b = self._make_matrix(matrices, "Matrix B", 1)

        controls = ttk.LabelFrame(self.root, text="Operation", padding=12)
        controls.pack(fill="x", padx=22, pady=8)

        self.operation = tk.StringVar(value="A + B  (Addition)")
        operations = [
            "A + B  (Addition)",
            "A - B  (Subtraction)",
            "A x B  (Matrix Multiplication)",
            "A element-wise x B",
            "Scalar x A",
            "Transpose of A",
            "Transpose of B",
            "Determinant of A",
            "Determinant of B",
            "Inverse of A",
            "Inverse of B",
            "Trace of A",
            "Trace of B",
            "A squared (A x A)",
        ]
        ttk.Label(controls, text="Choose:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Combobox(controls, textvariable=self.operation, values=operations,
                     state="readonly", width=28).grid(row=0, column=1, padx=5)
        ttk.Label(controls, text="Scalar:").grid(row=0, column=2, padx=(15, 4))
        self.scalar = ttk.Entry(controls, width=10)
        self.scalar.insert(0, "2")
        self.scalar.grid(row=0, column=3, padx=4)
        ttk.Button(controls, text="Calculate", command=self.calculate).grid(row=0, column=4, padx=12)
        ttk.Button(controls, text="Clear", command=self.clear).grid(row=0, column=5, padx=4)
        ttk.Button(controls, text="Load Sample", command=self.load_sample).grid(row=0, column=6, padx=4)

        result_frame = ttk.LabelFrame(self.root, text="Result", padding=12)
        result_frame.pack(fill="both", expand=True, padx=22, pady=(6, 15))
        self.result = tk.Text(result_frame, height=10, font=("Consolas", 12),
                              wrap="none", state="disabled")
        self.result.pack(fill="both", expand=True)

        footer = ttk.Label(self.root, text="Supports addition, subtraction, multiplication, transpose, determinant, inverse, trace and scalar multiplication.",
                           font=("Segoe UI", 9), foreground="#555")
        footer.pack(pady=(0, 10))

    def _make_matrix(self, parent, title, column):
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.grid(row=0, column=column, padx=18, sticky="n")
        entries = []
        for r in range(3):
            row = []
            for c in range(3):
                e = ttk.Entry(frame, width=9, justify="center")
                e.grid(row=r, column=c, padx=4, pady=4, ipady=5)
                e.insert(0, "0")
                row.append(e)
            entries.append(row)
        return entries

    def _read_matrix(self, entries, name):
        matrix = []
        for r in range(3):
            row = []
            for c in range(3):
                raw = entries[r][c].get().strip()
                try:
                    row.append(float(raw))
                except ValueError:
                    raise ValueError(f"{name}: please enter a valid number in row {r+1}, column {c+1}.")
            matrix.append(row)
        return matrix

    def _format_result(self, value):
        if isinstance(value, list):
            lines = []
            for row in value:
                lines.append("   ".join(f"{x:10.4g}" for x in row))
            return "\n".join(lines)
        if isinstance(value, float):
            return f"{value:.8g}"
        return str(value)

    def calculate(self):
        try:
            A = self._read_matrix(self.entries_a, "Matrix A")
            B = self._read_matrix(self.entries_b, "Matrix B")
            op = self.operation.get()
            if op == "A + B  (Addition)":
                answer = self.add(A, B)
            elif op == "A - B  (Subtraction)":
                answer = self.subtract(A, B)
            elif op == "A x B  (Matrix Multiplication)":
                answer = self.multiply(A, B)
            elif op == "A element-wise x B":
                answer = self.elementwise(A, B)
            elif op == "Scalar x A":
                try:
                    k = float(self.scalar.get())
                except ValueError:
                    raise ValueError("Please enter a valid numeric scalar.")
                answer = self.scalar_multiply(A, k)
            elif op == "Transpose of A":
                answer = self.transpose(A)
            elif op == "Transpose of B":
                answer = self.transpose(B)
            elif op == "Determinant of A":
                answer = self.determinant(A)
            elif op == "Determinant of B":
                answer = self.determinant(B)
            elif op == "Inverse of A":
                answer = self.inverse(A)
            elif op == "Inverse of B":
                answer = self.inverse(B)
            elif op == "Trace of A":
                answer = self.trace(A)
            elif op == "Trace of B":
                answer = self.trace(B)
            elif op == "A squared (A x A)":
                answer = self.multiply(A, A)
            else:
                raise ValueError("Please select an operation.")

            self.result.configure(state="normal")
            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, f"{op}\n\n{self._format_result(answer)}")
            self.result.configure(state="disabled")
        except (ValueError, ZeroDivisionError) as error:
            messagebox.showerror("Cannot calculate", str(error))

    def clear(self):
        for matrix in (self.entries_a, self.entries_b):
            for row in matrix:
                for entry in row:
                    entry.delete(0, tk.END)
                    entry.insert(0, "0")
        self.result.configure(state="normal")
        self.result.delete("1.0", tk.END)
        self.result.configure(state="disabled")

    def load_sample(self):
        sample_a = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        sample_b = [[2, 0, 1], [1, 3, 2], [4, 1, 0]]
        for entries, values in ((self.entries_a, sample_a), (self.entries_b, sample_b)):
            for r in range(3):
                for c in range(3):
                    entries[r][c].delete(0, tk.END)
                    entries[r][c].insert(0, str(values[r][c]))

    def add(self, A, B): raise NotImplementedError
    def subtract(self, A, B): raise NotImplementedError
    def multiply(self, A, B): raise NotImplementedError
    def elementwise(self, A, B): raise NotImplementedError
    def scalar_multiply(self, A, k): raise NotImplementedError
    def transpose(self, A): raise NotImplementedError
    def determinant(self, A): raise NotImplementedError
    def inverse(self, A): raise NotImplementedError
    def trace(self, A): raise NotImplementedError

def main():
    root = tk.Tk()
    MatrixGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

    def add(self, A, B):
        return [[A[r][c] + B[r][c] for c in range(3)] for r in range(3)]

    def subtract(self, A, B):
        return [[A[r][c] - B[r][c] for c in range(3)] for r in range(3)]

    def multiply(self, A, B):
        return [[sum(A[r][k] * B[k][c] for k in range(3))
                 for c in range(3)] for r in range(3)]

    def elementwise(self, A, B):
        return [[A[r][c] * B[r][c] for c in range(3)] for r in range(3)]

    def scalar_multiply(self, A, k):
        return [[A[r][c] * k for c in range(3)] for r in range(3)]

    def transpose(self, A):
        return [[A[c][r] for c in range(3)] for r in range(3)]

    def determinant(self, A):
        a, b, c = A[0]
        d, e, f = A[1]
        g, h, i = A[2]
        return (a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g))

    def inverse(self, A):
        det = self.determinant(A)
        if abs(det) < 1e-10:
            raise ValueError("This matrix is singular (determinant is zero), so it has no inverse.")
        # Cofactor matrix, then transpose it to get the adjugate.
        cof = []
        for r in range(3):
            row = []
            for c in range(3):
                minor = [[A[x][y] for y in range(3) if y != c]
                         for x in range(3) if x != r]
                minor_det = minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]
                row.append(((-1) ** (r + c)) * minor_det)
            cof.append(row)
        adj = self.transpose(cof)
        return [[adj[r][c] / det for c in range(3)] for r in range(3)]

    def trace(self, A):
        return A[0][0] + A[1][1] + A[2][2]
