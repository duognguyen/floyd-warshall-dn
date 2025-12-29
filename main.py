import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import FloydWarshallLogic

class FloydApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Floyd-Warshall - Đề 15")
        self.root.geometry("1100x800")
        
        self.logic = FloydWarshallLogic() 
        self.grid_widgets = []            # Lưu các ô Entry trên giao diện
        self.setup_ui()
    def setup_ui(self):
       
        # left_frame: Chứa nhập liệu, điều khiển và Log
        left_frame = tk.Frame(root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # right_frame: Chứa đồ thị trực quan và kết quả đường đi
        right_frame = tk.Frame(root, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- VÙNG NHẬP LIỆU (Bên trái) ---
        tk.Label(left_frame, text="Số đỉnh (n):").grid(row=0, column=0)
        self.ent_n = tk.Entry(left_frame, width=5)
        # self.ent_n.insert(0, "4") # Mặc định ban đầu là 4 đỉnh
        self.ent_n.grid(row=0, column=1)
        
        # Các nút thao tác cơ bản
        tk.Button(left_frame, text="Tạo bảng", command=self.create_table).grid(row=0, column=2, padx=5)
        self.btn_import = tk.Button(left_frame, text="Nhập từ File", bg="#3498db", fg="white", 
                                   command=self.import_from_file).grid(row=0, column=3, padx=5)

        # Container chứa ma trận đầu vào
        self.matrix_container = tk.Frame(left_frame, pady=20)
        self.matrix_container.grid(row=1, column=0, columnspan=4)

        # Cụm nút bấm điều khiển luồng chạy thuật toán
        self.btn_next = tk.Button(left_frame, text="BẮT ĐẦU", bg="#2ecc71", 
                                 command=self.handle_step, state=tk.DISABLED)
        self.btn_next.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.btn_clear = tk.Button(left_frame, text="XÓA TẤT CẢ", bg="#e74c3c", fg="white",
                                  command=self.clear_all)
        self.btn_clear.grid(row=2, column=2, columnspan=2, pady=10, padx=5, sticky="ew")

        # Vùng Log: Hiển thị chi tiết từng bước thay đổi số liệu
        tk.Label(left_frame, text="Log cập nhật giá trị (Ma trận Dist & Next):").grid(row=3, column=0, sticky="w", pady=(10,0))
        self.log_area = scrolledtext.ScrolledText(left_frame, width=50, height=18, bg="#2c3e50", fg="white")
        self.log_area.grid(row=4, column=0, columnspan=4, sticky="nsew")

        # --- VÙNG TRỰC QUAN (Bên phải) ---
        # Nơi chứa biểu đồ Matplotlib
        self.canvas_frame = tk.Frame(right_frame, bg="white", highlightbackground="#bdc3c7", highlightthickness=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Vùng hiển thị kết quả đường đi chi tiết sau khi chạy xong
        tk.Label(right_frame, text="Đường đi chi tiết giữa các cặp đỉnh:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.path_display = scrolledtext.ScrolledText(right_frame, height=12, bg="#ecf0f1")
        self.path_display.pack(fill=tk.X)

    def create_table(self):
        """Khởi tạo lưới các ô Entry tương ứng với số đỉnh n"""
        self.grid_widgets = []
        try:
            n = int(self.ent_n.get())
            if n <= 1 : raise ValueError 
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số đỉnh lớn hơn 0")
            return

        # Tạo lưới Entry
        for i in range(n):
            row_entries = []
            for j in range(n):
                ent = tk.Entry(self.matrix_container, width=6, justify='center')
                ent.grid(row=i, column=j, padx=2, pady=2)
                # Đường chéo chính là 0, các ô khác mặc định là 'inf' (vô cùng)
                ent.insert(0, "0" if i == j else "inf")
                row_entries.append(ent)
            self.grid_widgets.append(row_entries)
        
        self.btn_next.config(state=tk.NORMAL, text="BẮT ĐẦU")
        self.log_area.delete("1.0", tk.END)

    def get_figure(self):
        """Sử dụng NetworkX và Matplotlib để vẽ trực quan hóa đồ thị"""
        fig = plt.figure(figsize=(4, 3))
        G = nx.DiGraph() 
        
        # Lấy dữ liệu từ lớp logic để vẽ
        n = self.logic.n
        dist_matrix = self.logic.dist
        
        for i in range(n):
            for j in range(n):
                # Chỉ vẽ các cạnh có trọng số thực tế (không phải vô cùng)
                if i != j and dist_matrix[i][j] != np.inf:
                    G.add_edge(i, j, weight=int(dist_matrix[i][j]))
        
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='orange', 
                node_size=500, font_size=8, font_weight='bold')
        
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)
        return fig

    def update_graph(self):
        """Vẽ và hiển thị đồ thị lên Canvas của Tkinter"""
        for w in self.canvas_frame.winfo_children(): 
            w.destroy()
            
        # Gọi hàm get_figure
        fig = self.get_figure() 
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)
    

    def handle_step(self):
        """Hàm điều phối: Xử lý khi người dùng nhấn nút 'BƯỚC TIẾP THEO'"""
        # Giai đoạn 1: Đọc ma trận từ UI và khởi tạo logic
        if self.btn_next["text"] == "BẮT ĐẦU":
            try:
                n = len(self.grid_widgets)
                matrix = []
                for i in range(n):
                    row = [float(self.grid_widgets[i][j].get().lower()) for j in range(n)]
                    matrix.append(row)
                
                self.logic.initialize(matrix)
                self.update_graph()
                
                self.btn_next.config(text="BƯỚC TIẾP THEO (Next K)")
                self.log_area.insert(tk.END, ">> Đã khởi tạo ma trận và đồ thị.\n")
                return
            except:
                messagebox.showerror("Lỗi", "Ma trận không hợp lệ (Dùng số hoặc 'inf')")
                return
        
        # Giai đoạn 2: Chạy từng bước k
        for row in self.grid_widgets:
            for ent in row: ent.config(bg="white") # Reset màu nền

        k, updates = self.logic.run_step_k()
        
        if k is not None:
            self.log_area.insert(tk.END, f"--- Đang xét đỉnh trung gian k = {k} ---\n")
            
            # Cập nhật giá trị mới lên các ô Entry và đổi màu xanh để nhận biết
            for up in updates:
                r, c = up['pos']
                new_v = up['new']
                self.grid_widgets[r][c].delete(0, tk.END)
                self.grid_widgets[r][c].insert(0, str(int(new_v) if new_v != np.inf else "inf"))
                self.grid_widgets[r][c].config(bg="#90ee90") # Highlight màu xanh
                self.log_area.insert(tk.END, f"  [*] Cập nhật [{r}][{c}]: {up['old']} -> {new_v}\n")
            
            if not updates: 
                self.log_area.insert(tk.END, "  (Không có thay đổi trong bước này)\n")
            
            self.log_area.insert(tk.END, f"\n--- Ma trận TRUY VẾT (NEXT) tại k={k} ---\n")
            for row in self.logic.next:
                row_str = " ".join([str(x) if x != -1 else "-" for x in row])
                self.log_area.insert(tk.END, f"  {row_str}\n")
            
            self.log_area.see(tk.END)

            # Kiểm tra các điều kiện dừng
            if self.logic.negative_cycle:
                messagebox.showerror("Lỗi", "Phát hiện chu trình âm! Thuật toán dừng lại.")
                self.btn_next.config(state=tk.DISABLED)
            elif self.logic.current_k >= self.logic.n:
                self.show_final_paths() # Kết thúc: in đường đi chi tiết
        else:
            self.btn_next.config(state=tk.DISABLED)

    def show_final_paths(self):
        """In danh sách đường đi ngắn nhất của mọi cặp đỉnh"""
        self.btn_next.config(text="HOÀN THÀNH", state=tk.DISABLED)
        self.path_display.delete("1.0", tk.END)
        self.path_display.insert(tk.END, "--- DANH SÁCH ĐƯỜNG ĐI CHI TIẾT ---\n\n")
        
        n = self.logic.n
        for i in range(n):
            for j in range(n):
                if i != j:
                    path = self.logic.get_path(i, j)
                    dist = self.logic.dist[i][j]
                    
                    if dist == np.inf or not path:
                        self.path_display.insert(tk.END, f" ❌ {i} -> {j}: Không có đường đi\n")
                    else:
                        # Nối danh sách các đỉnh bằng dấu mũi tên
                        path_str = " -> ".join(map(str, path))
                        self.path_display.insert(tk.END, f" ✅ {i} -> {j}: {path_str} (Chi phí: {int(dist)})\n")
        self.path_display.see("1.0")

    def import_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path: return

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            matrix_data = []
            for line in lines:
                if line.strip():
                    row = line.replace(',', ' ').split()
                    matrix_data.append(row)

            n = len(matrix_data)
            self.ent_n.delete(0, tk.END)
            self.ent_n.insert(0, str(n))
            self.create_table()

            # Điền dữ liệu vào các ô Entry vừa tạo
            for i in range(n):
                for j in range(n):
                    self.grid_widgets[i][j].delete(0, tk.END)
                    self.grid_widgets[i][j].insert(0, matrix_data[i][j].lower())

            self.log_area.insert(tk.END, f">> Nhập file thành công: {n}x{n} đỉnh.\n")
        except Exception as e:
            messagebox.showerror("Lỗi File", f"Lỗi: {str(e)}")

    def clear_all(self):
        """Reset toàn bộ ứng dụng về trạng thái mới bắt đầu"""
        self.logic = FloydWarshallLogic()
        self.ent_n.delete(0, tk.END)
        for row in self.grid_widgets:
            for ent in row: ent.destroy()
        self.grid_widgets = []
        self.log_area.delete("1.0", tk.END)
        self.path_display.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children(): w.destroy()
        self.btn_next.config(text="BẮT ĐẦU (Khởi tạo)", state=tk.DISABLED)
        messagebox.showinfo("Reset", "Đã xóa toàn bộ dữ liệu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FloydApp(root)
    root.mainloop()