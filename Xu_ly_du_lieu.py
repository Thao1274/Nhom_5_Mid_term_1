# %% [markdown]
# ## Input dữ liệu

# %%
import pandas as pd

# %%
# Import dữ liệu
link = "https://docs.google.com/spreadsheets/d/1ZNKbIUmS5apHKtI_WUXlwHeBkyu19wrt/edit?gid=1149835378"

# %%
# tách chuỗi link và chỉ lấy phần 1ZNKbIUmS5apHKtI_WUXlwHeBkyu19wrt
sheet_id = link.split("/d/")[1].split("/")[0]

sheets = ["customer", "ticket", "film"]
data = {}

for name in sheets:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={name}"
    data[name] = pd.read_csv(url)

# Gọi từng sheet nếu cần
df_customer = data["customer"]
df_ticket = data["ticket"]
df_film = data["film"]

print(df_customer.head())


# %%
# Kiểm tra thông tin của 3 sheet
print(df_customer.info())
print(df_film.info())
print(df_ticket.info())

# %% [markdown]
# ## Chuẩn bị dữ liệu

# %% [markdown]
# ### Chuyển đối kiểu dữ liệu

# %%
# Bảng customer
df_customer.info()

# %% [markdown]
# Có thể thấy DOB đang bị sai kiểu dữ liệu, chúng ta cần chuyển sang dữ liệu date

# %%
df_customer['DOB'] = pd.to_datetime(df_customer['DOB'], errors='coerce')

# %%
df_ticket.info()

# %%
df_ticket.head(1)

# %% [markdown]
# saledate, total, D/O/B, age, date,time đang bị sai kiểu dữ liệu

# %%
df_ticket['saledate'] = pd.to_datetime(df_ticket['saledate'], errors='coerce')
df_ticket['date'] = pd.to_datetime(df_ticket['date'], errors='coerce')
df_ticket['time'] = pd.to_datetime(df_ticket['time'], format='%H:%M', errors='coerce').dt.time
df_ticket['total'] = pd.to_numeric(df_ticket['total'], errors='coerce').fillna(0).astype(int)

# %%
# check thấy data này có nhiều cột dư thừa và cần loại bỏ
df_film = df_film.drop(df_film.columns[10:25], axis=1)

# %% [markdown]
# ### Xử lý missing value

# %% [markdown]
# #### Bảng Customer

# %%
df_customer.head()

# %%
df_customer.info()

# %%
# Kiểm tra xem có bao nhiêu giá trị null
df_customer.isnull().sum()

# %%
df_customer_industry_null = df_customer[df_customer['industry'].isna()]

# %%
df_customer_industry_null['job'].unique()

# %% [markdown]
# Giá trị industry bị na ứng với nghề nghiệp là teenager, có thể fill giá trị na trong cột industry là ducation.

# %%
df_customer[['industry']] = df_customer[['industry']].fillna('education')

# %%
# Nhận thấy dữ liệu ở cột Address và Tỉnh bị miss số lượng nhỏ, không ảnh hưởng quá nhiều nếu phân phối dữ liệu, có thể xóa những giá trị đó khỏi tập dữ liệu.
df_customer = df_customer.dropna(subset = ["Tỉnh","Address","DOB"])
# Còn những dữ liệu bị thiếu ở cột khác, chuyển dữ liệu thành chưa biết, tránh ảnh hưởng đến phân phối dữ liệu
df_customer[["Phường/Đường","Quận/Huyện","Website"]] = df_customer[["Phường/Đường","Quận/Huyện","Website"]].fillna("Chưa biết")

# %% [markdown]
# #### Bảng Ticket

# %%
df_ticket.isna().sum()

# %%
# Nhận thấy giá trị bị null không ảnh hưởng nhiều đến phân phối dữ liệu, có thể loại bỏ, vì số lượng giá trị bị null chiếm phần nhỏ.
df_ticket = df_ticket.dropna(subset=["orderid"])

# %%
df_ticket.isna().sum()

# %%
# Các giá trị bị null cùng một hàng liên kết với nhau, như trên, chỉ cần xóa 1 cột các giá trị null khác cũng được loại bỏ

# %% [markdown]
# #### Bảng Film

# %%
df_film.isna().sum()

# %%
# Do số lượng những giá trị null ít nhưng số hàng ở bảng film cũng khá ít, chúng em đã dựa trên thông tin của bộ phim để cố gắng fill vào chỗ na
df_film_director_null = df_film[df_film['director'].isnull()]

