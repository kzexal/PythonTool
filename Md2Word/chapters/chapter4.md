# CHƯƠNG 4. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 4.1 Kết luận đạt được
Báo cáo giữa kỳ đã ứng dụng thành công lý thuyết mạng phức hợp để mô hình hóa và phân tích mạng lưới khí hậu Việt Nam từ chuỗi số liệu nhiệt độ năm 2025 thu thập từ dự án NOAA GHCN:
1. **Phân hóa không gian rõ rệt:** Mạng lưới tự động phân tách thành hai miền rõ rệt: khối liên kết mạnh Bắc – Trung Bộ và các trạm cô lập ở Nam Bộ, hoàn toàn phù hợp với phân vùng khí hậu học Việt Nam.
2. **Xác định các trạm trọng yếu:** Trạm Thanh Hóa và Hà Đông đóng vai trò nút trung tâm có tính đại diện cao nhất ($C_D \ge 0.60$); trạm Nội Bài là cầu nối trung gian quan trọng nhất ($C_B = 0.05$).
3. **Phát hiện vùng lõi và hành lang:** Sơn La và Quy Nhơn là các trạm lõi với hệ số cụm tuyệt đối ($C = 1.00$), trong khi liên kết Nội Bài – Quy Nhơn là hành lang tương quan dài có giá trị trung gian cạnh cao nhất ($C_B(e) \approx 0.04$).

## 4.2 Hạn chế của nghiên cứu
- Ngưỡng lọc tương quan $\theta = 0.8$ là ngưỡng cố định đơn biến, chưa xét đến độ trễ thời gian (lag-correlation) khi các khối khí lạnh mất từ 1 đến 3 ngày để di chuyển từ Bắc vào Nam.
- Dữ liệu mới chỉ dừng ở biến nhiệt độ trung bình (`TAVG`), chưa kết hợp các yếu tố quan trọng khác như áp suất khí quyển, lượng mưa hay độ ẩm.

## 4.3 Kế hoạch cho báo cáo cuối kỳ
Để hoàn thiện đề tài trong giai đoạn cuối kỳ, các nội dung sau sẽ được phát triển tiếp:
1. Xây dựng **Đồ thị có hướng có độ trễ (Time-lag Directed Climate Network)** để xác định hướng lan truyền chính xác của các đợt sóng nhiệt và gió mùa.
2. Ứng dụng thuật toán **Community Detection** (như Louvain hoặc Infomap) để tự động phân vùng khí hậu Việt Nam từ cấu trúc mạng lưới.
3. Tích hợp phương pháp đồng bộ hóa sự kiện (**Event Synchronization**) đối với các hiện tượng thời tiết cực đoan (nắng nóng gay gắt, rét đậm rét hại).
