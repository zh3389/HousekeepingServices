import sqlite3

class User:
    """用户类"""
    def __init__(self, username, password, email=None):
        """初始化用户对象"""
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        """将用户信息保存到数据库"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 将用户信息插入到 users 表中
        cursor.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (self.username, self.password, self.email)
        )

        # 提交事务并关闭数据库连接
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_username(username):
        """根据用户名查找用户"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 从 users 表中查找用户名为 username 的用户
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        result = cursor.fetchone()

        # 如果查找到了用户，则创建 User 对象并返回
        if result:
            user = User(result[1], result[2], result[3])
            user.id = result[0]
            user.trial_end_date = result[4]
            user.trial_max_count = result[5]
            user.trial_max_chars = result[6]
            user.avatar_path = result[7]
            return user

        # 如果没有查找到用户，则返回 None
        return None

    def update_trial(self, trial_end_date, trial_max_count=None, trial_max_chars=None):
        """更新用户的试用信息"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 更新 users 表中用户的试用信息
        cursor.execute(
            'UPDATE users SET trial_end_date=?, trial_max_count=?, trial_max_chars=? WHERE id=?',
            (trial_end_date, trial_max_count, trial_max_chars, self.id)
        )

        # 提交事务并关闭数据库连接
        conn.commit()
        conn.close()

    def update_avatar(self, avatar_path):
        """更新用户的头像"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 更新 users 表中用户的头像文件路径
        cursor.execute('UPDATE users SET avatar_path=? WHERE id=?', (avatar_path, self.id))

        # 提交事务并关闭数据库连接
        conn.commit()
        conn.close()

class Payment:
    """支付类"""

    def __init__(self, user_id, amount):
        """初始化支付对象"""
        self.user_id = user_id
        self.amount = amount
        self.status = 0
        self.created_at = None

    def save(self):
        """将支付信息保存到数据库"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 将支付信息插入到 payments 表中
        cursor.execute(
            'INSERT INTO payments (user_id, amount, status, created_at) VALUES (?, ?, ?, ?)',
            (self.user_id, self.amount, self.status, self.created_at)
        )

        # 提交事务并关闭数据库连接
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_user_id(user_id):
        """根据用户 ID 查找支付信息"""
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
            # 从 payments 表中查找用户 ID 为 user_id 的支付信息
        cursor.execute('SELECT * FROM payments WHERE user_id=?', (user_id,))
        result = cursor.fetchone()

        # 如果查找到了支付信息，则创建 Payment 对象并返回
        if result:
            payment = Payment(result[1], result[2])
            payment.id = result[0]
            payment.status = result[3]
            payment.created_at = result[4]
            return payment

        # 如果没有查找到支付信息，则返回 None
        return None

class Database:
    """数据库类"""
    def __init__(self):
        """初始化数据库连接"""
        self.conn = sqlite3.connect('app.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        """关闭数据库连接"""
        self.conn.close()

    def execute(self, sql, params=None):
        """执行 SQL 语句"""
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)

        # 提交事务并返回影响的行数
        self.conn.commit()
        return self.cursor.rowcount

    def query_one(self, sql, params=None):
        """查询单条记录"""
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)

        result = self.cursor.fetchone()
        return result

    def query_all(self, sql, params=None):
        """查询多条记录"""
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)

        result = self.cursor.fetchall()
        return result

if __name__ == 'main':
    """
    该代码中定义了三个类：`User`、`Payment` 和 `Database`。
    `User` 类封装了用户相关的操作，包括保存用户信息、根据用户名 查找用户、更新用户的试用信息和头像等。
    `Payment` 类封装了支付相关的操作，包括保存支付信息、根据用户ID 查找支付信息等。
    `Database` 类封装了数据库相关的操作，包括执行 SQL 语句、查询单条记录、查询多条记录等。
    在代码的最后，使用 `if __name__ == '__main__'` 判断是否是直接运行该文件，如果是，则创建 `users` 表和 `payments` 表。同时，`Database` 类的 `__del__` 方法会在程序结束时自动关闭数据库连接。
    """
    # 创建 users 表和 payments 表
    db = Database()
    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT,
    trial_end_date TEXT,
    trial_max_count INTEGER,
    trial_max_chars INTEGER,
    avatar_path TEXT
    )
    ''')
    db.execute('''
    CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    status INTEGER NOT NULL,
    created_at TEXT NOT NULL
    )
    ''')