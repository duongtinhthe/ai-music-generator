import streamlit as st
from google import genai

# Cấu hình giao diện trang web
st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Generator")
st.write("Tạo và phân tích bài hát theo phong cách, xu hướng hiện đại bằng Gemini AI.")

# 1. Nhận API Key từ Secrets hoặc từ ô nhập
api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
api_key_input = st.text_input(
    "Nhập Gemini API Key của bạn:", 
    type="password", 
    value=api_key_secret,
    help="Lấy miễn phí tại console.cloud.google.com hoặc aistudio.google.com"
)
api_key = api_key_secret if api_key_secret else api_key_input

# 2. Ô nhập Lời bài hát
lyrics_input = st.text_area(
    "1. Lời bài hát (Lyrics)",
    height=200,
    placeholder="Nhập lời bài hát vào đây...\nVí dụ:\n[Verse 1]\nPhố xá lung linh ánh đèn\n[Chorus]\nGiai điệu nhẹ nhàng cất lên...",
)

# 3. Ô nhập Phong cách / Giai điệu
tags_input = st.text_input(
    "2. Phong cách, giai điệu hoặc màu sắc bài hát",
    placeholder="Ví dụ: Modern V-Pop, R&B catchy, acoustic guitar, mượt mà, clear vocals",
)

# 4. Tùy chọn Độ dài / Cấu trúc bài hát
duration = st.select_slider(
    "3. Chọn thời lượng mong muốn:",
    options=["1 phút", "2 phút", "3 phút (Bài đầy đủ)"],
    value="2 phút"
)

# Nút Bấm Tạo bài hát
if st.button("🚀 Tạo bài hát", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key để tiếp tục!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập lời bài hát vào ô thứ nhất!")
    elif not tags_input.strip():
        st.warning("Vui lòng nhập phong cách bài hát vào ô thứ hai!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Gemini đang phân tích lyric và dàn dựng cấu trúc bài hát...")
        
        try:
            # Khởi tạo Client Gemini
            client = genai.Client(api_key=api_key)
            
            # Tạo Prompt chi tiết
            prompt = f"""
Bạn là một nhạc sĩ và producer chuyên nghiệp.
Hãy phân tích lời bài hát và xây dựng một bài hát hoàn chỉnh theo yêu cầu sau:

- **Thời lượng mục tiêu:** {duration}
- **Phong cách / Giai điệu / Màu sắc:** {tags_input}
- **Lời bài hát gốc:**
{lyrics_input}

Hãy trả về kết quả theo cấu trúc rõ ràng bao gồm:
1. **Phân tích giai điệu & phối khí** (BPM, Tone, Nhạc cụ chủ đạo).
2. **Cấu trúc bài hát phân bổ Timestamps** (Intro, Verse, Chorus, Bridge, Outro) khớp với thời lượng {duration}.
3. **Chi tiết cách thể hiện giọng hát (Vocal guide)** rõ ràng từng câu lời.
"""

            # Gọi model gemini-3.6-flash mới nhất
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            
            status_box.success("🎉 Đã hoàn thành bản thiết kế bài hát!")
            
            # Hiển thị kết quả ra màn hình
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            status_box.error(f"Lỗi khi kết nối Gemini API: {e}")
