good_stickers_id_list = [
    'CAACAgQAAxkBAAELPQplr97hg1Vh-X3xA8QKol4RDeyXXgACmAADX8YBGTYbvHBxeGbVNAQ',
    'CAACAgIAAxkBAAELPQxlr97mwC9vZScrg0p-Vcl0aT_eIQACagADpsrIDGtK7sZiKAktNAQ',
    'CAACAgEAAxkBAAELPQ5lr98puHM97K1HD-hHsnWSEfHAsAAC-wkAAr-MkAQMJ3Ulkwaw7jQE',
    'CAACAgIAAxkBAAELPRBlr9816KcFqgwiY7ESp2AQuEfHsgACHQADwDZPE17YptxBPd5INAQ'
]

bad_stickers_id_list = [
    'CAACAgIAAxkBAAELPRhlr-AMOcKdDnUX5NnrEdNyEKhDHgACYDgAAl_ywEtZdJgec6_qAzQE',
    'CAACAgIAAxkBAAELPRZlr-AJdqdAbi-HVJfiyOwLcJGSLgAC7D0AAnhtwUsfenJqLGhyATQE',
    'CAACAgIAAxkBAAELPRRlr9_-TjS7izaUVecx7Clgx75FDwACIwEAAiov8QuVnf8dwZorKTQE',
    'CAACAgIAAxkBAAELPRJlr9_6JDzof7-axb_q02h7FdVx2wACKwUAAiMFDQABW3KWmdNyE8o0BA'
]

junior_questions = [
    'Какой символ используется для обозначения <u>начала комментария</u> в однострочном комментарии в Python?',
    'Какой из следующих вариантов правильно определяет <u>пустой список</u> в Python?',
    'Какой оператор используется для проверки, <u>принадлежит ли элемент словарю</u> в Python?',
    'Какой метод используется для <u>добавления элемента в конец списка</u> в Python?'
]

junior_explanations = [
    'В Python символ # используется для обозначения начала комментария в одной строке.\nВсе, что идет после символа # на этой строке, считается комментарием и игнорируется интерпретатором Python.',
    'В Python пустой список определяется с помощью квадратных скобок [ ].\nЭто создает новый список, не содержащий ни одного элемента.',
    'В Python оператор in используется для проверки наличия элемента в словаре (и других контейнерах).\nНапример, key in my_dict вернет True, если key существует в словаре my_dict.',
    'Метод append() используется для добавления элемента в конец списка в Python.\nНапример, если у вас есть список my_list, то my_list.append(item) добавит item в конец этого списка.'
]

junior_explanation_code = [
    '<pre># Это комментарий в Python</pre>',
    '<pre>empty_list = []</pre>',
    '<pre>my_dict = {\'a\': 1, \'b\': 2, \'c\': 3}\nif \'a\' in my_dict:\n\tprint(\'Key \"a\" exists in the dictionary.\')</pre>',
    '<pre>my_list = [1, 2, 3]\nmy_list.append(4)  # Теперь my_list содержит [1, 2, 3, 4]</pre>'
]

junior_answers = [
    ['#', '//', '--', '/*'],
    ['[ ]', 'list()', '{}', 'None'],
    ['in', 'exists', 'contains', 'has'],
    ['append()', 'add()', 'insert()', 'extend()']
]


middle_questions = [
    'Как в Python проверить, является ли объект <u>итерируемым</u>?',
    'Какой метод класса в Python вызывается <u>при создании экземпляра класса</u>?',
    'Как в Python получить <u>список всех атрибутов и методов объекта</u>?',
    'Как в Python создать <u>анонимную (lambda) функцию</u>?'
]

middle_explanations = [
    'В Python для проверки, является ли объект итерируемым, можно использовать функцию iter(). Если она не вызывает исключение TypeError, объект итерируем.',
    'Метод __init__() класса в Python вызывается автоматически при создании экземпляра класса. Этот метод обычно используется для инициализации атрибутов экземпляра.',
    'Функция dir() в Python возвращает список атрибутов и методов любого объекта. Это включает как встроенные, так и пользовательские атрибуты и методы.',
    'Анонимные функции в Python создаются с использованием ключевого слова lambda. Они часто используются там, где функция требуется на короткое время, и где определение полноценной функции является избыточным.'
]

middle_explanation_code = [
    '<pre>iterable_object = [1, 2, 3]\ntry:\n\titerator = iter(iterable_object)\n\tprint("Object is iterable")\nexcept TypeError:\n\tprint("Object is not iterable")</pre>',
    '<pre>class MyClass:\n\tdef __init__(self):\n\t\tself.attribute = "value"\n\ninstance = MyClass()</pre>',
    '<pre>my_object = MyClass()\nattributes_and_methods = dir(my_object)\nprint(attributes_and_methods)</pre>',
    '<pre>sum = lambda a, b: a + b\nprint(sum(5, 3)) # Выведет 8</pre>'
]

middle_answers = [
    ['iter()', 'getattr()', 'type()', 'isinstance()'],
    ['__init__()', '__new__()', '__start__()', '__create__()'],
    ['dir()', 'help()', 'attributes()', 'methods()'],
    ['lambda', 'func', 'anonymous()', 'temp()']
]


senior_questions = [
    'Как использовать <u>декораторы</u> в Python?',
    'Что такое <u>список пониманий</u> (list comprehension) в Python?',
    'Как в Python <u>обрабатываются исключения</u>?',
    'Каковы основные <u>принципы ООП</u> в Python?'
]

senior_explanations = [
    'Декораторы в Python — это функции, которые изменяют функционал других функций. Они обычно определяются с помощью @decorator_name перед определением функции.',
    'Список пониманий (list comprehension) в Python — это способ создания списков, который предоставляет более сжатый синтаксис для итерации по последовательностям и их обработки.',
    'Исключения в Python обрабатываются с помощью блоков try...except. try определяет блок кода, в котором могут возникнуть исключения, а except позволяет перехватить исключение и обработать его.',
    'Основные принципы ООП в Python включают инкапсуляцию, наследование, полиморфизм и абстракцию. Эти принципы позволяют создавать структурированные и модульные программы.'
]

senior_explanation_code = [
    '<pre>def my_decorator(func):\n\tdef wrapper():\n\t\tprint("Something before function.")\n\t\tfunc()\n\t\tprint("Something after function.")\n\treturn wrapper\n\n@my_decorator\ndef say_hello():\n\tprint("Hello!")\n\nsay_hello()</pre>',
    '<pre>numbers = [1, 2, 3, 4, 5]\nsquares = [n**2 for n in numbers]</pre>',
    '<pre>try:\n\tresult = 10 / 0\nexcept ZeroDivisionError:\n\tprint("Division by zero!")</pre>',
    '<pre>class Animal:\n\tdef speak(self):\n\t\treturn "Some sound"\n\nclass Dog(Animal):\n\tdef speak(self):\n\t\treturn "Bark"</pre>'
]

senior_answers = [
    ['@decorator', '@function', '@classmethod', '@staticmethod'],
    ['[x for x in sequence]', '[sequence]', '(x for x in sequence)', '{x for x in sequence}'],
    ['try...except', 'if...else', 'for...else', 'with...as'],
    ['Инкапсуляция, Наследование, Полиморфизм, Абстракция', 'Функции, Модули, Пакеты, Классы', 'Ввод, Вывод, Циклы, Условия', 'Классы, Объекты, Функции, Переменные']
]