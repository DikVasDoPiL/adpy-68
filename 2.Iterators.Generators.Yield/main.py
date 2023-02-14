# 1. Доработать класс FlatIterator в коде ниже. Должен получиться итератор, который принимает список списков и возвращает их плоское представление, т.е последовательность состоящую из вложенных элементов. Функция test в коде ниже также должна отработать без ошибок.

class FlatIterator:

    def __init__(self, list_of_list):
        self.lol = list_of_list
        self.stop = False
        self.counter = [0,0]

    def __iter__(self):
        return self

    def __next__(self):
        c = self.counter
        lol = self.lol
        stop = self.stop
        if stop == False:
            while len(lol) > c[0]:
                if len(lol[c[0]]) > c[1]:
                    item = lol[c[0]][c[1]]
                    c[1] += 1
                    return item
                c[0] += 1
                c[1] = 0
            stop = True
        raise StopIteration


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()


# 2. Доработать функцию flat_generator, Должен получиться генератор, который принимает список списков и возвращает их плоское представление. Функция test в коде ниже также должна отработать без ошибок.

import types


def flat_generator(list_of_lists):
    for list_ in list_of_lists:
        for item in list_:
            yield item


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
    
