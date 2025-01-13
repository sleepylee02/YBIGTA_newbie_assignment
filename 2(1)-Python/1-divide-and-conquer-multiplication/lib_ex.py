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
        """

        self.matrix[key[0]][key[1]] = value

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
        일단 power list 내 최대 곱 형태로 구현
        A**13 이면 A**2 그리고 A**2 * A**2 으로 A**4 구현
        이떄 A**8이 최대 곱 형태
        이후 power list내 존재하는 A**4 를 활용해 A**12 구함
        마지막으로 남은 계산은 필요 횟수만큼 직접 A를 곱해주기 
        이때 곱해주는 과정은 result list에서 실행
        """
        
        x, m = self.shape

        power = 1
        while n >= 2 ** power:
            power += 1 
        
        power_lst: list[Matrix] = []
        power_lst.append(self @ self)
        #print(power)

        for i in range(power - 1):
            if i > 0:
                power_lst.append(power_lst[i-1] @ power_lst[i-1])
        #print(power_lst)

        id: Matrix = self.eye(x)

        while power > 0:
            if n > 2 ** (power-1):
                if (power-1) > 0:
                    id @= power_lst[power-2]
                    n -= 2 ** (power-1)
            power -= 1
            
        for _ in range(n):
            id = id @ self

        # result_lst: list[Matrix] = []

        # while power > 0:
        #     if n > 2 ** (power-1):
        #         if (power-1) > 0:
        #             result_lst.append(power_lst[power-2])
        #             n -= 2 ** (power-1)
        #     power -= 1
        
        # #print(result_lst)

        # id: Matrix = self.eye(x)
        
        # for i in range(len(result_lst)):
        #     id = id @ result_lst[i]
        
        # for _ in range(n):
        #     id = id @ self

        # #print(x,m)

        for i in range(x):
            for j in range(m):
                id[i, j] %= self.MOD

        return id


# def __pow__(self, n: int) -> Matrix:
#         x,m = self.shape
#         pow_lst = []      
#         pow_lst.append(n)
        
#         while n != 1:
#             n //= 2
#             pow_lst.append(n)
        
#         result: Matrix = self.clone()


#         for _ in range(len(pow_lst)-1):
#             pow_lst.pop()
#             if pow_lst[-1] % 2 ==0:
#                 result = result @ result
#             else:
#                 result = result @ result @ self
        
#         for i in range(x):
#             for j in range(m):
#                 result[i, j] %= self.MOD


#    def __pow__(self, n: int) -> Matrix:
#         x,m = self.shape
#         result = self.clone()

#         result = self.eye(x) 
#         base = self.clone()

#         while n != 1:
#             if n % 2 == 1:  
#                 result = result @ base
#             base = base @ base  
#             n //= 2
#         result @= base

#         for i in range(x):
#             for j in range(x):
#                 result[i, j] %= self.MOD

#         return result

    def __repr__(self) -> str:
        """
        self.matrix를 각 줄로 나눠 string으로 출력할 있도록 구현
        """

        back = '\n'.join([' '.join(map(str, row)) for row in self.matrix])
        return back
    # \n 으로 하나의 스트링 만들어서 리턴해주기~~~