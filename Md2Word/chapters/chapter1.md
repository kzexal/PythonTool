# CHƯƠNG 1. MỞ ĐẦU

## 1.1 Đặt vấn đề

Hoạt động đưa đón học sinh bằng xe buýt giúp phụ huynh chủ động hơn trong việc đưa trẻ đến trường và góp phần tổ chức giao thông học đường. Tuy nhiên, quá trình đón và trả học sinh cần được giám sát cẩn thận. Khi việc điểm danh phụ thuộc hoàn toàn vào ghi chép thủ công, người phụ trách có thể gặp khó khăn trong việc cập nhật trạng thái của từng học sinh, đặc biệt khi có nhiều học sinh lên hoặc xuống xe trong khoảng thời gian ngắn.

Bên cạnh việc xác nhận học sinh đã lên hoặc xuống xe, phụ huynh cũng có nhu cầu nhận thông tin kịp thời và biết vị trí tương đối của xe trong hành trình. Vì vậy, đề tài **“Thiết kế thiết bị giám sát học sinh lên xuống xe buýt đưa đón”** hướng đến việc xây dựng một hệ thống kết hợp nhận dạng RFID, định vị GPS, vi điều khiển ESP32 và kết nối Internet. Hệ thống dự kiến ghi nhận sự kiện quẹt thẻ, cập nhật dữ liệu trực tuyến và gửi thông báo đến phụ huynh.

Đề tài tập trung vào việc xây dựng mô hình nguyên mẫu để khảo sát tính khả thi của giải pháp. Hiệu quả thực tế cần được xác định thông qua quá trình kiểm thử, đo đạc và đánh giá trong các điều kiện sử dụng cụ thể.

## 1.2 Đối tượng khách hàng

### 1.2.1 Nhà trường và đơn vị cung cấp dịch vụ đưa đón học sinh

Đây là nhóm người dùng có nhu cầu theo dõi danh sách học sinh sử dụng dịch vụ đưa đón. Hệ thống có thể hỗ trợ người quản lý tra cứu thông tin học sinh, cập nhật dữ liệu thẻ và kiểm tra các sự kiện lên hoặc xuống xe. Việc lưu trữ dữ liệu tập trung giúp giảm sự phụ thuộc vào ghi chép giấy, đồng thời tạo cơ sở để đối chiếu thông tin khi cần thiết.

### 1.2.2 Phụ huynh học sinh

Phụ huynh là nhóm nhận thông báo về trạng thái di chuyển của học sinh. Khi hệ thống ghi nhận một sự kiện hợp lệ, thông báo có thể bao gồm thông tin nhận dạng đã được cấu hình, thời điểm ghi nhận và vị trí GPS nếu thiết bị có dữ liệu định vị phù hợp. Thông báo chỉ là một nguồn thông tin hỗ trợ; nhà trường và đơn vị vận hành vẫn cần duy trì quy trình giám sát an toàn phù hợp.

### 1.2.3 Người vận hành thiết bị

Người vận hành chịu trách nhiệm lắp đặt, cấp nguồn, kiểm tra kết nối mạng, quản lý thẻ và xử lý các tình huống bất thường. Giao diện và quy trình vận hành cần đủ đơn giản để người phụ trách có thể nhận biết khi thiết bị chưa sẵn sàng hoặc khi dữ liệu chưa được gửi thành công.

## 1.3 Mục tiêu của đề tài

Mục tiêu tổng quát là thiết kế và xây dựng mô hình thiết bị có khả năng ghi nhận sự kiện học sinh lên hoặc xuống xe, kết hợp thông tin vị trí và gửi dữ liệu đến hệ thống trực tuyến.

Các mục tiêu cụ thể gồm:

- Nghiên cứu phương án sử dụng thẻ RFID để nhận dạng học sinh.
- Sử dụng ESP32 làm bộ điều khiển trung tâm, tiếp nhận dữ liệu từ các khối phần cứng và điều phối hoạt động của thiết bị [@esp32].
- Tích hợp module GPS để thu thập tọa độ khi điều kiện tín hiệu cho phép.
- Xây dựng cơ chế gửi dữ liệu lên cơ sở dữ liệu trực tuyến để lưu thông tin học sinh và sự kiện điểm danh [@firebase].
- Xây dựng chức năng gửi thông báo tới phụ huynh thông qua dịch vụ nhắn tin được lựa chọn.
- Kiểm thử các chức năng chính, ghi nhận lỗi và đánh giá những giới hạn của mô hình nguyên mẫu.

### 1.3.1 Phạm vi thực hiện

Đề tài tập trung vào thiết bị điện tử, chương trình nhúng, luồng dữ liệu và cơ chế thông báo. Các nội dung như triển khai thương mại trên đội xe quy mô lớn, chứng nhận an toàn, vận hành liên tục trong mọi điều kiện thời tiết và tích hợp với hệ thống quản lý chính thức của nhà trường nằm ngoài phạm vi của mô hình thử nghiệm ban đầu.

### 1.3.2 Sản phẩm dự kiến

