import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import scrolledtext
import datetime

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry("800x600")
        
        # 连接数据库
        self.conn = sqlite3.connect("library.db")
        self.create_tables()
        
        # 登录界面
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=100)
        
        tk.Label(self.login_frame, text="用户名:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        self.username_entry.insert(0, "admin")
        
        tk.Label(self.login_frame, text="密码:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry.insert(0, "admin")
        
        tk.Button(self.login_frame, text="登录", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        
        # 主界面（初始隐藏）
        self.main_frame = tk.Frame(self.root)
        
        # 菜单栏
        menubar = tk.Menu(self.root)
        book_menu = tk.Menu(menubar, tearoff=0)
        book_menu.add_command(label="添加图书", command=self.show_add_book)
        book_menu.add_command(label="查询图书", command=self.show_search_book)
        book_menu.add_command(label="图书列表", command=self.show_book_list)
        
        borrow_menu = tk.Menu(menubar, tearoff=0)
        borrow_menu.add_command(label="借阅图书", command=self.show_borrow_book)
        borrow_menu.add_command(label="归还图书", command=self.show_return_book)
        
        menubar.add_cascade(label="图书管理", menu=book_menu)
        menubar.add_cascade(label="借阅管理", menu=borrow_menu)
        menubar.add_command(label="退出登录", command=self.logout)
        self.root.config(menu=menubar)
        
        # 标签页
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 添加图书页面
        self.add_book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_book_frame, text="添加图书")
        
        tk.Label(self.add_book_frame, text="图书ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.book_id_entry = tk.Entry(self.add_book_frame, width=20)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.add_book_frame, text="书名:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.book_name_entry = tk.Entry(self.add_book_frame, width=20)
        self.book_name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.add_book_frame, text="作者:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.author_entry = tk.Entry(self.add_book_frame, width=20)
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(self.add_book_frame, text="出版社:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.publisher_entry = tk.Entry(self.add_book_frame, width=20)
        self.publisher_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(self.add_book_frame, text="出版日期:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.publish_date_entry = tk.Entry(self.add_book_frame, width=20)
        self.publish_date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.publish_date_entry.insert(0, "2025-01-01")
        
        tk.Label(self.add_book_frame, text="库存数量:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.stock_entry = tk.Entry(self.add_book_frame, width=20)
        self.stock_entry.grid(row=5, column=1, padx=10, pady=5)
        self.stock_entry.insert(0, "10")
        
        tk.Button(self.add_book_frame, text="添加", command=self.add_book).grid(row=6, column=0, columnspan=2, pady=10)
        
        # 查询图书页面
        self.search_book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_book_frame, text="查询图书")
        
        tk.Label(self.search_book_frame, text="查询方式:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.search_var = tk.StringVar()
        self.search_var.set("书名")
        tk.OptionMenu(self.search_book_frame, self.search_var, "书名", "作者", "出版社").grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.search_book_frame, text="关键词:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.keyword_entry = tk.Entry(self.search_book_frame, width=20)
        self.keyword_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Button(self.search_book_frame, text="查询", command=self.search_book).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.search_result_text = scrolledtext.ScrolledText(self.search_book_frame, width=60, height=20)
        self.search_result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        # 图书列表页面
        self.book_list_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.book_list_frame, text="图书列表")
        
        columns = ("图书ID", "书名", "作者", "出版社", "出版日期", "库存数量")
        self.book_tree = ttk.Treeview(self.book_list_frame, columns=columns, show="headings")
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=100)
        self.book_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Button(self.book_list_frame, text="刷新列表", command=self.load_book_list).grid(row=1, column=0, pady=10)
        
        # 借阅图书页面
        self.borrow_book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.borrow_book_frame, text="借阅图书")
        
        tk.Label(self.borrow_book_frame, text="读者ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.reader_id_entry = tk.Entry(self.borrow_book_frame, width=20)
        self.reader_id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.reader_id_entry.insert(0, "R001")
        
        tk.Label(self.borrow_book_frame, text="图书ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.borrow_book_id_entry = tk.Entry(self.borrow_book_frame, width=20)
        self.borrow_book_id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Button(self.borrow_book_frame, text="借阅", command=self.borrow_book).grid(row=2, column=0, columnspan=2, pady=10)
        
        # 归还图书页面
        self.return_book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.return_book_frame, text="归还图书")
        
        tk.Label(self.return_book_frame, text="借阅ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.borrow_record_id_entry = tk.Entry(self.return_book_frame, width=20)
        self.borrow_record_id_entry.grid(row=0, column=1, p
