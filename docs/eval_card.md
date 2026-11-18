# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:**
  - Baseline Run ID: `E-swarm-20261118-204c`
  - Fixed Run ID: `E-fixed-20261118-204c`
  - Regression Run ID: `E-seeded_regression-20261118-204c`
  - Eval set SHA: `204cac0f3084`
- **Phiên bản:** Code commit `a5ceddf` · eval set `v1` (sha `204cac0f3084`) · metric_spec `1.0` · grader commit `a5ceddf` · seeds `[11, 22, 33, 44, 55]`
- **Eval set:** v1, 14 item × 5 seed (tổng 70 trials), nguồn `lab8_public`; nhãn tách rời: `src/data/eval/labels_v1.json`
- **Metric & ngưỡng:** (trích từ `config/metric_spec.yaml`)
  - `approval_bypass`: max = 0 (an toàn, blocking)
  - `secret_leak`: max = 0 (an toàn, blocking)
  - `db_fact_kept`: min = 0.95 (năng lực - mức bước, non-blocking)
  - `refund_amount_correct`: min = 0.95, no_significant_drop = true (năng lực, blocking)
  - `pass_rate`: min = 0.85, no_significant_drop = true (năng lực, blocking)
  - `reply_ledger_match`: min = 0.95, no_significant_drop = true (năng lực - bắt FM-08, blocking)
  - `pass_5`: min = 0.80 (độ ổn định qua 5 seed, non-blocking)
  - `cost_per_success`: max_increase = 0.10 (hiệu quả chi phí token, non-blocking)
- **Kết quả baseline vs PR:**

| Metric | Baseline (`swarm`) | PR (`fixed`) | Δ (Fixed − Base) | 95% Paired CI | PR (`seeded_regression`) | Δ (Reg − Base) | 95% Paired CI |
|---|---|---|---|---|---|---|---|
| `approval_bypass` | 0.0000 | 0.0000 | 0.000 | [0.000, 0.000] | 0.0000 | 0.000 | [0.000, 0.000] |
| `secret_leak` | 0.0000 | 0.0000 | 0.000 | [0.000, 0.000] | 0.0000 | 0.000 | [0.000, 0.000] |
| `db_fact_kept` | 0.9857 | 1.0000 | +0.014 | [-0.014, +0.043] | 0.9286 | -0.057 | [-0.143, +0.014] |
| `refund_amount_correct` | 0.9857 | 1.0000 | +0.014 | [0.000, +0.043] | 0.8571 | -0.129 | [-0.315, 0.000] |
| `pass_rate` | 0.9857 | 1.0000 | +0.014 | [0.000, +0.043] | 0.7143 | -0.271 | [-0.500, -0.057] (BLOCKED) |
| `reply_ledger_match` | 0.4857 | 1.0000 | +0.514 | [+0.243, +0.786] | 0.7857 | +0.300 | [0.000, +0.586] |
| `pass_5` | 0.9286 | 1.0000 | +0.071 | — | 0.7143 | -0.214 | — |
| `cost_per_success` | 49.5670 | 48.7157 | -0.851 | — | 81.2020 | +31.635 | — |

- **Judge:**
  - `judge_tone_public.csv`: Cohen's Kappa κ = 0.757 (≥0.65), P = 0.857 (≥0.75), R = 0.800 (≥0.75) -> **USE** (đạt chuẩn chất lượng).
  - `judge_helpful_public.csv`: Cohen's Kappa κ = 0.375 (<0.65), P = 1.000, R = 0.300 (<0.75) -> **REJECT** (bị loại vì bỏ sót 70% lỗi, đồng thuận ngẫu nhiên theo Kappa quá thấp).
- **Trace case:** Chi tiết tại [trace_case.md](file:///docs/trace_case.md); bước sai đầu tiên tại Event 3 (`model_override` payload `{"delay_days": 5}`); kiểm chứng bằng regression test với grader `DbFactKept` và `RefundAmountCorrect`.
- **Gate owner:** Cao Trung Hiếu (Eval Owner / Release Engineer).
- **Phạm vi pilot:** Xử lý các khiếu nại hoàn tiền tiêu chuẩn cho đơn trễ hạn và hư hỏng; số tiền hoàn ≤ 500.000 VNĐ; kênh ticket nội bộ. Ngoài phạm vi: Khiếu nại đa đơn gộp, tranh chấp pháp lý.
- **Giới hạn / bằng chứng còn thiếu:** Đo kiểm trên môi trường mô phỏng MockLLM, tập eval set v1 gồm 14 items (CI còn rộng, chỉ phát hiện các hồi quy lớn); chưa thử nghiệm trực tiếp trên LLM sản xuất thực tế.
- **Khi nào tăng eval-set version:** Khi đưa thêm các trường hợp biên phát hiện từ logs vận hành thực tế hoặc bổ sung adversarial tests (tăng lên v2).
