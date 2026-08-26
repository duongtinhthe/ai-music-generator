import streamlit as st
from google import genai

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Suno AI Prompt Assistant", page_icon="🎵", layout="centered")

st.title("🎵 Suno AI Song Builder")
st.write("Tạo Lời bài hát & Prompt nhạc chuẩn định dạng Suno AI bằng Gemini.")

# 1. Nhận API Key từ Secrets hoặc ô nhập
api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
api_key_input = st.text_input(
    "Nhập Gemini API Key của bạn:", 
    type="password", 
    value=api_key_secret,
    help="Lấy miễn phí tại console.cloud.google.com hoặc aistudio.google.com"
)
api_key = api_key_secret if api_key_secret else api_key_input

# 2. Ô nhập Lời bài hát gốc / Ý tưởng
lyrics_input = st.text_area(
    "1. Ý tưởng hoặc Lời bài hát thô:",
    height=150,
    placeholder="Nhập ý tưởng, câu chuyện hoặc bài thơ bạn muốn viết thành nhạc...",
)

# 3. Chọn Thể loại nhạc
genre = st.selectbox(
    "2. Thể loại nhạc mong muốn:",
    ["V-Pop Modern", "Acoustic Ballad", "R&B / Soul", "Lo-fi Chill", "Rap / Hip-Hop", "Indie Pop", "EDM / Dance"]
)

# 4. Tùy chọn Giọng hát & Tâm trạng
col1, col2 = st.columns(2)
with col1:
    vocal_style = st.selectbox("Giọng ca sĩ:", ["Nam (Male)", "Nữ (Female)", "Song ca (Duet)"])
with col2:
    mood = st.text_input("Tâm trạng / Cảm xúc:", value="Truyền cảm, nhẹ nhàng, catchy")

# Nút Tạo Prompt Suno
if st.button("🚀 Tạo cấu trúc nhạc cho Suno", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key để tiếp tục!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập nội dung ý tưởng vào ô thứ nhất!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Gemini đang thiết kế lời bài hát và Prompt chuẩn Suno...")
        
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
Bạn là một nhạc sĩ chuyên nghiệp tối ưu bài hát cho Suno AI. 
Dựa vào ý tưởng sau:
"{lyrics_input}"

Hãy tạo ra 2 phần riêng biệt:

1. **STYLE PROMPT (Bằng tiếng Anh, dùng dán vào ô Style of Music của Suno, dưới 120 ký tự):**
Bao gồm thể loại {genre}, giọng hát {vocal_style}, cảm xúc {mood}, nhạc cụ chủ đạo và nhịp điệu.

2. **LYRICS (Đã chia cấu trúc thẻ Suno chuẩn):**
Viết/tinh chỉnh lời bài hát tiếng Việt chuẩn vần điệu, có sử dụng đầy đủ các thẻ cấu trúc của Suno như:
[Intro]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Bridge]
[Guitar Solo]
[Chorus]
[Outro]
[End]
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            status_box.success("🎉 Tạo Prompt thành công!")
            st.markdown("---")
            st.markdown(response.text)
            
            st.info("👉 **Cách dùng:** Bạn bật tab **Custom** trên Suno.com, dán đoạn **Style Prompt** vào ô *Style of Music* và dán đoạn **Lyrics** vào ô *Lyrics* để tạo nhạc!")

        except Exception as e:
            status_box.error(f"Lỗi kết nối Gemini API: {e}")
