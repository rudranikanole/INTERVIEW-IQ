import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

# Create the Candidates Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_key TEXT UNIQUE,
        name VARCHAR(100),  -- Now defines a size of 100 characters for the candidate name
        resume TEXT,
        strengths TEXT,  -- Now stores multiple strengths as a comma-separated string
        proficiency_levels TEXT  -- Now stores multiple proficiency levels as a comma-separated string
    )
''')

# Create the Normal Questions Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS normal_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        strength TEXT CHECK(strength IN ('SQL', 'Python', 'JavaScript')),
        difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'advanced')),
        question_type TEXT
    )
''')

# Create the MCQ Questions Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mcq_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mcq_question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        correct_option TEXT,
        strength TEXT CHECK(strength IN ('SQL', 'Python', 'Javascript')),
        difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'advanced')),
        question_type TEXT
    )
''')

# Create the Code Questions Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code_question TEXT,
        code_placeholder TEXT,
        strength TEXT CHECK(strength IN ('SQL', 'Python', 'Javascript')),
        difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'advanced')),
        question_type TEXT
    )
''')

# Create the Response Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS  correct_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_key TEXT,
        answers TEXT,
        accuracy REAL,
        FOREIGN KEY (candidate_key) REFERENCES candidates(candidate_key)
    )
''')


# Candidate data
candidates = [
    ('key001', 'Alice Smith', 'Alice\'s resume details here', 'SQL,Python', '8/10,7/10'),
    ('key002', 'Bob Johnson', 'Bob\'s resume details here', 'JavaScript,SQL,Python', '6/10,4/10,9/10'),
    ('key003', 'Charlie Brown', 'Charlie\'s resume details here', 'Python', '7/10'),
    ('key004', 'Diana Prince', 'Diana\'s resume details here', 'SQL,JavaScript', '5/10,6/10'),
    ('key005', 'Eve Adams', 'Eve\'s resume details here', 'JavaScript,Python', '4/10,8/10'),
    ('key006', 'Frank Miller', 'Frank\'s resume details here', 'Python', '9/10'),
    ('key007', 'Grace Lee', 'Grace\'s resume details here', 'SQL,Python', '8/10,5/10'),
    ('key008', 'Hank Green', 'Hank\'s resume details here', 'JavaScript', '7/10'),
    ('key009', 'Ivy Hall', 'Ivy\'s resume details here', 'Python', '6/10'),
    ('key010', 'Jack White', 'Jack\'s resume details here', 'SQL,Python', '7/10,8/10')
]

# Insert candidate data into the database
cursor.executemany('''
    INSERT INTO candidates (candidate_key, name, resume, strengths, proficiency_levels)
    VALUES (?, ?, ?, ?, ?)
