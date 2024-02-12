junior_questions = [
    'Какой метод используется для <u>чтения файлов асинхронно</u> в Node.js?',
    'Что делает оператор `===` в JavaScript?',
    'Что возвращает метод `Array.map()` в JavaScript?',
    'Каким образом можно <u>экспортировать модуль</u> в Node.js?'
]

junior_explanations = [
    'В Node.js метод `fs.readFile()` используется для асинхронного чтения содержимого файла. Этот метод не блокирует выполнение программы во время чтения файла.',
    'Оператор `===` в JavaScript используется для проверки равенства значений и типов двух переменных. Это строгое сравнение, которое не выполняет приведение типов.',
    'Метод `Array.map()` в JavaScript создаёт новый массив, вызывая указанную функцию для каждого элемента исходного массива. Этот метод не изменяет исходный массив.',
    'Для экспорта модуля в Node.js можно использовать `module.exports`. Это позволяет делать доступными функции и переменные из одного модуля в других модулях.'
]

junior_explanation_code = [
    '<pre>const fs = require(\'fs\');\nfs.readFile(\'path/to/file\', \'utf8\', (err, data) => {\n  if (err) throw err;\n  console.log(data);\n});</pre>',
    '<pre>const a = 5;\nconst b = \'5\';\nconsole.log(a === b);  // false</pre>',
    '<pre>const numbers = [1, 2, 3];\nconst doubled = numbers.map(num => num * 2);\nconsole.log(doubled);  // [2, 4, 6]</pre>',
    '<pre>// В файле myModule.js\nmodule.exports = { myFunction, myVariable };</pre>'
]

junior_answers = [
    ['fs.readFile()', 'fs.readFileSync()', 'fs.read()', 'fs.loadFile()'],
    ['Сравнивает значения и типы данных', 'Сравнивает только значения', 'Проверяет неравенство', 'Приводит один из операндов к типу другого'],
    ['Возвращает новый массив', 'Модифицирует исходный массив', 'Не возвращает ничего', 'Вызывает функцию для каждого элемента, не создавая новый массив'],
    ['module.exports', 'export default', 'export', 'export const']
]


middle_questions = [
    'Какие методы Node.js используются для <u>работы с потоками данных</u>?',
    'Как в JavaScript создать <u>приватное свойство</u> в классе?',
    'Какой метод массива в JavaScript используется для <u>асинхронной обработки каждого элемента массива</u>?',
    'Какие инструменты используются для <u>управления асинхронными операциями</u> в JavaScript?',
    'Как управлять <u>асинхронными ошибками</u> в Node.js?',
    'Что такое <u>Event Loop</u> в Node.js?',
    'Как использовать Stream API в Node.js для обработки больших объёмов данных?',
    'Какие механизмы Node.js позволяют управлять <u>зависимостями</u> в проекте?'

]

middle_explanations = [
    'В Node.js для работы с потоками данных используются методы, такие как `stream.Readable` для чтения и `stream.Writable` для записи данных.',
    'В JavaScript приватные свойства в классе создаются с помощью символа # перед именем свойства. Это делает свойство доступным только внутри класса.',
    'Метод `Array.prototype.forEach()` не поддерживает асинхронную обработку, однако можно использовать методы вроде `Array.map()` в сочетании с `Promise.all()` для асинхронной обработки.',
    'Для управления асинхронными операциями в JavaScript используются промисы (Promises), async/await и колбэки (callbacks).',
    'Асинхронные ошибки в Node.js можно управлять с помощью промисов и async/await, обертывая асинхронные операции в try...catch блоки.',
    'Event Loop в Node.js — это механизм, который позволяет Node.js выполнять неблокирующие операции I/O, переключаясь между разными задачами.',
    'Stream API в Node.js используется для эффективной обработки больших объёмов данных путём чтения и записи данных в потоках.',
    'Для управления зависимостями в Node.js проектах используются npm или yarn, которые управляют пакетами и их версиями.'

]

