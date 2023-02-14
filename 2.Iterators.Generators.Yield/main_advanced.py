# 3.* Написать итератор аналогичный итератору из задания 1, но обрабатывающий списки с любым уровнем вложенности. Шаблон и тест в коде ниже:

class FlatIterator:

    def __init__(self, list_of_list):
        self.lol = list_of_list
        self.stop = False
        self.i = [0, 0]


    def __iter__(self):
        return self

    def __next__(self):
        level = self.i[0]
        if self.stop == False:
            while len(self.lol) > self.i:
                if len(self.lol[self.i[level]]) > self.j:
                    item = self.lol[self.i][self.j]
                    self.j += 1
                    return item
                self.i += 1
                self.j = 0
            self.stop = True
        raise StopIteration
    
    
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    # test_3()

    list_of_lists_2 = [
            [['a'], ['b', 'c']],
            ['d', 'e', [['f'], 'h'], False],
            [1, 2, None, [[[[['!']]]]], []]
        ]

    print(list(FlatIterator(list_of_lists_2)))