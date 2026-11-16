import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import os

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN CHỦ ĐẠO (CHẠM DESIGN SYSTEM)
# ==============================================================================
st.set_page_config(
    page_title="CHẠM Hub | Thấu hiểu để kết nối – Không ai phải đi một mình",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="collapsed" # Ẩn sidebar mặc định để tập trung toàn bộ không gian cho menu ngang
)

# Custom CSS tinh chỉnh giao diện menu ngang, thẻ card và màu sắc chuẩn CHẠM
st.markdown("""
<style>
    .main {
        background-color: #FAF9F6;
    }
    h1, h2, h3 {
        color: #18324A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .cham-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #55A88B;
        box-shadow: 0 4px 12px rgba(24, 50, 74, 0.06);
        margin-bottom: 20px;
    }
    .cham-card-warm {
        background-color: #FFFDF9;
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #D18A55;
        box-shadow: 0 4px 12px rgba(209, 138, 85, 0.08);
        margin-bottom: 20px;
    }
    .cham-quote {
        background-color: #E0F0E8;
        color: #18324A;
        padding: 20px 26px;
        border-radius: 12px;
        font-style: italic;
        font-size: 1.08em;
        border: 1px solid #55A88B;
        margin: 18px 0;
    }
    .badge-nc { background-color: #DCEAF5; color: #18324A; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em; }
    .badge-cs { background-color: #E0F0E8; color: #2D6A4F; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em; }
    .badge-cd { background-color: #FCE8D5; color: #9C5221; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em; }
    .badge-cn { background-color: #E8E2F4; color: #5B4E8C; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em; }
    
    /* Tinh chỉnh thanh chọn radio thành dạng tab ngang hiện đại */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MÀN HÌNH CHÀO MỪNG (INTRO SPLASH SCREEN)
# ==============================================================================
if 'visited' not in st.session_state:
    intro_placeholder = st.empty()
    with intro_placeholder.container():
        st.markdown("""
            <style>
            @keyframes floatUp {
                0% { transform: translateY(40px) scale(0.9); opacity: 0; }
                50% { opacity: 1; }
                100% { transform: translateY(-20px) scale(1.05); opacity: 1; }
            }
            .splash-screen {
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(135deg, #18324A 0%, #2C5E8A 50%, #55A88B 100%);
                z-index: 9999;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                text-align: center;
                padding: 20px;
            }
            .splash-icon { font-size: 110px; animation: floatUp 2.5s ease-out forwards; }
            .splash-title { font-size: 46px; font-weight: 800; letter-spacing: 6px; margin-top: 15px; }
            .splash-sub { font-size: 21px; color: #F2C66D; margin-top: 10px; font-weight: 500; }
            </style>
            <div class="splash-screen">
                <div class="splash-icon">🪷 🤝</div>
                <div class="splash-title">DỰ ÁN CHẠM</div>
                <div class="splash-sub">THẤU HIỂU ĐỂ KẾT NỐI – KẾT NỐI ĐỂ SẺ CHIA</div>
                <p style="margin-top: 25px; opacity: 0.85; font-size: 16px;">"Không ai phải đi một mình trên hành trình đối diện với Alzheimer"</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    intro_placeholder.empty()
    st.session_state['visited'] = True

# Khởi tạo kho lưu trữ dữ liệu trong session_state
if 'community_notes' not in st.session_state:
    st.session_state['community_notes'] = [
        {"author": "Minh Thư (Học sinh lớp 11)", "role": "Người chơi trải nghiệm CHẠM", "msg": "Trước đây mình hay gắt gỏng mỗi khi bà hỏi đi hỏi lại một câu. Sau khi chơi bàn cờ CHẠM và đọc phần trải nghiệm góc nhìn, mình mới hiểu bà không cố tình làm phiền mà vì ký ức của bà đang rơi rụng từng ngày."},
        {"author": "Cô Thanh Hương", "role": "Người chăm sóc gia đình", "msg": "Cảm ơn dự án đã nói lên tiếng lòng của những người chăm sóc. Đôi khi chúng tôi không cần lời khuyên y khoa cao siêu, chỉ cần một câu hỏi thăm: 'Hôm nay bạn có mệt không?' là đủ ấm lòng."},
        {"author": "Hoàng Nam", "role": "Tình nguyện viên cộng đồng", "msg": "Thông điệp 'Không ai phải đi một mình' thực sự chạm đến trái tim. Mong bộ board game này sẽ sớm có mặt tại các trường học và nhà văn hóa."}
    ]

if 'caregiver_journal' not in st.session_state:
    st.session_state['caregiver_journal'] = []

# ==============================================================================
# 3. HEADER & THANH MENU NGANG TRỰC TIẾP TRÊN MAIN MENU
# ==============================================================================
col_logo, col_title = st.columns([0.15, 0.85])
with col_logo:
    if os.path.exists("AlkaLotus/logo.png"):
        st.image("AlkaLotus/logo.png", width=100)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1>🪷</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#18324A;'>CHẠM Hub — Không Gian Tri Thức & Kết Nối</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#55A88B; font-weight:600; margin-top:0;'>Thấu hiểu để kết nối – Kết nối để sẻ chia • Nền tảng số bổ trợ Board Game CHẠM</p>", unsafe_allow_html=True)

st.divider()

# Thanh menu ngang chính hiển thị ngay trên màn hình (Main Menu Navigation)
selected_tab = st.selectbox(
    "📌 LỰA CHỌN KHÔNG GIAN TRẢI NGHIỆM:",
    [
        "🏠 1. Trang chủ & Tổng quan Dự án",
        "🔬 2. Khoa học Thần kinh & Bản chất Bệnh lý",
        "👁️ 3. Trải nghiệm Góc nhìn & Mô phỏng Đồng cảm",
        "💬 4. Cẩm nang Giao tiếp & Chăm sóc Nhân văn",
        "🎲 5. Trạm Tương tác Thẻ bài CHẠM (132 Thẻ)",
        "🧠 6. Thử thách Phá bỏ Định kiến (Quiz)",
        "📝 7. Nhật ký Người chăm sóc & Sức khỏe Tinh thần",
        "📚 8. Tài nguyên Nghiên cứu & Thư viện",
        "💌 9. Bức tường Sẻ chia Cộng đồng"
    ],
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: TRANG CHỦ & TỔNG QUAN DỰ ÁN
# ==============================================================================
if selected_tab == "🏠 1. Trang chủ & Tổng quan Dự án":
    st.title("🪷 CHẠM — Hành Trình Đánh Thức Sự Thấu Cảm")
    st.markdown("#### *“Alzheimer có thể lấy đi những ký ức trong tâm trí, nhưng không bao giờ có thể lấy đi nhu cầu được yêu thương và tôn trọng của một con người.”*")
    
    st.markdown("""
    <div class="cham-quote">
        Dự án <b>CHẠM</b> kết hợp hoàn hảo giữa <b>Board Game giáo dục thực tế (64 ô hành trình chiến lược)</b> và 
        <b>Nền tảng số trực tuyến</b>, quy tụ 4 trụ cột liên ngành: <b>Nghiên cứu – Công nghệ – Chăm sóc – Cộng đồng</b> 
        nhằm xóa bỏ sự kỳ thị, lan tỏa tri thức và đồng hành cùng người mắc bệnh Alzheimer và gia đình họ.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Bức tranh toàn cảnh: Sa sút trí tuệ & Thách thức toàn cầu")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Người mắc toàn cầu", "55+ Triệu", "Tăng 10 triệu ca mới/năm")
    c2.metric("Tỷ lệ do Alzheimer", "60% – 70%", "Nguyên nhân hàng đầu")
    c3.metric("Tại Việt Nam (Ước tính)", "~500.000+", "Gia tăng mạnh theo già hóa dân số")
    c4.metric("Người chịu ảnh hưởng", "150+ Triệu", "Gia đình và người chăm sóc")

    col_chart, col_info = st.columns([1.3, 1])
    with col_chart:
        st.markdown("##### 📈 Dự báo xu hướng gia tăng số ca mắc toàn cầu (Triệu người)")
        df_trend = pd.DataFrame({
            "Năm": ["2020", "2030 (Dự báo)", "2050 (Dự báo)"],
            "Số lượng (Triệu người)": [55, 78, 139]
        })
        fig = px.bar(
            df_trend, x="Năm", y="Số lượng (Triệu người)",
            text="Số lượng (Triệu người)",
            color="Năm",
            color_discrete_sequence=["#3979B9", "#55A88B", "#D18A55"]
        )
        fig.update_traces(textposition="outside", textfont_size=14)
        fig.update_layout(showlegend=False, height=340, margin=dict(t=20, b=20, l=20, r=20), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("##### 🎯 Sứ mệnh cốt lõi của CHẠM")
        st.markdown("""
        <div class="cham-card">
            <b>1. Chuyển dịch góc nhìn:</b><br>
            Không xem bệnh tật là kẻ thù để tiêu diệt hay kỳ thị người bệnh, mà hướng tới sự thấu hiểu, kiên nhẫn và sẻ chia gánh nặng.<br><br>
            <b>2. Mô hình Phygital (Kết hợp Vật lý & Số):</b><br>
            Board game 600x600mm để kết nối trực tiếp tại bàn chơi; Web Hub trực tuyến để mở rộng kiến thức, tra cứu tình huống và kết nối cộng đồng.<br><br>
            <b>3. Khẩu hiệu hành động:</b><br>
            <i>Thấu hiểu để kết nối – Kết nối để sẻ chia. Không ai phải đi một mình!</i>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏛️ Chi tiết 4 Trụ cột chiến lược trong hệ sinh thái CHẠM")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        <div class="cham-card">
            <span class="badge-nc">NGHIÊN CỨU</span>
            <h4 style="margin-top:10px;">Khoa học & Dược liệu</h4>
            <p style="font-size:0.9em;">Khám phá cơ chế sinh học phân tử, vai trò của enzyme AChE, BACE1 và tiềm năng ứng dụng các hoạt chất tự nhiên (như Alkaloid lá sen).</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="cham-card">
            <span class="badge-cn">CÔNG NGHỆ</span>
            <h4 style="margin-top:10px;">Giải pháp số vì con người</h4>
            <p style="font-size:0.9em;">Ứng dụng AI hỗ trợ sàng lọc sớm, thiết bị định vị an toàn, ứng dụng nhắc nhở sinh hoạt và mô phỏng tin sinh học trực quan.</p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="cham-card">
            <span class="badge-cs">CHĂM SÓC</span>
            <h4 style="margin-top:10px;">Không gian thấu hiểu</h4>
            <p style="font-size:0.9em;">Xây dựng mô hình chăm sóc toàn diện tại nhà, bảo vệ phẩm giá người bệnh và xoa dịu áp lực tâm lý cho người chăm sóc chính.</p>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="cham-card">
            <span class="badge-cd">CỘNG ĐỒNG</span>
            <h4 style="margin-top:10px;">Lan tỏa & Mạng lưới</h4>
            <p style="font-size:0.9em;">Tổ chức các chiến dịch giáo dục cộng đồng, xóa bỏ định kỳ xã hội và kết nối các nguồn lực xã hội để đồng hành bền vững.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 2: KHOA HỌC THẦN KINH & BẢN CHẤT BỆNH LÝ
# ==============================================================================
elif selected_tab == "🔬 2. Khoa học Thần kinh & Bản chất Bệnh lý":
    st.title("🔬 Khoa Học Thần Kinh Về Bệnh Alzheimer")
    st.markdown("Hiểu rõ cơ chế sinh học bên trong não bộ giúp chúng ta có cái nhìn khoa học, khách quan và thấu cảm hơn với người bệnh.")

    tab_bio1, tab_bio2, tab_bio3 = st.tabs(["🧬 Mảng bám Amyloid & Đám rối Tau", "📉 Sự suy giảm chất dẫn truyền thần kinh", "🌿 Tiềm năng từ Hướng đi Dược liệu tự nhiên"])

    with tab_bio1:
        st.subheader("Cơ chế phân tử hình thành tổn thương não bộ")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("""
            <div class="cham-card">
                <h4>1. Mảng bám Amyloid-beta (Aβ Plaques)</h4>
                <p>Bình thường, protein tiền thân amyloid (APP) được cắt xẻ an toàn. Tuy nhiên, do sự hoạt động bất thường của các enzyme (đặc biệt là <b>BACE1</b>), các đoạn protein bị cắt ngắn tạo thành các mảng dính kết tụ lại bên ngoài tế bào thần kinh, gây cản trở truyền tín hiệu và kích hoạt phản ứng viêm.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b2:
            st.markdown("""
            <div class="cham-card">
                <h4>2. Đám rối sợi thần kinh Tau (Tau Tangles)</h4>
                <p>Bên trong tế bào thần kinh, protein Tau đóng vai trò như các 'thanh ray' giúp vận chuyển chất dinh dưỡng. Ở người bệnh Alzheimer, protein Tau bị biến đổi hóa học (phosphoryl hóa quá mức), cuộn xoắn lại thành các đám rối, làm sập hệ thống giao thông nội bào và khiến tế bào chết đi.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_bio2:
        st.subheader("Sự thiếu hụt Acetylcholine và vai trò của Enzyme AChE")
        st.write("Acetylcholine là chất dẫn truyền thần kinh cực kỳ quan trọng đối với trí nhớ, khả năng học tập và sự tỉnh táo.")
        st.markdown("""
        <div class="cham-card-warm">
            <b>Cơ chế tác động của Enzyme Acetylcholinesterase (AChE):</b><br>
            Ở người mắc Alzheimer, các tế bào sản xuất Acetylcholine bị suy giảm nghiêm trọng. Thêm vào đó, enzyme AChE liên tục phân hủy lượng chất dẫn truyền ít ỏi còn lại, làm gián đoạn hoàn toàn các mạch ghi nhớ.<br><br>
            <b>Hướng tiếp cận y học hiện đại:</b><br>
            Việc tìm kiếm các chất ức chế enzyme AChE và BACE1 giúp duy trì nồng độ Acetylcholine, làm chậm tốc độ tiến triển của triệu chứng suy giảm trí nhớ.
        </div>
        """, unsafe_allow_html=True)

    with tab_bio3:
        st.subheader("Triển vọng nghiên cứu dược liệu tự nhiên (Alkaloid lá sen)")
        st.markdown("""
        Trong các nghiên cứu khoa học gần đây, việc khai thác các hợp chất tự nhiên như nhóm **Alkaloid chiết xuất từ lá sen** (ví dụ: Nuciferine, Roemerine) cho thấy triển vọng tích cực trong việc thể hiện ái lực gắn kết với các đích enzyme gây bệnh ($AChE$ và $BACE1$). 
        Điều này mở ra hướng đi mới trong việc tận dụng nguồn dược liệu y học cổ truyền kết hợp công nghệ tin sinh học hiện đại để phát triển các giải pháp hỗ trợ an toàn, chi phí hợp lý.
        """)

# ==============================================================================
# MODULE 3: TRẢI NGHIỆM GÓC NHÌN & MÔ PHỎNG ĐỒNG CẢM
# ==============================================================================
elif selected_tab == "👁️ 3. Trải nghiệm Góc nhìn & Mô phỏng Đồng cảm":
    st.title("👁️ Đặt Mình Vào Vị Trí Của Nhau")
    st.markdown("Sự đồng cảm thực sự bắt đầu khi chúng ta tạm gác lại góc nhìn chủ quan để thử cảm nhận thế giới qua lăng kính của người bệnh và người chăm sóc.")

    tab_patient, tab_caregiver = st.tabs(["🧠 Mô phỏng góc nhìn Người mắc Alzheimer", "❤️ Đánh giá áp lực Người chăm sóc (Caregiver Burnout)"])

    with tab_patient:
        st.subheader("Mô phỏng tương tác: 'Sự dịch chuyển nhận thức theo giai đoạn'")
        stage = st.select_slider(
            "Chọn mức độ tiến triển của triệu chứng:",
            options=["Bình thường", "Giai đoạn Sớm (Quên nhẹ & lúng túng)", "Giai đoạn Trung bình (Hoang mang không gian)", "Giai đoạn Muộn (Mất định hướng toàn diện)"]
        )

        col_sim1, col_sim2 = st.columns([1.3, 1])
        with col_sim1:
            with st.container(border=True):
                st.markdown("#### 🏠 Bối cảnh: Một buổi chiều tại gia đình")
                if stage == "Bình thường":
                    st.success("**Trạng thái nhận thức:** Bạn nhận ra con gái vừa đi làm về. Bạn nhớ hôm nay là thứ Ba và chuẩn bị bữa tối cùng gia đình.")
                    st.write("💬 **Cảm xúc:** An tâm, chủ động, kết nối tốt với thực tại.")
                elif stage == "Giai đoạn Sớm (Quên nhẹ & lúng túng)":
                    st.info("**Trạng thái nhận thức:** Bạn thấy con gái về, muốn hỏi con một câu hỏi nhưng bỗng từ ngữ trôi tuột đi đâu mất. Bạn mất 15 giây để nhớ ra từ cần nói.")
                    st.write("💬 **Cảm xúc:** Hơi lo âu, tự ti, cố gắng che giấu sự lúng túng vì sợ con cái lo lắng.")
                elif stage == "Giai đoạn Trung bình (Hoang mang không gian)":
                    st.warning("**Trạng thái nhận thức:** Ánh nắng chiều xiên ngang phòng (hiện tượng Sundowning). Căn phòng quen thuộc bỗng trở nên lạ lẫm như một trạm xe buýt xa lạ. Người phụ nữ đứng trước mặt gọi bạn là 'Mẹ', nhưng trong đầu bạn, bạn mới chỉ là cô thiếu nữ 20 tuổi.")
                    st.write("💬 **Cảm xúc:** Bất an tột độ, hoảng hốt, muốn tìm đường 'về nhà thật sự'.")
                else:
                    st.error("**Trạng thái nhận thức:** Ngôn ngữ và khái niệm thời gian không còn ý nghĩa. Mọi thứ xung quanh là âm thanh hỗn độn. Điểm bấu víu duy nhất là sự ấm áp từ bàn tay hoặc giọng nói dịu dàng của người chăm sóc.")
                    st.write("💬 **Cảm xúc:** Nhạy cảm cực độ với năng lượng và thái độ của người đối diện.")

        with col_sim2:
            st.markdown("""
            <div class="cham-card-warm">
                <h4>💡 Góc nhìn nhân văn từ CHẠM:</h4>
                <p>Khi người bệnh nói những câu vô lý hoặc nhầm lẫn, họ <b>không hề cố tình gây khó dễ</b>. Đó là lúc não bộ của họ đang chịu tổn thương sâu sắc.</p>
                <p>Điều họ cần không phải là một cuộc tranh cãi đúng - sai, mà là sự bao dung và một cái ôm trấn an.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_caregiver:
        st.subheader("Công cụ tự đánh giá: Khảo sát mức độ kiệt sức (Caregiver Stress Index)")
        st.write("Hãy tích chọn những biểu hiện bạn hoặc người quen đang gặp phải khi chăm sóc người bệnh:")

        c_q1 = st.checkbox("1. Thường xuyên bị gián đoạn giấc ngủ, thức dậy nhiều lần trong đêm để kiểm tra người thân.")
        c_q2 = st.checkbox("2. Cảm thấy tội lỗi mỗi khi dành một chút thời gian nghỉ ngơi hoặc đi chơi riêng.")
        c_q3 = st.checkbox("3. Dễ bị cáu gắt, sau đó lại tự dằn vặt vì đã lỡ lớn tiếng với người bệnh.")
        c_q4 = st.checkbox("4. Phải thu hẹp các mối quan hệ xã hội vì không có thời gian trống.")

        total_burnout = sum([c_q1, c_q2, c_q3, c_q4])
        if total_burnout == 0:
            st.info("Hãy tích chọn các biểu hiện thực tế để hệ thống đưa ra lời khuyên hỗ trợ.")
        elif total_burnout <= 2:
            st.warning(f"⚠️ **Cảnh báo mức độ nhẹ ({total_burnout}/4):** Bạn đang chịu áp lực đáng kể. Hãy chủ động phân chia công việc chăm sóc với các thành viên khác.")
        else:
            st.error(f"🚨 **Báo động kiệt sức cao ({total_burnout}/4):** Bạn đang gánh vác quá nhiều một mình! Hãy nhớ thông điệp của CHẠM: *'Không ai phải đi một mình'*. Hãy tìm kiếm sự hỗ trợ từ các nhóm chuyên gia hoặc dịch vụ cộng đồng ngay.")

# ==============================================================================
# MODULE 4: CẨM NANG GIAO TIẾP & CHĂM SÓC NHÂN VĂN
# ==============================================================================
elif selected_tab == "💬 4. Cẩm nang Giao tiếp & Chăm sóc Nhân văn":
    st.title("💬 Nghệ Thuật Giao Tiếp Bằng Trái Tim")
    st.markdown("Những nguyên tắc ứng xử thực tế giúp giảm căng thẳng, xoa dịu hoảng loạn và bảo vệ phẩm giá cho người mắc Alzheimer.")

    scenarios = {
        "Tình huống 1: Người bệnh hỏi lặp lại một câu hỏi liên tục mỗi 5 phút": {
            "avoid": "❌ 'Mẹ vừa hỏi câu này 5 lần rồi cơ mà! Sao mẹ cứ quên mãi thế?'",
            "why": "Người bệnh thực sự quên mất mình đã hỏi. Câu trách cứ tạo cảm giác tủi thân và làm họ thêm bất an.",
            "do": "✅ Nhẹ nhàng trả lời lại bằng nụ cười và tông giọng ấm áp như lần đầu, sau đó chuyển hướng chú ý sang một hoạt động khác (như uống nước, nghe nhạc)."
        },
        "Tình huống 2: Người bệnh khăng khăng đòi đi tìm người thân đã qua đời": {
            "avoid": "❌ 'Bố đừng tìm nữa, mẹ mất từ chục năm trước rồi cơ mà!'",
            "why": "Đánh thức sự thật mất mát một cách đột ngột gây ra cú sốc tâm lý đau đớn như thể sự việc vừa mới xảy ra.",
            "do": "✅ Đồng cảm với cảm xúc của họ: 'Bố đang rất nhớ mẹ phải không ạ? Mẹ thương bố nhiều lắm. Bố kể cho con nghe kỷ niệm vui nhất của bố với mẹ đi.'"
        },
        "Tình huống 3: Người bệnh cáo buộc con cái lấy trộm đồ của họ": {
            "avoid": "❌ 'Con không hề lấy! Lúc nào bố cũng đổ oan cho con hết!'",
            "why": "Tranh cãi logic với người đang suy giảm trí nhớ chỉ làm tăng sự nghi kỵ và kích động mạnh hơn.",
            "do": "✅ Công nhận cảm xúc lo lắng của họ và kiên nhẫn cùng đi tìm: 'Mất đồ chắc bố lo lắm nhỉ, để con cùng bố lục lại quanh phòng xem sao nhé!'"
        },
        "Tình huống 4: Người bệnh đi lạc, hoảng loạn khi ở nơi đông người": {
            "avoid": "❌ Ôm giữ chặt từ phía sau hoặc quát lớn hỏi dồn dập thông tin cá nhân.",
            "why": "Hành động bất ngờ từ phía sau kích hoạt phản xạ tự vệ và làm người bệnh hoảng loạn hơn.",
            "do": "✅ Tiến lại từ phía trước trong tầm mắt, mỉm cười thân thiện, hạ thấp tông giọng và trấn an: 'Cháu chào bác, có cháu ở đây rồi, bác cứ thong thả bình tĩnh nhé.'"
        }
    }

    sel_sc = st.selectbox("📌 Chọn tình huống thực tế cần tham khảo cách ứng xử:", list(scenarios.keys()))
    sc_info = scenarios[sel_sc]

    col_bad, col_good = st.columns(2)
    with col_bad:
        st.error("### 🚫 Phản ứng dễ gây tổn thương")
        st.write(sc_info["avoid"])
        st.caption(f"**Vì sao không nên?** {sc_info['why']}")
    with col_good:
        st.success("### 💚 Ứng xử thấu cảm chuẩn CHẠM")
        st.write(sc_info["do"])
        st.caption("**Hiệu quả:** Xoa dịu cảm xúc, bảo vệ lòng tự trọng và duy trì kết nối an toàn.")

# ==============================================================================
# MODULE 5: TRẠM TƯƠNG TÁC THẺ BÀI CHẠM (132 THẺ MỞ RỘNG)
# ==============================================================================
elif selected_tab == "🎲 5. Trạm Tương tác Thẻ bài CHẠM (132 Thẻ)":
    st.title("🎲 Trạm Rút Thẻ Tình Huống CHẠM")
    st.markdown("Trợ lý kỹ thuật số tích hợp song song cùng bàn cờ giấy **CHẠM**. Rút thẻ ngẫu nhiên để nhận câu hỏi thảo luận, thử thách hoặc kiến thức mở rộng.")

    deck_library = {
        "Thẻ Kiến thức (KT) — Lĩnh vực Khoa học & Sự thật": [
            {"code": "KT-01", "title": "Bản chất sa sút trí tuệ", "content": "Sa sút trí tuệ không phải là tên một bệnh lý đơn lẻ, mà là hội chứng bao gồm nhiều bệnh lý suy giảm chức năng não bộ, trong đó Alzheimer chiếm đa số.", "action": "Thảo luận nhóm: Phân biệt rõ sự khác nhau giữa người hay quên tuổi già và bệnh nhân Alzheimer."},
            {"code": "KT-08", "title": "Vai trò của Giấc ngủ đối với não bộ", "content": "Giấc ngủ sâu là thời điểm hệ thống thanh thải glymphatic trong não hoạt động mạnh mẽ nhất để dọn dẹp các mảng protein độc hại tích tụ trong ngày.", "action": "Đề xuất 2 thói quen giúp cải thiện chất lượng giấc ngủ cho người cao tuổi."},
            {"code": "KT-14", "title": "Dinh dưỡng và Sức khỏe não bộ", "content": "Chế độ ăn Địa Trung Hải giàu rau xanh, cá béo, quả mọng và dầu ô liu hỗ trợ bảo vệ tế bào thần kinh và làm chậm quá trình suy giảm nhận thức.", "action": "Kể tên 3 loại thực phẩm tốt cho trí nhớ mà bạn biết."}
        ],
        "Thẻ Góc nhìn (GN) — Thấu cảm & Phẩm giá": [
            {"code": "GN-03", "title": "Sự tự ti thầm lặng", "content": "Nhiều người bệnh ở giai đoạn đầu nhận thức được sự sa sút của mình nhưng cố giấu giếm vì sợ trở thành gánh nặng cho con cháu.", "action": "Làm thế nào để con cái nhận biết được sự bất an giấu kín này?"},
            {"code": "GN-11", "title": "Không gian sinh hoạt quen thuộc", "content": "Việc chuyển người bệnh đến một môi trường hoàn toàn mới (như nhà mới xây hoặc viện dưỡng lão) có thể gây ra cú sốc tâm lý mạnh làm bệnh nặng hơn.", "action": "Thảo luận cách giữ lại những dấu ấn quen thuộc trong không gian sống."}
        ],
        "Thẻ Thử thách (TC) — Xử lý tình huống thực tế": [
            {"code": "TC-04", "title": "Từ chối tắm rửa và vệ sinh", "content": "Người bệnh kiên quyết từ chối đi tắm vì cảm thấy lạnh, sợ nước hoặc không hiểu lý do vì sao cần phải tắm.", "action": "Đưa ra giải pháp nhẹ nhàng để thuyết phục người bệnh mà không dùng vũ lực hay ép buộc."},
            {"code": "TC-07", "title": "Đi lang thang và mất định hướng", "content": "Người bệnh tự ý mở cửa ra ngoài vào buổi trưa và đi lạc đến một khu chợ cách nhà 2km không nhớ đường về.", "action": "Xây dựng quy trình phối hợp khẩn cấp giữa gia đình và mạng lưới cộng đồng."}
        ],
        "Thẻ Hợp tác (HT) — Sức mạnh cộng đồng": [
            {"code": "HT-02", "title": "Mạng lưới 'Hàng xóm Tươi cười'", "content": "Xây dựng liên kết giữa các hộ gia đình trong khu dân cư để cùng hỗ trợ quan sát, giúp đỡ người cao tuổi đi lại an toàn trong khu vực.", "action": "Mỗi thành viên trong đội đóng góp một sáng kiến gắn kết tình làng nghĩa xóm."}
        ]
    }

    c_sel, c_res = st.columns([1, 1.5])
    with c_sel:
        chosen_cat = st.selectbox("Chọn bộ thẻ cần rút:", list(deck_library.keys()))
        if st.button("✨ RÚT LÁ THẺ NGẪU NHIÊN", type="primary", use_container_width=True):
            st.session_state['active_card'] = random.choice(deck_library[chosen_cat])
            st.session_state['active_cat'] = chosen_cat

    with c_res:
        if 'active_card' in st.session_state:
            ac = st.session_state['active_card']
            st.markdown(f"""
            <div class="cham-card" style="border-left: 8px solid #18324A;">
                <span class="badge-nc">{st.session_state['active_cat']}</span>
                <h3 style="margin-top:12px;">[{ac['code']}] {ac['title']}</h3>
                <p style="font-size:1.08em; line-height:1.6;">{ac['content']}</p>
                <hr>
                <p style="color:#2D6A4F; font-weight:bold;">🎯 Gợi ý thảo luận / Hành động thực tế:</p>
                <p>{ac['action']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Nhấn nút **RÚT LÁ THẺ NGẪU NHIÊN** bên trái để mở thẻ bài tương tác!")

# ==============================================================================
# MODULE 6: THỬ THÁCH PHÁ BỎ ĐỊNH KIẾN (QUIZ)
# ==============================================================================
elif selected_tab == "🧠 6. Thử thách Phá bỏ Định kiến (Quiz)":
    st.title("🧠 Kiểm Tra Kiến Thức & Phá Bỏ Định Kiến")
    st.markdown("Trắc nghiệm nhanh 5 câu hỏi giúp bạn củng cố nhận thức chuẩn xác về bệnh Alzheimer.")

    with st.form("quiz_comprehensive"):
        q1 = st.radio("1. Bệnh Alzheimer có phải là một phần tất yếu của quá trình lão hóa tự nhiên không?", ["Đúng, tuổi cao ai cũng mắc", "Sai, đây là bệnh lý thoái hóa thần kinh mạn tính"])
        q2 = st.radio("2. Trí tuệ nhân tạo (AI) trong y tế nên được ứng dụng thế nào đối với Alzheimer?", ["Thay thế hoàn toàn bác sĩ chuyên khoa", "Hỗ trợ sàng lọc sớm, quản lý dữ liệu và trợ giúp người chăm sóc"])
        q3 = st.radio("3. Khi người bệnh nhớ nhầm hoặc hoang tưởng nhẹ, chúng ta nên ứng xử ra sao?", ["Tranh cãi đến cùng để bắt họ công nhận sự thật", "Tôn trọng cảm xúc, thấu hiểu và khéo léo chuyển hướng"])
        q4 = st.radio("4. Người mắc Alzheimer ở giai đoạn tiến triển có còn cảm nhận được sự yêu thương không?", ["Còn, trí nhớ cảm xúc rất nhạy bén", "Không còn cảm nhận được gì nữa"])
        q5 = st.radio("5. Thông điệp cốt lõi của dự án CHẠM là gì?", ["Đóng cửa cách ly người bệnh để đảm bảo an toàn", "Thấu hiểu để kết nối – Không ai phải đi một mình"])

        submit_q = st.form_submit_button("Nộp bài & Nhận huy hiệu Đại sứ Thấu cảm")

    if submit_q:
        points = 0
        if "Sai" in q1: points += 1
        if "Hỗ trợ" in q2: points += 1
        if "Tôn trọng" in q3: points += 1
        if "Còn" in q4: points += 1
        if "Thấu hiểu" in q5: points += 1

        st.divider()
        if points == 5:
            st.balloons()
            st.success(f"🏆 **XUẤT SẮC ({points}/5 điểm)!** Bạn chính thức đạt danh hiệu **Đại sứ Thấu cảm CHẠM** với nhận thức vô cùng sâu sắc và nhân văn.")
        elif points >= 3:
            st.info(f"🌟 **RẤT TỐT ({points}/5 điểm)!** Bạn đã nắm vững các nguyên tắc cốt lõi để đồng hành cùng người bệnh.")
        else:
            st.warning(f"🌱 **HOÀN THÀNH TỐT ({points}/5 điểm)!** Hãy khám phá thêm các chuyên mục cẩm nang để hiểu thêm nhiều kiến thức bổ ích nhé.")

# ==============================================================================
# MODULE 7: NHẬT KÝ NGƯỜI CHĂM SÓC & SỨC KHỎE TINH THẦN
# ==============================================================================
elif selected_tab == "📝 7. Nhật ký Người chăm sóc & Sức khỏe Tinh thần":
    st.title("📝 Góc Nhật Ký & Trạm Chữa Lành Tâm Hồn")
    st.markdown("Nơi ghi lại những tâm tư, áp lực hoặc những khoảnh khắc ấm áp của những người làm công tác chăm sóc gia đình.")

    col_j1, col_j2 = st.columns([1, 1.3])
    with col_j1:
        with st.container(border=True):
            st.subheader("✍️ Viết nhật ký hôm nay")
            j_title = st.text_input("Tiêu đề / Cảm xúc chủ đạo:", placeholder="Ví dụ: Một ngày bình yên hơn hôm qua...")
            j_content = st.text_area("Chia sẻ suy nghĩ của bạn:", height=120, placeholder="Hôm nay bạn đã trải qua những áp lực hay khoảnh khắc đáng nhớ nào...")
            if st.button("Lưu vào Sổ tay Chữa lành", type="primary", use_container_width=True):
                if j_title and j_content:
                    st.session_state['caregiver_journal'].insert(0, {"title": j_title, "content": j_content, "time": time.strftime("%d/%m/%Y %H:%M")})
                    st.success("Đã lưu tâm sự của bạn vào sổ tay cá nhân.")
                    st.rerun()
                else:
                    st.warning("Vui lòng điền đầy đủ tiêu đề và nội dung.")

    with col_j2:
        st.subheader("📖 Những trang nhật ký đã lưu")
        if not st.session_state['caregiver_journal']:
            st.info("Chưa có trang nhật ký nào được ghi lại. Hãy chia sẻ cảm xúc của bạn ở khung bên trái.")
        else:
            for item in st.session_state['caregiver_journal']:
                st.markdown(f"""
                <div class="cham-card-warm">
                    <div style="display:flex; justify-content:space-between;">
                        <b>📌 {item['title']}</b>
                        <span style="font-size:0.85em; color:#666;">{item['time']}</span>
                    </div>
                    <p style="margin-top:8px; font-style:italic;">“{item['content']}”</p>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 8: TÀI NGUYÊN NGHIÊN CỨU & THƯ VIỆN
# ==============================================================================
elif selected_tab == "📚 8. Tài nguyên Nghiên cứu & Thư viện":
    st.title("📚 Thư Viện Tài Nguyên & Nghiên Cứu CHẠM")
    st.markdown("Tổng hợp các tài liệu hướng dẫn, báo cáo khoa học và tài nguyên truyền thông phục vụ cộng đồng.")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        with st.container(border=True):
            st.subheader("📑 Tài liệu Hướng dẫn Chăm sóc")
            st.write("• **Cẩm nang gia đình đồng hành cùng Alzheimer** (PDF - 42 trang)")
            st.write("• **Bộ quy tắc giao tiếp ứng xử trong nhà** (Infographic chuẩn hóa)")
            st.write("• **Thiết kế không gian an toàn chống ngã cho người cao tuổi**")
            st.button("📥 Tải bộ cẩm nang gia đình", key="dl_1")

    with col_r2:
        with st.container(border=True):
            st.subheader("🔬 Tài liệu Khoa học & Dự án")
            st.write("• **Báo cáo kỹ thuật chi tiết Board Game CHẠM (64 ô)**")
            st.write("• **Tài liệu nghiên cứu định hướng dược liệu tự nhiên & Tin sinh học**")
            st.write("• **Slide Pitch Deck thuyết trình dự án khởi nghiệp xã hội**")
            st.button("📥 Tải tài liệu kỹ thuật dự án", key="dl_2")

# ==============================================================================
# MODULE 9: BỨC TƯỜNG SẺ CHIA CỘNG ĐỒNG
# ==============================================================================
elif selected_tab == "💌 9. Bức tường Sẻ chia Cộng đồng":
    st.title("💌 Bức Tường Sẻ Chia — Không Ai Phải Đi Một Mình")
    st.markdown("Nơi gắn kết những trái tim yêu thương, gửi gắm những lời nhắn động viên ý nghĩa đến cộng đồng.")

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
                        "author": user_name if user_name.strip() else "Người bạn ẩn danh",
                        "role": user_role,
                        "msg": user_msg.strip()
                    })
                    st.success("Cảm ơn bạn! Thông điệp của bạn đã được lan tỏa.")
                    st.rerun()
                else:
                    st.warning("Vui lòng viết nội dung trước khi gửi.")

    with col_wall:
        st.subheader(f"🌿 Những lời nhắn từ cộng đồng ({len(st.session_state['community_notes'])})")
        for note in st.session_state['community_notes']:
            st.markdown(f"""
            <div class="cham-card-warm">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#18324A; font-size:1.05em;">👤 {note['author']}</b>
                    <span class="badge-cd">{note['role']}</span>
                </div>
                <p style="margin-top:10px; color:#333; font-style:italic;">“{note['msg']}”</p>
            </div>
            """, unsafe_allow_html=True)
