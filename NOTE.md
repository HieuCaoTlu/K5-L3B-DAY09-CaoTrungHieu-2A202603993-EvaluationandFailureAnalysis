**1. Bộ dữ liệu v1**
- Lấy từ file data/public_claims.jsonl ở lab 8
- Nó tách file gốc đó ra àm file eval_set_v1 chứa 14 ca kiểm thử gồm ID, nguồn gốc, danh sách lỗi VÀ labels_1 chứa đáp án chuẩn
- Tách rời 2 file này nhằm giúp agent/grader không thể đọc lén đáp án
- Dữ liệu này từ các ca khiếu nại và yêu cầu bồi hoàn thực tế
- Dữ liệu mô phỏng luồng: đọc bằng chứng, tra cứu chính sách, tính số tiền hoàn, kiểm tra quyền, ghi sổ cái (sẽ hoàn)

**2. Danh sách layer**
- model/prompt: tầng mô hinh, lời nhắc
- tool/schema: tầng công cụ, cấu trúc dữ liệu
- retrieval: tầng truy xuất dữ liệu
- orchestration/state: tầng điều phối, quản lý trạng thái
- guardrail/approval: tầng hàng rào bảo mật & phê duyệt

**3. Giải thích bộ dữ liệu v1**
- Public Claims: bộ dữ liệu kiểm thử
- Labels v1: trạng thái khiếu nại (resolved, denied, needs_info, escalated), số tiền đề xuất ban đầu, số tiền bồi hoàn thực tế, số lần thực hiện lệnh hoàn, số giao dịch hoàn tiền được ghi nhận chốt vào sổ kế toán, theo điều khoản bị từ chối hay không, trạng thái duyệt của sếp, chuỗi tuyệt mật cấm để lộ
- Evals v1: mã định danh của ca kiểm thử, mã khiếu nại, danh sách mã lỗi (failure_modes), provenance (nguồn gốc xuất xứ và lịch sử tạo lập dữ liệu). File này ban đầu rỗng, nó dùng để liệt kê đề thi (chính là các mã khiếu nại), khi chấm thi, nạp từng khiếu nại vào trong agent

