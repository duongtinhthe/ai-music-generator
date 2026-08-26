import io
import streamlit as st
from gtts import gTTS
from google import genai

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="AI Music & Audio Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Music & Audio Generator")
st.write("Tạo bài hát và xuất thành file MP3 phát trực tiếp / tải về bằng Gemini & Google Audio Engine.")

# 1. Nhận API Key từ Secrets hoặc ô nhập
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

# 3. Ô nhập Phong cách thể hiện
tags_input = st.text_input(
    "2. Phong cách thể hiện / Nhạc điệu",
    value="V-Pop mượt mà, giai điệu truyền cảm",
    placeholder="Ví dụ: V-Pop, Acoustic, R&B sôi động",
)

# Nút Tạo bài hát & File MP3
if st.button("🚀 Tạo bài hát MP3", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key để tiếp tục!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập lời bài hát vào ô thứ nhất!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Gemini đang tối ưu lời bài hát và xuất file âm thanh MP3...")
        
        try:
            # Bước 1: Dùng Gemini 3.6 Flash để tối ưu Lời bài hát
            client = genai.Client(api_key=api_key)
            prompt = f"""
            Bạn là một nhạc sĩ. Hãy tinh chỉnh lại lời bài hát sau cho mượt mà, đúng vần điệu theo phong cách {tags_input}:
            {lyrics_input}
            """
            
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            song_text = response.text if response.text else lyrics_input

            # Bước 2: Chuyển đổi văn bản thành File MP3 âm thanh thật
            tts = gTTS(text=song_text, lang='vi', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()

            status_box.success("🎉 Tạo file MP3 thành công!")
            st.markdown("---")

            # 1. Trình phát nhạc trên Web
            st.audio(audio_bytes, format="audio/mp3")

            # 2. Nút Tải file MP3
            st.download_button(
                label="⬇️ Tải file MP3 về máy",
                data=audio_bytes,
                file_name="bai_hat_ai.mp3",
                mime="audio/mp3"
            )

            # Hiển thị lời bài hát đã được tối ưu
            st.markdown("### 📝 Lời bài hát hoàn chỉnh:")
            st.write(song_text)

        except Exception as e:
            status_box.error(f"Lỗi hệ thống: {e}")
