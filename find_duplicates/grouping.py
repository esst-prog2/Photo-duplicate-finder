from pathlib import Path


class _UnionFind:
    def __init__(self, items):
        self._parent = {item: item for item in items}

    def find(self, item):
        while self._parent[item] != item:
            self._parent[item] = self._parent[self._parent[item]]
            item = self._parent[item]
        return item

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a != root_b:
            self._parent[root_b] = root_a


def merge_duplicate_groups(
    files: list[Path],
    exact_groups: list[list[Path]],
    near_duplicate_pairs: list[tuple[Path, Path]],
) -> list[list[Path]]:
    union_find = _UnionFind(files)

    for group in exact_groups:
        for member in group[1:]:
            union_find.union(group[0], member)

    for file_a, file_b in near_duplicate_pairs:
        union_find.union(file_a, file_b)

    groups: dict[Path, list[Path]] = {}
    for file in files:
        groups.setdefault(union_find.find(file), []).append(file)
    return [group for group in groups.values() if len(group) > 1]
