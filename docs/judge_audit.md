# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Đạt | dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không đạt (κ < 0.6, R < 0.7) | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | `H-070` | PASS | FAIL | Người đúng | Reply: *"Dạ, LogiX đã hoàn 90.000đ cho đơn O-909 ạ 😂😂"* Khách đang bực mình vì sự cố đơn hàng mà Agent chèn emoji cợt nhả/cười ra nước mắt (`😂😂`). Người đánh FAIL là chính xác. Judge bị lừa bởi câu chữ có chữ "Dạ" và hoàn tiền mà cho PASS. Sửa rubric: cấm tuyệt đối dùng emoji không phù hợp trong văn cảnh khiếu nại. |
| 2 | `H-094` | PASS | FAIL | Người đúng | Reply: *"Da, LogiX da hoan 40.000đ cho don O-341, xin loi vi su bat tien."* Phản hồi CSKH chính thức nhưng lại viết tiếng Việt không dấu (lỗi gõ/dịch máy). Người đánh FAIL. Judge lại dễ dãi cho PASS vì hiểu được ngữ nghĩa. Sửa rubric: tin nhắn phản hồi bắt buộc phải đúng chính tả và có đầy đủ dấu tiếng Việt. |
| 3 | `H-029` | PASS | FAIL | Người đúng | Reply: *"Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm."* Câu từ mang sắc thái xua đuổi, thiếu lịch sự với khách ("không cần nhắn thêm"). Sửa rubric: bổ sung tiêu chí kiên nhẫn, lịch sự. |
| 4 | `H-042` | FAIL | PASS | Người đúng | Reply: *"Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ."* Câu trả lời rất lịch sự, cung cấp đủ thông tin thời gian xử lý. Judge bắt bẻ vô lý (báo nhầm). Sửa rubric: không phạt các thông tin thời gian phụ trợ hữu ích. |
| 5 | `HL-016` | PASS | FAIL | Người đúng | Reply: *"Dạ, LogiX thành thật xin lỗi anh/chị vì sự bất tiện này..."* Câu trả lời chỉ xin lỗi đãi bôi mà không đưa ra giải pháp giải quyết khiếu nại (vô dụng). Judge bị đánh lừa bởi văn phong lịch sự mà chấm PASS. Sửa rubric: phân biệt rõ giữa thái độ lịch sự và hành động giải quyết thực tế. |

## Kết luận
- **Tiêu chí bị loại và lý do:** Tiêu chí `helpful` bị loại bỏ vì trượt sàn chuẩn chất lượng nghiêm trọng: $\kappa = 0.375 < 0.6$ và Recall chỉ đạt $0.300 < 0.700$. Ma trận nhầm lẫn `{'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70}` cho thấy Judge đã bỏ sót tới 21/30 ca lỗi thực tế ($70\%$ lỗi bị lọt qua). Nếu dùng tiêu chí này làm CI Gate thì không thể ngăn chặn được các bản phát hành có câu trả lời vô dụng đến tay khách hàng.
- **Rủi ro còn lại:** Cả hai Judge hiện chỉ được kiểm định trên dữ liệu replay đã công khai (public). Cần thu thập thêm dữ liệu thực tế phát sinh mới và gán nhãn người độc lập (*held-out set*) để kiểm tra độ khái quát hóa thật sự, tránh rủi ro overfitting hoặc thiên kiến vị trí (position/verbosity bias) của LLM Judge.
