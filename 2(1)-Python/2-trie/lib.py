from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        current_node = 0  # 루트 노드의 인덱스

        for element in seq:
            # 현재 노드의 children에서 해당 element의 노드를 찾음
            found = False
            for child_index in self[current_node].children:
                if self[child_index].body == element:
                    current_node = child_index
                    found = True
                    break

            # 노드가 없다면 새로 추가
            if not found:
                new_node_index = len(self)
                new_node = TrieNode(body=element)
                self.append(new_node)
                self[current_node].children.append(new_node_index)
                current_node = new_node_index

        # 마지막 노드에 대해 is_end 플래그 설정
        self[current_node].is_end = True
        

# trie = Trie[str]()
# trie.push("hello")
# trie.push("world")
# trie.push("hell")

# # 트리 구조 확인
# for i, node in enumerate(trie):
#     print(f"Node {i}: body={node.body}, children={node.children}, is_end={node.is_end}")