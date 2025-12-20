import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class FloydWarshallLogic:
    def __init__(self):
        self.dist = None
        self.next = None
        self.n = 0
        self.history = [] # Lưu lại ma trận sau mỗi bước k
        self.negative_cycle = False

    def process_matrix(self, matrix_data):
        """
        Input: Ma trận kề từ UI (với np.inf cho các cạnh không có kết nối)
        """
        self.n = len(matrix_data)
        self.dist = np.array(matrix_data, dtype=float)
        # Ma trận truy vết: next[i][j] lưu đỉnh tiếp theo trên đường đi từ i đến j
        self.next = np.full((self.n, self.n), -1)
        
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i][j] != np.inf:
                    self.next[i][j] = j
        
        self.history = []
        self.negative_cycle = False

    def run_floyd(self):
        # Lưu trạng thái ban đầu (k = -1 hoặc khởi tạo)
        self.history.append(("Khởi tạo", self.dist.copy(), self.next.copy()))

        for k in range(self.n):
            prev_dist = self.dist.copy()
            updates = []
            for i in range(self.n):
                for j in range(self.n):
                    # Công thức Quy hoạch động: Vai trò đỉnh trung gian k
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.next[i][j] = self.next[i][k]
                        updates.append((i, j))
            
            # Lưu lại ma trận sau mỗi vòng lặp k để hiển thị Log
            self.history.append((f"k = {k}", self.dist.copy(), self.next.copy(), updates))

            # Kiểm tra chu trình âm: Nếu đường đi từ i đến chính nó < 0
            for i in range(self.n):
                if self.dist[i][i] < 0:
                    self.negative_cycle = True
                    return False
        return True

    def get_path(self, u, v):
        """Truy vết đường đi từ u đến v dựa trên ma trận next"""
        if self.next[u][v] == -1:
            return []
        path = [u]
        while u != v:
            u = int(self.next[u][v])
            path.append(u)
        return path

    def get_figure(self):
        """Trực quan hóa đồ thị ban đầu"""
        fig = plt.figure(figsize=(5, 4))
        G = nx.DiGraph()
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i][j] != np.inf:
                    G.add_edge(i, j, weight=self.dist[i][j])
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='orange', node_size=700)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        return fig