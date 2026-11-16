
import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
from datetime import datetime

# ============================================================
# CHẠM HUB – NỀN TẢNG ĐỒNG HÀNH VÀ NÂNG CAO NHẬN THỨC
# Phiên bản nâng cấp – Một tệp Python duy nhất
# ============================================================

st.set_page_config(
    page_title="CHẠM Hub | Thấu hiểu để kết nối",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- NHẬN DIỆN GIAO DIỆN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background: #F5F7F5;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1, h2, h3, h4 {
    color: #18324A;
    font-weight: 750;
}

.hero {
    background: linear-gradient(120deg, #18324A 0%, #24536A 55%, #2D6A4F 100%);
    padding: 48px 42px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(24,50,74,.13);
}

.hero h1 {
    color: white;
    font-size: 42px;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.hero p {
    color: #E8F2ED;
    font-size: 16px;
    line-height: 1.8;
}

.hero-tag {
    color: #F2C66D;
    font-weight: 700;
    letter-spacing: 2px;
    font-size: 13px;
}

.section-label {
    color: #2D6A4F;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.info-card {
    background: white;
    padding: 23px;
    border-radius: 17px;
    border: 1px solid #E6ECE8;
    box-shadow: 0 5px 18px rgba(24,50,74,.045);
    margin-bottom: 15px;
    transition: .2s ease;
}

.info-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(24,50,74,.09);
}

.green-card {
    background: linear-gradient(135deg,#E7F3EC,#F8FCF9);
    border-left: 5px solid #55A88B;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.warm-card {
    background: linear-gradient(135deg,#FFF4E9,#FFFBF6);
    border-left: 5px solid #D18A55;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.purple-card {
    background: linear-gradient(135deg,#F0EDFA,#FAF9FD);
    border-left: 5px solid #7867B5;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.quote {
    background: #E5F1E9;
    color: #18324A;
    padding: 22px 26px;
    border-radius: 15px;
    font-size: 17px;
    font-style: italic;
    line-height: 1.8;
    border-left: 5px solid #2D6A4F;
    margin: 20px 0;
}

.small-note {
    color: #6B7C75;
    font-size: 12px;
    line-height: 1.6;
}

.metric-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E6ECE8;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #2D6A4F;
}

.metric-title {
    color: #64756D;
    font-size: 13px;
}

.card-display {
    background: linear-gradient(145deg,#18324A,#2D6A4F);
    color: white;
    padding: 30px;
    border-radius: 20px;
    min-height: 260px;
    box-shadow: 0 12px 30px rgba(24,50,74,.18);
}

.card-display h2, .card-display h3 {
    color: white;
}

.card-code {
    color: #F2C66D;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
}

div.stButton > button {
    border-radius: 11px;
    font-weight: 700;
    min-height: 43px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #E6ECE8;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 10px;
    padding: 10px 18px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# -------------------- DỮ LIỆU KHỞI TẠO --------------------

if "journal" not in st.session_state:
    st.session_state.journal = []

if "community" not in st.session_state:
    st.session_state.community = [
        {
            "name": "Một người bạn của CHẠM",
            "role": "Người chơi trải nghiệm",
            "message": "Đôi khi điều người thân cần không phải là chúng ta nhắc họ nhớ, mà là chúng ta đủ kiên nhẫn để ở bên họ.",
            "time": "Chia sẻ mẫu"
        }
    ]

if "active_card" not in st.session_state:
    st.session_state.active_card = None

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = {}

if "badge_unlocked" not in st.session_state:
    st.session_state.badge_unlocked = False


# -------------------- THƯ VIỆN THẺ MẪU --------------------
# Các thẻ dưới đây là nội dung minh họa trên nền tảng.
# Cần thay bằng nội dung đã được nhóm chốt trong bộ 132 thẻ chính thức.

deck_library = {
    "Kiến thức": [
        {
            "code": "KT-01",
            "title": "Hiểu về Alzheimer",
            "content": "Alzheimer là một bệnh lý tiến triển của não, có thể ảnh hưởng đến trí nhớ, tư duy và khả năng thực hiện các hoạt động thường ngày.",
            "task": "Hãy giải thích bằng lời của bạn: Alzheimer có đơn thuần là hiện tượng quên do tuổi già không?"
        },
        {
            "code": "KT-02",
            "title": "Khi câu hỏi được lặp lại",
            "content": "Người mắc Alzheimer có thể lặp lại câu hỏi do gặp khó khăn trong việc ghi nhớ thông tin vừa tiếp nhận.",
            "task": "Nêu một cách phản hồi kiên nhẫn khi người thân hỏi đi hỏi lại."
        }
    ],
    "Góc nhìn": [
        {
            "code": "GN-01",
            "title": "Một câu hỏi quen thuộc",
            "content": "Bà hỏi bạn lần thứ năm rằng hôm nay bố mẹ bạn có về ăn cơm không. Bà vẫn đang chờ một câu trả lời.",
            "task": "Hãy thử đặt mình vào cảm xúc của bà và chọn cách phản hồi phù hợp."
        },
        {
            "code": "GN-02",
            "title": "Điều chưa được nói ra",
            "content": "Một người lớn tuổi bắt đầu ngại tham gia những cuộc trò chuyện vì sợ mình nói sai hoặc quên mất điều định nói.",
            "task": "Bạn có thể làm gì để người đó cảm thấy được tôn trọng?"
        }
    ],
    "Nghiên cứu": [
        {
            "code": "NC-01",
            "title": "Tìm hiểu từ nguồn đáng tin cậy",
            "content": "Một bài đăng trên mạng xã hội khẳng định rằng một loại thực phẩm có thể ngăn ngừa hoàn toàn Alzheimer.",
            "task": "Bạn cần kiểm tra những yếu tố nào trước khi tin và chia sẻ thông tin?"
        }
    ],
    "Công nghệ": [
        {
            "code": "CN-01",
            "title": "Nhắc việc hằng ngày",
            "content": "Một gia đình muốn hỗ trợ người thân nhớ giờ uống thuốc và các hoạt động trong ngày.",
            "task": "Đề xuất một giải pháp công nghệ đơn giản, dễ sử dụng và có người thân hỗ trợ."
        }
    ],
    "Chăm sóc – Cộng đồng": [
        {
            "code": "CS-01",
            "title": "Một môi trường thân thiện",
            "content": "Một người lớn tuổi gặp khó khăn khi tìm đường trong khu sinh hoạt cộng đồng.",
            "task": "Đề xuất hai thay đổi giúp không gian dễ nhận biết và an toàn hơn."
        }
    ],
    "Hợp tác": [
        {
            "code": "HT-01",
            "title": "Cùng nhau sẻ chia",
            "content": "Một gia đình đang gặp khó khăn vì chỉ có một người đảm nhận phần lớn việc chăm sóc.",
            "task": "Hãy đề xuất cách phân chia và kết nối sự hỗ trợ giữa các thành viên."
        }
    ],
    "Thử thách": [
        {
            "code": "TC-01",
            "title": "Từ chối tắm rửa",
            "content": "Người thân của bạn không muốn tắm vì cảm thấy lạnh và lo lắng.",
            "task": "Hãy đưa ra cách hỗ trợ nhẹ nhàng, tôn trọng và không ép buộc."
        }
    ],
    "Thời gian – Sự kiện": [
        {
            "code": "TG-01",
            "title": "Ngày hội cộng đồng",
            "content": "Địa phương tổ chức một ngày hội dành cho người cao tuổi. Nhóm bạn muốn lồng ghép hoạt động nâng cao nhận thức về Alzheimer.",
            "task": "Hãy đề xuất một hoạt động giúp cộng đồng hiểu và đồng cảm hơn."
        }
    ]
}


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">HỆ SINH THÁI GIÁO DỤC VÀ KẾT NỐI CỘNG ĐỒNG</div>
    <h1>🪷 CHẠM HUB</h1>
    <p>
        Thấu hiểu để kết nối – Kết nối để sẻ chia.<br>
        Một không gian khám phá kiến thức, thực hành sự thấu cảm
        và lan tỏa những hành động tử tế dành cho cộng đồng Alzheimer.
    </p>
    <div style="margin-top:22px;font-size:14px;color:#F2C66D;font-weight:700;">
        KHÔNG AI PHẢI ĐI MỘT MÌNH.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- ĐIỀU HƯỚNG --------------------

pages = [
    "🏛️ Tổng quan",
    "🧠 Cẩm nang đồng hành",
    "🎲 Trải nghiệm tương tác",
    "💌 Không gian sẻ chia"
]

selected_page = st.radio(
    "KHÁM PHÁ CHẠM HUB",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# ============================================================
# MODULE 1 – TỔNG QUAN
# ============================================================

if selected_page == "🏛️ Tổng quan":

    st.markdown('<div class="section-label">01 / KHÁM PHÁ CHẠM</div>', unsafe_allow_html=True)
    st.title("Một hành trình bắt đầu từ sự thấu hiểu")
    st.write(
        "CHẠM là dự án trò chơi giáo dục tương tác hướng đến nâng cao nhận thức "
        "về Alzheimer, khuyến khích sự đồng cảm và thúc đẩy kết nối cộng đồng."
    )

    st.markdown("""
    <div class="quote">
        “Alzheimer có thể ảnh hưởng đến ký ức, nhưng mỗi người vẫn xứng đáng
        được yêu thương, tôn trọng và đồng hành.”
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Alzheimer và chứng sa sút trí tuệ")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>🧠 Alzheimer</h3>
            <p>Là một bệnh lý tiến triển của não và là nguyên nhân phổ biến
            nhất gây sa sút trí tuệ.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>💭 Trí nhớ</h3>
            <p>Người mắc bệnh có thể gặp khó khăn trong ghi nhớ thông tin,
            định hướng và thực hiện công việc quen thuộc.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <h3>🤝 Đồng hành</h3>
            <p>Sự kiên nhẫn, tôn trọng và hỗ trợ phù hợp có thể góp phần
            cải thiện trải nghiệm sống của người bệnh.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Sa sút trí tuệ trên thế giới")

    m1, m2, m3 = st.columns(3)

    m1.metric("Người sống chung với sa sút trí tuệ", "55 triệu+", help="Ước tính toàn cầu được WHO công bố.")
    m2.metric("Ca mắc mới mỗi năm", "Gần 10 triệu", help="Ước tính toàn cầu của WHO.")
    m3.metric("Tỷ trọng Alzheimer", "60–70%", help="Alzheimer được ước tính chiếm khoảng 60–70% trường hợp sa sút trí tuệ.")

    st.caption(
        "Nguồn: WHO – Dementia. Số liệu mang tính ước tính toàn cầu; "
        "không phải số liệu thống kê riêng của Việt Nam."
    )

    df = pd.DataFrame({
        "Chỉ số": ["Người mắc hiện tại", "Ca mắc mới mỗi năm"],
        "Số lượng (triệu người)": [55, 10]
    })

    fig = px.bar(
        df,
        x="Chỉ số",
        y="Số lượng (triệu người)",
        text="Số lượng (triệu người)",
        color="Chỉ số",
        color_discrete_sequence=["#2D6A4F", "#D18A55"]
    )

    fig.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_title="Triệu người",
        xaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Lưu ý: Đây là hai chỉ số có ý nghĩa khác nhau, không phải hai nhóm "
        "dữ liệu để cộng thành tổng số người mắc bệnh."
    )

    st.divider()
    st.subheader("🌿 Bốn trụ cột của CHẠM")

    p1, p2, p3, p4 = st.columns(4)

    pillars = [
        ("🔬", "NGHIÊN CỨU", "Tìm hiểu vấn đề, kiểm chứng thông tin và xây dựng nội dung có cơ sở."),
        ("💡", "CÔNG NGHỆ", "Ứng dụng giải pháp số hỗ trợ học tập, tra cứu và đồng hành."),
        ("🫶", "CHĂM SÓC", "Khuyến khích giao tiếp kiên nhẫn, tôn trọng và hỗ trợ phù hợp."),
        ("🌍", "CỘNG ĐỒNG", "Lan tỏa nhận thức, giảm định kiến và thúc đẩy sự tham gia.")
    ]

    for col, pillar in zip([p1, p2, p3, p4], pillars):
        with col:
            st.markdown(f"""
            <div class="info-card" style="text-align:center;min-height:190px;">
                <div style="font-size:35px;">{pillar[0]}</div>
                <h4>{pillar[1]}</h4>
                <p style="font-size:13px;">{pillar[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🎲 Hệ sinh thái kết hợp vật lý và số hóa")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="green-card">
            <h3>🎲 Trò chơi bàn CHẠM</h3>
            <p><b>64 ô hành trình – 4 vùng – 4 tài nguyên – 4 thanh tiến độ.</b></p>
            <p>132 thẻ thuộc 8 nhóm nội dung, tạo ra các tình huống học tập,
            tương tác và hợp tác giữa người chơi.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="purple-card">
            <h3>💻 Nền tảng số CHẠM Hub</h3>
            <p>Không gian mở rộng kiến thức, thực hành xử lý tình huống,
            trải nghiệm mini-game và chia sẻ thông điệp cộng đồng.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📚 Nguồn tham khảo")

    references = [
        ("WHO – Dementia", "https://www.who.int/news-room/fact-sheets/detail/dementia"),
        ("NIA – Alzheimer’s Symptoms and Diagnosis", "https://www.nia.nih.gov/health/alzheimers-symptoms-and-diagnosis"),
        ("CDC – Signs and Symptoms of Alzheimer’s", "https://www.cdc.gov/alzheimers-dementia/signs-symptoms/alzheimers.html")
    ]

    for title, url in references:
        st.markdown(f"- [{title}]({url})")


# ============================================================
# MODULE 2 – CẨM NANG ĐỒNG HÀNH
# ============================================================

elif selected_page == "🧠 Cẩm nang đồng hành":

    st.markdown('<div class="section-label">02 / THẤU HIỂU VÀ ĐỒNG HÀNH</div>', unsafe_allow_html=True)
    st.title("Cẩm nang giao tiếp và chăm sóc")
    st.write(
        "Mỗi tình huống đều cần được nhìn nhận từ góc độ của người mắc bệnh. "
        "Không có một cách ứng xử duy nhất phù hợp với tất cả mọi người."
    )

    situations = {
        "🗣️ Lặp lại câu hỏi và khó khăn ngôn ngữ": {
            "context": "Người thân hỏi đi hỏi lại cùng một câu hỏi dù bạn vừa trả lời cách đó vài phút.",
            "nature": "Người mắc Alzheimer có thể gặp khó khăn trong việc ghi nhận và lưu giữ thông tin mới. Việc lặp lại câu hỏi không nhất thiết là hành động cố ý.",
            "avoid": "Quát mắng, tỏ thái độ khó chịu hoặc liên tục nhắc rằng mình đã trả lời.",
            "try": "Kiên nhẫn trả lời bằng câu ngắn, giọng nhẹ nhàng. Có thể sử dụng đồng hồ, giấy ghi chú hoặc lịch sinh hoạt trực quan.",
            "why": "Cách giao tiếp bình tĩnh có thể giúp người bệnh cảm thấy an tâm hơn và hạn chế căng thẳng trong cuộc trò chuyện.",
            "safety": "Nếu khả năng giao tiếp hoặc trí nhớ thay đổi đáng kể, gia đình nên trao đổi với nhân viên y tế để được đánh giá."
        },
        "🔍 Lo lắng và cáo buộc mất đồ": {
            "context": "Người thân cho rằng bạn đã lấy chiếc ví hoặc chìa khóa của họ.",
            "nature": "Khó khăn về trí nhớ có thể khiến người bệnh không nhớ nơi đã đặt đồ vật. Cảm giác bất an có thể đi kèm sự việc này.",
            "avoid": "Cãi vã, chế giễu hoặc cố ép người bệnh thừa nhận mình đã nhớ nhầm.",
            "try": "Lắng nghe cảm xúc, trấn an và cùng tìm kiếm đồ vật ở những nơi quen thuộc.",
            "why": "Tập trung vào cảm xúc và nhu cầu trước mắt thường hữu ích hơn việc tranh luận đúng sai.",
            "safety": "Nếu có biểu hiện thay đổi hành vi đột ngột hoặc gây nguy hiểm, cần tìm hỗ trợ y tế phù hợp."
        },
        "🌅 Bối rối vào chiều tối và nguy cơ đi lạc": {
            "context": "Vào buổi chiều, người thân trở nên bối rối, muốn ra ngoài hoặc đòi về một nơi ở cũ.",
            "nature": "Một số người mắc sa sút trí tuệ có thể tăng mức độ bối rối, lo lắng vào cuối ngày. Cần quan sát các yếu tố như mệt mỏi, ánh sáng và môi trường.",
            "avoid": "Quát mắng, bỏ mặc hoặc nhốt người bệnh trong không gian không an toàn.",
            "try": "Giữ lịch sinh hoạt ổn định, cải thiện ánh sáng, giảm tiếng ồn và đồng hành khi người bệnh muốn di chuyển.",
            "why": "Không gian quen thuộc và ít gây kích thích có thể giúp người bệnh cảm thấy dễ chịu hơn.",
            "safety": "Cần có kế hoạch phòng ngừa đi lạc, thông tin liên hệ khẩn cấp và người hỗ trợ phù hợp."
        },
        "🛁 Vệ sinh cá nhân và ăn uống": {
            "context": "Người thân từ chối tắm hoặc gặp khó khăn khi sử dụng dụng cụ ăn uống.",
            "nature": "Người bệnh có thể cảm thấy lạnh, lo lắng, không hiểu yêu cầu hoặc gặp khó khăn khi thực hiện các bước của hoạt động.",
            "avoid": "Dùng vũ lực, ép buộc hoặc làm người bệnh xấu hổ.",
            "try": "Giải thích từng bước, tạo không gian riêng tư, chuẩn bị vật dụng trước và cho người bệnh thêm thời gian.",
            "why": "Sự tôn trọng, lựa chọn phù hợp và hỗ trợ từng bước có thể giúp hoạt động bớt căng thẳng.",
            "safety": "Nếu có khó khăn nuốt, sụt cân, mất nước hoặc nguy cơ té ngã, cần trao đổi với nhân viên y tế."
        }
    }

    selected_situation = st.selectbox(
        "Chọn tình huống bạn muốn tìm hiểu:",
        list(situations.keys())
    )

    item = situations[selected_situation]

    st.markdown(f"""
    <div class="info-card">
        <div class="section-label">TÌNH HUỐNG THỰC TẾ</div>
        <h3>{selected_situation}</h3>
        <p style="font-size:17px;line-height:1.8;">{item['context']}</p>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown(f"""
        <div class="warm-card">
            <h4>🧠 Điều có thể đang xảy ra</h4>
            <p>{item['nature']}</p>
        </div>
        <div class="warm-card">
            <h4>⚠️ Cách ứng xử nên tránh</h4>
            <p>{item['avoid']}</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown(f"""
        <div class="green-card">
            <h4>🫶 Cách ứng xử có thể thử</h4>
            <p>{item['try']}</p>
        </div>
        <div class="green-card">
            <h4>💡 Vì sao nên thử?</h4>
            <p>{item['why']}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔎 Lưu ý về an toàn và hỗ trợ chuyên môn"):
        st.write(item["safety"])

    st.divider()
    st.subheader("🧩 Thử suy nghĩ từ một tình huống")

    st.write("Bà của bạn hỏi lần thứ tư: “Mấy giờ rồi con?” Bạn sẽ phản hồi thế nào?")

    answer = st.radio(
        "Chọn phương án bạn cho là phù hợp:",
        [
            "A. Nói lớn rằng con vừa trả lời rồi.",
            "B. Kiên nhẫn trả lời lại và hỗ trợ bà bằng đồng hồ dễ nhìn.",
            "C. Bỏ đi vì không muốn trả lời thêm."
        ],
        key="care_question"
    )

    if st.button("Kiểm tra lựa chọn", key="care_check"):
        if answer.startswith("B"):
            st.success("Đây là lựa chọn phù hợp hơn. Trả lời bình tĩnh và sử dụng công cụ trực quan có thể giúp bà an tâm.")
        else:
            st.warning("Hãy thử nhìn tình huống từ góc độ của bà: bà có thể thực sự không nhớ câu trả lời vừa nghe. Bạn có thể chọn cách phản hồi kiên nhẫn hơn.")

    st.caption(
        "Nội dung mang tính giáo dục và tham khảo, không thay thế tư vấn, "
        "đánh giá hoặc hướng dẫn chăm sóc cá nhân từ nhân viên y tế."
    )

    st.subheader("📚 Tài liệu đọc thêm")

    care_refs = [
        ("NHS – Communicating with Someone with Dementia", "https://www.nhs.uk/conditions/dementia/living-with-dementia/communication/"),
        ("NIA – Alzheimer’s Caregiving", "https://www.nia.nih.gov/health/alzheimers-caregiving"),
        ("WHO – Dementia", "https://www.who.int/news-room/fact-sheets/detail/dementia")
    ]

    for title, url in care_refs:
        st.markdown(f"- [{title}]({url})")



# ============================================================
# MODULE 3 – TRẢI NGHIỆM TƯƠNG TÁC
# ============================================================

elif selected_page == "🎲 Trải nghiệm tương tác":

    st.markdown(
        '<div class="section-label">03 / HỌC BẰNG TRẢI NGHIỆM</div>',
        unsafe_allow_html=True
    )
    st.title("Trạm trải nghiệm CHẠM")
    st.write(
        "Khám phá thẻ tình huống, thực hành lựa chọn ứng xử "
        "và theo dõi hành trình thấu cảm."
    )

    # Khởi tạo dữ liệu mini-game
    if "game_feedback" not in st.session_state:
        st.session_state.game_feedback = {}

    if "game_round" not in st.session_state:
        st.session_state.game_round = 0

    if "answered" not in st.session_state:
        st.session_state.answered = {}

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "badge_unlocked" not in st.session_state:
        st.session_state.badge_unlocked = False

    # Điều hướng bằng radio thay cho tabs
    experience_area = st.radio(
        "CHỌN KHU VỰC TRẢI NGHIỆM",
        [
            "🎴 Trạm rút thẻ",
            "🎮 Mini-game",
            "🏅 Hành trình thấu cảm"
        ],
        horizontal=True,
        key="experience_area",
        label_visibility="collapsed"
    )

    st.divider()

    # ========================================================
    # 1. TRẠM RÚT THẺ
    # ========================================================

    if experience_area == "🎴 Trạm rút thẻ":

        st.subheader("🎴 Trạm rút thẻ tình huống")

        st.write(
            "Chọn một nhóm thẻ để khám phá nội dung. "
            "Các thẻ đang hiển thị là dữ liệu minh họa, "
            "không phải toàn bộ bộ 132 thẻ chính thức."
        )

        category = st.selectbox(
            "Chọn nhóm thẻ:",
            list(deck_library.keys()),
            key="draw_category"
        )

        if st.button(
            "✨ RÚT MỘT LÁ THẺ",
            type="primary",
            use_container_width=True,
            key="draw_card"
        ):
            st.session_state.active_card = random.choice(
                deck_library[category]
            )
            st.session_state.active_category = category

        if st.session_state.active_card:

            card = st.session_state.active_card

            st.markdown(f"""
            <div class="card-display">
                <div class="card-code">
                    {st.session_state.get('active_category', 'CHẠM').upper()}
                </div>

                <h2 style="margin-top:18px;">
                    {card['title']}
                </h2>

                <div style="color:#F2C66D;font-weight:700;">
                    {card['code']}
                </div>

                <p style="font-size:17px;line-height:1.8;margin-top:20px;">
                    {card['content']}
                </p>

                <hr style="border-color:rgba(255,255,255,.3);">

                <p><b>🎯 NHIỆM VỤ</b></p>
                <p>{card['task']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "🔄 RÚT THẺ KHÁC",
                key="draw_another_card"
            ):
                st.session_state.active_card = random.choice(
                    deck_library[category]
                )
                st.session_state.active_category = category
                st.rerun()

        else:
            st.info(
                "Chọn nhóm thẻ và nhấn **Rút một lá thẻ** để bắt đầu."
            )

        st.caption(
            "Bộ trò chơi vật lý CHẠM gồm 132 thẻ thuộc 8 nhóm. "
            "Thư viện trên nền tảng hiện là bộ dữ liệu minh họa."
        )

    # ========================================================
    # 2. MINI-GAME
    # ========================================================

    elif experience_area == "🎮 Mini-game":

        st.subheader("🎮 Thử thách xử lý tình huống")

        st.write(
            "Đọc tình huống, chọn cách ứng xử bạn cho là phù hợp nhất "
            "và nhấn **Xác nhận lựa chọn** để nhận phản hồi."
        )

        questions = [
            {
                "title": "Thử thách 1 – Câu hỏi lặp lại",
                "question": (
                    "Mẹ hỏi đi hỏi lại: “Mấy giờ rồi con?” "
                    "Bạn nên làm gì?"
                ),
                "options": [
                    "A. Quát lên vì đã trả lời nhiều lần.",
                    "B. Kiên nhẫn trả lời và dùng đồng hồ dễ nhìn để hỗ trợ.",
                    "C. Phớt lờ câu hỏi."
                ],
                "correct": 1,
                "explain": (
                    "Người mắc Alzheimer có thể không nhớ câu trả lời "
                    "trước đó. Trả lời nhẹ nhàng và dùng công cụ trực quan "
                    "có thể hỗ trợ họ."
                )
            },
            {
                "title": "Thử thách 2 – Cáo buộc mất đồ",
                "question": (
                    "Bố cho rằng bạn đã lấy chiếc kính của ông. "
                    "Bạn nên làm gì?"
                ),
                "options": [
                    "A. Cãi lý để chứng minh mình không lấy.",
                    "B. Chê trách vì bố không nhớ.",
                    "C. Lắng nghe, trấn an và cùng bố tìm chiếc kính."
                ],
                "correct": 2,
                "explain": (
                    "Lắng nghe cảm xúc và cùng tìm kiếm có thể giảm "
                    "căng thẳng hơn là tranh luận đúng sai."
                )
            },
            {
                "title": "Thử thách 3 – Bối rối vào chiều tối",
                "question": (
                    "Mẹ muốn ra ngoài tìm một nơi ở cũ. "
                    "Bạn nên làm gì?"
                ),
                "options": [
                    "A. Quát mắng và bắt mẹ ngồi yên.",
                    "B. Bỏ mặc mẹ tự đi.",
                    "C. Bình tĩnh trò chuyện, tìm hiểu nhu cầu và đảm bảo an toàn."
                ],
                "correct": 2,
                "explain": (
                    "Cần chú ý cảm xúc, nhu cầu và nguy cơ an toàn. "
                    "Không nên bỏ mặc hoặc dùng cách ép buộc."
                )
            },
            {
                "title": "Thử thách 4 – Từ chối tắm",
                "question": (
                    "Người thân không muốn tắm vì cảm thấy lo lắng. "
                    "Bạn nên làm gì?"
                ),
                "options": [
                    "A. Ép buộc để hoàn thành việc tắm.",
                    "B. Tìm hiểu nguyên nhân, giải thích từng bước và tôn trọng lựa chọn.",
                    "C. Quát mắng vì người thân không hợp tác."
                ],
                "correct": 1,
                "explain": (
                    "Tìm hiểu nguyên nhân và hỗ trợ từng bước có thể "
                    "giúp người bệnh cảm thấy an toàn, được tôn trọng."
                )
            }
        ]

        # Chọn câu hỏi
        game_choice = st.selectbox(
            "Chọn thử thách:",
            [q["title"] for q in questions],
            key="minigame_question"
        )

        question_key = next(
            i for i, item in enumerate(questions)
            if item["title"] == game_choice
        )

        q = questions[question_key]

        # Hiển thị tình huống
        st.markdown(f"""
        <div class="info-card">
            <div class="section-label">
                TÌNH HUỐNG THỬ THÁCH {question_key + 1}/4
            </div>
            <h3>{q['title']}</h3>
            <p style="font-size:18px;line-height:1.7;">
                {q['question']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Mỗi lần làm mới sẽ có một bộ khóa mới cho lựa chọn
        answer_widget_key = (
            f"minigame_answer_{question_key}_"
            f"{st.session_state.game_round}"
        )

        user_answer = st.radio(
            "Lựa chọn của bạn:",
            q["options"],
            key=answer_widget_key
        )

        # Xác nhận đáp án
        if st.button(
            "✅ XÁC NHẬN LỰA CHỌN",
            type="primary",
            use_container_width=True,
            key=f"check_answer_{question_key}"
        ):

            selected_index = q["options"].index(user_answer)

            if selected_index == q["correct"]:

                # Chỉ cộng điểm một lần cho mỗi câu
                if not st.session_state.answered.get(
                    question_key, False
                ):
                    st.session_state.score += 1
                    st.session_state.answered[question_key] = True

                st.session_state.game_feedback[question_key] = (
                    "correct",
                    q["explain"]
                )

            else:

                # Trả lời sai vẫn được thử lại
                st.session_state.game_feedback[question_key] = (
                    "retry",
                    q["explain"]
                )

        # Hiển thị phản hồi sau khi xác nhận
        feedback = st.session_state.game_feedback.get(
            question_key
        )

        if feedback:

            if feedback[0] == "correct":
                st.success(
                    "🌿 Chính xác! Bạn đã chọn cách ứng xử phù hợp."
                )
            else:
                st.warning(
                    "Bạn chưa chọn đúng. Hãy suy nghĩ thêm "
                    "và thử lại nhé."
                )

            st.info(feedback[1])

        # Trạng thái hoàn thành câu hỏi
        if st.session_state.answered.get(question_key, False):
            st.caption(
                "✓ Bạn đã hoàn thành thử thách này. "
                "Điểm của câu hỏi chỉ được tính một lần."
            )

        # ====================================================
        # BẢNG ĐIỂM VÀ TIẾN ĐỘ
        # ====================================================

        st.divider()
        st.subheader("📊 Kết quả hành trình")

        score = st.session_state.score

        completed = sum(
            1 for value in st.session_state.answered.values()
            if value
        )

        metric1, metric2 = st.columns(2)

        metric1.metric(
            "Số thử thách trả lời đúng",
            f"{score}/4"
        )

        metric2.metric(
            "Thử thách đã hoàn thành",
            f"{completed}/4"
        )

        st.progress(min(score / 4, 1.0))

        if score >= 4:
            st.session_state.badge_unlocked = True

            st.success(
                "🏅 Bạn đã mở khóa danh hiệu: ĐẠI SỨ THẤU CẢM!"
            )

            st.balloons()

        # Làm mới toàn bộ hành trình
        if st.button(
            "↻ LÀM MỚI HÀNH TRÌNH THỬ THÁCH",
            key="reset_minigame"
        ):

            st.session_state.score = 0
            st.session_state.answered = {}
            st.session_state.game_feedback = {}
            st.session_state.badge_unlocked = False

            # Tạo khóa widget mới để xóa lựa chọn cũ
            st.session_state.game_round += 1

            st.rerun()

    # ========================================================
    # 3. HÀNH TRÌNH THẤU CẢM
    # ========================================================

    elif experience_area == "🏅 Hành trình thấu cảm":

        st.subheader("🏅 Hành trình Đại sứ Thấu cảm")

        st.write(
            "Mỗi thử thách là một cơ hội để học cách lắng nghe, "
            "hiểu và tôn trọng người khác."
        )

        milestones = [
            (
                "🌱",
                "Bắt đầu thấu hiểu",
                "Khám phá kiến thức cơ bản về Alzheimer."
            ),
            (
                "🫶",
                "Học cách đồng hành",
                "Tìm hiểu cách giao tiếp và chăm sóc phù hợp."
            ),
            (
                "🤝",
                "Kết nối yêu thương",
                "Thực hành các tình huống và lựa chọn ứng xử."
            ),
            (
                "🏅",
                "Đại sứ thấu cảm",
                "Hoàn thành các thử thách của CHẠM."
            )
        ]

        for icon, title, desc in milestones:

            st.markdown(f"""
            <div class="info-card">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

        current_score = st.session_state.score

        completed = sum(
            1 for value in st.session_state.answered.values()
            if value
        )

        st.divider()
        st.subheader("Tiến độ của bạn")

        st.metric(
            "Điểm thử thách hiện tại",
            f"{current_score}/4"
        )

        st.progress(min(current_score / 4, 1.0))

        st.write(
            f"Bạn đã hoàn thành **{completed}/4 thử thách**."
        )

        if current_score >= 4:
            st.session_state.badge_unlocked = True

        if st.session_state.badge_unlocked:

            st.success(
                "🏅 Chúc mừng! Bạn đã hoàn thành hành trình "
                "thử thách mẫu – ĐẠI SỨ THẤU CẢM."
            )

        else:

            st.info(
                "Tiếp tục Mini-game để hoàn thành các thử thách "
                "và mở khóa danh hiệu Đại sứ Thấu cảm."
            )

        if st.button(
            "🎮 ĐẾN MINI-GAME",
            key="go_to_minigame"
        ):
            st.session_state.experience_area = "🎮 Mini-game"
            st.rerun()


'''
print("Replacement module prepared.")

# ============================================================
# MODULE 4 – KHÔNG GIAN SẺ CHIA
# ============================================================

elif selected_page == "💌 Không gian sẻ chia":

    st.markdown('<div class="section-label">04 / KẾT NỐI VÀ LAN TỎA</div>', unsafe_allow_html=True)
    st.title("Không gian sẻ chia")
    st.write(
        "Một nơi để ghi lại những điều muốn nói, gửi đi lời động viên "
        "và cùng nhau lan tỏa sự thấu hiểu."
    )

    journal_tab, wall_tab = st.tabs([
        "📖 Nhật ký cá nhân",
        "🕊️ Bức tường sẻ chia"
    ])

    with journal_tab:

        st.subheader("📖 Nhật ký của riêng bạn")

        st.markdown("""
        <div class="warm-card">
            <h4>Một khoảng lặng dành cho cảm xúc</h4>
            <p>Bạn có thể ghi lại suy nghĩ, những điều đã học được
            hoặc một khoảnh khắc tử tế trong ngày.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("journal_form", clear_on_submit=True):

            journal_title = st.text_input(
                "Tiêu đề",
                placeholder="Ví dụ: Một ngày kiên nhẫn hơn..."
            )

            journal_content = st.text_area(
                "Nội dung",
                placeholder="Hãy viết những điều bạn muốn lưu giữ...",
                height=150
            )

            save_journal = st.form_submit_button(
                "💚 LƯU TRANG NHẬT KÝ",
                use_container_width=True
            )

            if save_journal:

                if journal_title.strip() and journal_content.strip():

                    st.session_state.journal.insert(0, {
                        "title": journal_title.strip(),
                        "content": journal_content.strip(),
                        "time": datetime.now().strftime("%d/%m/%Y %H:%M")
                    })

                    st.success("Đã lưu nhật ký trong phiên sử dụng hiện tại.")

                else:
                    st.warning("Vui lòng nhập đầy đủ tiêu đề và nội dung.")

        st.divider()
        st.subheader(f"Những trang đã lưu ({len(st.session_state.journal)})")

        if not st.session_state.journal:
            st.info("Nhật ký của bạn đang chờ những dòng viết đầu tiên.")

        for i, entry in enumerate(st.session_state.journal):

            with st.container(border=True):

                st.markdown(f"### 📌 {entry['title']}")
                st.caption(entry["time"])
                st.write(entry["content"])

                if st.button("Xóa trang này", key=f"delete_journal_{i}"):

                    st.session_state.journal.pop(i)
                    st.rerun()

        st.caption(
            "Lưu ý: Nhật ký hiện được lưu trong phiên làm việc của ứng dụng. "
            "Đây chưa phải hệ thống lưu trữ riêng tư lâu dài."
        )

    with wall_tab:

        st.subheader("🕊️ Bức tường sẻ chia")

        st.markdown("""
        <div class="green-card">
            <h4>Một lời nhắn nhỏ – Một sự kết nối lớn</h4>
            <p>Hãy gửi một lời động viên, một suy nghĩ tích cực
            hoặc một thông điệp về sự thấu hiểu dành cho cộng đồng.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("community_form", clear_on_submit=True):

            author = st.text_input(
                "Tên hoặc bút danh",
                placeholder="Bạn có thể để trống để đăng ẩn danh"
            )

            role = st.selectbox(
                "Bạn tham gia với vai trò:",
                [
                    "Học sinh / Sinh viên",
                    "Người chơi trải nghiệm CHẠM",
                    "Người thân / Người chăm sóc",
                    "Tình nguyện viên / Cộng đồng",
                    "Khác"
                ]
            )

            message = st.text_area(
                "Thông điệp của bạn",
                placeholder="Hãy viết điều bạn muốn gửi đến mọi người...",
                height=130
            )

            submit_message = st.form_submit_button(
                "🕊️ GỬI THÔNG ĐIỆP",
                use_container_width=True
            )

            if submit_message:

                if message.strip():

                    st.session_state.community.insert(0, {
                        "name": author.strip() if author.strip() else "Ẩn danh",
                        "role": role,
                        "message": message.strip(),
                        "time": datetime.now().strftime("%d/%m/%Y %H:%M")
                    })

                    st.success("Thông điệp đã được thêm vào bức tường trong phiên hiện tại.")

                else:
                    st.warning("Bạn hãy viết một thông điệp trước khi gửi.")

        st.divider()

        st.subheader(
            f"🌿 Những thông điệp được chia sẻ ({len(st.session_state.community)})"
        )

        for note in st.session_state.community:

            st.markdown(f"""
            <div class="info-card">
                <div style="color:#2D6A4F;font-weight:800;">
                    👤 {note['name']}
                </div>
                <div style="font-size:12px;color:#87958D;margin-top:4px;">
                    {note['role']} · {note['time']}
                </div>
                <p style="font-size:16px;line-height:1.8;margin-top:15px;">
                    “{note['message']}”
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "Bức tường hiện là bản thử nghiệm lưu trong phiên Streamlit. "
            "Nội dung chưa được chia sẻ giữa các người dùng khác nhau và "
            "chưa có hệ thống kiểm duyệt hoặc cơ sở dữ liệu chung."
        )


# -------------------- FOOTER --------------------

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px 10px;">
    <div style="font-size:30px;">🪷</div>
    <h3 style="margin-bottom:5px;">CHẠM</h3>
    <p style="color:#2D6A4F;font-weight:700;">
        Thấu hiểu để kết nối – Kết nối để sẻ chia.
    </p>
    <p style="color:#819087;font-size:12px;">
        Không ai phải đi một mình.
    </p>
    <p style="color:#9AA69F;font-size:11px;">
        CHẠM Hub · Nền tảng giáo dục và kết nối cộng đồng
    </p>
</div>
""", unsafe_allow_html=True)
