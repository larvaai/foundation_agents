# 01 - Một File `main.py` Trước

Giai đoạn học ban đầu chỉ viết trong một file:

```text
main.py
```

Các thư mục như `tools/`, `core/`, `agents/`, `output_gate/` chỉ được tạo ở bước tách file sau.

Luật:

- Không import module tự viết từ file khác.
- Chỉ dùng Python standard library nếu có thể.
- Mỗi hàm trong `main.py` phải có trách nhiệm nhỏ và tên rõ nghĩa.
- Khi code bắt đầu dài hoặc chức năng đã ổn định, mới tạo bước refactor để tách folder/import.

Thứ tự học trong một file:

1. Hằng số cấu hình.
2. Exception/domain error.
3. Hàm xử lý path.
4. Hàm đọc file.
5. Hàm ghép dữ liệu.
6. Hàm xử lý CLI.
7. Hàm tạo output.
8. Hàm `main()`.