# %%
update_dict = {
    'Man vs. Shark': 'David Diley',
    'Lost City of Machu Picchu': 'Chưa biết',
    'Oil Spill of The Century': 'Fabrice Gardel, Josselin Mahot',
    "Star Wars: Galaxy's Edge-Adventure Awaits": 'Christian Lamb',
    'Women Of Impact: Changing The World': 'Lisa Feit',
    'Marvel Rising: Battle of The Bands': 'Chris Rutkowski',
    'Marvel Rising: Chasing Ghosts': 'Alfred Gimeno',
    'Marvel Rising: Heart of Iron': 'Sol Choi',
    'Happy Birthday, Mickey!': 'Bert Gillett',
    'Marvel Studios: Expanding the Universe': 'Jon Watts',
    '(PĐ) DORAEMON: NOBITA VÀ MẶT TRĂNG PHIÊU LƯU KÝ (G)': 'Yakuwa Shinnosuke' 
}

# %%
for title, director in update_dict.items():
    df_film.loc[
        (df_film['title'] == title) & (df_film['director'].isnull()),
        'director'
    ] = director


# %%
# Và khi chọn 1 bộ phim, bộ phim đến từ nước nào cũng rất quan trọng, đó là lý do nên fill cột country
df_film_country_null = df_film[df_film['country'].isnull()]
df_film_country_null

# %%
update_country = {
    'Disney My Music Story: Perfume': 'Japan',
    'Great Shark Chow Down': 'United States',
    'Ultimate Viking Sword': 'United States',
    "Oil Spill of The Century": 'United States',
    'Chasing the Equinox': 'United States',
    'Happy Birthday, Mickey!': 'United States',
    'Marvel Studios: Expanding the Universe': 'United States',
    '(PĐ) DORAEMON: NOBITA VÀ MẶT TRĂNG PHIÊU LƯU KÝ (G)': 'Japan' 
}

# %%
for title, country in update_country.items():
    df_film.loc[
        (df_film['title'] == title) & (df_film['country'].isnull()),
        'country'
    ] = country

# %%
df_film_rating_null = df_film[df_film['rating'].isna()]

# %%
df_film_rating_null

# %%
update_rating = {
    'Disney My Music Story: Perfume': 'TV-G',
    'NGÔI ĐỀN KỲ QUÁI  (Pee Nak)': 'PG-13',
    'VÔ GIAN ĐẠO (C18)': 'C18',
    "THẰNG EM LÝ TƯỞNG (Inseparable Bros)": 'PG-13',
    "(LT) DORAEMON: NOBITA VÀ MẶT TRĂNG PHIÊU LƯU KÝ (Doraemon: Nobita's Chronicle of the Moon Exploration)": 'G',
    'LẬT MẶT: NHÀ CÓ KHÁCH': 'C16',
    'NỤ HÔN MA QUÁI (Sang Krasue)': 'PG-13',
    '(PĐ) DORAEMON: NOBITA VÀ MẶT TRĂNG PHIÊU LƯU KÝ (G)': 'G',
    'CÀ CHỚN ANH ĐỪNG ĐI': 'C13-C16'
}

# %%
for title, rating in update_rating.items():
    df_film.loc[
        (df_film['title'] == title) & (df_film['rating'].isnull()),
        'rating'
    ] = rating

# %%

df_film_listed_in_null = df_film[df_film['listed_in'].isna()]

# %%
df_film_listed_in_null

# %%
# Bộ phim doraemon có thể loại: Animation, Action, Adventure
df_film[['listed_in']] = df_film[['listed_in']].fillna('Animation, Action, Adventure')

# %% [markdown]
# Còn một số cột bị thiếu nhưng chúng em nhận thấy nó không ảnh hưởng đến hành vi mua hàng của khách hàng, nên chúng tôi vẫn giữ nguyên và chỉ dùng những cột quan trọng của bộ data này.

# %% [markdown]
# Trước khi tiến hành feature engineering, để thuận tiện hơn cho việc visualize cũng như các bước phân tích sau đó, chúng em sẽ quyết định gộp 3 file lại thành 1 file final.
# 
# Trong đó:
# - Bảng customer: Customerid là khóa chính merged với cột customerid bên bảng ticket
# - Bảng film: show_id là khóa chính và merged với cột show_id bên bảng ticket
# 

# %%
# Merged ticket với customer
merged_ticket_customer = pd.merge(df_ticket,df_customer, left_on = 'customerid', right_on = 'Customerid',how = 'left')

