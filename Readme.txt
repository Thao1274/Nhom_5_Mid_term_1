
# Cinema Ticket Sales Analytics - CineInsight

## Giới thiệu dự án

**CineInsight** là một dự án phân tích dữ liệu bán vé xem phim từ hệ thống rạp chiếu phim tại khu vực Đà Nẵng. Dữ liệu sử dụng là dữ liệu thực tế, được chuẩn hóa nhằm phục vụ các phân tích về hành vi khách hàng, hiệu quả kinh doanh và tối ưu hóa hoạt động vận hành của rạp.

## Mục tiêu phân tích

- Phân tích nhóm khách hàng chính và hành vi mua vé theo độ tuổi, giới tính.
- Doanh thu theo ngày, giờ, thể loại phim, loại vé.
- Hiệu quả bán hàng qua các kênh (offline, website).
- Cơ hội bán chéo (bỏng ngô, combo).
- So sánh tỷ trọng doanh thu phim Việt Nam và phim nước ngoài (Mỹ).
- Xác định nhóm khách hàng tiềm năng theo độ tuổi, ngành nghề.

## Cấu trúc dữ liệu

### 1. Bảng `customer` – Thông tin khách hàng
- `customerid`: ID khách hàng duy nhất
- `DOB`: Ngày sinh
- `Gender`: Nam / Nữ
- `Address`, `Phường/Đường`, `Quận/Huyện`, `Tỉnh`: Địa chỉ cư trú
- `Website`: Có đặt vé qua web hay không
- `job`: Nghề nghiệp
- `industry`: Ngành nghề làm việc

### 2. Bảng `ticket` – Giao dịch bán vé
- `orderid`: Mã giao dịch
- `cashier`: Nhân viên/kênh bán vé
- `saledate`: Ngày giao dịch
- `total`: Tổng tiền thanh toán
- `customerid`: Khóa ngoại liên kết đến bảng `customer`
- `ticketcode`: Mã vé duy nhất
- `date`: Ngày xem phim
- `time`: Giờ chiếu
- `slot`, `room`: Suất chiếu, phòng chiếu
- `show_id`: Mã suất chiếu (liên kết với bảng `film`)
- `slot type`, `ticket type`: Loại ghế, loại vé
- `ticket price`: Giá vé
- `popcorn`: Có mua bắp/bỏng ngô hay không

### 3. Bảng `film` – Thông tin phim
- `show_id`: Mã suất chiếu
- `title`: Tên phim
- `director`, `cast`: Đạo diễn, diễn viên
- `country`: Quốc gia sản xuất
- `release_year`: Năm công chiếu
- `rating`: Phân loại độ tuổi (P, C13, C16, C18,...)
- `duration`: Thời lượng phim
- `listed_in`: Thể loại (Action, Comedy,...)
- `description`: Mô tả nội dung

## Các thư viện sử dụng

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
```

## Ví dụ đơn giản

```python
import pandas as pd
df = pd.read_excel("final_dataset.xlsx", sheet_name="Final")
df["Ngày bán"] = pd.to_datetime(df["Ngày bán"])
daily_revenue = df.groupby(df["Ngày bán"].dt.date)["Tổng"].sum()
daily_revenue.plot(kind="bar")
```

## Mục tiêu
Dự án được thực hiện bởi nhóm nghiên cứu dữ liệu tại Đà Nẵng, với mục tiêu hỗ trợ tối ưu hoạt động rạp chiếu phim qua phân tích dữ liệu thực tế.

---

