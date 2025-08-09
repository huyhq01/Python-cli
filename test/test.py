import sqlite3

# Khởi tạo kết nối và con trỏ
conn = sqlite3.connect(":memory:") # Dùng bộ nhớ để tiện test
cursor = conn.cursor()

print(f"'__enter__' in dir(cursor): { '__enter__' in dir(cursor) }") # Output: False
print(f"'__exit__' in dir(cursor): { '__exit__' in dir(cursor) }")   # Output: False

print("\n--- Thử dùng cursor với 'with' ---")
try:
    with cursor as c: # Sử dụng cursor với with statement
        c.execute("SELECT 1")
        print("Đã vào và thực thi trong khối 'with cursor'.")
    print("Đã thoát khỏi khối 'with cursor' thành công.")
except TypeError as e:
    print(f"Lỗi: Đối tượng cursor không hỗ trợ context manager protocol: {e}")
except sqlite3.Error as e:
    print(f"Lỗi SQLite: {e}")

print("\n--- Thử dùng connection với 'with' ---")
try:
    with conn as c: # Sử dụng connection với with statement
        c.execute("SELECT 2")
        print("Đã vào và thực thi trong khối 'with connection'.")
    print("Đã thoát khỏi khối 'with connection' thành công.")
except TypeError as e:
    print(f"Lỗi: Đối tượng connection không hỗ trợ context manager protocol: {e}")
except sqlite3.Error as e:
    print(f"Lỗi SQLite: {e}")

# Đảm bảo đóng kết nối cuối cùng nếu không được đóng bởi with
conn.close()