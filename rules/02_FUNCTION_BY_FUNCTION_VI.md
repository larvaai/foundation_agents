# 02 - Viết Từng Hàm Một

Mỗi hàm/tính năng đi theo nhịp:

1. Nói mục đích của hàm.
2. Nói input/output.
3. Viết hàm.
4. Chạy kiểm tra nhỏ nếu có thể.
5. Giải thích kết quả.
6. Chỉ sau đó mới sang hàm/tính năng kế tiếp.

Mẫu giải thích:

```text
Hàm: read_text_file(path)
Mục đích: đọc một file text bằng UTF-8.
Input: đường dẫn file.
Output: nội dung dạng string.
Lỗi cần xử lý: file không tồn tại, sai encoding.
```

Luật giữ nhịp:

- Nếu một hàm bắt đầu làm hai việc, tách ý tưởng ra nhưng vẫn để trong cùng `main.py`.
- Nếu chưa hiểu vì sao cần hàm đó, chưa viết.
- Nếu chạy lỗi, sửa lỗi của hàm hiện tại trước khi thêm hàm mới.
