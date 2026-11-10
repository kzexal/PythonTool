# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ PHƯƠNG PHÁP NGHIÊN CỨU

## 2.1 Tổng quan về mạng lưới khí hậu (Climate Networks)
Mạng lưới khí hậu là một đồ thị $G = (V, E)$, trong đó:
- Tập hợp nút $V = \{v_1, v_2, \dots, v_N\}$ đại diện cho $N$ trạm khí tượng hoặc các điểm lưới không gian.
- Tập hợp cạnh $E \subseteq V \times V$ đại diện cho sự tương quan có ý nghĩa thống kê giữa hai trạm tương ứng.
- Trọng số cạnh $w_{ij}$ phản ánh cường độ đồng pha hoặc phụ thuộc giữa biến thiên nhiệt độ tại trạm $i$ và trạm $j$.

## 2.2 Phương pháp tính toán tương quan Pearson
Hệ số tương quan tuyến tính Pearson $r_{ij}$ giữa chuỗi nhiệt độ $X_i$ của trạm $i$ và chuỗi $X_j$ của trạm $j$ gồm $T$ mốc quan trắc được xác định theo công thức:

$$r_{ij} = \frac{\sum_{t=1}^{T} (X_{i,t} - \bar{X}_i)(X_{j,t} - \bar{X}_j)}{\sqrt{\sum_{t=1}^{T} (X_{i,t} - \bar{X}_i)^2} \sqrt{\sum_{t=1}^{T} (X_{j,t} - \bar{X}_j)^2}}$$

Trong đó $\bar{X}_i$ và $\bar{X}_j$ lần lượt là giá trị nhiệt độ trung bình cả năm của từng trạm.

Ma trận kề $A$ của mạng lưới được xác định qua bước lọc ngưỡng (thresholding) với ngưỡng cố định $\theta = 0.8$:

$$A_{ij} = \begin{cases} 1, & \text{nếu } r_{ij} > \theta \text{ và } i \neq j \\ 0, & \text{ngược lại} \end{cases}$$

Trọng số gán cho mỗi cạnh tồn tại là $w_{ij} = r_{ij}$.

## 2.3 Các chỉ số đo lường cấu trúc mạng phức hợp

### 2.3.1 Degree Centrality (Độ đo bậc trung tâm)
Degree Centrality phản ánh số lượng liên kết trực tiếp của một trạm với các trạm khác trong mạng lưới đã được chuẩn hóa:

$$C_D(v) = \frac{\deg(v)}{N - 1} = \frac{1}{N - 1} \sum_{u \in V, u \neq v} A_{vu}$$

Trong mạng lưới khí hậu, trạm có $C_D$ cao đại diện cho khu vực có diễn biến thời tiết đồng pha với phần lớn các vùng khác.

### 2.3.2 Betweenness Centrality (Độ đo trung gian nút)
Betweenness Centrality đo lường tần suất một nút nằm trên đường đi ngắn nhất giữa tất cả các cặp nút khác:

$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Trong đó $\sigma_{st}$ là tổng số đường đi ngắn nhất giữa hai nút $s$ và $t$, còn $\sigma_{st}(v)$ là số đường đi ngắn nhất đi qua nút $v$. Nút có $C_B$ cao đóng vai trò là "cầu nối" trung chuyển các đợt biến động khí hậu giữa các tiểu vùng tách biệt.

### 2.3.3 Clustering Coefficient (Hệ số gom cụm)
Hệ số gom cụm của nút $v$ đánh giá mức độ gắn kết giữa các nút lân cận của $v$:

$$C(v) = \frac{2 e_v}{k_v(k_v - 1)} = \frac{\sum_{j, k} A_{vj} A_{jk} A_{kv}}{k_v(k_v - 1)}$$

Trong đó $k_v = \deg(v)$ và $e_v$ là số cạnh thực tế nối giữa các lân cận của $v$. Trong nghiên cứu khí hậu, giá trị này biểu thị trạm nằm sâu trong một đới khí hậu đồng nhất, có tính ổn định không gian cao.

### 2.3.4 Edge Betweenness Centrality (Độ đo trung gian cạnh)
Edge Betweenness Centrality đo lường tỉ lệ các đường đi ngắn nhất đi qua một cạnh $e = (u, v)$:

$$C_B(e) = \sum_{s \neq t} \frac{\sigma_{st}(e)}{\sigma_{st}}$$

Cạnh có $C_B(e)$ lớn đóng vai trò là liên kết huyết mạch (bottleneck), kết nối hai cộng đồng hoặc hai khối khí hậu khác nhau.

## 2.4 Quy trình triển khai trên Python
Quy trình thực nghiệm được cài đặt trên môi trường Python sử dụng các thư viện chuyên dụng:
1. **Pandas:** Nạp dữ liệu từ tệp nguồn GHCN/NOAA, làm sạch các bản ghi lỗi, chuyển đổi kiểu dữ liệu thời gian và tạo bảng xoay ma trận nhiệt độ `pivot_table(index='DATE', columns='NAME', values='TAVG')`.
2. **Nội suy tuyến tính:** Áp dụng phương thức `interpolate(method='linear')` để xử lý triệt để các ô dữ liệu bị thiếu do gián đoạn quan trắc hoặc truyền tin tại trạm.
3. **NetworkX:** Khởi tạo đồ thị `nx.Graph()`, tính toán các chỉ số trung tâm `nx.degree_centrality()`, `nx.betweenness_centrality()`, `nx.clustering()`, và `nx.edge_betweenness_centrality()`.
4. **Matplotlib:** Trực quan hóa đồ thị bố trí tròn (`circular_layout`), vẽ chuỗi thời gian biến thiên và các đặc tính nút/cạnh.
