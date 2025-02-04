from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """
        get_item과 같은 맥락으로 value를 넣어줄 수 있도록 구현
        연산량을 줄이기위해 matrix에 넣어줄때마다 바로 모듈로 연산 적용하기
        """

        self.matrix[key[0]][key[1]] = value % self.MOD

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        """
        재귀적으로 제곱 연산 진행해주기
        
        n=1이 stopping case가 됨
        이때 제곱횟수가 1일때는 모듈로 연산이 자동적으로 적용이 되지 않으므로
        self.clone의 내용에 따로 모듈로 연산 적용해주기

        추가적으로 n이 1보다 클때는 recursive case를 적용시켜줌
        제곱수가 짝수일때는 서로를 곱해주고
        홀수 일때는 서로를 곱하고 추가로 self.clone을 곱해주는 형식으로 적용
        """

        x, m = self.shape

        if n == 1:
            one = self.clone()
            for i in range(x):
                for j in range(m):
                    one[i, j] %= self.MOD
            return one 

        half = self ** (n // 2)

        if n % 2 == 0:
            return half @ half
        else:
            return half @ half @ self


    def __repr__(self) -> str:
        """
        self.matrix를 각 줄로 나눠 string으로 출력할 있도록 구현
        """

        back = '\n'.join([' '.join(map(str, row)) for row in self.matrix])
        return back


from typing import Callable
import sys


"""
아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)

    print(modmat ** B)


if __name__ == "__main__":
    main()