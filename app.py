import requests
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Music Studio", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Studio")
st.write("Tự động sáng tác lời, tạo prompt Suno và phát bài hát MP3 ngay trên Web.")

# 1. Nhập API Key
api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
api_key_input = st.text_input(
    "Nhập Gemini API Key:", 
    type="password", 
    value=api_key_secret
)
api_key = api_key_secret if api_key_secret else api_key_input

# 2. Nhập Ý tưởng
lyrics_input = st.text_area("1. Nhập Ý tưởng / Lời bài hát:", height=150)
tags_input = st.text_input("2. Phong cách nhạc:", value="V-Pop, Male Voice, Acoustic Guitar")

if st.button("🚀 Bước 1: Tạo Prompt & Lời bài hát", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key!")
    elif not lyrics_input.strip():
        st.warning("Vui lòng nhập nội dung ý tưởng!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            Hãy tạo 2 phần cho Suno AI dựa trên: "{lyrics_input}" và phong cách "{tags_input}":
            1. STYLE PROMPT (Tiếng Anh, dưới 120 ký tự):
            2. LYRICS (Có các thẻ [Verse], [Chorus], [Outro]):
            """
            res = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
            st.success("Tạo Prompt thành công! Hãy copy nội dung bên dưới dán vào Suno.com để tạo bài hát:")
            st.markdown(res.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")

st.markdown("---")
st.subsection = st.markdown("### 🎧 Bước 2: Dán Link nhạc từ Suno để nghe/tải MP3 trực tiếp")

# 3. Ô dán link nhạc sau khi tạo bên Suno
suno_link = st.text_input(
    "Dán link bài hát Suno vào đây (Ví dụ: https://suno.com/song/xxx):",
    placeholder="https://suno.com/song/..."
)

if suno_link:
    # Tự động lấy file MP3 trực tiếp từ Suno
    if "suno.com/song/" in suno_link:
        song_id = suno_link.split("suno.com/song/")[-1].split("?")[0].strip()
        mp3_url = f"https://cdn1.suno.ai/{song_id}.mp3"
        
        st.success("🎵 Đã kết nối bài hát thành công!")
        # Trình phát nhạc MP3
        st.audio(mp3_url, format="audio/mp3")
        
        # Nút tải file MP3
        try:
            audio_data = requests.get(mp3_url).content
            st.download_button(
                label="⬇️ Tải file MP3 về máy",
                data=audio_data,
                file_name="bai_hat_suno.mp3",
                mime="audio/mp3"
            )
        except:
            st.info(f"Hoặc tải trực tiếp tại: {mp3_url}")
    else:
        st.warning("Link không đúng định dạng của Suno!")
