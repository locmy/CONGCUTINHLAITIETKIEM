import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
st.image("IMG_20260811_151724.jpg")

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm _ Phạm Thị Mỹ Lộc",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    amount = Decimal(str(amount)).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return f"{amount:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

loai_lai = st.radio(
    "Loại lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================
P = Decimal(str(tien_gui))
r = Decimal(str(lai_suat)) / Decimal("100")
months = Decimal(str(ky_han))

# Lãi suất theo tháng
lai_suat_thang = r / Decimal("12")

# Số kỳ nhận lãi
if hinh_thuc_nhan_lai == "Hàng tháng":
    so_ky = int(ky_han)
    lai_suat_ky = lai_suat_thang

elif hinh_thuc_nhan_lai == "Hàng quý":
    so_ky = int(ky_han // 3)
    lai_suat_ky = r / Decimal("4")

else:
    so_ky = 1
    lai_suat_ky = r * months / Decimal("12")


# =========================
# LÃI ĐƠN
# =========================
if loai_lai == "Lãi đơn":

    # Tổng lãi trong toàn bộ kỳ hạn
    tong_lai = P * r * months / Decimal("12")

    # Tiền lãi mỗi kỳ
    if hinh_thuc_nhan_lai == "Cuối kỳ":
        lai_dinh_ky = tong_lai

    elif hinh_thuc_nhan_lai == "Hàng tháng":
        lai_dinh_ky = P * lai_suat_thang

    else:  # Hàng quý
        lai_dinh_ky = P * (r / Decimal("4"))

    tong_tien = P + tong_lai


# =========================
# LÃI KÉP
# =========================
else:

    # Lãi kép:
    # Nếu nhận lãi hàng tháng -> nhập lãi hàng tháng
    # Nếu nhận lãi hàng quý -> nhập lãi hàng quý
    # Nếu cuối kỳ -> tính theo tháng để phản ánh lãi kép theo tháng

    if hinh_thuc_nhan_lai == "Hàng tháng":

        so_ky = int(ky_han)

        tong_tien = P * (
            Decimal("1") + lai_suat_thang
        ) ** so_ky

        tong_lai = tong_tien - P

        # Lãi kỳ đầu tiên
        lai_dinh_ky = P * lai_suat_thang

    elif hinh_thuc_nhan_lai == "Hàng quý":

        so_ky = int(ky_han // 3)
        lai_suat_quy = r / Decimal("4")

        tong_tien = P * (
            Decimal("1") + lai_suat_quy
        ) ** so_ky

        tong_lai = tong_tien - P

        # Lãi kỳ đầu tiên
        lai_dinh_ky = P * lai_suat_quy

    else:
        # Cuối kỳ: ghép lãi theo tháng
        so_ky = int(ky_han)

        tong_tien = P * (
            Decimal("1") + lai_suat_thang
        ) ** so_ky

        tong_lai = tong_tien - P

        lai_dinh_ky = tong_lai


# =========================
# KẾT QUẢ
# =========================
st.subheader("📊 Kết quả")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💵 Tiền lãi định kỳ",
        format_money(lai_dinh_ky)
    )

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        format_money(tong_lai)
    )

st.metric(
    "💰 Tổng tiền gốc + lãi",
    format_money(tong_tien)
)

st.divider()

# =========================
# CHI TIẾT
# =========================
st.subheader("📝 Chi tiết khoản gửi")

st.write(f"**Số tiền gốc:** {format_money(P)}")
st.write(f"**Kỳ hạn:** {ky_han} tháng")
st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
st.write(f"**Phương pháp tính:** {loai_lai}")

# =========================
# BẢNG TÓM TẮT
# =========================
st.subheader("📋 Bảng tổng kết")

data = {
    "Nội dung": [
        "Tiền gốc",
        "Lãi suất",
        "Kỳ hạn",
        "Tiền lãi định kỳ",
        "Tổng tiền lãi",
        "Tổng tiền nhận được"
    ],
    "Giá trị": [
        format_money(P),
        f"{lai_suat:.2f}%/năm",
        f"{ky_han} tháng",
        format_money(lai_dinh_ky),
        format_money(tong_lai),
        format_money(tong_tien)
    ]
}

st.table(data)

st.caption(
    "⚠️ Kết quả là số tiền ước tính theo lãi suất nhập vào và chưa xét thuế, "
    "phí hoặc các điều kiện riêng của từng ngân hàng."
)
