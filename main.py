import programs.todo_list_app.app as todo_app
import sys

def main():
    while True:
        print('Chon chương trinh demo:')
        print("1. Quan li todo list")
        print("2. Thoat")
        print("\n")

        match(input("Nhap lua chon cua ban: ")):
            case '1':
                insert_line()
                print("Chuong trinh quan li todo list")
                todo_app.main()
            case '2':
                print("Thoat chuong trinh...")
                insert_line()
                return
            case _:
                print("Lua chon khong hop le.")
                insert_line()
                main()
                
def insert_line():
    print('-' * 30)

if __name__ == "__main__":
    # sys.path.append("Python/programs")
    # sys.path.append("Python/programs/todo_list_app")
    print(sys.path)
    main()