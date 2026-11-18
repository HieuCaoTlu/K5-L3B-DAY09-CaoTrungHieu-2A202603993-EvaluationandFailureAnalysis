# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi bạn 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `E-seeded_regression-20261118-a9d4` |
| Triệu chứng | Grader `RefundAmountCorrect` fail (ledger=20000 != label=0), `DbFactKept` fail; Lab 8 grader FAIL (`status resolved != denied`). Reply nói "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202." trong khi label quy định từ chối hoàn (0đ). |
| Bước sai đầu tiên | Event 3: `model_override` payload `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 (`handoff`) và Event 2 (`investigator`) thực hiện tra cứu DB hoàn toàn đúng đắn (`order_id: O-202`, DB xác định không trễ). Bước 3 là nơi agent bắt đầu sai khi tự ý lấy số ngày trễ từ ticket của khách để ghi đè dữ liệu DB. |
| Failure mode | `FM-03` (`ticket_trust — tin ticket hơn DB`) |
| Đối chứng | Cùng `C-002@11` trên shape `fixed`: không có event `model_override`; Event 3 chạy thẳng vào `quote` với `amount_vnd: 0`, từ chối hoàn tiền; ledger ghi 0đ hoàn toàn khớp với nhãn. |
| Regression test | Grader `DbFactKept` và `RefundAmountCorrect` trong `tests/test_lab9_graders.py`; đã kiểm chứng bắt được 100% lỗi trên `seeded_regression` và đạt 100% pass trên `fixed`. |
| Chưa chắc chắn | Trace chỉ ghi nhận payload các event, không lưu chain-of-thought nội bộ của LLM nên không chứng minh được tại sao model lại ưu tiên tin văn bản khách nói hơn kết quả truy vấn tool investigator. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
