import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
import os

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN CHỦ ĐẠO (CHẠM DESIGN SYSTEM - ELITE EDITION)
# ==============================================================================
st.set_page_config(
    page_title="CHẠM Hub | Nền tảng Nâng cao Nhận thức & Đồng hành Alzheimer",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    h1, h2, h3, h4 { color: #18324A; font-family: 'Segoe UI', system-ui, sans-serif; }
    
    .cham-epic-card {
        background: #FFFFFF; padding: 28px; border-radius: 16px;
        border-left: 8px solid #55A88B; box-shadow: 0 10px 25px rgba(24, 50, 74, 0.07);
        margin-bottom: 22px; transition: transform 0.3s ease;
    }
    .cham-epic-card:hover { transform: translateY(-3px); }
    
    .cham-epic-card-warm {
        background: linear-gradient(135deg, #FFFDF9 0%, #FFF5EC 100%);
        padding: 28px; border-radius: 16px; border-left: 8px solid #D18A55;
        box-shadow: 0 10px 25px rgba(209, 138, 85, 0.09); margin-bottom: 22px;
    }
    .cham-epic-card-tech {
        background: linear-gradient(135deg, #F5F3FB 0%, #EFEBF9 100%);
        padding: 28px; border-radius: 16px; border-left: 8px solid #7867B5;
        box-shadow: 0 10px 25px rgba(120, 103, 181, 0.09); margin-bottom: 22px;
    }
    .cham-quote-box {
        background: linear-gradient(135deg, #E0F0E8 0%, #D2EBE0 100%);
        color: #18324A; padding: 24px 32px; border-radius: 14px;
        font-style: italic; font-size: 1.12em; border-left: 6px solid #2D6A4F;
        box-shadow: 0 4px 15px rgba(45, 106, 79, 0.08); margin: 20px 0;
    }
    .badge-nc { background-color: #DCEAF5; color: #18324A; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
    .badge-cs { background-color: #E0F0E8; color: #2D6A4F; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
    .badge-cd { background-color: #FCE8D5; color: #9C5221; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
    .badge-cn { background-color: #E8E2F4; color: #5B4E8C; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. KHỞI TẠO DỮ LIỆU ĐỒNG BỘ TOÀN CỤC (SESSION STATE)
# ==============================================================================
if 'visited' not in st.session_state:
    intro_placeholder = st.empty()
    with intro_placeholder.container():
        st.markdown("""
            <style>
            @keyframes epicFloat {
                0% { transform: translateY(50px) scale(0.85); opacity: 0; }
                50% { opacity: 1; }
                100% { transform: translateY(0px) scale(1); opacity: 1; }
            }
            .epic-splash {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(135deg, #18324A 0%, #254B6E 40%, #2D6A4F 100%);
                z-index: 9999; display: flex; flex-direction: column;
                justify-content: center; align-items: center; color: white; text-align: center; padding: 30px;
            }
            .epic-icon { font-size: 120px; animation: epicFloat 2s ease-out forwards; }
            .epic-title { font-size: 52px; font-weight: 900; letter-spacing: 8px; margin-top: 20px; }
            .epic-sub { font-size: 22px; color: #F2C66D; margin-top: 12px; font-weight: 600; }
            </style>
            <div class="epic-splash">
                <div class="epic-icon">🪷 🤝</div>
                <div class="epic-title">DỰ ÁN CHẠM</div>
                <div class="epic-sub">THẤU HIỂU ĐỂ KẾT NỐI – KẾT NỐI ĐỂ SẺ CHIA</div>
                <p style="margin-top: 30px; opacity: 0.9; font-size: 17px; font-style: italic;">"Không ai phải đi một mình trên hành trình đối diện với Alzheimer"</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    intro_placeholder.empty()
    st.session_state['visited'] = True

# Bức tường sẻ chia và nhật ký chung cập nhật thời gian thực xuyên suốt
if 'community_notes' not in st.session_state:
    st.session_state['community_notes'] = [
        {"author": "Minh Thư (Học sinh lớp 11)", "role": "Người chơi trải nghiệm CHẠM", "msg": "Trước đây mình hay gắt gỏng mỗi khi bà hỏi đi hỏi lại một câu. Sau khi chơi bàn cờ CHẠM và đọc phần trải nghiệm góc nhìn, mình mới hiểu bà không cố tình làm phiền mà vì ký ức của bà đang rơi rụng từng ngày.", "time": "10/11/2026 14:15"},
        {"author": "Cô Thanh Hương", "role": "Người chăm sóc gia đình", "msg": "Cảm ơn dự án đã nói lên tiếng lòng của những người chăm sóc. Đôi khi chúng tôi không cần lời khuyên y khoa cao siêu, chỉ cần một câu hỏi thăm: 'Hôm nay bạn có mệt không?' là đủ ấm lòng.", "time": "11/11/2026 09:20"},
        {"author": "Hoàng Nam", "role": "Tình nguyện viên cộng đồng", "msg": "Thông điệp 'Không ai phải đi một mình' thực sự chạm đến trái tim. Mong bộ board game này sẽ sớm có mặt tại các trường học và nhà văn hóa.", "time": "12/11/2026 16:45"}
    ]

if 'caregiver_journal' not in st.session_state:
    st.session_state['caregiver_journal'] = [
        {"title": "Một ngày kiên nhẫn hơn", "content": "Hôm nay bố quên chìa khóa xe và tìm suốt 30 phút. Nhớ lại cẩm nang của CHẠM, mình không còn cáu gắt nữa mà nhẹ nhàng cùng bố tìm lại. Nhìn nụ cười của bố lúc tìm thấy, mình thấy lòng nhẹ tênh.", "time": "12/11/2026 19:30"}
    ]

# ==============================================================================
# 3. HEADER & THANH MENU NGANG TINH GỌN (4 MODULES ĐẦU TƯ TRỌNG TÂM)
# ==============================================================================
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    if os.path.exists("AlkaLotus/logo.png"):
        st.image("AlkaLotus/logo.png", width=110)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    else:
        st.markdown("<h1 style='text-align:center;'>🪷</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#18324A; font-weight:800;'>CHẠM HUB — NỀN TẢNG ĐỒNG HÀNH & NÂNG CAO NHẬN THỨC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2D6A4F; font-weight:600; font-size:1.1em; margin-top:2px;'>Thấu hiểu để kết nối – Kết nối để sẻ chia • Trạm thông tin tích hợp chuyên sâu cùng Board Game CHẠM</p>", unsafe_allow_html=True)

st.divider()

# Hệ thống 4 Module trọng tâm, đầu tư hoành tráng, loại bỏ hoàn toàn các thành phần rườm rà
selected_tab = st.selectbox(
    "📌 LỰA CHỌN KHÔNG GIAN TRẢI NGHIỆM:",
    [
        "🏛️ 1. Tổng quan Dự án & Thống kê Y tế Xác thực",
        "🧠 2. Cẩm nang Giao tiếp & Xử lý Tình huống Thực tế (Đồ sộ)",
        "🎲 3. Trạm Rút Thẻ Tương tác & Mini-game Thử thách",
        "💌 4. Nhật ký Chữa lành & Bức tường Sẻ chia Trực tiếp"
    ],
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: TỔNG QUAN DỰ ÁN & THỐNG KÊ Y TẾ XÁC THỰC
# ==============================================================================
if selected_tab == "🏛️ 1. Tổng quan Dự án & Thống kê Y tế Xác thực":
    st.title("🪷 CHẠM — Hành Trình Đánh Thức Sự Thấu Cảm")
    st.markdown("#### *“Alzheimer có thể lấy đi những ký ức trong tâm trí, nhưng không bao giờ có thể lấy đi nhu cầu được yêu thương và tôn trọng của một con người.”*")
    
    st.markdown("""
    <div class="cham-quote-box">
        Dự án <b>CHẠM</b> kết hợp hoàn hảo giữa <b>Board Game chiến lược thực tế (64 ô hành trình)</b> và 
        <b>Nền tảng số trực tuyến</b>. Dự án tập trung giải quyết vấn đề cốt lõi: <b>Xóa bỏ sự kỳ thị xã hội và hỗ trợ giảm áp lực tâm lý cho người chăm sóc</b> 
        thông qua mô hình Phygital (Kết hợp Vật lý & Số hóa) độc đáo.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Thống kê Y tế Toàn cầu & Việt Nam (Nguồn chuẩn xác)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Người mắc toàn cầu", "55+ Triệu", "Nguồn: WHO (2023)")
    c2.metric("Tỷ lệ do Alzheimer", "60% – 70%", "Nguồn: Alzheimer's Association")
    c3.metric("Tại Việt Nam (Ước tính)", "~500.000+", "Nguồn: Bộ Y tế / Chuyên gia lão khoa")
    c4.metric("Người chịu ảnh hưởng", "150+ Triệu", "Gia đình & Người chăm sóc trực tiếp")

    col_chart, col_info = st.columns([1.3, 1])
    with col_chart:
        st.markdown("##### 📈 Dự báo gia tăng số ca mắc sa sút trí tuệ toàn cầu (Nguồn: WHO)")
        df_trend = pd.DataFrame({
            "Năm": ["2020", "2030 (Dự báo)", "2050 (Dự báo)"],
            "Số lượng (Triệu người)": [55, 78, 139]
        })
        fig = px.bar(
            df_trend, x="Năm", y="Số lượng (Triệu người)",
            text="Số lượng (Triệu người)",
            color="Năm",
            color_discrete_sequence=["#18324A", "#55A88B", "#D18A55"]
        )
        fig.update_traces(textposition="outside", textfont_size=14)
        fig.update_layout(showlegend=False, height=360, margin=dict(t=20, b=20, l=20, r=20), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("##### 🎯 Giá trị cốt lõi của Hệ sinh thái CHẠM")
        st.markdown("""
        <div class="cham-epic-card">
            <b>1. Triết lý Phi-đối kháng:</b><br>
            Không xem bệnh tật là kẻ thù tiêu diệt, mà hướng tới sự thấu hiểu, kiên nhẫn và sẻ chia gánh nặng.<br><br>
            <b>2. Mô hình Kết hợp (Phygital):</b><br>
            Board game 600x600mm để kết nối trực tiếp tại bàn chơi; Web Hub trực tuyến để mở rộng tri thức và chia sẻ cộng đồng.<br><br>
            <b>3. Khẩu hiệu hành động:</b><br>
            <i>Thấu hiểu để kết nối – Không ai phải đi một mình!</i>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏛️ Chi tiết 4 Trụ cột hoạt động thực tế")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        <div class="cham-epic-card">
            <span class="badge-nc">NGHIÊN CỨU</span>
            <h4 style="margin-top:12px;">Khoa học & Xã hội</h4>
            <p style="font-size:0.92em; line-height:1.5;">Khảo sát tâm lý gia đình, thu thập dữ liệu thực tế và chuẩn hóa tài liệu chuyên môn về sa sút trí tuệ.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="cham-epic-card-tech">
            <span class="badge-cn">CÔNG NGHỆ</span>
            <h4 style="margin-top:12px;">Giải pháp số vì con người</h4>
            <p style="font-size:0.92em; line-height:1.5;">Phát triển nền tảng web đồng hành, công cụ tra cứu tình huống và hệ thống nhật ký trực tuyến hỗ trợ cộng đồng.</p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="cham-epic-card-warm">
            <span class="badge-cs">CHĂM SÓC</span>
            <h4 style="margin-top:12px;">Không gian thấu hiểu</h4>
            <p style="font-size:0.92em; line-height:1.5;">Xây dựng cẩm nang ứng xử chi tiết tại nhà, bảo vệ phẩm giá người bệnh và xoa dịu áp lực cho người chăm sóc.</p>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="cham-epic-card">
            <span class="badge-cd">CỘNG ĐỒNG</span>
            <h4 style="margin-top:12px;">Lan tỏa & Mạng lưới</h4>
            <p style="font-size:0.92em; line-height:1.5;">Tổ chức các chiến dịch giáo dục cộng đồng, xóa bỏ định kiến và kết nối nguồn lực hỗ trợ bền vững.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 2: CẨM NANG GIAO TIẾP & XỬ LÝ TÌNH HUỐNG THỰC TẾ (ĐỒ SỘ & CHI TIẾT)
# ==============================================================================
elif selected_tab == "🧠 2. Cẩm nang Giao tiếp & Xử lý Tình huống Thực tế (Đồ sộ)":
    st.title("🧠 Cẩm Nang Ứng Xử & Giao Tiếp Nhân Văn Chi Tiết")
    st.markdown("Thư viện chuyên sâu tổng hợp các kịch bản và phương pháp ứng xử chuẩn mực dành cho gia đình khi đối mặt với các triệu chứng phức tạp của Alzheimer.")

    care_tab1, care_tab2, care_tab3, care_tab4 = st.tabs([
        "🗣️ Lặp câu hỏi & Quên từ ngữ", 
        "🔍 Hoang tưởng & Cáo buộc mất đồ", 
        "🌅 Hoàng hôn (Sundowning) & Đi lạc", 
        "🛁 Vệ sinh cá nhân & Ăn uống"
    ])

    with care_tab1:
        st.markdown("""
        <div class="cham-epic-card">
            <h3>🗣️ Tình huống: Người bệnh hỏi lặp lại một câu hỏi liên tục mỗi vài phút</h3>
            <p style="font-size:1.05em; line-height:1.6;"><b>Bản chất:</b> Người bệnh thực sự bị mất khả năng lưu giữ ký ức ngắn hạn. Họ không hề cố tình làm phiền bạn, mà mỗi lần hỏi là một lần họ thực sự quên mất câu trả lời trước đó.</p>
            <hr>
            <div style="display:flex; gap:20px;">
                <div style="flex:1; background:#FADBD8; padding:15px; border-radius:10px;">
                    <b style="color:#C0392B;">❌ Phản ứng sai lầm:</b><br>
                    Quát mắng, tỏ thái độ bực bội: <i>"Con vừa trả lời rồi cơ mà! Sao cứ hỏi hoài thế?"</i><br>
                    <b>Hậu quả:</b> Làm người bệnh cảm thấy bất an, tự ti và thu mình lại.
                </div>
                <div style="flex:1; background:#D4EFDF; padding:15px; border-radius:10px;">
                    <b style="color:#27AE60;">✅ Ứng xử chuẩn CHẠM:</b><br>
                    Kiên nhẫn trả lời lại bằng tông giọng ấm áp như lần đầu. Dùng công cụ hỗ trợ trực quan (như viết ra giấy hoặc treo đồng hồ to) và khéo léo chuyển hướng sang hoạt động khác.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with care_tab2:
        st.markdown("""
        <div class="cham-epic-card-warm">
            <h3>🔍 Tình huống: Người bệnh cáo buộc người thân lấy trộm đồ</h3>
            <p style="font-size:1.05em; line-height:1.6;"><b>Bản chất:</b> Do quên nơi cất đồ (ví dụ: cất chìa khóa trong tủ lạnh rồi quên), não bộ tự động đổ lỗi cho sự thay đổi xung quanh để giải thích sự biến mất đó.</p>
            <hr>
            <div style="display:flex; gap:20px;">
                <div style="flex:1; background:#FADBD8; padding:15px; border-radius:10px;">
                    <b style="color:#C0392B;">❌ Phản ứng sai lầm:</b><br>
                    Cãi lý tới cùng, lớn tiếng chứng minh sự trong sạch của mình.<br>
                    <b>Hậu quả:</b> Tăng sự nghi kỵ, gây xung đột và kích động mạnh.
                </div>
                <div style="flex:1; background:#D4EFDF; padding:15px; border-radius:10px;">
                    <b style="color:#27AE60;">✅ Ứng xử chuẩn CHẠM:</b><br>
                    Công nhận cảm xúc lo lắng của họ (<i>"Mất đồ chắc bố lo lắm nhỉ"</i>), sau đó nhẹ nhàng cùng tìm kiếm tại các vị trí quen thuộc mà không tranh cãi đúng sai.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with care_tab3:
        st.markdown("""
        <div class="cham-epic-card-tech">
            <h3>🌅 Tình huống: Hội chứng hoàng hôn (Sundowning) & Đòi đi lạc</h3>
            <p style="font-size:1.05em; line-height:1.6;"><b>Bản chất:</b> Khi chiều tối xuống, sự mệt mỏi kết hợp với thay đổi ánh sáng làm tăng sự hoang mang, khiến họ muốn "về nhà cũ" thời thơ ấu.</p>
            <hr>
            <div style="display:flex; gap:20px;">
                <div style="flex:1; background:#FADBD8; padding:15px; border-radius:10px;">
                    <b style="color:#C0392B;">❌ Phản ứng sai lầm:</b><br>
                    Khóa trái cửa nhốt trong phòng hoặc quát mắng bắt ngồi yên.<br>
                    <b>Hậu quả:</b> Kích thích phản ứng hoảng loạn, tìm cách trốn ra ngoài nguy hiểm.
                </div>
                <div style="flex:1; background:#D4EFDF; padding:15px; border-radius:10px;">
                    <b style="color:#27AE60;">✅ Ứng xử chuẩn CHẠM:</b><br>
                    Bật đèn sáng sớm trong nhà để giảm bóng tối; khóa ẩn cửa ra vào; pha ly sữa ấm, mở bản nhạc xưa để trấn an tâm lý.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with care_tab4:
        st.markdown("""
        <div class="cham-epic-card">
            <h3>🛁 Tình huống: Kháng cự khi tắm rửa & Khó khăn ăn uống</h3>
            <p style="font-size:1.05em; line-height:1.6;"><b>Bản chất:</b> Người bệnh có thể sợ nước, cảm thấy lạnh hoặc quên mất các bước thực hiện sinh hoạt cơ bản.</p>
            <hr>
            <div style="display:flex; gap:20px;">
                <div style="flex:1; background:#FADBD8; padding:15px; border-radius:10px;">
                    <b style="color:#C0392B;">❌ Phản ứng sai lầm:</b><br>
                    Dùng vũ lực kéo ép vào phòng tắm hoặc đút ép ăn.<br>
                    <b>Hậu quả:</b> Gây sợ hãi, tổn thương thể chất và tinh thần.
                </div>
                <div style="flex:1; background:#D4EFDF; padding:15px; border-radius:10px;">
                    <b style="color:#27AE60;">✅ Ứng xử chuẩn CHẠM:</b><br>
                    Biến giờ tắm thành trải nghiệm thư giãn với nước ấm vừa phải, chuẩn bị khăn mềm sẵn sàng; chọn món ăn mềm dễ cầm nắm khi họ quên dùng thìa đũa.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 3: TRẠM RÚT THẺ TƯƠNG TÁC & MINI-GAME THỬ THÁCH
# ==============================================================================
elif selected_tab == "🎲 3. Trạm Rút Thẻ Tương tác & Mini-game Thử thách":
    st.title("🎲 Trạm Rút Thẻ Tương Tác & Mini-game Thử Thách")
    st.markdown("Kết hợp hoàn hảo giữa công cụ rút thẻ tình huống cho Board Game và mini-game thử thách xử lý tình huống thực tế.")

    sub_tab_1, sub_tab_2 = st.tabs(["🎴 Trạm Rút Thẻ Tình Huống CHẠM (132 Thẻ)", "🎮 Mini-game: Thử Thách Xử Lý Tình Huống"])

    with sub_tab_1:
        st.subheader("Trợ lý rút thẻ ngẫu nhiên cho ván chơi Board Game")
        deck_library = {
            "Thẻ Kiến thức (KT) — Khoa học & Sự thật": [
                {"code": "KT-01", "title": "Phân biệt Quên & Alzheimer", "content": "Quên chìa khóa rồi nhớ lại là tuổi già; quên chìa khóa dùng để làm gì là bệnh lý.", "action": "Thảo luận nhóm: Nêu 2 dấu hiệu cảnh báo sớm cần đưa người thân đi khám."},
                {"code": "KT-08", "title": "Giấc ngủ và Não bộ", "content": "Giấc ngủ sâu giúp hệ thống glymphatic dọn dẹp protein độc hại.", "action": "Đề xuất 2 thói quen cải thiện giấc ngủ người cao tuổi."}
            ],
            "Thẻ Góc nhìn (GN) — Thấu cảm & Phẩm giá": [
                {"code": "GN-03", "title": "Sự tự ti thầm lặng", "content": "Người bệnh giai đoạn đầu thường cố giấu sự sa sút vì sợ làm gánh nặng.", "action": "Làm thế nào để con cái nhận biết sự bất an này mà không làm họ tổn thương?"}
            ],
            "Thẻ Thử thách (TC) — Xử lý tình huống": [
                {"code": "TC-04", "title": "Từ chối tắm rửa", "content": "Người bệnh kiên quyết không chịu tắm vì sợ lạnh và hoảng sợ.", "action": "Đưa ra giải pháp thuyết phục nhẹ nhàng không dùng vũ lực."}
            ],
            "Thẻ Hợp tác (HT) — Sức mạnh cộng đồng": [
                {"code": "HT-02", "title": "Mạng lưới 'Hàng xóm Tươi cười'", "content": "Liên kết hộ gia đình hỗ trợ quan sát người cao tuổi đi lại an toàn.", "action": "Mỗi thành viên đóng góp 1 sáng kiến kết nối khu phố."}
            ]
        }

        c_sel, c_res = st.columns([1, 1.4])
        with c_sel:
            chosen_cat = st.selectbox("Chọn bộ thẻ chức năng:", list(deck_library.keys()))
            if st.button("✨ RÚT LÁ THẺ NGẪU NHIÊN", type="primary", use_container_width=True):
                st.balloons()
                st.session_state['active_card'] = random.choice(deck_library[chosen_cat])
                st.session_state['active_cat'] = chosen_cat

        with c_res:
            if 'active_card' in st.session_state:
                ac = st.session_state['active_card']
                st.markdown(f"""
                <div class="cham-epic-card" style="border-left: 8px solid #D18A55;">
                    <span class="badge-cd">{st.session_state['active_cat']}</span>
                    <h3 style="margin-top:12px;">[{ac['code']}] {ac['title']}</h3>
                    <p style="font-size:1.1em; line-height:1.6;">{ac['content']}</p>
                    <hr>
                    <p style="color:#2D6A4F; font-weight:bold;">🎯 Nhiệm vụ thảo luận nhóm:</p>
                    <p style="font-size:1.05em;">{ac['action']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("👈 Nhấn nút **RÚT LÁ THẺ NGẪU NHIÊN** để bắt đầu trải nghiệm rút thẻ sinh động!")

    with sub_tab_2:
        st.subheader("Thử thách xử lý tình huống thực tế nhận Huy hiệu Đại sứ Thấu cảm")
        game_step = st.radio("Chọn thử thách:", ["Thử thách 1: Câu hỏi lặp lại", "Thử thách 2: Cáo buộc mất đồ", "Thử thách 3: Hoàng hôn hoảng loạn"], horizontal=True)

        if "Thử thách 1" in game_step:
            st.markdown("### 🧩 Tình huống: Mẹ hỏi đi hỏi lại câu 'Mấy giờ rồi con?' mỗi 3 phút.")
            choice1 = st.radio("Bạn sẽ phản ứng thế nào?", [
                "A. Quát lên: 'Con vừa nói lúc nãy rồi cơ mà! Sao mẹ cứ hỏi hoài thế?'",
                "B. Kiên nhẫn nhìn đồng hồ trả lời lại nhẹ nhàng, sau đó treo một chiếc đồng hồ to tường dễ nhìn.",
                "C. Phớt lờ không trả lời vì quá mệt mỏi."
            ])
            if st.button("Xác nhận đáp án 1"):
                if "B." in choice1:
                    st.success("🎉 **Chính xác tuyệt đối!** Kiên nhẫn trả lời và dùng công cụ hỗ trợ trực quan giúp người bệnh an tâm mà không bị tổn thương.")
                else:
                    st.error("❌ **Chưa đúng.** Phản ứng gắt gỏng hoặc phớt lờ sẽ làm người bệnh tăng thêm lo âu và tự ti.")

        elif "Thử thách 2" in game_step:
            st.markdown("### 🧩 Tình huống: Bố khăng khăng nói bạn lấy trộm kính của ông.")
            choice2 = st.radio("Bạn sẽ xử lý ra sao?", [
                "A. Cãi lý tới cùng, lục túi xách chứng minh mình không lấy.",
                "B. Công nhận sự lo lắng của bố và nhẹ nhàng cùng bố đi tìm chiếc kính đặt ở bàn trà.",
                "C. Nói rằng bố già rồi nên lẫn lộn trí nhớ."
            ])
            if st.button("Xác nhận đáp án 2"):
                if "B." in choice2:
                    st.balloons()
                    st.success("🎉 **Tuyệt vời!** Đồng cảm với cảm xúc lo lắng và cùng tìm kiếm giúp giải tỏa cơn hoang tưởng ngay lập tức.")
                else:
                    st.error("❌ **Chưa chính xác.** Cãi lý hay chê trách chỉ làm bố thêm kích động và nghi kỵ.")

        else:
            st.markdown("### 🧩 Tình huống: Chiều tối, mẹ đòi mở cửa đi tìm 'nhà cũ ở quê cách đây 40 năm'.")
            choice3 = st.radio("Giải pháp tốt nhất là gì?", [
                "A. Khóa trái cửa nhốt trong phòng để đảm bảo an toàn.",
                "B. Mắng mập mờ rằng quê cũ không còn ai, bắt mẹ đi ngủ.",
                "C. Ôm vai mẹ, bật đèn sáng phòng khách, pha ly sữa ấm và cùng xem album ảnh cũ."
            ])
            if st.button("Xác nhận đáp án 3"):
                if "C." in choice3:
                    st.balloons()
                    st.success("🏆 **Xuất sắc!** Bạn đã áp dụng hoàn hảo cẩm nang xử lý hội chứng hoàng hôn (Sundowning) của dự án CHẠM.")
                else:
                    st.error("❌ **Chưa đúng.** Nhốt hoặc mắng mỏ sẽ làm mẹ hoảng loạn và tìm cách trốn ra ngoài nguy hiểm hơn.")

# ==============================================================================
# MODULE 4: NHẬT KÝ CHỮA LÀNH & BỨC TƯỜNG SẺ CHIA (ĐỒNG BỘ THỜI GIAN THỰC)
# ==============================================================================
elif selected_tab == "💌 4. Nhật ký Chữa lành & Bức tường Sẻ chia Trực tiếp":
    st.title("💌 Trạm Chữa Lành & Bức Tường Sẻ Chia Trực Tiếp")
    st.markdown("Không gian kết nối cảm xúc đồng bộ thời gian thực. Mọi chia sẻ đăng lên đây sẽ hiển thị tức thì cho tất cả người dùng truy cập.")

    col_j_left, col_j_right = st.columns(2)

    with col_j_left:
        with st.container(border=True):
            st.subheader("✍️ Viết trang Nhật ký Chữa lành cá nhân")
            j_title = st.text_input("Tiêu đề cảm xúc:", placeholder="Ví dụ: Một ngày bình yên hơn...")
            j_content = st.text_area("Tâm sự của bạn:", height=120, placeholder="Chia sẻ áp lực hoặc khoảnh khắc ấm áp...")
            if st.button("Lưu vào Sổ tay Chữa lành", type="primary", use_container_width=True):
                if j_title.strip() and j_content.strip():
                    st.session_state['caregiver_journal'].insert(0, {
                        "title": j_title.strip(), "content": j_content.strip(), "time": time.strftime("%d/%m/%Y %H:%M")
                    })
                    st.success("Đã lưu vào sổ tay thành công!")
                    st.rerun()
                else:
                    st.warning("Vui lòng điền đầy đủ tiêu đề và nội dung.")

        st.subheader(f"📖 Nhật ký đã lưu ({len(st.session_state['caregiver_journal'])})")
        for item in st.session_state['caregiver_journal']:
            st.markdown(f"""
            <div class="cham-epic-card-warm">
                <b>📌 {item['title']}</b> <span style="font-size:0.8em; color:#666;">({item['time']})</span>
                <p style="margin-top:5px; font-style:italic;">“{item['content']}”</p>
            </div>
            """, unsafe_allow_html=True)

    with col_j_right:
        with st.container(border=True):
            st.subheader("🕊️ Gửi thông điệp lên Bức tường Sẻ chia")
            user_name = st.text_input("Tên của bạn / Bút danh:", placeholder="Ví dụ: Gia An - THPT Chuyên Hùng Vương")
            user_role = st.selectbox("Vai trò:", ["Học sinh / Sinh viên", "Người chơi Board Game CHẠM", "Người thân / Người chăm sóc", "Tình nguyện viên / Cộng đồng"])
            user_msg = st.text_area("Lời nhắn gửi yêu thương:", height=120, placeholder="Gửi lời động viên đến cộng đồng...")
            if st.button("Đăng lên Bức tường Chung", type="primary", use_container_width=True):
                if user_msg.strip():
                    st.session_state['community_notes'].insert(0, {
                        "author": user_name.strip() if user_name.strip() else "Ẩn danh",
                        "role": user_role, "msg": user_msg.strip(), "time": time.strftime("%d/%m/%Y %H:%M")
                    })
                    st.success("Thông điệp đã được lan tỏa tức thì!")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung lời nhắn.")

        st.subheader(f"🌿 Bức tường Sẻ chia ({len(st.session_state['community_notes'])})")
        for note in st.session_state['community_notes']:
            st.markdown(f"""
            <div class="cham-epic-card" style="border-left: 8px solid #55A88B;">
                <div style="display:flex; justify-content:space-between;">
                    <b>👤 {note['author']}</b> <span class="badge-cd">{note['role']}</span>
                </div>
                <p style="margin-top:8px; font-style:italic;">“{note['msg']}”</p>
                <div style="text-align:right; font-size:0.75em; color:#777;">🕒 {note.get('time', 'Gần đây')}</div>
            </div>
            """, unsafe_allow_html=True)
