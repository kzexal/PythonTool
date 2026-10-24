"""Tạo file template Word chuẩn từ Mẫu ĐATN 2019 của ĐHBKHN kèm trang bìa, lời cam đoan, lời cảm ơn và tóm tắt."""
from pathlib import Path
import os, sys, zipfile, re
import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ưu tiên Mẫu ĐATN 2019 chính thức của trường; nếu không có thì fallback sang DATN(1).docx
SOURCE = Path('Mẫu ĐATN_2019_version 1_1.docx')
if not SOURCE.exists():
    SOURCE = Path('DATN(1).docx')
OUTPUT = Path('template_clean.docx')

if not SOURCE.exists():
    raise FileNotFoundError(f'Không tìm thấy {SOURCE}. Hãy đặt file mẫu cạnh script này.')

doc = Document(SOURCE)

# 1. Căn lề chuẩn A4 theo đúng qui định Mẫu ĐATN 2019:
# A4: 21.0cm x 29.7cm
# Top: 2.0cm, Bottom: 2.0cm, Left: 3.5cm, Right: 2.5cm
for section in doc.sections:
    section.page_width = Inches(8.2677)    # 21.0 cm
    section.page_height = Inches(11.6929)  # 29.7 cm
    section.top_margin = Inches(0.7874)    # 2.0 cm
    section.bottom_margin = Inches(0.7874) # 2.0 cm
    section.left_margin = Inches(1.3780)   # 3.5 cm
    section.right_margin = Inches(0.9843)  # 2.5 cm

# 2. Cập nhật thông tin trang bìa (Cover Page)
for p in doc.paragraphs[:20]:
    if 'Thiết kế hệ thống tự động điều chỉnh' in p.text:
        p.text = 'Thiết kế thiết bị giám sát học sinh'
        for r in p.runs: r.bold = True; r.font.size = Pt(22)
    elif 'nhiệt độ trong thiết bị sấy hoa quả' in p.text:
        p.text = 'lên xuống xe buýt đưa đón'
        for r in p.runs: r.bold = True; r.font.size = Pt(22)
    elif 'NGUYỄN VĂN A' in p.text:
        p.text = 'BÙI DUY KHÁNH'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(14)
    elif 'nguyenvanabc@sis.hust.edu.vn' in p.text:
        p.text = 'khanh.bd204017@sis.hust.edu.vn'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif 'Ngành Kỹ thuật điện' in p.text:
        p.text = 'Ngành Kỹ thuật Điện tử - Viễn thông'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(13)
    elif 'Chuyên ngành Hệ thống điện' in p.text:
        p.text = 'Chuyên ngành Hệ thống nhúng và IoT'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(13)

# Cập nhật bảng thông tin bìa (Table 0)
if doc.tables:
    tbl0 = doc.tables[0]
    tbl0.rows[0].cells[1].paragraphs[0].text = 'ThS. Đinh Thị Nhung'
    tbl0.rows[1].cells[1].paragraphs[0].text = 'Kỹ thuật Điện tử'
    tbl0.rows[2].cells[1].paragraphs[0].text = 'Trường Điện – Điện tử'
    tbl0.rows[3].cells[0].paragraphs[0].text = 'HÀ NỘI, 6/2026'
    tbl0.rows[3].cells[1].paragraphs[0].text = 'HÀ NỘI, 6/2026'

# 3. Cập nhật Lời cam đoan
if len(doc.paragraphs) > 24:
    doc.paragraphs[19].text = 'LỜI CAM ĐOAN'
    doc.paragraphs[19].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in doc.paragraphs[19].runs: r.bold = True; r.font.size = Pt(14)

    doc.paragraphs[20].text = (
        'Tôi là Bùi Duy Khánh, mã số sinh viên 20224017, sinh viên lớp Điện tử 03 – Khóa 67, '
        'Trường Điện – Điện tử, Đại học Bách Khoa Hà Nội. Người hướng dẫn là ThS. Đinh Thị Nhung. '
        'Tôi xin cam đoan toàn bộ nội dung được viết trong quyển đồ án “Thiết kế thiết bị giám sát '
        'học sinh lên xuống xe buýt đưa đón” là kết quả nghiên cứu của bản thân. Mọi thông tin được '
        'trích dẫn đều tuân thủ quy định về sở hữu trí tuệ; các tài liệu tham khảo được liệt kê rõ ràng. '
        'Tôi xin chịu hoàn toàn trách nhiệm với những nội dung được viết trong đồ án này.'
    )
    doc.paragraphs[20].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.paragraphs[21].text = 'Hà Nội, ngày 26 tháng 6 năm 2026'
    doc.paragraphs[21].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.paragraphs[22].text = 'Sinh viên thực hiện'
    doc.paragraphs[22].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.paragraphs[23].text = '(Ký và ghi rõ họ tên)'
    doc.paragraphs[23].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.paragraphs[24].text = '\n\nBùi Duy Khánh'
    doc.paragraphs[24].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.paragraphs[24].add_run().add_break(WD_BREAK.PAGE)

