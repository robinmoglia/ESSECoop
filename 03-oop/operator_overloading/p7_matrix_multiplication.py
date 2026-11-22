"""Problem 7: matrix multiplication with *"""

class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])

    def __mul__(self, other):
        if self.n_cols != other.n_rows:
            raise ValueError(
                f"Dimensions incompatibles : ({self.n_rows}x{self.n_cols}) * ({other.n_rows}x{other.n_cols})"
            )
        result = []
        for i in range(self.n_rows):
            new_row = []
            for j in range(other.n_cols):
                total = 0
                for k in range(self.n_cols):
                    total += self.rows[i][k] * other.rows[k][j]
                new_row.append(total)
            result.append(new_row)
        return Matrix(result)

    def __repr__(self):
        return f"Matrix({self.rows})"


if __name__ == "__main__":
    A = Matrix([[1, 2],
                [3, 4]])
    B = Matrix([[5, 6],
                [7, 8]])
    print(A * B)

    C = Matrix([[1, 2, 3]])
    D = Matrix([[1], [2], [3]])
    print(C * D)
    print(D * C)

    try:
        A * C
    except ValueError as e:
        print("Erreur :", e)
