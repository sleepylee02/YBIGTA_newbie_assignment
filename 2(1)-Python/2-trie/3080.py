from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    trie = Trie[str]()

    lines = int(input())
    for _ in range(lines):
        names = input()
        trie.push(names)

    for i, node in enumerate(trie):
        print(f"Node {i}: body={node.body}, children={node.children}, is_end={node.is_end}")


if __name__ == "__main__":
    main()