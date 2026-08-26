import base64
import streamlit as st
from google import genai

# Cấu hình trang web
st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Generator")
st.write("Tạo bài hát mới mẻ, chuẩn xu hướng từ lời bài hát của bạn bằng Gemini AI.")

# 1. Nhập API Key của Gemini
api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy miễn phí tại aistudio.google.com")

# 2. Ô 1: Nhập Lời bài hát
lyrics_input = st.text_area(
    "1. Lời bài hát (Lyrics)",
    height=200,
    placeholder="Nhập lời bài hát vào đây...\nVí dụ:\n[Verse 1]\nPhố xá lung linh ánh đèn\n[Chorus]\nGiai điệu nhẹ nhàng cất lên...",
)

# 3. Ô 2: Nhập Phong cách / Giai điệu
tags_input = st.text_input(
    "2. Phong cách, giai điệu hoặc màu sắc bài hát",
    placeholder="Ví dụ: Modern V-Pop, R&B catchy, acoustic guitar, mượt mà, clear vocals",
)

# 4. Tùy chọn độ dài bài hát
duration = st.select_slider(
    "3. Chọn độ dài bài hát mong muốn:",
    options=["1 phút", "2 phút", "3 phút (Đầy đủ)"],
    value="2 phút"
)

# Nút Tạo bài hát
if st.button("🚀 Tạo bài hát", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key để tiếp tục!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập lời bài hát vào ô thứ nhất!")
    elif not tags_input.strip():
        st.warning("Vui lòng nhập phong cách bài hát vào ô thứ hai!")
    else:
        status_box = st.empty()
        status_box.info(f"⏳ Gemini đang phân tích lời và tạo bài hát ({duration})... Vui lòng chờ 1-2 phút.")
        
        try:
            # Khởi tạo kết nối với Gemini API
            client = genai.Client(api_key=api_key)
            
            # Xây dựng prompt tối ưu
            full_prompt = (
                f"Target duration: {duration}.\n"
                f"Style and Mood: {tags_input}\n\n"
                f"Structure and Lyrics:\n{lyrics_input}"
            )
            
            # Gọi mô hình Lyria 3 Pro hỗ trợ tạo nhạc
            interaction = client.interactions.create(
                model="lyria-3-pro-preview",
                input=full_prompt,
                response_format={"type": "audio"}
            )
            
            generated_audio = interaction.output_audio
            
            if generated_audio:
                audio_bytes = base64.b64decode(generated_audio.data)
                
                status_box.success("🎉 Tạo bài hát thành công!")
                
                # Trình phát nhạc
                st.audio(audio_bytes, format="audio/mp3")
                
                # Nút tải file MP3
                st.download_button(
                    label="⬇️ Tải file MP3",
                    data=audio_bytes,
                    file_name=f"gemini_song_{duration.replace(' ', '_')}.mp3",
                    mime="audio/mp3"
                )
            else:
                status_box.error("Không nhận được dữ liệu âm thanh từ hệ thống. Vui lòng thử lại.")
                
        except Exception as e:
            status_box.error(f"Lỗi khi kết nối Gemini API: {e}")
