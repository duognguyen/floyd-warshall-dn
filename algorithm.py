import numpy as np

class FloydWarshallLogic:
    def __init__(self):
        self.dist = None
        self.next = None
        self.n = 0
        self.current_k = -1

    def initialize(self, matrix):
        self.n = len(matrix)
        self.dist = np.array(matrix, dtype=float)
        self.next = np.full((self.n, self.n), -1)
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.dist[i][j] != np.inf:
                    self.next[i][j] = j
        self.current_k = 0

    def run_step_k(self):
        """Chạy duy nhất một bước k và trả về danh sách các ô được cập nhật"""
        if self.current_k >= self.n:
            return None, []

        k = self.current_k
        updates = []
        
        for i in range(self.n):
            for j in range(self.n):
                # Công thức: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                old_val = self.dist[i][j]
                new_val = self.dist[i][k] + self.dist[k][j]
                
                if new_val < old_val:
                    self.dist[i][j] = new_val
                    self.next[i][j] = self.next[i][k]
                    updates.append({
                        'pos': (i, j),
                        'old': old_val,
                        'new': new_val
                    })
        
        self.current_k += 1
        return k, updates

    def check_negative_cycle(self):
        for i in range(self.n):
            if self.dist[i][i] < 0:
                return True
        return False