Sản phẩm dự kiến gồm một mô hình phần cứng tích hợp bộ điều khiển, đầu đọc RFID, module GPS và các linh kiện hiển thị hoặc báo trạng thái cần thiết; chương trình nhúng để đọc dữ liệu và truyền thông; cấu trúc lưu trữ dữ liệu trực tuyến; cùng quy trình kiểm thử các tình huống sử dụng cơ bản.

## 1.4 Phương pháp thực hiện

### 1.4.1 Nghiên cứu và phân tích

Tìm hiểu yêu cầu của quy trình đưa đón học sinh, xác định thông tin cần ghi nhận và phân tích các công nghệ có thể sử dụng. Từ đó, xác định yêu cầu chức năng, yêu cầu phi chức năng và những ràng buộc về chi phí, nguồn điện, kết nối mạng và tính thuận tiện khi sử dụng.

### 1.4.2 Thiết kế hệ thống

Phân chia hệ thống thành các khối chức năng: nhận dạng RFID, xử lý trung tâm, định vị GPS, kết nối mạng, lưu trữ dữ liệu và thông báo. Xác định giao tiếp giữa các khối, định dạng dữ liệu trao đổi và trình tự xử lý một sự kiện điểm danh.

### 1.4.3 Xây dựng phân hệ phần cứng

Lựa chọn linh kiện theo yêu cầu chức năng và khả năng tương thích điện. Thiết kế sơ đồ nguyên lý, bố trí kết nối, kiểm tra nguồn cấp và lắp ráp mô hình. Trước khi vận hành đồng thời, từng module cần được kiểm tra độc lập để khoanh vùng lỗi thuận tiện hơn.

### 1.4.4 Xây dựng phân hệ phần mềm

Phát triển chương trình nhúng để đọc thẻ, tiếp nhận dữ liệu GPS, quản lý trạng thái kết nối và gửi dữ liệu đến dịch vụ trực tuyến. Các lỗi như thẻ không hợp lệ, GPS chưa có tọa độ, mất Wi-Fi hoặc máy chủ không phản hồi cần được xử lý có kiểm soát.

### 1.4.5 Kiểm thử và đánh giá

Xây dựng các kịch bản thử nghiệm cho việc đọc thẻ hợp lệ, đọc thẻ chưa đăng ký, nhận dữ liệu GPS, gửi dữ liệu trực tuyến và xử lý khi mất kết nối. Ghi lại kết quả đo được thay vì giả định trước hiệu năng của hệ thống.

### 1.4.6 Đề xuất hướng cải tiến

Dựa trên kết quả kiểm thử, xác định các điểm còn hạn chế và đề xuất cải tiến như lưu đệm dữ liệu khi mất mạng, tăng cường bảo mật, cải thiện giao diện quản lý hoặc bổ sung phương thức truyền thông dự phòng.

## 1.5 Các tiêu chí đánh giá hệ thống

### 1.5.1 Tính chính xác

Đánh giá khả năng đọc đúng mã thẻ đã đăng ký, liên kết sự kiện với đúng học sinh và ghi nhận thời gian, vị trí phù hợp với dữ liệu thực tế. Các trường hợp đọc thẻ thất bại hoặc dữ liệu GPS chưa hợp lệ cần được phân biệt rõ.

### 1.5.2 Tính khả dụng

Đánh giá mức độ thuận tiện khi lắp đặt, cấp nguồn, quẹt thẻ và kiểm tra trạng thái thiết bị. Người vận hành cần nhận biết được các trạng thái cơ bản như sẵn sàng, đang xử lý và lỗi kết nối.

### 1.5.3 Tính tin cậy và bảo mật

Đánh giá khả năng duy trì hoạt động, xử lý lỗi và hạn chế truy cập trái phép. Thông tin cá nhân của học sinh cần được thu thập ở mức cần thiết, bảo vệ thông tin xác thực và giới hạn quyền truy cập vào dữ liệu.

### 1.5.4 Hiệu suất

Đo thời gian từ lúc quẹt thẻ đến khi thiết bị xử lý xong và khi thông báo được gửi thành công. Kết quả cần được tổng hợp từ nhiều lần thử nghiệm và ghi rõ điều kiện mạng trong quá trình đo.

### 1.5.5 Khả năng mở rộng

Xem xét khả năng bổ sung thẻ, thay đổi thông tin học sinh và mở rộng số lượng thiết bị mà không phải thay đổi toàn bộ kiến trúc. Việc mở rộng cần đi kèm cơ chế quản lý dữ liệu và phân quyền phù hợp.

### 1.5.6 Chi phí và hiệu quả sử dụng

Tổng hợp chi phí linh kiện, lắp ráp và vận hành thử nghiệm. Hiệu quả cần được đánh giá dựa trên mức độ hỗ trợ quy trình điểm danh và chất lượng thông tin cung cấp cho người dùng, không chỉ dựa trên số lượng chức năng đã xây dựng.

## 1.6 Kết luận chương

Chương 1 đã trình bày bối cảnh, đối tượng sử dụng, mục tiêu, phạm vi và phương pháp thực hiện đề tài. Các tiêu chí đánh giá cũng được xác định để làm cơ sở kiểm thử mô hình. Chương tiếp theo trình bày yêu cầu thiết kế, kiến trúc tổng quan và lựa chọn giải pháp công nghệ cho hệ thống.
