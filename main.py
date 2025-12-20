import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from algorithm import FloydWarshallLogic
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FloydApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm mô phỏng Floyd-Warshall - Đề 15")
        self.root.geometry("1100x700")
        self.logic = FloydWarshallLogic()

        # --- Layout chia 2 cột ---
        left_frame = tk.Frame(root, width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Input Area ---
        tk.Label(left_frame, text="Nhập ma trận kề (Dùng 'inf' cho vô cùng):", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.txt_input = tk.Text(left_frame, height=8, width=50)
        self.txt_input.pack(pady=5)
        self.txt_input.insert(tk.END, "0 5 inf 10\ninf 0 3 inf\ninf inf 0 1\ninf inf inf 0")

        btn_box = tk.Frame(left_frame)
        btn_box.pack(pady=5)
        tk.Button(btn_box, text="Đọc từ File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="Chạy Floyd-Warshall", bg="green", fg="white", command=self.run_floyd).pack(side=tk.LEFT, padx=5)

        # --- Log Area ---
        tk.Label(left_frame, text="Bảng log cập nhật giá trị (từng bước k):").pack(anchor="w", pady=(10, 0))
        self.log_display = scrolledtext.ScrolledText(left_frame, height=20, width=55, bg="#2c3e50", fg="#ecf0f1")
        self.log_display.pack(pady=5)

        # --- Visual & Path Area ---
        self.canvas_frame = tk.Frame(right_frame, height=350, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(right_frame, text="Danh sách đường đi ngắn nhất:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.path_display = scrolledtext.ScrolledText(right_frame, height=10, width=60)
        self.path_display.pack(pady=5, fill=tk.BOTH)

    def load_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, 'r') as f:
                self.txt_input.delete("1.0", tk.END)
                self.txt_input.insert(tk.END, f.read())

    def run_floyd(self):
        try:
            # Xử lý input
            lines = self.txt_input.get("1.0", tk.END).strip().split('\n')
            matrix = []
            for line in lines:
                row = [float(x) if x.lower() != 'inf' else np.inf for x in line.split()]
                matrix.append(row)
            
            self.logic.process_matrix(matrix)
            success = self.logic.run_floyd()

            # Hiển thị đồ thị
            for widget in self.canvas_frame.winfo_children(): widget.destroy()
            canvas = FigureCanvasTkAgg(self.logic.get_figure(), master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Xuất Log
            self.log_display.delete("1.0", tk.END)
            if self.logic.negative_cycle:
                self.log_display.insert(tk.END, "!!! CẢNH BÁO: PHÁT HIỆN CHU TRÌNH ÂM !!!\n")
                return

            for entry in self.logic.history:
                step_name = entry[0]
                mat = entry[1]
                updates = entry[3] if len(entry) > 3 else []
                
                self.log_display.insert(tk.END, f"--- Bước {step_name} ---\n")
                for i in range(len(mat)):
                    row_str = ""
                    for j in range(len(mat)):
                        val = "∞" if mat[i][j] == np.inf else f"{int(mat[i][j]):>3}"
                        # Highlight cập nhật (giảm chi phí) bằng dấu sao
                        mark = "*" if (i, j) in updates else " "
                        row_str += f"{val}{mark} "
                    self.log_display.insert(tk.END, f"  [{row_str}]\n")
                self.log_display.insert(tk.END, "\n")

            # Xuất đường đi
            self.path_display.delete("1.0", tk.END)
            for i in range(self.logic.n):
                for j in range(self.logic.n):
                    if i != j:
                        path = self.logic.get_path(i, j)
                        dist = self.logic.dist[i][j]
                        if dist == np.inf:
                            self.path_display.insert(tk.END, f"{i} -> {j}: Không có đường đi\n")
                        else:
                            self.path_display.insert(tk.END, f"{i} -> {j}: {' -> '.join(map(str, path))} (CP: {dist})\n")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FloydApp(root)
    root.mainloop()