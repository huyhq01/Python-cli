from task import Task
import data_manager as TaskServices
import sys
from datetime import datetime, date
from tabulate import tabulate

def main():
    """
    Functions Menu to run the todo list app.
    """
    TaskServices.create_table()  # đảm bảo database tạo nếu chưa có
    TaskServices.update_list_task()

    while True:
        print("Chon chuc nang:")
        print("1. Xem danh sach todo")
        print("2. Them")
        print("3. Cap nhat")
        print("4. Xoa")
        print("5. Quay lai menu chinh")
        print("6. Thoat")

        match (input("Nhap lua chon cua ban: ")):
            case '1':
                view_task()
            case '2':
                add_task()
            case '3':
                update_task()
            case '4':
                delete_task()
            case '5':
                print("Quay lai menu chinh...")
                return
            case '6':
                print("Thoat chuong trinh...")
                sys.exit()
            case _:
                print("Lua chon khong hop le.")
        print('-' * 30)


def view_task():
    """
    View the todo list.
    """
    response = TaskServices.get_all_tasks()
    if not response:
        print("Khong co gi o day.")
        if(input("Thêm task mới không? 'y' để có hoặc phím bất kì để quay lại: ").lower().strip() == 'y'):
            add_task()
        else: return
    else:
        table_data = [[
            i, 
            task.content, 
            task.deadline or 'Không có', 
            "Đã xong" if task.status else "Chưa xong"]
            for i,task in enumerate(response, start=1)
        ]
        headers = ["STT", "Nội dung", "Hạn chót", "Tiến độ"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

def add_task():
    """
    Add a new todo item.
    """
    content = get_content()
    deadline = get_valid_date()
    print('Nội dung là: ', content, ' -- Thời gian là ', deadline or 'Null = Vô thời hạn')

    # Thêm task mới vào cơ sở dữ liệu
    TaskServices.add_task(content, deadline)
    TaskServices.update_list_task()
    
def update_task():
    """
    Update an existing todo item.
    """
    # Update thông tin của todo item
    list_ids = TaskServices.get_list_task_ids()
    stt_input = input('Số thứ tự Task bạn muốn sửa: ')

    if not (stt_input.isdigit() and 1 <= (i:=int(stt_input)) <= len(list_ids)): # nếu số thứ tự task tồn tại
        print('Số thứ tự không tồn tại. Quay lại menu nhá!')
        return
    
    # *Sửa -> cập nhật db
    # cập nhật nội dung
    content_update = input("Cập nhật nội dung: ")
    if not (content_update.strip()): # nếu chuỗi rỗng
        print('Nội dung giữ nguyên')
        content_update = None
    
    # cập nhật deadline
    deadline_update = get_valid_date(True) 
    
    # cập nhật tiến độ hoàn thành bool
    while True:
        complete = input("Hoàn thành chưa? y/n: ").strip().lower()
        if complete in ('y','n'):
            break
        print("Nhập 'y' hoặc 'n' thôi")
            
    
    TaskServices.update_task(list_ids[i], content_update, deadline_update, complete == 'y')
    # Cập nhật db
    TaskServices.update_list_task() 
    
def delete_task():
    """
    Delete a todo item.
    """
    # Xóa todo item khỏi danh sách

def get_content():
    while True:
        content = input("Nội dung cần hoàn thành: \n")
        if not content.strip():
            print("Ờ ờ để trống thì ăn vòng lặp nhá.")
        else:
            return content.strip()  # Trả về nội dung đã loại bỏ khoảng trắng đầu cuối

def get_valid_date(is_update=False):
    """
    Get a valid date input from the user.
    """
    while True:
        match (input(f"Có {'đổi' if is_update else ''} hạn chót không fen? (y/n)").lower().strip()):
            case 'n':
                return None
            case 'y':
                while True:
                    date_str = input(f"Hạn chót {'' if is_update else 'nếu có'} (DD-MM-YYYY): ")
                    if not date_str:
                            print(f"Để trống xem như không {"đổi"if is_update else "có"} nhá.")
                            return None
                    try:
                        return datetime.strptime(date_str, "%d-%m-%Y").date()
                    except ValueError:
                        print("Không được.Nhập đúng ngày DD-MM-YYYY và ngày có tồn tại.")
            case _:
                print("Đừng có nghịch. Vui lòng nhập 'y' (yes) hoặc 'n' (no).")

if __name__ == '__main__':
    main()