middle_explanation_code = [
    '<pre>const fs = require(\'fs\');\nconst readableStream = fs.createReadStream(\'file.txt\');\nreadableStream.on(\'data\', function(chunk) {\n\tconsole.log(chunk);\n});</pre>',
    '<pre>class MyClass {\n\t#privateProperty = "secret";\n\tgetPrivateProperty() {\n\t\treturn this.#privateProperty;\n\t}\n}</pre>',
    '<pre>async function processArray(array) {\n\tawait Promise.all(array.map(async (item) => {\n\t\t// обработка элемента\n\t}));\n}</pre>',
    '<pre>function asyncOperation() {\n\treturn new Promise((resolve, reject) => {\n\t\t// асинхронная операция\n\t});\n}\nasyncOperation().then(result => console.log(result));</pre>',
    '<pre>async function asyncOperation() {\n\ttry {\n\t\tawait someAsyncFunction();\n\t} catch (error) {\n\t\tconsole.error(error);\n\t}\n}</pre>',
    '<pre>// Event Loop обрабатывает события и вызывает соответствующие обратные вызовы (callbacks)</pre>',
    '<pre>const fs = require(\'fs\');\nconst readStream = fs.createReadStream(\'largefile.txt\');\nreadStream.on(\'data\', (chunk) => {\n\t// Обработка данных\n});</pre>',
    '<pre>// В файле package.json\n{\n\t"dependencies": {\n\t\t"express": "^4.17.1"\n\t}\n}</pre>'

]

middle_answers = [
    ['stream.Readable и stream.Writable', 'fs.readFile и fs.writeFile', 'http.get и http.post', 'buffer.from и buffer.alloc'],
    ['Символ #', 'Ключевое слово private', 'Метод _.private()', 'Символ _'],
    ['Array.map() и Promise.all()', 'Array.forEach()', 'Array.filter()', 'Array.reduce()'],
    ['Promises, async/await, callbacks', 'setTimeout и setInterval', 'EventEmitter', 'try/catch'],
    ['Промисы и async/await', 'EventEmitter', 'Callback функции', 'Process.on(\'uncaughtException\')'],
    ['Event Loop', 'Callback Queue', 'Thread Pool', 'Child Process'],
    ['Stream API', 'Buffer', 'EventEmitter', 'Global Objects'],
    ['npm и yarn', 'Webpack и Babel', 'Express и Koa', 'HTTP и HTTPS модули']
]


senior_questions = [
    'Как управлять состоянием в Node.js при использовании <u>асинхронных вызовов</u>?',
    'Как реализовать <u>микросервисную архитектуру</u> в Node.js?',
    'Как использовать Event Emitter в Node.js для управления событиями?',
    'Как <u>оптимизировать производительность</u> Node.js приложения?'
]

senior_explanations = [
    'Для управления состоянием в асинхронных вызовах Node.js используются Promises и async/await, позволяя писать асинхронный код в синхронном стиле.',
    'Микросервисная архитектура в Node.js может быть реализована с использованием фреймворков, таких как Express или Koa, в сочетании с Docker и Kubernetes для оркестрации контейнеров.',
    'Event Emitter в Node.js позволяет создавать объекты, которые могут генерировать события и вызывать зарегистрированные функции-слушатели.',
    'Оптимизация производительности Node.js включает в себя профилирование приложения, оптимизацию асинхронных операций и использование кэширования.'
]

senior_explanation_code = [
    '<pre>async function asyncOperation() {\n\tconst result = await someAsyncFunction();\n\t// Обработка результата\n}</pre>',
    '<pre>// Реализация микросервиса в Node.js\nconst express = require(\'express\');\nconst app = express();\n// Определение маршрутов\napp.listen(3000);</pre>',
    '<pre>const EventEmitter = require(\'events\');\nclass MyEmitter extends EventEmitter {}\nconst myEmitter = new MyEmitter();\nmyEmitter.on(\'event\', () => console.log(\'Event fired!\'));\nmyEmitter.emit(\'event\');</pre>',
    '<pre>// Использование кэширования\nconst cache = {};\nfunction getData(key) {\n\tif (!cache[key]) {\n\t\tcache[key] = expensiveOperation();\n\t}\n\treturn cache[key];\n}</pre>'
]

senior_answers = [
    ['Promises и async/await', 'EventEmitter', 'Callback Hell', 'Global Variables'],
    ['Express/Koa, Docker, Kubernetes', 'HTTP/HTTPS модули, Socket.io', 'Stream API, Buffer', 'Event Loop, Child Processes'],
    ['EventEmitter, on/emit', 'Callback Functions', 'Async/Await', 'Streams'],
    ['Профилирование, Асинхронные операции, Кэширование', 'Увеличение числа потоков', 'Минификация и бандлинг файлов', 'Использование PM2 или Nodemon']
]
