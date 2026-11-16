import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import os

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN CHỦ ĐẠO (CHẠM DESIGN SYSTEM - ULTIMATE)
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
        background: #FFFFFF; padding: 26px; border-radius: 16px;
        border-left: 8px solid #55A88B; box-shadow: 0 10px 25px rgba(24, 50, 74, 0.07);
        margin-bottom: 20px; transition: transform 0.3s ease;
    }
    .cham-epic-card:hover { transform: translateY(-3px); }
    
    .cham-epic-card-warm {
        background: linear-gradient(135deg, #FFFDF9 0%, #FFF5EC 100%);
        padding: 26px; border-radius: 16px; border-left: 8px solid #D18A55;
        box-shadow: 0 10px 25px rgba(209, 138, 85, 0.09); margin-bottom: 20px;
    }
    .cham-epic-card-tech {
        background: linear-gradient(135deg, #F5F3FB 0%, #EFEBF9 100%);
        padding: 26px; border-radius: 16px; border-left: 8px solid #7867B5;
        box-shadow: 0 10px 25px rgba(120, 103, 181, 0.09); margin-bottom: 20px;
    }
    .cham-quote-box {
        background: linear-gradient(135deg, #E0F0E8 0%, #D2EBE0 100%);
        color: #18324A; padding: 24px 30px; border-radius: 14px;
        font-style: italic; font-size: 1.1em; border-left: 6px solid #2D6A4F;
        box-shadow: 0 4px 15px rgba(45, 106, 79, 0.08); margin: 18px 0;
    }
    .badge-nc { background-color: #DCEAF5; color: #18324A; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 0.82em; }
    .badge-cs { background-color: #E0F0E8; color: #2D6A4F; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 0.82em; }
    .badge-cd { background-color: #FCE8D5; color: #9C5221; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 0.82em; }
    .badge-cn { background-color: #E8E2F4; color: #5B4E8C; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 0.82em; }
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
            .epic-icon { font-size: 110px; animation: epicFloat 2s ease-out forwards; }
            .epic-title { font-size: 48px; font-weight: 900; letter-spacing: 6px; margin-top: 15px; }
            .epic-sub { font-size: 20px; color: #F2C66D; margin-top: 10px; font-weight: 600; }
            </style>
            <div class="epic-splash">
                <div class="epic-icon">🪷 🤝</div>
                <div class="epic-title">DỰ ÁN CHẠM</div>
                <div class="epic-sub">THẤU HIỂU ĐỂ KẾT NỐI – KẾT NỐI ĐỂ SẺ CHIA</div>
                <p style="margin-top: 25px; opacity: 0.9; font-size: 16px; font-style: italic;">"Không ai phải đi một mình trên hành trình đối diện với Alzheimer"</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    intro_placeholder.empty()
    st.session_state['visited'] = True

# Bức tường sẻ chia và nhật ký chung cập nhật thời gian thực
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
# 3. HEADER & THANH MENU NGANG CHÍNH (MAIN NAVIGATION)
# ==============================================================================
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    if os.path.exists("AlkaLotus/logo.png"):
        st.image("AlkaLotus/logo.png", width=100)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='text-align:center;'>🪷</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#18324A; font-weight:800;'>CHẠM HUB — TRẠM TRI THỨC & KẾT NỐI CỘNG ĐỒNG</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2D6A4F; font-weight:600; font-size:1.05em; margin-top:2px;'>Thấu hiểu để kết nối – Kết nối để sẻ chia • Nền tảng số tích hợp toàn diện cùng Board Game CHẠM</p>", unsafe_allow_html=True)

st.divider()

# Thanh menu ngang chính tối ưu trải nghiệm (Đã gộp module 1 & 2 cũ thành 1-2 hợp lý)
selected_tab = st.selectbox(
    "📌 CHỌN KHÔNG GIAN KHÁM PHÁ:",
    [
        "🏠 1. Tổng quan Dự án & Tầm nhìn",
        "🔬 2. Khoa học Thần kinh, Bệnh lý & Dược liệu",
        "👁️ 3. Trải nghiệm Góc nhìn & Mô phỏng Đồng cảm",
        "💬 4. Cẩm nang Giao tiếp & Chăm sóc Chi tiết",
        "🎲 5. Trạm Rút Thẻ Tương tác CHẠM (132 Thẻ)",
        "🧠 6. Mini-game Thử thách & Phá bỏ Định kiến",
        "📝 7. Nhật ký Người chăm sóc & Trạm Chữa lành",
        "📚 8. Thư viện Tài nguyên Kiến thức Trực tuyến",
        "💌 9. Bức tường Sẻ chia & Cập nhật Trực tiếp"
    ],
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: TỔNG QUAN DỰ ÁN & TẦM NHÌN (CÓ NGUỒN XÁC THỰC)
# ==============================================================================
if selected_tab == "🏠 1. Tổng quan Dự án & Tầm nhìn":
    st.title("🪷 CHẠM — Hành Trình Đánh Thức Sự Thấu Cảm")
    st.markdown("#### *“Alzheimer có thể lấy đi những ký ức trong tâm trí, nhưng không bao giờ có thể lấy đi nhu cầu được yêu thương và tôn trọng của một con người.”*")
    
    st.markdown("""
    <div class="cham-quote-box">
        Dự án <b>CHẠM</b> là hệ sinh thái giáo dục và xã hội kết hợp giữa <b>Board Game chiến lược thực tế (64 ô hành trình)</b> và 
        <b>Nền tảng số trực tuyến</b>. Dự án quy tụ 4 trụ cột liên ngành: <b>Nghiên cứu – Công nghệ – Chăm sóc – Cộng đồng</b> 
        nhằm xóa bỏ mọi định kiến, lan tỏa tri thức khoa học và đồng hành bền vững cùng người mắc bệnh Alzheimer.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Bức tranh toàn cảnh & Thống kê Y tế Xác thực")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Người mắc toàn cầu", "55+ Triệu", "Nguồn: WHO (2023)")
    c2.metric("Tỷ lệ do Alzheimer", "60% – 70%", "Nguồn: Alzheimer's Association")
    c3.metric("Tại Việt Nam (Ước tính)", "~500.000+", "Nguồn: Bộ Y tế / Chuyên gia lão khoa")
    c4.metric("Người chịu ảnh hưởng", "150+ Triệu", "Gia đình & Người chăm sóc trực tiếp")

    col_chart, col_info = st.columns([1.3, 1])
    with col_chart:
        st.markdown("##### 📈 Dự báo xu hướng gia tăng số ca mắc sa sút trí tuệ toàn cầu (Nguồn: WHO)")
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
        fig.update_layout(showlegend=False, height=350, margin=dict(t=20, b=20, l=20, r=20), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("##### 🎯 Triết lý thiết kế 'Phygital' độc tôn")
        st.markdown("""
        <div class="cham-epic-card">
            <b>1. Trải nghiệm kết hợp (Phygital):</b><br>
            Kết hợp Board Game vật lý (tương tác trực tiếp tại bàn chơi) và Web Hub số hóa (mở rộng tri thức, tra cứu tình huống).<br><br>
            <b>2. Phi-đối kháng (Non-Antagonistic):</b><br>
            Không xem bệnh tật là kẻ thù tiêu diệt, mà hướng tới sự thấu hiểu, kiên nhẫn và sẻ chia gánh nặng.<br><br>
            <b>3. Khẩu hiệu hành động:</b><br>
            <i>Thấu hiểu để kết nối – Không ai phải đi một mình!</i>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏛️ Chi tiết 4 Trụ cột chiến lược trong hệ sinh thái CHẠM")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        <div class="cham-epic-card">
            <span class="badge-nc">NGHIÊN CỨU</span>
            <h4 style="margin-top:12px;">Khoa học & Dược liệu</h4>
            <p style="font-size:0.9em; line-height:1.5;">Khám phá cơ chế sinh học phân tử, vai trò enzyme AChE, BACE1 và tiềm năng dược liệu tự nhiên (như Alkaloid lá sen).</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="cham-epic-card-tech">
            <span class="badge-cn">CÔNG NGHỆ</span>
            <h4 style="margin-top:12px;">Giải pháp số vì người bệnh</h4>
            <p style="font-size:0.9em; line-height:1.5;">Ứng dụng AI sàng lọc sớm, thiết bị định vị an toàn, công cụ nhắc nhở sinh hoạt và mô phỏng tin sinh học trực quan.</p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="cham-epic-card-warm">
            <span class="badge-cs">CHĂM SÓC</span>
            <h4 style="margin-top:12px;">Không gian thấu hiểu</h4>
            <p style="font-size:0.9em; line-height:1.5;">Xây dựng mô hình chăm sóc toàn diện tại nhà, bảo vệ phẩm giá người bệnh và xoa dịu áp lực cho người chăm sóc chính.</p>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="cham-epic-card">
            <span class="badge-cd">CỘNG ĐỒNG</span>
            <h4 style="margin-top:12px;">Lan tỏa & Mạng lưới</h4>
            <p style="font-size:0.9em; line-height:1.5;">Tổ chức chiến dịch giáo dục cộng đồng, xóa bỏ định kiến xã hội và kết nối nguồn lực để đồng hành bền vững.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 2: KHOA HỌC THẦN KINH, BỆNH LÝ & DƯỢC LIỆU (ĐÃ GỘP & NÂNG CẤP HOÀNH TRÁNG)
# ==============================================================================
elif selected_tab == "🔬 2. Khoa học Thần kinh, Bệnh lý & Dược liệu":
    st.title("🔬 Khoa Học Thần Kinh, Cơ Chế Bệnh Lý & Hướng Đi Dược Liệu")
    st.markdown("Chuyên đề khoa học tích hợp sâu về sinh học phân tử bệnh Alzheimer, cơ chế enzyme và tiềm năng ứng dụng dược liệu tự nhiên theo tài liệu kiểm chứng.")

    tab_m2_1, tab_m2_2, tab_m2_3 = st.tabs([
        "🧬 Cơ chế phân tử (Amyloid & Tau)", 
        "📉 Hệ thống dẫn truyền thần kinh & Enzyme", 
        "🌿 Tiềm năng chiết xuất Alkaloid lá sen"
    ])

    with tab_m2_1:
        st.subheader("Cơ chế phân tử hình thành tổn thương tế bào não (Nguồn: National Institute on Aging)")
        col_m2_a, col_m2_b = st.columns(2)
        with col_m2_a:
            st.markdown("""
            <div class="cham-epic-card">
                <h4>1. Mảng bám Amyloid-beta (Aβ Plaques)</h4>
                <p style="line-height:1.6;">Protein tiền thân amyloid (APP) bị cắt xẻ bất thường bởi các enzyme (đặc biệt là <b>BACE1</b>), tạo ra các mảnh peptide dính kết thành mảng bám tích tụ ngoài tế bào thần kinh. Các mảng này gây độc thần kinh, cản trở synap và kích hoạt phản ứng viêm mãn tính.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2_b:
            st.markdown("""
            <div class="cham-epic-card">
                <h4>2. Đám rối sợi thần kinh Tau (Tau Tangles)</h4>
                <p style="line-height:1.6;">Bên trong tế bào, protein Tau có nhiệm vụ ổn định 'đường ray' vận chuyển dưỡng chất. Trong bệnh Alzheimer, Tau bị phosphoryl hóa quá mức, tự tách rời và cuộn xoắn lại thành đám rối, làm sập hệ thống giao thông nội bào khiến tế bào chết theo chương trình.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_m2_2:
        st.subheader("Sự suy giảm Acetylcholine và vai trò của Enzyme Acetylcholinesterase (AChE)")
        st.write("Acetylcholine là chất dẫn truyền thần kinh chủ chốt chi phối trí nhớ và nhận thức học tập.")
        st.markdown("""
        <div class="cham-epic-card-warm">
            <b>Cơ chế suy giảm nhận thức:</b><br>
            • Tại não bộ người bệnh Alzheimer, các tế bào thần kinh sản xuất Acetylcholine bị tiêu vong dần.<br>
            • Enzyme <b>AChE</b> liên tục thủy phân lượng chất dẫn truyền ít ỏi còn lại, cắt đứt hoàn toàn mạch thông tin ghi nhớ.<br><br>
            <b>Mục tiêu can thiệp dược lý:</b><br>
            Ức chế hoạt tính của AChE và BACE1 là chiến lược kinh điển giúp duy trì nồng độ Acetylcholine, cải thiện tạm thời triệu chứng nhận thức cho bệnh nhân.
        </div>
        """, unsafe_allow_html=True)

    with tab_m2_3:
        st.subheader("Định hướng nghiên cứu Alkaloid lá sen (Nuciferine, Roemerine)")
        st.markdown("""
        <div class="cham-epic-card-tech">
            <b>Tiềm năng từ dược liệu y học cổ truyền Việt Nam:</b><br>
            • Các nghiên cứu mô phỏng phân tử (In Silico Docking) cho thấy nhóm hoạt chất <b>Alkaloid trong lá sen</b> (như Nuciferine, Roemerine, Liensinine) sở hữu năng lượng liên kết tự do Gibbs ($\Delta G$) rất âm khi tương tác với túi liên kết của enzyme AChE và BACE1.<br>
            • Điều này chứng minh tiềm năng phát triển các dòng sản phẩm hỗ trợ từ thiên nhiên với độ an toàn cao và chi phí tối ưu cho cộng đồng.
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 3: TRẢI NGHIỆM GÓC NHÌN & MÔ PHỎNG ĐỒNG CẢM
# ==============================================================================
elif selected_tab == "👁️ 3. Trải nghiệm Góc nhìn & Mô phỏng Đồng cảm":
    st.title("👁️ Đặt Mình Vào Vị Trí Của Nhau")
    st.markdown("Trải nghiệm không gian mô phỏng tâm lý để thấu cảm sâu sắc những khó khăn của người bệnh và gánh nặng của người chăm sóc.")

    tab_patient, tab_caregiver = st.tabs(["🧠 Mô phỏng góc nhìn Người mắc Alzheimer", "❤️ Đánh giá áp lực Người chăm sóc (Caregiver Burnout)"])

    with tab_patient:
        st.subheader("Mô phỏng tương tác: 'Sự dịch chuyển nhận thức theo giai đoạn'")
        stage = st.select_slider(
            "Chọn mức độ tiến triển triệu chứng:",
            options=["Bình thường", "Giai đoạn Sớm (Quên nhẹ & lúng túng)", "Giai đoạn Trung bình (Hoang mang không gian)", "Giai đoạn Muộn (Mất định hướng toàn diện)"]
        )

        col_sim1, col_sim2 = st.columns([1.3, 1])
        with col_sim1:
            with st.container(border=True):
                st.markdown("#### 🏠 Bối cảnh: Phòng khách lúc hoàng hôn")
                if stage == "Bình thường":
                    st.success("**Nhận thức:** Bạn nhận ra con gái đi làm về, nhớ rõ hôm nay thứ Ba và chuẩn bị bữa tối.")
                    st.write("💬 **Cảm xúc:** Bình yên, chủ động, kết nối tốt.")
                elif stage == "Giai đoạn Sớm (Quên nhẹ & lúng túng)":
                    st.info("**Nhận thức:** Bạn muốn hỏi con gái câu hỏi nhưng từ ngữ bỗng biến mất khỏi đầu. Bạn mất 15 giây ngập ngừng.")
                    st.write("💬 **Cảm xúc:** Lo âu nhẹ, tự ti, cố che giấu sự lúng túng.")
                elif stage == "Giai đoạn Trung bình (Hoang mang không gian)":
                    st.warning("**Nhận thức:** Ánh nắng chiều xiên ngang (Sundowning). Căn phòng quen bỗng lạ lẫm như bến xe. Người phụ nữ gọi bạn là 'Mẹ', nhưng trong đầu bạn mới 20 tuổi.")
                    st.write("💬 **Cảm xúc:** Hoảng hốt tột độ, muốn tìm đường 'về nhà thật sự'.")
                else:
                    st.error("**Nhận thức:** Ngôn ngữ và thời gian tan biến. Xung quanh là âm thanh hỗn độn. Điểm bấu víu duy nhất là sự ấm áp từ đôi bàn tay.")
                    st.write("💬 **Cảm xúc:** Nhạy cảm cực độ với thái độ của người đối diện.")

        with col_sim2:
            st.markdown("""
            <div class="cham-epic-card-warm">
                <h4>💡 Góc nhìn nhân văn từ CHẠM:</h4>
                <p>Người bệnh không hề cố tình gây khó dễ. Khi họ nói muốn 'về nhà' dù đang ở nhà, đó là tìm kiếm cảm giác an toàn thời thơ ấu.</p>
                <p><b>Cần nhất:</b> Sự kiên nhẫn và một cái ôm trấn an.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_caregiver:
        st.subheader("Công cụ tự đánh giá: Khảo sát mức độ kiệt sức (Caregiver Stress Index)")
        c_q1 = st.checkbox("1. Thường xuyên bị gián đoạn giấc ngủ, thức dậy nhiều lần trong đêm.")
        c_q2 = st.checkbox("2. Cảm thấy tội lỗi mỗi khi dành thời gian nghỉ ngơi riêng.")
        c_q3 = st.checkbox("3. Dễ cáu gắt, sau đó lại tự dằn vặt vì đã lớn tiếng với người bệnh.")
        c_q4 = st.checkbox("4. Phải thu hẹp các mối quan hệ xã hội vì không có thời gian trống.")

        total_burnout = sum([c_q1, c_q2, c_q3, c_q4])
        if total_burnout == 0:
            st.info("Hãy tích chọn các biểu hiện thực tế.")
        elif total_burnout <= 2:
            st.warning(f"⚠️ **Cảnh báo nhẹ ({total_burnout}/4):** Bạn đang chịu áp lực đáng kể. Hãy chủ động phân chia công việc.")
        else:
            st.error(f"🚨 **Báo động kiệt sức cao ({total_burnout}/4):** Bạn đang gánh vác quá nhiều một mình! Hãy nhớ: *'Không ai phải đi một mình'*.")

# ==============================================================================
# MODULE 4: CẨM NANG GIAO TIẾP & CHĂM SÓC CHI TIẾT (ĐỒ SỘ HƠN)
# ==============================================================================
elif selected_tab == "💬 4. Cẩm nang Giao tiếp & Chăm sóc Chi tiết":
    st.title("💬 Cẩm Nang Giao Tiếp & Ứng Xử Nhân Văn (Đồ Sộ & Chi Tiết)")
    st.markdown("Thư viện hướng dẫn toàn diện các tình huống thực tế giúp gia đình và cộng đồng xử lý khéo léo mọi tình huống chăm sóc.")

    care_category = st.selectbox("📌 Chọn nhóm tình huống cần tra cứu:", [
        "1. Giao tiếp khi bị lặp câu hỏi & Rối loạn ngôn ngữ",
        "2. Xử lý khi người bệnh hoang tưởng & Cáo buộc",
        "3. Ứng phó hiện tượng hoàng hôn (Sundowning) & Đi lạc",
        "4. Hỗ trợ sinh hoạt hằng ngày (Tắm rửa, ăn uống, ngủ nghỉ)"
    ])

    if "1." in care_category:
        st.markdown("""
        <div class="cham-epic-card">
            <h3>🗣️ Nhóm 1: Giao tiếp khi lặp câu hỏi & Quên từ ngữ</h3>
            <p><b>Biểu hiện:</b> Người bệnh hỏi đi hỏi lại một câu 10 lần trong 15 phút hoặc dừng giữa câu vì quên từ.</p>
            <hr>
            <p style="color: #C0392B;"><b>❌ Phản ứng sai lầm:</b> Gắt gỏng, nhắc đi nhắc lại rằng 'Con vừa trả lời rồi cơ mà', tỏ thái độ bực bội.</p>
            <p style="color: #27AE60;"><b>✅ Ứng xử chuẩn CHẠM:</b> Luôn trả lời nhẹ nhàng, ân cần như mới nghe lần đầu. Sử dụng phương pháp chuyển hướng chú ý sang vật dụng hoặc bài hát quen thuộc thay vì tranh cãi trí nhớ.</p>
        </div>
        """, unsafe_allow_html=True)
    elif "2." in care_category:
        st.markdown("""
        <div class="cham-epic-card-warm">
            <h3>🔍 Nhóm 2: Xử lý khi hoang tưởng & Cáo buộc mất đồ</h3>
            <p><b>Biểu hiện:</b> Người bệnh tự cất ví tiền/chìa khóa rồi cáo buộc con cái hoặc người giúp việc lấy trộm.</p>
            <hr>
            <p style="color: #C0392B;"><b>❌ Phản ứng sai lầm:</b> Đôi co, cãi lý chứng minh sự trong sạch của mình, lớn tiếng trách móc.</p>
            <p style="color: #27AE60;"><b>✅ Ứng xử chuẩn CHẠM:</b> Tuyệt đối không cãi lý. Công nhận cảm xúc lo lắng của họ ('Mất đồ chắc bố lo lắm'), sau đó nhẹ nhàng cùng đi tìm ở những chỗ họ hay cất (tủ quần áo, dưới gối).</p>
        </div>
        """, unsafe_allow_html=True)
    elif "3." in care_category:
        st.markdown("""
        <div class="cham-epic-card-tech">
            <h3>🌅 Nhóm 3: Ứng phó hội chứng hoàng hôn & Đi lạc</h3>
            <p><b>Biểu hiện:</b> Khi chiều tối xuống, người bệnh bồn chồn, lo âu, đòi 'về nhà cũ' hoặc tự ý mở cửa ra ngoài.</p>
            <hr>
            <p style="color: #C0392B;"><b>❌ Phản ứng sai lầm:</b> Khóa trái cửa nhốt trong phòng, quát mắng bắt ngồi yên.</p>
            <p style="color: #27AE60;"><b>✅ Ứng xử chuẩn CHẠM:</b> Bật đèn sáng sớm trong nhà để giảm ảo ảnh bóng tối; đóng kín cửa ra vào bằng khóa ẩn; pha một ly sữa ấm và mở bản nhạc xưa để trấn an tinh thần.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="cham-epic-card">
            <h3>🛁 Nhóm 4: Hỗ trợ sinh hoạt hằng ngày (Tắm rửa, Ăn uống)</h3>
            <p><b>Biểu hiện:</b> Kháng cự khi đi tắm do sợ lạnh hoặc không hiểu lý do; chán ăn hoặc quên cách dùng thìa đũa.</p>
            <hr>
            <p style="color: #C0392B;"><b>❌ Phản ứng sai lầm:</b> Dùng vũ lực kéo ép vào phòng tắm hoặc đút ép ăn.</p>
            <p style="color: #27AE60;"><b>✅ Ứng xử chuẩn CHẠM:</b> Biến giờ tắm thành trải nghiệm thư giãn với nước ấm vừa phải, chuẩn bị sẵn khăn bông mềm; chọn các món ăn mềm dễ cầm nắm trực tiếp khi họ quên dùng dụng cụ.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 5: TRẠM RÚT THẺ TƯƠNG TÁC CHẠM (132 THẺ - SINH ĐỘNG HƠN)
# ==============================================================================
elif selected_tab == "🎲 5. Trạm Rút Thẻ Tương tác CHẠM (132 Thẻ)":
    st.title("🎲 Trạm Rút Thẻ Tình Huống CHẠM (Phiên Bản Sống Động)")
    st.markdown("Trợ lý kỹ thuật số đồng hành cùng bàn cờ giấy **CHẠM**. Rút thẻ ngẫu nhiên với hiệu ứng sinh động để kích hoạt thảo luận nhóm!")

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

# ==============================================================================
# MODULE 6: MINI-GAME THỬ THÁCH & PHÁ BỎ ĐỊNH KIẾN (SINH ĐỘNG)
# ==============================================================================
elif selected_tab == "🧠 6. Mini-game Thử thách & Phá bỏ Định kiến":
    st.title("🎮 Mini-game: Thử Thách Xử Lý Tình Huống Thực Tế")
    st.markdown("Hóa thân thành người chăm sóc và giải quyết 3 thử thách tình huống thực tế để nhận huy hiệu **Đại sứ Thấu cảm**.")

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
# MODULE 7: NHẬT KÝ NGƯỜI CHĂM SÓC & TRẠM CHỮA LÀNH (ĐỒNG BỘ THỜI GIAN THỰC)
# ==============================================================================
elif selected_tab == "📝 7. Nhật ký Người chăm sóc & Trạm Chữa lành":
    st.title("📝 Góc Nhật Ký & Trạm Chữa Lành Tâm Hồn")
    st.markdown("Nơi ghi lại những tâm tư, áp lực hoặc khoảnh khắc ấm áp. Dữ liệu được đồng bộ trực tiếp xuyên suốt hệ thống.")

    col_j1, col_j2 = st.columns([1, 1.3])
    with col_j1:
        with st.container(border=True):
            st.subheader("✍️ Viết trang nhật ký mới")
            j_title = st.text_input("Tiêu đề / Cảm xúc chủ đạo:", placeholder="Ví dụ: Một ngày kiên nhẫn hơn...")
            j_content = st.text_area("Chia sẻ suy nghĩ của bạn:", height=130, placeholder="Hôm nay bạn đã trải qua những áp lực hay khoảnh khắc ấm áp nào...")
            if st.button("Lưu vào Sổ tay Chữa lành", type="primary", use_container_width=True):
                if j_title.strip() and j_content.strip():
                    st.session_state['caregiver_journal'].insert(0, {
                        "title": j_title.strip(),
                        "content": j_content.strip(),
                        "time": time.strftime("%d/%m/%Y %H:%M")
                    })
                    st.success("Đã lưu tâm sự của bạn vào sổ tay thành công!")
                    st.rerun()
                else:
                    st.warning("Vui lòng điền đầy đủ tiêu đề và nội dung.")

    with col_j2:
        st.subheader(f"📖 Nhật ký chung ({len(st.session_state['caregiver_journal'])})")
        for item in st.session_state['caregiver_journal']:
            st.markdown(f"""
            <div class="cham-epic-card-warm">
                <div style="display:flex; justify-content:space-between;">
                    <b>📌 {item['title']}</b>
                    <span style="font-size:0.82em; color:#666;">{item['time']}</span>
                </div>
                <p style="margin-top:8px; font-style:italic;">“{item['content']}”</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 8: THƯ VIỆN TÀI NGUYÊN KIẾN THỨC TRỰC TUYẾN (ĐÃ LOẠN NÚT XUẤT FILE ẢO)
# ==============================================================================
elif selected_tab == "📚 8. Thư viện Tài nguyên Kiến thức Trực tuyến":
    st.title("📚 Thư Viện Tài Nguyên & Nghiên Cứu CHẠM")
    st.markdown("Kho tài liệu kiến thức chuyên sâu trực tuyến phục vụ gia đình, học sinh và cộng đồng.")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        with st.container(border=True):
            st.subheader("📑 Tài liệu Hướng dẫn Chăm sóc (Đọc trực tuyến)")
            st.markdown("""
            • **Cẩm nang gia đình đồng hành cùng Alzheimer** (Tài liệu tổng hợp chuẩn y khoa)<br>
            • **Bộ quy tắc giao tiếp ứng xử trong nhà** (Infographic trực quan)<br>
            • **Hướng dẫn thiết kế không gian an toàn chống ngã cho người cao tuổi**
            """)
            st.info("💡 Bạn có thể tra cứu trực tiếp các nội dung này tại mục Cẩm nang (Module 4).")

    with col_r2:
        with st.container(border=True):
            st.subheader("🔬 Tài liệu Khoa học & Dự án CHẠM")
            st.markdown("""
            • **Báo cáo kỹ thuật chi tiết Board Game CHẠM (64 ô tiêu chuẩn)**<br>
            • **Tài liệu nghiên cứu định hướng dược liệu tự nhiên & Tin sinh học**<br>
            • **Slide Pitch Deck thuyết trình dự án khởi nghiệp xã hội**
            """)
            st.success("🌟 Tất cả thông số kỹ thuật và bản vẽ bàn cờ đã được tích hợp trực tiếp trong các vòng chơi và phần giới thiệu.")

# ==============================================================================
# MODULE 9: BỨC TƯỜNG SẺ CHIA (CẬP NHẬT TRỰC TIẾP THỜI GIAN THỰC CHO MỌI NGƯỜI)
# ==============================================================================
elif selected_tab == "💌 9. Bức tường Sẻ chia & Cập nhật Trực tiếp":
    st.title("💌 Bức Tường Sẻ Chia — Không Ai Phải Đi Một Mình")
    st.markdown("Nơi gắn kết mọi trái tim yêu thương. Bất kỳ thông điệp nào được gửi lên đây sẽ được **cập nhật tức thì** để bạn bè hay bất kỳ ai truy cập đều nhìn thấy.")

    col_form, col_wall = st.columns([1, 1.4])

    with col_form:
        with st.container(border=True):
            st.subheader("✍️ Gửi thông điệp yêu thương")
            user_name = st.text_input("Tên của bạn (hoặc bút danh):", placeholder="Ví dụ: Gia An - THPT Chuyên Hùng Vương")
            user_role = st.selectbox("Vai trò của bạn:", [
                "Học sinh / Sinh viên tìm hiểu dự án",
                "Người chơi Board Game CHẠM",
                "Người thân / Người chăm sóc gia đình",
                "Tình nguyện viên / Cộng đồng"
            ])
            user_msg = st.text_area("Lời nhắn gửi của bạn:", height=130, placeholder="Chia sẻ suy nghĩ hoặc lời động viên chân thành...")
            
            if st.button("🕊️ Đăng lên Bức tường Sẻ chia", type="primary", use_container_width=True):
                if user_msg.strip():
                    st.session_state['community_notes'].insert(0, {
                        "author": user_name.strip() if user_name.strip() else "Người bạn ẩn danh",
                        "role": user_role,
                        "msg": user_msg.strip(),
                        "time": time.strftime("%d/%m/%Y %H:%M")
                    })
                    st.success("Thông điệp đã được đưa lên bức tường chung thành công!")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung lời nhắn trước khi gửi.")

    with col_wall:
        st.subheader(f"🌿 Những lời nhắn từ cộng đồng ({len(st.session_state['community_notes'])})")
        for note in st.session_state['community_notes']:
            time_str = note.get('time', 'Gần đây')
            st.markdown(f"""
            <div class="cham-epic-card-warm">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#18324A; font-size:1.05em;">👤 {note['author']}</b>
                    <span class="badge-cd">{note['role']}</span>
                </div>
                <p style="margin-top:10px; color:#333; font-style:italic;">“{note['msg']}”</p>
                <div style="text-align:right; font-size:0.78em; color:#777; margin-top:5px;">🕒 {time_str}</div>
            </div>
            """, unsafe_allow_html=True)
