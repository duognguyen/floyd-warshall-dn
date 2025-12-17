# main.py
import tkinter as tk
from tkinter import messagebox
from algorithm import FloydWarshallSolver, INF

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Floyd-Warshall - Đồ án 15")
        
        # --- Vùng Nhập liệu ---
        self.input_frame = tk.LabelFrame(root, text="Thiết lập Đồ thị")
        self.input_frame.pack(side="top", fill="x", padx=10, pady=5)

        tk.Label(self.input_frame, text="Số đỉnh:").grid(row=0, column=0)
        self.entry_nodes = tk.Entry(self.input_frame, width=5)
        self.entry_nodes.grid(row=0, column=1)
        self.entry_nodes.insert(0, "4")

        tk.Button(self.input_frame, text="Tạo Ma trận Trống", command=self.init_graph).grid(row=0, column=2, padx=5)

        # --- Vùng Hiển thị Ma trận ---
        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.pack(padx=10, pady=10)
        self.cells = [] # Lưu các label hiển thị ma trận
        
        # --- Vùng Điều khiển & Log ---
        self.ctrl_frame = tk.Frame(root)
        self.ctrl_frame.pack(fill="both", expand=True)
        
        self.btn_next = tk.Button(self.ctrl_frame, text="BƯỚC TIẾP THEO (Next K)", 
                                  state="disabled", command=self.process_step)
        self.btn_next.pack(pady=5)

        self.log_box = tk.Text(self.ctrl_frame, height=8, width=50)
        self.log_box.pack(padx=10, pady=5)

        self.current_k = 0
        self.solver = None

    def init_graph(self):
        """Khởi tạo ma trận hiển thị dựa trên số đỉnh"""
        try:
            n = int(self.entry_nodes.get())
            self.solver = FloydWarshallSolver(n)
            self.current_k = 0
            
            # Xóa các label cũ nếu có
            for row in self.cells:
                for cell in row: cell.destroy()
            self.cells = []

            # Tạo bảng lưới các ô nhập trọng số (Ma trận kề ban đầu)
            for i in range(n):
                row_cells = []
                for j in range(n):
                    # Dùng Entry để người dùng nhập trọng số ban đầu
                    e = tk.Entry(self.matrix_frame, width=5, justify='center')
                    e.grid(row=i, column=j, padx=2, pady=2)
                    if i == j: e.insert(0, "0")
                    else: e.insert(0, "INF")
                    row_cells.append(e)
                self.cells.append(row_cells)
            
            self.btn_next.config(state="normal")
            self.log_box.delete('1.0', tk.END)
            self.log_box.insert(tk.END, "Đã khởi tạo. Hãy nhập trọng số và bấm Next K.\n")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số đỉnh hợp lệ")

    def process_step(self):
        n = self.solver.n
        # Ở bước k=0 đầu tiên, đọc dữ liệu từ các ô Entry vào solver
        if self.current_k == 0:
            for i in range(n):
                for j in range(n):
                    val = self.cells[i][j].get()
                    weight = INF if val.upper() == "INF" else int(val)
                    self.solver.add_edge(i, j, weight)
            # Chuyển các Entry sang Label (chế độ chỉ đọc) để mô phỏng
            self.lock_input()

        if self.current_k < n:
            changes = self.solver.step_k(self.current_k)
            self.update_display(changes)
            self.current_k += 1
        else:
            messagebox.showinfo("Xong", "Thuật toán đã hoàn thành!")
            self.btn_next.config(state="disabled")

    def lock_input(self):
        """Chuyển giao diện từ nhập liệu sang hiển thị tĩnh"""
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                val = self.cells[i][j].get()
                self.cells[i][j].destroy()
                lbl = tk.Label(self.matrix_frame, text=val, width=5, 
                               relief="ridge", bg="white")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.cells[i][j] = lbl

    def update_display(self, changes):
        """Cập nhật giá trị và tô màu các ô thay đổi"""
        # Reset màu nền về trắng
        for row in self.cells:
            for cell in row: cell.config(bg="white")
            
        self.log_box.insert(tk.END, f">> Xét đỉnh trung gian k={self.current_k}\n")
        for i, j, old, new in changes:
            self.cells[i][j].config(text=str(new), bg="lightgreen")
            log_msg = f"   Cập nhật [{i}][{j}]: {old} -> {new}\n"
            self.log_box.insert(tk.END, log_msg)
        self.log_box.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()