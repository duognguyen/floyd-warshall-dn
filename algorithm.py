import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class FloydWarshallLogic:
    def __init__(self):
        self.dist = None
        self.next = None
        self.n = 0
        self.current_k = -1
        self.history = []
        self.negative_cycle = False

    def initialize(self, matrix):
        """Khởi tạo dữ liệu ban đầu từ ma trận kề"""
        self.n = len(matrix)
        self.dist = np.array(matrix, dtype=float)
        self.next = np.full((self.n, self.n), -1)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i][j] != np.inf:
                    self.next[i][j] = j
        self.current_k = 0
        self.history = []
        self.negative_cycle = False

    def run_step_k(self):
        """Chạy duy nhất một bước k (đỉnh trung gian)"""
        if self.current_k >= self.n or self.negative_cycle:
            return None, []

        k = self.current_k
        updates = []
        for i in range(self.n):
            for j in range(self.n):
                old_val = self.dist[i][j]
                new_val = self.dist[i][k] + self.dist[k][j]
                
                if new_val < old_val:
                    self.dist[i][j] = new_val
                    self.next[i][j] = self.next[i][k]
                    updates.append({'pos': (i, j), 'old': old_val, 'new': new_val})
        
        self.history.append((f"k={k}", self.dist.copy(), updates))
        if self.check_negative_cycle(): 
            self.negative_cycle = True
            
        self.current_k += 1
        return k, updates

    def check_negative_cycle(self):
        """Kiểm tra đường chéo chính xem có giá trị âm không"""
        for i in range(self.n):
            if self.dist[i][i] < 0: return True
        return False

    def get_path(self, u, v):
        """Truy vết đường đi ngắn nhất từ u đến v"""
        if self.next[u][v] == -1: return []
        path = [u]
        curr = u
        while curr != v:
            curr = int(self.next[curr][v])
            path.append(curr)
        return path

    def get_figure(self):
        """Tạo hình ảnh đồ thị bằng Matplotlib"""
        fig = plt.figure(figsize=(4, 3))
        G = nx.DiGraph()
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i][j] != np.inf:
                    G.add_edge(i, j, weight=int(self.dist[i][j]))
        
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='orange', 
                node_size=500, font_size=8, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)
        return fig