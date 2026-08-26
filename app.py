import time
import requests
import streamlit as st

st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Generator")
st.write("Nhập lời bài hát & phong cách để xuất trực tiếp file MP3 nghe trên web hoặc tải về.")

# 1. Nhập Suno Cookie / API Endpoint
with st.expander("⚙️ Cấu hình Server (Nếu cần)"):
    api_url = st.text_input(
        "Suno API Endpoint:",
        value="https://suno-api-platform.vercel.app/api/generate",
        help="Đường dẫn Server API xử lý tạo nhạc"
    )

# 2. Nhập Lời bài hát
lyrics_input = st.text_area(
    "1. Nhập Lời bài hát (Lyrics):",
    height=200,
    placeholder="[Verse 1]\nPhố xá lung linh ánh đèn\n[Chorus]\nGiai điệu nhẹ nhàng cất lên...",
)

# 3. Nhập Phong cách bài hát
tags_input = st.text_input(
    "2. Nhập Phong cách bài hát (Style):",
    value="V-Pop, Acoustic Guitar, Male Vocal, Melodic",
    placeholder="Ví dụ: V-Pop, R&B, Male Voice, Melodic",
)

# 4. Tiêu đề
title_input = st.text_input("3. Tiêu đề bài hát:", value="Bài hát của tôi")

# Nút Tạo bài hát MP3
if st.button("🚀 Tạo bài hát MP3", type="primary"):
    if not lyrics_input.strip():
        st.warning("Vui lòng nhập lời bài hát!")
    elif not tags_input.strip():
        st.warning("Vui lòng nhập phong cách bài hát!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Đang gửi lời bài hát tới Music Engine để phối khí và tạo file MP3...")

        try:
            payload = {
                "prompt": lyrics_input,
                "tags": tags_input,
                "title": title_input,
                "make_instrumental": False,
                "wait_audio": True
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=payload, headers=headers, timeout=120)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    song_data = data[0]
                    audio_url = song_data.get("audio_url")

                    if audio_url:
                        status_box.success("🎉 Đã tạo xong bài hát MP3!")
                        st.markdown("---")

                        # Trình phát nhạc nghe trực tiếp
                        st.audio(audio_url, format="audio/mp3")

                        # Nút Tải file MP3 về máy
                        audio_bytes = requests.get(audio_url).content
                        st.download_button(
                            label="⬇️ Tải file MP3 về máy",
                            data=audio_bytes,
                            file_name=f"{title_input}.mp3",
                            mime="audio/mp3"
                        )
                    else:
                        status_box.error("Không tìm thấy link âm thanh trả về từ Server.")
                else:
                    status_box.error("Phản hồi từ Server không đúng định dạng.")
            else:
                status_box.error(f"Lỗi Server (Mã {response.status_code}). Vui lòng thử lại sau vài giây.")

        except Exception as e:
            status_box.error(f"Lỗi kết nối: {e}")
