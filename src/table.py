class Table:
    _index: list[str]
    _columns: list[str]
    _values: list[list[int or float]]

    _cur_row: int
    _cur_col: int

    def __init__(self, index: list[str], columns: list[str]):
        self._index = index
        self._columns = columns
        self._values = [[0 for _ in range(len(columns))] for __ in range(len(index))]
        self._cur_col = 0
        self._cur_row = 0

    def set(self, value: int) -> None:
        self._values[self._cur_row][self._cur_col] = value
        self._cur_col += 1
        if self._cur_col == len(self._columns):
            self._cur_row += 1
            self._cur_col = 0

    def to_tsv(self, file_name: str) -> None:
        with open(file_name, 'w+', encoding='utf-8') as file:
            file.write('\t' + '\t'.join(self._columns) + '\n')
            for row_name, row in zip(self._index, self._values):
                file.write('\t'.join([row_name] + list(map(str, row))) + '\n')
