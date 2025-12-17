# algorithm.py
import numpy as np

INF = 999999

class FloydWarshallSolver:
    def __init__(self, num_nodes):
        self.n = num_nodes
        self.dist = np.full((num_nodes, num_nodes), INF)
        # Đường chéo chính khởi tạo bằng 0
        for i in range(num_nodes):
            self.dist[i][i] = 0

    def add_edge(self, u, v, w):
        self.dist[u][v] = w
        self.dist[v][u] = w 
        
    def step_k(self, k):
        """Thực hiện một bước k duy nhất và trả về các thay đổi"""
        updates = []
        for i in range(self.n):
            for j in range(self.n):
                # Chỉ xét nếu có đường đi từ i đến k và từ k đến j
                if self.dist[i][k] != INF and self.dist[k][j] != INF:
                    new_dist = self.dist[i][k] + self.dist[k][j]
                    if self.dist[i][j] > new_dist:
                        old_val = self.dist[i][j]
                        self.dist[i][j] = new_dist
                        # Trả về: (hàng, cột, giá trị cũ, giá trị mới)
                        updates.append((i, j, old_val, new_dist))
        return updates