#!/usr/bin/env python3

class SparseMatrix:
    """
    implementation of a sparse matrix using a dictionary.
    """

    def __init__(self, num_rows=0, num_cols=0):
        """Initialize an empty sparse matrix"""
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.data = {}  

    @classmethod
    def from_file(cls, file_path):
        """Create a SparseMatrix from a formatted text file"""
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                raise ValueError("Input file has wrong format")

            num_rows = int(lines[0].split('=')[1])
            num_cols = int(lines[1].split('=')[1])
            matrix = cls(num_rows, num_cols)

            for line in lines[2:]:
                if not (line.startswith('(') and line.endswith(')')):
                    raise ValueError("Input file has wrong format")

                parts = line[1:-1].split(',')
                if len(parts) != 3:
                    raise ValueError("Input file has wrong format")

                try:
                    r = int(parts[0].strip())
                    c = int(parts[1].strip())
                    v = int(parts[2].strip())
                except:
                    raise ValueError("Input file has wrong format")

                matrix.set_element(r, c, v)

            return matrix
        except Exception as e:
            raise ValueError("Input file has wrong format") from e

    def get_element(self, row, col):
        """Return the element at (row, col); returns 0 if not set"""
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """Set the element at (row, col); removes it if value is 0"""
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def add(self, other):
        """Return a new matrix that is the sum of self and other"""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Addition requires matrices of same dimensions")

        result = SparseMatrix(self.num_rows, self.num_cols)
        all_keys = set(self.data.keys()).union(other.data.keys())

        for key in all_keys:
            val = self.get_element(*key) + other.get_element(*key)
            result.set_element(*key, val)

        return result

    def subtract(self, other):
        """Return a new matrix that is the difference of self and other"""
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Subtraction requires matrices of same dimensions")

        result = SparseMatrix(self.num_rows, self.num_cols)
        all_keys = set(self.data.keys()).union(other.data.keys())

        for key in all_keys:
            val = self.get_element(*key) - other.get_element(*key)
            result.set_element(*key, val)

        return result

    def multiply(self, other):
        """Return the product of self and other as a new matrix"""
        if self.num_cols != other.num_rows:
            raise ValueError("Multiplication requires self.cols == other.rows")

        result = SparseMatrix(self.num_rows, other.num_cols)

        for (i, k), val1 in self.data.items():
            for j in range(other.num_cols):
                val2 = other.get_element(k, j)
                if val2 != 0:
                    prev = result.get_element(i, j)
                    result.set_element(i, j, prev + val1 * val2)

        return result

    def __str__(self):
        """Return a string representation of the matrix in file format"""
        lines = [f"rows={self.num_rows}", f"cols={self.num_cols}"]
        for (r, c), v in sorted(self.data.items()):
            lines.append(f"({r}, {c}, {v})")
        return "\n".join(lines)

    def save_to_file(self, file_path):
        """Save the matrix to a text file in a readable format"""
        try:
            with open(file_path, 'w') as f:
                f.write(str(self))
        except IOError as e:
            raise IOError(f"Failed to write to file: {file_path}") from e


def main():
    """CLI interface for matrix operations: add, subtract, multiply"""
    try:
        file1 = input("Enter the path to the first matrix file: ").strip()
        file2 = input("Enter the path to the second matrix file: ").strip()
        operation = input("Enter operation (add / subtract / multiply): ").strip().lower()
        output = input("Enter output file name: ").strip()

        m1 = SparseMatrix.from_file(file1)
        m2 = SparseMatrix.from_file(file2)

        if operation == 'add':
            result = m1.add(m2)
        elif operation == 'subtract':
            result = m1.subtract(m2)
        elif operation == 'multiply':
            result = m1.multiply(m2)
        else:
            raise ValueError("Invalid operation")

        result.save_to_file(output)
        print(f"Result saved to {output}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
