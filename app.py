import base64
import streamlit as st
from google import genai

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="AI Audio & Music Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Audio Generator")
st.write("Tạo bài hát / giọng đọc âm thanh MP3 trực tiếp bằng Gemini AI.")

# 1. Nhận API Key
api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
api_key_input = st.text_input(
    "Nhập Gemini API Key của bạn:", 
    type="password", 
    value=api_key_secret,
    help="Lấy miễn phí tại console.cloud.google.com hoặc aistudio.google.com"
)
api_key = api_key_secret if api_key_secret else api_key_input

# 2. Ô nhập Lời bài hát / Nội dung
lyrics_input = st.text_area(
    "1. Lời bài hát hoặc kịch bản (Lyrics/Prompt)",
    height=200,
    placeholder="Nhập lời bài hát vào đây...\nVí dụ:\nPhố xá lung linh ánh đèn, giai điệu nhẹ nhàng cất lên...",
)

# 3. Ô nhập Phong cách thể hiện
tags_input = st.text_input(
    "2. Phong cách thể hiện / Giọng hát",
    value="Hát giai điệu truyền cảm, nhẹ nhàng, du dương",
    placeholder="Ví dụ: Giọng hát truyền cảm, phong cách V-Pop mượt mà",
)

# Nút Tạo Âm Thanh
if st.button("🚀 Tạo file MP3", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key để tiếp tục!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập nội dung vào ô thứ nhất!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Gemini đang khởi tạo và tổng hợp file âm thanh MP3...")
        
        try:
            # Khởi tạo Client Gemini
            client = genai.Client(api_key=api_key)
            
            # Kết hợp phong cách và nội dung
            prompt_content = f"Phong cách: {tags_input}\n\nNội dung:\n{lyrics_input}"
            
            # Gọi mô hình Gemini TTS (Tạo âm thanh)
            response = client.models.generate_content(
                model="gemini-3.1-flash-tts-preview",
                contents=prompt_content,
                config={
                    "response_mime_type": "audio/mp3"
                }
            )
            
            # Lấy dữ liệu audio dạng binary/base64
            if hasattr(response, 'audio') and response.audio:
                audio_bytes = response.audio
            elif hasattr(response, 'candidates') and response.candidates[0].content.parts[0].inline_data:
                audio_bytes = base64.b64decode(response.candidates[0].content.parts[0].inline_data.data)
            else:
                audio_bytes = None

            if audio_bytes:
                status_box.success("🎉 Tạo âm thanh thành công!")
                
                st.markdown("---")
                # 1. Trình phát nhạc trực tiếp trên Web
                st.audio(audio_bytes, format="audio/mp3")
                
                # 2. Nút Tải file MP3 về máy
                st.download_button(
                    label="⬇️ Tải file MP3 về máy",
                    data=audio_bytes,
                    file_name="gemini_song.mp3",
                    mime="audio/mp3"
                )
            else:
                # Nếu model trả về text dạng fallback
                status_box.success("🎉 Hoàn thành!")
                st.write(response.text)

        except Exception as e:
            # Nếu gặp lỗi model TTS preview, gọi fallback Audio
            status_box.warning("Đang chuyển đổi phương thức phát âm thanh...")
            try:
                client = genai.Client(api_key=api_key)
                res = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=f"Đọc/hát diễn cảm: {lyrics_input}"
                )
                st.write(res.text)
            except Exception as err:
                status_box.error(f"Lỗi tạo âm thanh: {e}")
