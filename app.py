import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. TẠO VÀ XỬ LÝ DỮ LIỆU
data = {
    "Họ và tên": [
        "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E",
        "Vũ Thị F", "Đặng Văn G", "Bùi Thị H", "Đỗ Văn I", "Ngô Thị K"
    ],
    "Chuyên cần": [9.0, 8.5, 7.0, 10.0, 6.5, 8.0, 9.5, 7.5, 5.0, 8.5],
    "Giữa kỳ": [8.0, 7.5, 6.0, 9.0, 5.5, 7.0, 8.5, 6.5, 4.5, 8.0],
    "Cuối kỳ": [8.5, 8.0, 6.5, 9.5, 6.0, 7.5, 9.0, 7.0, 5.5, 8.5]
}

df = pd.DataFrame(data)

# Tính Điểm tổng kết
df["Tong_ket"] = (0.20 * df["Chuyên cần"] + 0.30 * df["Giữa kỳ"] + 0.50 * df["Cuối kỳ"]).round(2)

# Hàm Xếp loại
def xep_loai(score):
    if score >= 8.5: return "Giỏi"
    elif score >= 7.0: return "Khá"
    elif score >= 5.0: return "Trung bình"
    else: return "Yếu"

df["Xếp loại"] = df["Tong_ket"].apply(xep_loai)


# 2. XÂY DỰNG GIAO DIỆN WEB STREAMLIT

# Yêu cầu: Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Yêu cầu: Hiển thị bảng điểm
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df[["Họ và tên", "Chuyên cần", "Giữa kỳ", "Cuối kỳ", "Tong_ket", "Xếp loại"]], use_container_width=True)

# Yêu cầu: Thống kê (Điểm trung bình, Cao nhất/Thấp nhất, Số SV đạt)
st.subheader("📊 Thống kê chung")
col1, col2, col3 = st.columns(3)

tb_lop = df["Tong_ket"].mean().round(2)
sv_max = df.loc[df["Tong_ket"].idxmax()]["Họ và tên"]
sv_min = df.loc[df["Tong_ket"].idxmin()]["Họ và tên"]
so_sv_dat = (df["Tong_ket"] >= 5).sum()

col1.metric("Điểm TB của lớp", f"{tb_lop}")
col2.metric("Số SV đạt (>=5)", f"{so_sv_dat}/{len(df)}")
col3.metric("Cao nhất / Thấp nhất", f"{sv_max} / {sv_min}")

st.markdown("---")

# Yêu cầu: Tạo danh sách xổ xuống (Selectbox) để xem điểm từng sinh viên
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn một sinh viên:", df["Họ và tên"])

sv_info = df[df["Họ và tên"] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv_info["Chuyên cần"])
c2.metric("Giữa kỳ", sv_info["Giữa kỳ"])
c3.metric("Cuối kỳ", sv_info["Cuối kỳ"])
c4.metric("Tổng kết", sv_info["Tong_ket"])
c5.metric("Xếp loại", sv_info["Xếp loại"])

st.markdown("---")

# Yêu cầu: Hiển thị biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(df["Họ và tên"], df["Tong_ket"], color="#4CAF50")
ax.set_xlabel("Điểm tổng kết")
ax.set_xlim(0, 10)
ax.invert_yaxis()

for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width}', va='center')

st.pyplot(fig)

# Yêu cầu: Họ tên & MSSV ở cuối trang
st.markdown("---")
st.caption("<p style='text-align: center; color: gray; font-size: 13px;'>Thực hiện bởi: Phạm Hoàng Kim - MSSV: 052208015014</p>", unsafe_allow_html=True)
