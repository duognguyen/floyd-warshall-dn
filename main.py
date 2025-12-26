import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# LIÊN KẾT: Import class từ file algorithm.py
from algorithm import FloydWarshallLogic 

class FloydApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Floyd-Warshall - Đề 15")
        self.root.geometry("1100x800") # Tăng nhẹ chiều cao để chứa Log
        
        self.logic = FloydWarshallLogic()
        self.grid_widgets = []

        # --- Layout chia 2 vùng ---
        left_frame = tk.Frame(root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        right_frame = tk.Frame(root, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- VÙNG BÊN TRÁI: Nhập liệu & Log cập nhật ---
        tk.Label(left_frame, text="Số đỉnh (n):").grid(row=0, column=0)
        self.ent_n = tk.Entry(left_frame, width=5)
        self.ent_n.insert(0, "4")
        self.ent_n.grid(row=0, column=1)
        
        tk.Button(left_frame, text="Tạo lưới", command=self.create_grid).grid(row=0, column=2, padx=5)
        self.btn_import = tk.Button(left_frame, text="Nhập từ File", bg="#3498db", fg="white", 
                                   command=self.import_from_file).grid(row=0, column=3, padx=5)

        self.matrix_container = tk.Frame(left_frame, pady=20)
        self.matrix_container.grid(row=1, column=0, columnspan=4)

        # Cụm nút điều khiển
        self.btn_next = tk.Button(left_frame, text="BẮT ĐẦU (Khởi tạo)", bg="#2ecc71", 
                                 command=self.handle_step, state=tk.DISABLED)
        self.btn_next.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_clear = tk.Button(left_frame, text="XÓA TẤT CẢ", bg="#e74c3c", fg="white",
                                  command=self.clear_all)
        self.btn_clear.grid(row=2, column=2, columnspan=2, pady=10, padx=5, sticky="ew")

        # ĐỔI VỊ TRÍ: Đưa Log cập nhật giá trị sang bên trái
        tk.Label(left_frame, text="Log cập nhật giá trị:").grid(row=3, column=0, sticky="w", pady=(10,0))
        self.log_area = scrolledtext.ScrolledText(left_frame, width=50, height=18, bg="#2c3e50", fg="white")
        self.log_area.grid(row=4, column=0, columnspan=4, sticky="nsew")


        # --- VÙNG BÊN PHẢI: Đồ thị & Đường đi chi tiết ---
        self.canvas_frame = tk.Frame(right_frame, bg="white", highlightbackground="#bdc3c7", highlightthickness=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # ĐỔI VỊ TRÍ: Đưa Đường đi chi tiết sang bên phải (dưới đồ thị)
        tk.Label(right_frame, text="Đường đi chi tiết giữa các cặp đỉnh:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.path_display = scrolledtext.ScrolledText(right_frame, height=12, bg="#ecf0f1")
        self.path_display.pack(fill=tk.X)

    def create_grid(self):
        """Tạo lưới Entry để nhập ma trận"""
        try:
            n = int(self.ent_n.get())
            if n > 8: raise ValueError
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số đỉnh từ 2-8")
            return

        for row in self.grid_widgets:
            for w in row: w.destroy()
        self.grid_widgets = []

        for i in range(n):
            row_entries = []
            for j in range(n):
                ent = tk.Entry(self.matrix_container, width=6, justify='center')
                ent.grid(row=i, column=j, padx=2, pady=2)
                ent.insert(0, "0" if i == j else "inf")
                row_entries.append(ent)
            self.grid_widgets.append(row_entries)
        
        self.btn_next.config(state=tk.NORMAL, text="BẮT ĐẦU (Khởi tạo)")
        self.log_area.delete("1.0", tk.END)

    def update_graph(self):
        """Vẽ lại đồ thị lên Canvas"""
        for w in self.canvas_frame.winfo_children(): w.destroy()
        fig = self.logic.get_figure()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def handle_step(self):
        """Xử lý khi nhấn nút Bước tiếp theo"""
        # --- BƯỚC KHỞI TẠO (Chỉ vẽ đồ thị 1 lần duy nhất tại đây) ---
        if self.btn_next["text"] == "BẮT ĐẦU (Khởi tạo)":
            try:
                n = len(self.grid_widgets)
                matrix = []
                for i in range(n):
                    row = [float(self.grid_widgets[i][j].get().lower()) for j in range(n)]
                    matrix.append(row)
                
                self.logic.initialize(matrix)
                
                # Vẽ đồ thị lần đầu và duy nhất
                self.update_graph() 
                
                self.btn_next.config(text="BƯỚC TIẾP THEO (Next K)")
                self.log_area.insert(tk.END, ">> Đã khởi tạo ma trận và đồ thị.\n")
                return
            except:
                messagebox.showerror("Lỗi", "Ma trận không hợp lệ (Dùng số hoặc 'inf')")
                return
        
        # --- BƯỚC CHẠY K (Chỉ cập nhật số liệu trên lưới, không vẽ lại đồ thị) ---
        # Reset màu nền các ô về trắng
        for row in self.grid_widgets:
            for ent in row: ent.config(bg="white")

        k, updates = self.logic.run_step_k()
        
        if k is not None:
            self.log_area.insert(tk.END, f"--- Đang xét đỉnh trung gian k = {k} ---\n")
            
            # Cập nhật các ô có thay đổi giá trị trên lưới (Grid)
            for up in updates:
                r, c = up['pos']
                new_v = up['new']
                self.grid_widgets[r][c].delete(0, tk.END)
                self.grid_widgets[r][c].insert(0, str(int(new_v) if new_v != np.inf else "inf"))
                self.grid_widgets[r][c].config(bg="#90ee90") # Highlight màu xanh lá
                self.log_area.insert(tk.END, f"  [*] Cập nhật [{r}][{c}]: {up['old']} -> {new_v}\n")
            
            if not updates: 
                self.log_area.insert(tk.END, "  (Không có thay đổi)\n")
            
            self.log_area.see(tk.END)


            # ĐÃ XÓA LỆNH self.update_graph() TẠI ĐÂY ĐỂ TRÁNH VẼ LẠI

            # Kiểm tra kết thúc hoặc lỗi chu trình âm
            if self.logic.negative_cycle:
                messagebox.showerror("Lỗi", "Phát hiện chu trình âm! Thuật toán dừng.")
                self.btn_next.config(state=tk.DISABLED)
            elif self.logic.current_k >= self.logic.n:
                self.show_final_paths()
                
            # Đoạn code bổ sung vào trong hàm handle_step (khi k is not None)
            self.log_area.insert(tk.END, f"\n--- Ma trận NEXT tại bước k={k} ---\n")
            for row in self.logic.next:
            # Chuyển đổi -1 thành '-' để dễ nhìn trong bảng Log
                row_str = " ".join([str(x) if x != -1 else "-" for x in row])
                self.log_area.insert(tk.END, f"  {row_str}\n")
        else:
            self.btn_next.config(state=tk.DISABLED)

    def show_final_paths(self):
        """Hiển thị kết quả đường đi ngắn nhất cuối cùng"""
        self.btn_next.config(text="HOÀN THÀNH", state=tk.DISABLED)
        self.path_display.delete("1.0", tk.END)
        n = self.logic.n
        for i in range(n):
            for j in range(n):
                if i != j:
                    path = self.logic.get_path(i, j)
                    dist = self.logic.dist[i][j]
                    if dist == np.inf:
                        self.path_display.insert(tk.END, f"{i} -> {j}: Không có đường\n")
                    else:
                        path_str = " -> ".join(map(str, path))
                        self.path_display.insert(tk.END, f"{i} -> {j}: {path_str} (CP: {int(dist)})\n") 
    def import_from_file(self):
        """Đọc ma trận từ file .txt hoặc .csv và đổ vào giao diện"""
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            matrix_data = []
            for line in lines:
                if line.strip(): # Bỏ qua dòng trống
                    # Tách các giá trị bằng khoảng trắng hoặc dấu phẩy
                    row = line.replace(',', ' ').split()
                    matrix_data.append(row)

            n = len(matrix_data)
            
            # Kiểm tra tính hợp lệ: Ma trận vuông
            if any(len(row) != n for row in matrix_data):
                messagebox.showerror("Lỗi", "Dữ liệu trong file không phải là ma trận vuông!")
                return

            # 1. Cập nhật con số n trên giao diện
            self.ent_n.delete(0, tk.END)
            self.ent_n.insert(0, str(n))

            # 2. Gọi hàm tạo lưới ma trận (đã có của bạn) để dựng các ô Entry
            self.create_grid()

            # 3. Điền dữ liệu từ file vào các ô Entry vừa tạo
            for i in range(n):
                for j in range(n):
                    val = matrix_data[i][j].lower()
                    self.grid_widgets[i][j].delete(0, tk.END)
                    self.grid_widgets[i][j].insert(0, val)

            self.log_area.insert(tk.END, f">> Đã nhập thành công ma trận {n}x{n} từ file.\n")
            self.log_area.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    def clear_all(self):
        """Reset toàn bộ ứng dụng về trạng thái ban đầu"""
        # 1. Reset logic thuật toán
        self.logic = FloydWarshallLogic()
        
        # 2. Xóa lưới ma trận (Entry widgets)
        for row in self.grid_widgets:
            for ent in row:
                ent.destroy()
        self.grid_widgets = []
        
        # 3. Xóa trắng các vùng văn bản
        self.log_area.delete("1.0", tk.END)
        self.path_display.delete("1.0", tk.END)
        
        # 4. Xóa đồ thị hiện tại trên Canvas
        for w in self.canvas_frame.winfo_children():
            w.destroy()
            
        # 5. Reset trạng thái các nút và ô nhập n
        self.btn_next.config(text="BẮT ĐẦU (Khởi tạo)", state=tk.DISABLED)
        self.ent_n.delete(0, tk.END)
        self.ent_n.insert(0, "4") # Mặc định lại là 4 đỉnh
        
        messagebox.showinfo("Thông báo", "Đã xóa toàn bộ dữ liệu!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FloydApp(root)
    root.mainloop()