# 00 - Trước Khi Code

Trước khi viết code cho một tầng mới, luôn trả lời ngắn gọn 5 câu:

1. Tầng này giải quyết vấn đề gì?
2. Input là gì?
3. Output là gì?
4. Tối thiểu cần những hàm nào?
5. Lệnh kiểm tra sau khi viết xong là gì?

Luật:

- Không nhảy sang tầng sau khi tầng hiện tại chưa chạy được.
- Không thêm LLM, tool, agent, MCP, JsonGate nếu tầng hiện tại chưa cần.
- Không tách file sớm.
- Không viết nhiều tính năng cùng lúc.
- Mỗi lần thêm một hàm hoặc một tính năng nhỏ phải giải thích nó làm gì.