# 4. Cập nhật Lời cảm ơn
if len(doc.paragraphs) > 29:
    doc.paragraphs[25].text = 'LỜI CẢM ƠN'
    doc.paragraphs[25].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in doc.paragraphs[25].runs: r.bold = True; r.font.size = Pt(14)

    doc.paragraphs[26].text = (
        'Để hoàn thành chương trình học tập và hoàn thiện đồ án tốt nghiệp này, bên cạnh sự nỗ lực '
        'của bản thân, em đã nhận được sự quan tâm, dạy dỗ và giúp đỡ vô cùng quý báu từ các Thầy Cô, '
        'gia đình và bạn bè.\n\n'
        'Trước hết, em xin bày tỏ lòng biết ơn sâu sắc và chân thành đến ThS. Đinh Thị Nhung – giảng viên '
        'Trường Điện – Điện tử, Đại học Bách Khoa Hà Nội đã tận tình hướng dẫn, đưa ra định hướng, ý kiến '
        'giúp em hoàn thành tốt đồ án.\n\n'
        'Em xin chân thành cảm ơn Ban Giám hiệu nhà trường, cùng toàn thể quý Thầy Cô trong Khoa đã tận tình '
        'truyền đạt những kiến thức nền tảng và chuyên sâu quý báu, tạo mọi điều kiện thuận lợi nhất cho em '
        'trong suốt những năm tháng học tập và rèn luyện dưới mái trường.\n\n'
        'Dù đã dành nhiều thời gian, công sức và sự nghiêm túc để hoàn thành báo cáo song quyển đồ án tốt nghiệp '
        'chắc chắn khó tránh khỏi những thiếu sót nhất định. Em rất mong nhận được những ý kiến đóng góp, phê bình '
        'quý báu từ quý Thầy Cô trong Hội đồng chấm đồ án tốt nghiệp để đề tài được hoàn thiện và phát triển sâu sắc hơn.\n\n'
        'Em xin trân trọng cảm ơn!'
    )
    doc.paragraphs[26].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.paragraphs[27].text = 'Hà Nội, ngày 26 tháng 6 năm 2026'
    doc.paragraphs[27].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.paragraphs[28].text = 'Sinh viên thực hiện'
    doc.paragraphs[28].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.paragraphs[29].text = '\n\nBùi Duy Khánh'
    doc.paragraphs[29].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.paragraphs[29].add_run().add_break(WD_BREAK.PAGE)

# 5. Cập nhật Tóm tắt nội dung đồ án
if len(doc.paragraphs) > 31:
    doc.paragraphs[30].text = 'TÓM TẮT NỘI DUNG ĐỒ ÁN'
    doc.paragraphs[30].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in doc.paragraphs[30].runs: r.bold = True; r.font.size = Pt(14)

    doc.paragraphs[31].text = (
        'Trong những năm gần đây, tình trạng bỏ quên học sinh trên các phương tiện đưa đón đã trở thành '
        'một vấn đề nhức nhối, gây ra những hậu quả nghiêm trọng về mặt an toàn và tâm lý. Nhằm giải quyết '
        'bài toán này, đồ án tiến hành nghiên cứu, thiết kế và chế tạo “Thiết bị giám sát học sinh lên xuống '
        'xe buýt đưa đón”.\n\n'
        'Hệ thống được xây dựng dựa trên vi điều khiển trung tâm lõi kép ESP32 kết hợp với hệ điều hành nhúng '
        'thời gian thực FreeRTOS, cho phép xử lý đa luồng dữ liệu liên tục mà không gây trễ phần cứng. Về mặt '
        'thiết bị, sản phẩm tích hợp đầu đọc thẻ RFID RC522 để định danh học sinh khi lên/xuống xe, module '
        'định vị vệ tinh ATGM336H thu thập tọa độ địa lý, cùng màn hình OLED hiển thị thông tin trực quan. '
        'Toàn bộ dữ liệu thu thập được đồng bộ hóa tự động lên cơ sở dữ liệu đám mây Firebase Realtime Database.\n\n'
        'Điểm nổi bật của đề tài là khả năng đồng bộ dữ liệu nhanh chóng và gửi thông báo tức thì. Hệ thống '
        'sử dụng kết nối Wi-Fi để đẩy thông báo trạng thái kèm vị trí chính xác (thông qua liên kết Google Maps) '
        'đến điện thoại của phụ huynh thông qua nền tảng Telegram Bot. Kết quả thực nghiệm thực tế cho thấy '
        'hệ thống hoạt động ổn định, độ sai số định vị thấp và thời gian phản hồi thông báo đạt dưới 2 giây, '
        'mở ra một giải pháp quản lý toàn diện, tiết kiệm chi phí và có tính khả thi cao.'
    )
    doc.paragraphs[31].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.paragraphs[31].add_run().add_break(WD_BREAK.PAGE)

# 6. Sửa tiêu đề Danh mục bảng biểu nếu bị lỗi tên trong mẫu
for p in doc.paragraphs[35:48]:
    if p.text.strip() == 'DANH MỤC HÌNH VẼ' and p != doc.paragraphs[34]:
        p.text = 'DANH MỤC BẢNG BIỂU'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True

# 7. Xóa bỏ các chương mẫu hướng dẫn của trường (từ index 50 trở đi), giữ lại Section 0 và Section 1
body = doc._element.body
elements = list(body)
sectPr = body.sectPr
for el in elements[50:]:
    if el is not sectPr:
        body.remove(el)

# Thiết lập keep_with_next cho các heading
for name in ('Heading 1', 'Heading 2', 'Heading 3', 'Heading 4'):
    try:
        style = doc.styles[name]
        style.paragraph_format.keep_with_next = True
    except KeyError:
        pass
try:
    doc.styles['Heading 1'].paragraph_format.page_break_before = True
except KeyError:
    pass

# Yêu cầu Word cập nhật tất cả trường (TOC, số trang, TOF) khi mở file
settings = doc.settings._element
update = settings.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}updateFields')
if update is None:
    update = OxmlElement('w:updateFields')
    settings.append(update)
update.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'true')

doc.save(OUTPUT)

print(f'Đã tạo template chuẩn: {OUTPUT.resolve()}')
print('Bao gồm: Trang bìa, Lời cam đoan, Lời cảm ơn, Tóm tắt, Mục lục, Danh mục hình, Danh mục bảng.')
