# CHƯƠNG 1. MỞ ĐẦU

## 1.1 Đặt vấn đề
Hệ thống khí hậu toàn cầu nói chung và khí hậu Việt Nam nói riêng là một hệ thống động lực phi tuyến phức tạp (complex dynamical system) với sự tương tác nhiều tầng bậc giữa khí quyển, đại dương và địa hình. Các phương pháp khí tượng truyền thống thường phân tích dữ liệu tại từng trạm đo đơn lẻ hoặc mô hình hóa bằng các phương trình vi phân động lực học chất lưu quy mô lớn. Tuy nhiên, cách tiếp cận này gặp khó khăn trong việc nắm bắt các mối liên kết từ xa (teleconnections) và đặc tính cấu trúc mạng lưới quy mô vùng.

Trong những năm gần đây, lý thuyết mạng phức hợp (Complex Network Theory) đã mở ra hướng tiếp cận mới đầy tiềm năng mang tên **Climate Networks** (Mạng lưới khí hậu). Bằng cách ánh xạ mỗi trạm quan trắc thành một nút (node) và mức độ tương đồng giữa các chuỗi biến thiên thời gian thành các cạnh (edges), mạng phức hợp cho phép nghiên cứu tô-pô không gian, xác định các trung tâm điều hòa khí hậu và các hành lang lan truyền biến động nhiệt độ.

## 1.2 Mục tiêu đề tài
Nghiên cứu tập trung giải quyết các mục tiêu cụ thể sau:

### 1.2.1 Thu thập và xử lý dữ liệu chuỗi thời gian
Thu thập dữ liệu quan trắc khí hậu từ Cơ quan Quản lý Khí quyển và Đại dương Quốc gia Hoa Kỳ (NOAA) thông qua dự án Mạng lưới Khí hậu Lịch sử Toàn cầu (GHCN). Trích xuất và chuẩn hóa dữ liệu nhiệt độ trung bình hàng ngày (`TAVG`) trong năm 2025 từ 16 trạm khí tượng tiêu biểu tại Việt Nam, đồng thời thực hiện xử lý dữ liệu khuyết bằng kỹ thuật nội suy tuyến tính.

### 1.2.2 Xây dựng mô hình mạng lưới khí hậu
Tính toán ma trận hệ số tương quan tuyến tính Pearson giữa các chuỗi thời gian nhiệt độ của từng cặp trạm; áp dụng ngưỡng lọc tương quan $\theta = 0.8$ để thiết lập đồ thị mạng lưới vô hướng có trọng số.

### 1.2.3 Khảo sát các đặc trưng tô-pô mạng lưới
Tính toán và phân tích các chỉ số trung tâm vi mô và vĩ mô bao gồm: Bậc kết nối (**Degree Centrality**), Trung gian nút (**Betweenness Centrality**), Hệ số gom cụm (**Clustering Coefficient**) và Trung gian cạnh (**Edge Betweenness Centrality**).

### 1.2.4 Đánh giá động thái khí hậu cục bộ
Phân tích chi tiết chuỗi thời gian nhiệt độ tại trạm trung tâm đại diện (Hà Đông) nhằm đối chiếu và kiểm chứng các quy luật vật lý với kết quả thu được từ cấu trúc đồ thị.

## 1.3 Đối tượng và phạm vi nghiên cứu
- **Nguồn dữ liệu:** Dữ liệu được trích xuất từ dự án **Global Historical Climatology Network (GHCN)** do **NOAA** (Cơ quan Quản lý Khí quyển và Đại dương Quốc gia Hoa Kỳ) cung cấp công khai và miễn phí, chứa dữ liệu lịch sử từ hàng ngàn trạm khí tượng chuẩn hóa trên toàn thế giới.
- **Đối tượng nghiên cứu:** Chuỗi số liệu nhiệt độ trung bình ngày (`TAVG`) từ tệp dữ liệu `weather_data.csv`.
- **Phạm vi không gian:** 16 trạm khí tượng tiêu biểu phân bố trải dài từ Bắc vào Nam của Việt Nam.
- **Phạm vi thời gian:** Giai đoạn quan trắc trọn vẹn năm 2025 (từ 01/01/2025 đến 31/12/2025).