''', candidates)

# Commit the changes
conn.commit()

    # Add data for questions
normal_questions_data = [
        # SQL - EASY
        ('What is a primary key in SQL, and why is it important?', 'A primary key is a unique identifier for each record in a table. It ensures that no two rows have the same value in the primary key column(s).', 'easy', 'SQL', 'normal'),
        ('How do you retrieve unique values from a column in SQL?', 'SELECT DISTINCT column_name FROM table_name;', 'easy', 'SQL', 'normal'),
        ('What does the WHERE clause do in an SQL query?', 'The WHERE clause filters the rows returned by the query based on specified conditions.', 'easy', 'SQL', 'normal'),
        ('How do you combine the results of two SELECT statements into a single result set?', 'Use the UNION operator.', 'easy', 'SQL', 'normal'),
        ('What is the difference between the CHAR and VARCHAR data types in SQL?', 'CHAR is a fixed-length string, while VARCHAR is a variable-length string.', 'easy', 'SQL', 'normal'),
        # SQL - MEDIUM
        ('What are the set operators in SQL?', 'Set operators combine the results of two or more queries. Common set operators include UNION (combines results and removes duplicates), UNION ALL (combines results without removing duplicates), INTERSECT (returns common rows), and EXCEPT (returns rows from the first query not in the second).', 'medium', 'SQL', 'normal'),
        ('What is a cross join in SQL?', 'A cross join returns the Cartesian product of two tables, meaning it combines each row from the first table with every row from the second table.', 'medium', 'SQL', 'normal'),
        ('How to fetch alternate records from the table?', 'Use a row number function with a filtering condition. Example with SQL Server:\n\nSELECT *\nFROM (\n    SELECT *, ROW_NUMBER() OVER (ORDER BY column_name) AS rn\n    FROM table_name\n) AS sub\nWHERE rn % 2 = 1;', 'medium', 'SQL', 'normal'),
        ('What is the difference between the RANK() and DENSE_RANK() functions in SQL?', 'RANK() assigns the same rank to identical values but leaves gaps in the ranking sequence. DENSE_RANK() also assigns the same rank to identical values but does not leave gaps.', 'medium', 'SQL', 'normal'),
        ('What are stored procedures? Why do we need them?', 'Stored procedures are precompiled SQL statements stored in the database. They encapsulate complex logic, improve performance, and enhance security by controlling access to data.', 'medium', 'SQL', 'normal'),
        # SQL - ADVANCED
        ('How would you optimize a slow-running SQL query?', 'Query performance tuning, indexing strategies, analyzing execution plans.', 'advanced', 'SQL', 'normal'),
        ('Explain the difference between LEFT JOIN and LEFT OUTER JOIN, and how do they behave with NULL values?', 'Join types, NULL handling, and result set differences.', 'advanced', 'SQL', 'normal'),
        ('What are window functions in SQL, and provide an example use case?', 'Window functions perform calculations across a set of table rows related to the current row. Example: ROW_NUMBER() to assign a unique sequential integer to rows within a partition.', 'advanced', 'SQL', 'normal'),
        ('How do you handle transactions in SQL, and what are the key properties of transactions?', 'Transactions ensure data integrity. Key properties: Atomicity, Consistency, Isolation, Durability (ACID).', 'advanced', 'SQL', 'normal'),
        ('What is a CTE (Common Table Expression) and how does it differ from a derived table?', 'CTE is a temporary result set defined within the execution scope of a single `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. It improves query readability and can be self-referencing.', 'advanced', 'SQL', 'normal'),
        # Python - EASY
        ('What is the purpose of the `self` keyword in Python classes?', 'The `self` keyword represents the instance of the class and allows access to the attributes and methods of the class.', 'easy', 'Python', 'normal'),
        ('How do you handle exceptions in Python?', 'Use `try`, `except`, `finally`, and `else` blocks to handle and manage exceptions.', 'easy', 'Python', 'normal'),
        ('What does the `len()` function do in Python?', 'The `len()` function returns the number of items in an object such as a list, tuple, or string.', 'easy', 'Python', 'normal'),
        ('How do you create a list in Python?', 'Lists are created using square brackets. Example: `my_list = [1, 2, 3]`.', 'easy', 'Python', 'normal'),
        ('What is the difference between `append()` and `extend()` methods for lists in Python?', '`append()` adds a single element to the end of a list, while `extend()` adds all elements from an iterable to the end of a list.', 'easy', 'Python', 'normal'),
        # Python - MEDIUM
        ('Explain how decorators work in Python.', 'Decorators are functions that modify the behavior of other functions or methods. They are used to add functionality to functions or methods without modifying their structure.', 'medium', 'Python', 'normal'),
        ('What are lambda functions in Python?', 'Lambda functions are anonymous, one-line functions created with the `lambda` keyword. They can have any number of arguments but only one expression.', 'medium', 'Python', 'normal'),
        ('What is the difference between `deepcopy` and `shallow copy` in Python?', 'Shallow copy creates a new object but inserts references into it to the objects found in the original. Deep copy creates a new object and recursively copies all objects found in the original.', 'medium', 'Python', 'normal'),
        ('How does Python’s garbage collection work?', 'Python uses reference counting and a cyclic garbage collector to clean up unused objects and free memory.', 'medium', 'Python', 'normal'),
        ('What are Python generators, and how do they differ from regular functions?', 'Generators are functions that use `yield` instead of `return` to produce a sequence of values. They are more memory-efficient than regular functions because they generate values on the fly.', 'medium', 'Python', 'normal'),
        # Python - ADVANCED
        ('What is the Global Interpreter Lock (GIL) in Python, and how does it affect multithreading?', 'The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes simultaneously. It can limit the effectiveness of multithreading for CPU-bound tasks.', 'advanced', 'Python', 'normal'),
        ('How do you implement metaclasses in Python?', 'Metaclasses are classes of classes that define how classes are created. They are implemented by defining a class that inherits from `type` and overriding its methods.', 'advanced', 'Python', 'normal'),
        ('What are Python’s built-in functions for concurrency and parallelism?', 'Python provides `concurrent.futures`, `threading`, and `multiprocessing` modules for concurrency and parallelism.', 'advanced', 'Python', 'normal'),
        ('Explain how the `yield` keyword works in Python and its use cases.', 'The `yield` keyword is used to create generators. It allows a function to return an iterator that produces values one at a time, which can be used to manage large datasets efficiently.', 'advanced', 'Python', 'normal'),
        ('What is the purpose of `__new__` and `__init__` methods in Python classes?', ' `__new__` is responsible for creating a new instance of a class, while `__init__` initializes the created instance.', 'advanced', 'Python', 'normal'),
        # JavaScript - EASY
        ('What is a closure in JavaScript?', 'A closure is a function that retains access to its lexical scope, even after the function has finished executing.', 'easy', 'JavaScript', 'normal'),
        ('How do you declare a variable in JavaScript?', 'Variables are declared using `var`, `let`, or `const` keywords. Example: `let x = 10;`', 'easy', 'JavaScript', 'normal'),
        ('What is the difference between `==` and `===` in JavaScript?', '`==` is the equality operator that performs type coercion, while `===` is the strict equality operator that checks both value and type without coercion.', 'easy', 'JavaScript', 'normal'),
        ('How do you create an object in JavaScript?', 'Objects are created using curly braces or the `new Object()` syntax. Example: `let obj = { key: value };`', 'easy', 'JavaScript', 'normal'),
        ('What is the purpose of the `this` keyword in JavaScript?', 'The `this` keyword refers to the context in which the function is called, allowing access to the object that invoked the function.', 'easy', 'JavaScript', 'normal'),
        # JavaScript - MEDIUM
        ('Explain the concept of prototypal inheritance in JavaScript.', 'Prototypal inheritance allows objects to inherit properties and methods from other objects. It is based on a prototype chain where objects can access properties and methods from their prototype.', 'medium', 'JavaScript', 'normal'),
        ('How do you handle asynchronous operations in JavaScript?', 'Asynchronous operations can be handled using callbacks, promises, or async/await syntax. Promises and async/await are preferred for better readability and error handling.', 'medium', 'JavaScript', 'normal'),
        ('What is the event loop in JavaScript?', 'The event loop is a mechanism that handles asynchronous operations by continuously checking the message queue and executing tasks from it.', 'medium', 'JavaScript', 'normal'),
        ('What are JavaScript modules, and how do you use them?', 'JavaScript modules are units of code that export and import functionality. Use `export` and `import` statements to share code between modules.', 'medium', 'JavaScript', 'normal'),
        ('What is a promise in JavaScript, and how do you use it?', 'A promise is an object representing the eventual completion (or failure) of an asynchronous operation. Use `.then()` and `.catch()` methods to handle resolved and rejected promises.', 'medium', 'JavaScript', 'normal'),
        # JavaScript - ADVANCED
        ('Explain the concept of JavaScript closures and their use cases.', 'Closures are functions that have access to variables in their lexical scope even after the function has finished executing. They are useful for data encapsulation and function factories.', 'advanced', 'JavaScript', 'normal'),
        ('How do you optimize performance in JavaScript applications?', 'Optimize performance by minimizing DOM manipulations, using efficient algorithms, employing lazy loading, and leveraging browser caching.', 'advanced', 'JavaScript', 'normal'),
        ('What is the purpose of the `Symbol` type in JavaScript?', 'The `Symbol` type creates unique identifiers for object properties, ensuring that property keys are unique and do not conflict with other keys.', 'advanced', 'JavaScript', 'normal'),
        ('How does JavaScript’s prototype chain work?', 'JavaScript objects inherit properties and methods from their prototype objects. The prototype chain allows object instances to access properties and methods defined in their prototype.', 'advanced', 'JavaScript', 'normal'),
        ('What is the difference between `Object.create()` and `Object.assign()`?', '`Object.create()` creates a new object with a specified prototype, while `Object.assign()` copies properties from one or more source objects to a target object.', 'advanced', 'JavaScript', 'normal'),
    ]

cursor.executemany('''
    INSERT INTO normal_questions (question, answer, difficulty, strength, question_type)
    VALUES (?, ?, ?, ?, ?)
