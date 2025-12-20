import tkinter as tk
from tkinter import messagebox, scrolledtext
from algorithm import FloydWarshallLogic
import numpy as np

class FloydApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Floyd-Warshall - Đồ án 15")
        self.root.geometry("900x750")
        self.logic = FloydWarshallLogic()
        self.grid_widgets = [] # Lưu các ô Entry trên giao diện

        # --- Khu vực thiết lập số đỉnh ---
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack()
        
        tk.Label(top_frame, text="Số đỉnh:").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(top_frame, width=5)
        self.ent_n.insert(0, "4")
        self.ent_n.pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="Tạo Ma trận Trống", command=self.create_grid).pack(side=tk.LEFT)

        # --- Khu vực hiển thị Ma trận (Lưới) ---
        self.matrix_frame = tk.Frame(root, pady=20)
        self.matrix_frame.pack()

        # --- Nút điều khiển ---
        self.btn_next = tk.Button(root, text="BƯỚC TIẾP THEO (Next K)", 
                                 command=self.next_step, state=tk.DISABLED, 
                                 font=("Arial", 10, "bold"), bg="#f0f0f0")
        self.btn_next.pack(pady=10)

        # --- Bảng Log cập nhật ---
        log_label = tk.Label(root, text="Bảng log thay đổi:", font=("Arial", 10, "italic"))
        log_label.pack()
        self.log_area = scrolledtext.ScrolledText(root, height=15, width=80, bg="white", font=("Consolas", 10))
        self.log_area.pack(pady=10)

    def create_grid(self):
        """Tạo lưới ô nhập dựa trên số đỉnh n"""
        try:
            n = int(self.ent_n.get())
            if n > 10: raise ValueError("Số đỉnh quá lớn để hiển thị lưới.")
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số đỉnh hợp lệ (2-10).")
            return

        # Xóa lưới cũ
        for row in self.grid_widgets:
            for w in row: w.destroy()
        self.grid_widgets = []
        self.log_area.delete("1.0", tk.END)
        self.btn_next.config(state=tk.NORMAL, text="BẮT ĐẦU (Khởi tạo)")

        # Tạo lưới mới
        for i in range(n):
            row_entries = []
            for j in range(n):
                ent = tk.Entry(self.matrix_frame, width=6, justify='center', font=("Arial", 11))
                ent.grid(row=i, column=j, padx=2, pady=2)
                if i == j:
                    ent.insert(0, "0")
                else:
                    ent.insert(0, "inf")
                row_entries.append(ent)
            self.grid_widgets.append(row_entries)
        
        self.logic.n = n
        self.log_area.insert(tk.END, f"Đã tạo ma trận {n}x{n}. Nhập trọng số và bấm 'Bắt đầu'.\n")

    def next_step(self):
        # Bước 0: Đọc dữ liệu từ lưới vào logic
        if self.btn_next["text"] == "BẮT ĐẦU (Khởi tạo)":
            matrix = []
            try:
                for i in range(self.logic.n):
                    row = []
                    for j in range(self.logic.n):
                        val = self.grid_widgets[i][j].get().lower()
                        row.append(float(val) if val != "inf" else np.inf)
                    matrix.append(row)
                self.logic.initialize(matrix)
                self.log_area.insert(tk.END, ">> Đã khởi tạo. Hãy bấm 'Next K' để chạy từng bước.\n")
                self.btn_next.config(text="BƯỚC TIẾP THEO (Next K)")
                return
            except:
                messagebox.showerror("Lỗi", "Dữ liệu ma trận không hợp lệ (Dùng số hoặc 'inf').")
                return

        # Reset màu nền về trắng trước khi highlight mới
        for row in self.grid_widgets:
            for ent in row: ent.config(bg="white")

        # Chạy bước k
        k, updates = self.logic.run_step_k()

        if k is not None:
            self.log_area.insert(tk.END, f">> Xét đỉnh trung gian k = {k}\n")
            if not updates:
                self.log_area.insert(tk.END, f"   (Không có thay đổi nào tại bước k={k})\n")
            
            for up in updates:
                r, c = up['pos']
                old, new = up['old'], up['new']
                # Cập nhật giá trị lên giao diện
                self.grid_widgets[r][c].delete(0, tk.END)
                self.grid_widgets[r][c].insert(0, str(int(new) if new != np.inf else "inf"))
                # Highlight màu xanh
                self.grid_widgets[r][c].config(bg="#90ee90") # Màu xanh lá nhạt
                # Ghi log chi tiết
                self.log_area.insert(tk.END, f"   Cập nhật [{r}][{c}]: {int(old) if old!=np.inf else 'inf'} -> {int(new)}\n")
            
            self.log_area.see(tk.END)
            
            # Kiểm tra hoàn thành hoặc chu trình âm
            if self.logic.check_negative_cycle():
                self.log_area.insert(tk.END, "!!! PHÁT HIỆN CHU TRÌNH ÂM !!!\n")
                self.btn_next.config(state=tk.DISABLED)
            elif self.logic.current_k >= self.logic.n:
                self.log_area.insert(tk.END, "== THUẬT TOÁN KẾT THÚC ==\n")
                self.btn_next.config(state=tk.DISABLED)
        else:
            self.btn_next.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloydApp(root)
    root.mainloop()