# %%
df_final = pd.merge(merged_ticket_customer,df_film, on = 'show_id',how = 'left' )

# %%
df_final.isna().sum()

# %% [markdown]
# Những cột Customerid, DOB, Gender,... như quan sát trên có số hàng miss value là như nhau, có thể do có thông tin vé mua nhưng mà không có thông tin khách hàng, số lượng missing value cũng không lớn, có tầm 95 hàng, rất ít so với 35378 quan sát, nên có thể loại bỏ các hàng này.
# 
# Cùng với đó chúng em tiến hành loại bỏ những cột mà không cần dùng đến để tranh gây rối, khó quan sát.
# 

# %%
columns_to_check = ['Customerid', 'DOB', 'Gender', 'Address', 'Phường/Đường',
                    'Quận/Huyện', 'Tỉnh', 'Website', 'job', 'industry']

df_final = df_final.dropna(subset=columns_to_check)


# %%
columns_to_drop = ['cast', 'release_year', 'duration', 'description', 'Unnamed: 25', 'Customerid','Website','Phường/Đường','Address']
df_final.drop(columns=columns_to_drop, inplace=True)

# %%
df_final.isna().sum()

# %%
df_final['Tỉnh'].value_counts()

# %% [markdown]
# Dữ liệu chủ yếu là từ Đà Nẵng, để có cái nhìn toàn diện hơn, xóa các tỉnh thành khác, chỉ giữ lại Đà Nẵng để xem doanh thu, xu hướng mua vé của khách hàng tại Đà Nẵng.

# %%
df_final = df_final[df_final['Tỉnh'] == 'Đà Nẵng']

# %%
df_final.info()

# %% [markdown]
# Sau khi đã merge các bảng lại với nhau và cũng như đã xử ly dữ liệu, dữ liệu đã sẵn sàng được đưa vào phân tích, cũng như visualization.

# %% [markdown]
# ## Feature Engineering

# %%
df_final.head(5)

# %% [markdown]
# Sau khi quan sát dữ liệu, có thể thêm một số cột sau:
# - Tuổi: tính tuổi khách hàng
# - Khoảng tuối, chia tuổi khách hàng thành nhiều nhóm tuổi khác nhau
# - Thời gian trong ngày, sáng, chiều

# %%
# Đảm bảo cả 'DOB' và 'saledate' đều là kiểu datetime
df_final['DOB'] = pd.to_datetime(df_final['DOB'], errors='coerce')
df_final['saledate'] = pd.to_datetime(df_final['saledate'], errors='coerce')

# Tính tuổi tại thời điểm mua hàng
df_final['Tuổi'] = (df_final['saledate'] - df_final['DOB']).dt.days // 365


# %%
def time_of_day(hour):
    if 5 <= hour < 12:
        return "Sáng"
    elif 12 <= hour < 17:
        return "Chiều"
    elif 17 <= hour < 21:
        return "Tối"
    else:
        return "Đêm"

df_final['time'] = pd.to_datetime(df_final['time'], format='%H:%M:%S', errors='coerce')
df_final['Thời gian trong ngày'] = df_final['time'].dt.hour.apply(time_of_day)


# %%
df_final['Tuổi'].value_counts()

# %%
df_final = df_final[~df_final['Tuổi'].isin([-1, -76])]

# %%
df_tre = df_final[df_final['Tuổi'].isin([0,1,2,3])]
df_tre['job'].unique()

# %% [markdown]
# Đang có sự sai lệch tuổi nghiêm trọng, các job là teenager nhưng vẫn có độ tuổi 0,1,2,3, tuy nhiên số lượng chúng khá lớn, nên cách tốt nhất là để những quan sát như vậy làm một nhóm tuổi riêng.

# %%
def group_age(age):
    if age == 0:
        return '0 tuổi'
    elif age == 1:
        return '1 tuổi'
    elif age == 2:
        return '2 tuổi'
    elif age == 3:
        return '3 tuổi'
    elif 4 <= age <= 11:
        return 'Trẻ em (4-11)'
    elif 12 <= age <= 17:
        return 'Thiếu niên (12-17)'
    elif 18 <= age <= 25:
        return 'Thanh niên (18-25)'
    elif 26 <= age <= 40:
        return 'Trưởng thành (26-40)'
    elif 41 <= age <= 60:
        return 'Trung niên (41-60)'
    else:
        return 'Cao tuổi (trên 60)'
df_final['Nhóm tuổi'] = df_final['Tuổi'].apply(group_age)


# %%
print(df_final)