''', normal_questions_data)
conn.commit()

    # List of questions to insert
mcq_questions_data = [
    # MCQ Questions 
    # (SQL - easy)
    ('Which SQL command is used to extract data from a database?', 'mcq', 'INSERT', 'UPDATE', 'SELECT', 'DELETE', 'SELECT','easy','SQL'),
    ('What does the "WHERE" clause do in SQL?', 'mcq', 'Filters rows based on a condition', 'Specifies the columns to select', 'Orders the results', 'Joins two tables', 'Filters rows based on a condition','easy','SQL'),
    ('Which keyword is used to sort the result set in SQL?', 'mcq', 'SORT', 'ORDER BY', 'GROUP BY', 'FILTER', 'ORDER BY','easy','SQL'),
    ('Which SQL function is used to count the number of rows in a table?', 'mcq', 'COUNT()', 'SUM()', 'AVG()', 'MAX()', 'COUNT()','easy','SQL'),
    ('What does the "GROUP BY" clause do in SQL?', 'mcq', 'Groups rows that have the same values into summary rows', 'Filters rows based on a condition', 'Sorts the result set', 'Combines two tables', 'Groups rows that have the same values into summary rows','easy','SQL'),
    # (SQL - medium)
    ('What does the "JOIN" clause do in SQL?', 'mcq', 'Combines columns from two tables', 'Combines rows from two tables', 'Deletes rows from two tables', 'None of the above', 'Combines rows from two tables','medium','SQL'),
    ('Which SQL function is used to find the maximum value in a column?', 'mcq', 'MAX()', 'MIN()', 'SUM()', 'COUNT()', 'MAX()','medium','SQL'),
    ('How do you filter records between two values?', 'mcq', 'WHERE column BETWEEN value1 AND value2', 'WHERE column IN (value1, value2)', 'FILTER column FROM value1 TO value2', 'SELECT column BETWEEN value1 AND value2', 'WHERE column BETWEEN value1 AND value2','medium','SQL'),
    ('Which keyword is used to remove a table in SQL?', 'mcq', 'DELETE', 'DROP', 'TRUNCATE', 'REMOVE', 'DROP','medium','SQL'),
    ('How do you get the current date in SQL?', 'mcq', 'CURRENT_DATE()', 'GETDATE()', 'NOW()', 'DATE()', 'CURRENT_DATE()','medium','SQL'),
    # (SQL - advanced)
    ('Which SQL statement is used to create a new table in a database?', 'mcq', 'CREATE TABLE', 'ADD TABLE', 'NEW TABLE', 'MAKE TABLE', 'CREATE TABLE','advanced','SQL'),
    ('What is the result of the following SQL query: SELECT ROUND(123.4567, 2);', 'mcq', '123.46', '123.45', '123.47', '124', '123.46','advanced','SQL'),
    ('How do you add a primary key constraint to an existing table?', 'mcq', 'ALTER TABLE table_name ADD PRIMARY KEY (column_name);', 'ALTER TABLE table_name ADD CONSTRAINT PRIMARY KEY (column_name);', 'ALTER TABLE table_name MODIFY COLUMN column_name PRIMARY KEY;', 'ADD PRIMARY KEY (column_name) TO table_name;', 'ALTER TABLE table_name ADD PRIMARY KEY (column_name);','advanced','SQL'),
    ('How do you perform a full outer join in SQL?', 'mcq', 'SELECT * FROM table1 FULL OUTER JOIN table2 ON table1.id = table2.id;', 'SELECT * FROM table1 LEFT JOIN table2 ON table1.id = table2.id UNION SELECT * FROM table1 RIGHT JOIN table2 ON table1.id = table2.id;', 'SELECT * FROM table1 INNER JOIN table2 ON table1.id = table2.id;', 'SELECT * FROM table1 LEFT JOIN table2 ON table1.id = table2.id;', 'SELECT * FROM table1 LEFT JOIN table2 ON table1.id = table2.id UNION SELECT * FROM table1 RIGHT JOIN table2 ON table1.id = table2.id;','advanced','SQL'),
    ('What is the purpose of the "HAVING" clause in SQL?', 'mcq', 'Filters groups based on a condition', 'Filters rows based on a condition', 'Sorts the result set', 'Groups rows based on a condition', 'Filters groups based on a condition','advanced','SQL'),
    # (Python - easy)
    ('What is the keyword used to define a function in Python?', 'mcq', 'function', 'def', 'func', 'define', 'def','easy','Python'),
    ('What is the output of print(2 + 3 * 4) in Python?', 'mcq', '20', '26', '14', '12', '14','easy','Python'),
    ('Which of the following is a valid list declaration in Python?', 'mcq', 'list = [1, 2, 3]', 'list = (1, 2, 3)', 'list = {1, 2, 3}', 'list = 1, 2, 3', 'list = [1, 2, 3]','easy','Python'),
    ('How do you add a new item to a list in Python?', 'mcq', 'list.add(item)', 'list.append(item)', 'list.insert(item)', 'list.extend(item)', 'list.append(item)','easy','Python'),
    ('What is the result of len("Python")?', 'mcq', '6', '5', '7', '8', '6','easy','Python'),
    # (Python - medium)
     ('What is the purpose of the __init__ method in Python classes?', 'mcq', 'To initialize the class', 'To initialize the object', 'To destroy the object', 'To define the class', 'To initialize the object','medium','Python'),
     ('How do you create a dictionary in Python?', 'mcq', 'dict = {}', 'dict = []', 'dict = ()', 'dict = set()', 'dict = {}','medium','Python'),
     ('How do you handle exceptions in Python?', 'mcq', 'try/except', 'catch/throw', 'if/else', 'handle/catch', 'try/except','medium','Python'),
     ('What is the output of the following code: print(3**2**2)?', 'mcq', '81', '9', '729', '27', '729','medium','Python'),
     ('Which method is used to remove the last item from a list in Python?', 'mcq', 'pop()', 'remove()', 'delete()', 'discard()', 'pop()','medium','Python'),
    # (Python - advanced)
    ('What is the difference between deep copy and shallow copy in Python?', 'mcq', 'Shallow copy duplicates the references, deep copy duplicates the objects.', 'Deep copy duplicates the references, shallow copy duplicates the objects.', 'Both are the same.', 'Shallow copy and deep copy are not valid in Python.', 'Shallow copy duplicates the references, deep copy duplicates the objects.','advanced','Python'),
    ('How do you define a generator function in Python?', 'mcq', 'Using the yield keyword', 'Using the return keyword', 'Using the def keyword', 'Using the lambda keyword', 'Using the yield keyword','advanced','Python'),
    ('What is the output of the following code snippet: print([1,2,3] + [4,5,6])?', 'mcq', '[1, 2, 3, 4, 5, 6]', '[5, 7, 9]', '[1, 2, 3, [4, 5, 6]]', 'Error', '[1, 2, 3, 4, 5, 6]','advanced','Python'),
    ('What is the purpose of the "self" keyword in Python classes?', 'mcq', 'To refer to the instance of the class', 'To refer to the class itself', 'To refer to a method', 'To refer to a variable', 'To refer to the instance of the class','advanced','Python'),
     ('What is the output of the following code: print(2 * 3 ** 2)?', 'mcq', '18', '12', '36', '27', '18','advanced','Python'),
    # (JavaScript - easy)
    ('Which of the following is the correct syntax to declare a variable in JavaScript?', 'mcq', 'var name;', 'variable name;', 'let name;', 'name = var;', 'var name;','easy','Javascript'),
    ('What is the output of console.log(5 + "5") in JavaScript?', 'mcq', '55', '10', 'Error', '5', '55','easy','Javascript'),
    ('How do you create a function in JavaScript?', 'mcq', 'function name() {}', 'function = name() {}', 'create function name() {}', 'def name() {}', 'function name() {}','easy','Javascript'),
    ('Which operator is used to compare two values in JavaScript?', 'mcq', '==', '=', '===', '!=', '==','easy','Javascript'),
    ('Which of the following methods is used to remove the last element from an array in JavaScript?', 'mcq', 'pop()', 'shift()', 'slice()', 'splice()', 'pop()','easy','Javascript'),
    # (JavaScript - medium)
    ('How do you define an arrow function in JavaScript?', 'mcq', '() => {}', 'function() {}', '=> function() {}', 'function: {}', '() => {}','medium','Javascript'),
    ('Which keyword is used to declare a constant in JavaScript?', 'mcq', 'let', 'const', 'var', 'static', 'const','medium','Javascript'),
    ('How do you create an object in JavaScript?', 'mcq', 'let obj = {};', 'let obj = [];', 'let obj = ();', 'let obj = new Object();', 'let obj = {};','medium','Javascript'),
    ('What is the purpose of the "this" keyword in JavaScript?', 'mcq', 'Refers to the global object', 'Refers to the function that is executing', 'Refers to the current object', 'Refers to the previous object', 'Refers to the current object','medium','Javascript'),
    ('How can you check if an element is in an array in JavaScript?', 'mcq', 'array.contains(element)', 'array.has(element)', 'array.includes(element)', 'array.indexOf(element) != -1', 'array.includes(element)','medium','Javascript'),
    # (JavaScript - advanced)
    ('What is the purpose of closures in JavaScript?', 'mcq', 'To access variables from an outer function scope', 'To create global variables', 'To execute asynchronous code', 'To bind functions', 'To access variables from an outer function scope','advanced','Javascript'),
    ('How do you implement a promise in JavaScript?', 'mcq', 'new Promise((resolve, reject) => {})', 'Promise.create()', 'Promise.new()', 'new AsyncPromise()', 'new Promise((resolve, reject) => {})','advanced','Javascript'),
    ('How do you create a class in JavaScript?', 'mcq', 'class MyClass {}', 'create class MyClass {}', 'function MyClass() {}', 'MyClass = class {}', 'class MyClass {}','advanced','Javascript'),
    ('What is the output of the following code: console.log(!!"false")?', 'mcq', 'false', 'true', 'null', 'undefined', 'true','advanced','Javascript'),
    ('What will be the output of console.log([] == ![])?', 'mcq', 'true', 'false', 'undefined', 'Error', 'true','advanced','Javascript'),
]


# Insert MCQ questions into the database
cursor.executemany('''
    INSERT INTO mcq_questions (mcq_question, question_type, option1, option2, option3, option4, correct_option, difficulty, strength)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', mcq_questions_data)
conn.commit()

# List of questions to insert
code_questions_data = [ 
    # Type-in Code Questions 
    # (SQL - easy)
     ('Write a SQL query to retrieve all columns from a table named "employees".', 'code', 'SELECT * FROM employees;','easy','SQL'),
     ('Write a SQL query to get all distinct values from a column named "department" in the "employees" table.', 'code', 'SELECT DISTINCT department FROM employees;','easy','SQL'),
     ('Write a SQL query to find employees with salary greater than 50000.', 'code', 'SELECT * FROM employees WHERE salary > 50000;','easy','SQL'),
    # (SQL - medium)
    ('Write a SQL query to find the average salary from a table named "salaries".', 'code', 'SELECT AVG(salary) FROM salaries;','medium','SQL'),
    ('Write a SQL query to retrieve the top 3 highest salaries from a table named "employees".', 'code', 'SELECT salary FROM employees ORDER BY salary DESC LIMIT 3;','medium','SQL'),
    ('Write a SQL query to update the salary of an employee with ID 10 to 60000.', 'code', 'UPDATE employees SET salary = 60000 WHERE id = 10;','medium','SQL'),
    # (SQL - Advanced)
    ('Write a SQL query to find employees who earn more than the average salary in their department.', 'code', 'SELECT * FROM employees e1 WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e1.department = e2.department);', 'advanced', 'SQL'),
    ('Write a SQL query to perform a self-join on the "employees" table to find pairs of employees who work in the same department.', 'code', 'SELECT e1.name AS Employee1, e2.name AS Employee2 FROM employees e1 JOIN employees e2 ON e1.department = e2.department AND e1.id <> e2.id;', 'advanced', 'SQL'),
    ('Write a SQL query to create a view that shows the average salary by department.', 'code', 'CREATE VIEW avg_salary_by_department AS SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department;', 'advanced', 'SQL'),
    # (Python - easy)
    ('Write a Python function to return the sum of two numbers.', 'code', 'def sum_two_numbers(a, b):\n    return a + b','easy','Python'),
    ('Write a Python function to find the maximum of three numbers.', 'code', 'def max_of_three(a, b, c):\n    return max(a, b, c)','easy','Python'),
    ('Write a Python function to check if a number is even or odd.', 'code', 'def is_even_or_odd(n):\n    return "Even" if n % 2 == 0 else "Odd"','easy','Python'),
    # (Python - medium)
    ('Write a Python function to reverse a string.', 'code', 'def reverse_string(s):\n    return s[::-1]','medium','Python'),
    ('Write a Python function to check if a string is a palindrome.', 'code', 'def is_palindrome(s):\n    return s == s[::-1]','medium','Python'),
    ('Write a Python function to find the factorial of a number using recursion.', 'code', 'def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)','medium','Python'),
    # (Python - advanced)
    ('Write a Python function to generate a Fibonacci sequence up to n terms using memoization.', 'code', 'def fibonacci(n, memo={0: 0, 1: 1}):\n    if n not in memo:\n        memo[n] = fibonacci(n-1) + fibonacci(n-2)\n    return memo[n]','advanced','Python'),
    ('Write a Python code snippet to create a generator that yields the Fibonacci sequence.', 'code', 'def fibonacci_generator():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b','advanced','Python'),
    ('Write a Python function to perform a binary search on a sorted list.', 'code', 'def binary_search(lst, target):\n    left, right = 0, len(lst) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if lst[mid] == target:\n            return mid\n        elif lst[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1','advanced','Python'),
    # (JavaScript - easy)
    ('Write a JavaScript function to check if a number is even.', 'code', 'function isEven(num) {\n    return num % 2 === 0;\n}','easy','Javascript'),
    ('Write a JavaScript function to return the factorial of a number.', 'code', 'function factorial(n) {\n    if (n === 0) return 1;\n    return n * factorial(n - 1);\n}','easy','Javascript'),
    ('Write a JavaScript code snippet to concatenate two strings.', 'code', 'const concatenate = (str1, str2) => str1 + str2;','easy','Javascript'),
    # (JavaScript - medium)
    ('Write a JavaScript function to filter out odd numbers from an array.', 'code', 'function filterOdds(arr) {\n    return arr.filter(num => num % 2 === 0);\n}','medium','Javascript'),
    ('Write a JavaScript function to flatten a nested array.', 'code', 'function flattenArray(arr) {\n    return arr.flat();\n}','medium','Javascript'),
    ('Write a JavaScript code snippet to remove duplicate values from an array.', 'code', 'const removeDuplicates = (arr) => [...new Set(arr)];','medium','Javascript'),
    # (JavaScript - Advanced)
    ('Write a JavaScript function to debounce a given function.', 'code', 'function debounce(func, delay) {\n    let timeout;\n    return function(...args) {\n        clearTimeout(timeout);\n        timeout = setTimeout(() => func.apply(this, args), delay);\n    };\n}','advanced','Javascript'),
    ('Write a JavaScript function to implement a deep clone of an object.', 'code', 'function deepClone(obj) {\n    return JSON.parse(JSON.stringify(obj));\n}','advanced','Javascript'),
    ('Write a JavaScript function to implement a basic event emitter.', 'code', 'class EventEmitter {\n    constructor() {\n        this.events = {};\n    }\n    on(event, listener) {\n        if (!this.events[event]) {\n            this.events[event] = [];\n        }\n        this.events[event].push(listener);\n    }\n    emit(event, ...args) {\n        if (this.events[event]) {\n            this.events[event].forEach(listener => listener(...args));\n        }\n    }\n}','advanced','Javascript'),
]


# Insert code questions into the database
cursor.executemany('''
    INSERT INTO code_questions (code_question,question_type, code_placeholder, difficulty, strength)
    VALUES (?, ?, ?, ?, ?)
''', code_questions_data)
conn.commit()

# Commit the changes and close the connection
conn.commit()
conn.close()