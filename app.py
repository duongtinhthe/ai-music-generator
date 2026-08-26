import time
import requests
import streamlit as st

# Cấu hình trang web Streamlit
st.set_page_config(page_title="AI Music Maker", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Maker (Xuất MP3 thật)")
st.write("Tạo bài hát hoàn chỉnh (Lời + Nhạc nền + Ca sĩ hát) và tải file MP3 về máy.")

# 1. Ô nhập Lời bài hát
lyrics_input = st.text_area(
    "1. Lời bài hát (Lyrics)",
    height=180,
    placeholder="[Verse 1]\nĐêm nay mưa rơi rơi ngoài hiên\n[Chorus]\nLời ca cất lên nhẹ nhàng...",
)

# 2. Ô nhập Phong cách nhạc
tags_input = st.text_input(
    "2. Phong cách nhạc (Style/Genre)",
    value="V-Pop, Acoustic Guitar, Male Vocal, Melodic",
    placeholder="Ví dụ: V-Pop, R&B, Male Voice, Catchy",
)

# 3. Tiêu đề bài hát
title_input = st.text_input("3. Tiêu đề bài hát", value="Bài hát của tôi")

# Nút bấm Tạo Nhạc
if st.button("🚀 Tạo bài hát MP3", type="primary"):
    if not lyrics_input.strip():
        st.warning("Vui lòng nhập lời bài hát!")
    else:
        status_box = st.empty()
        status_box.info("⏳ Đang gửi yêu cầu phối khí và thu âm bài hát...")

        try:
            # Gửi yêu cầu tới Server tạo nhạc Suno API
            api_url = "https://suno-api-platform.vercel.app/api/generate"
            payload = {
                "prompt": lyrics_input,
                "tags": tags_input,
                "title": title_input,
                "make_instrumental": False,
                "wait_audio": True
            }

            response = requests.post(api_url, json=payload, timeout=120)
            data = response.json()

            if response.status_code == 200 and len(data) > 0:
                audio_url = data[0].get("audio_url")
                
                status_box.success("🎉 Tạo bài hát thành công!")
                st.markdown("---")

                # 1. Trình phát nhạc MP3 trực tiếp trên Web
                st.audio(audio_url, format="audio/mp3")

                # 2. Nút Tải file MP3 về máy
                audio_data = requests.get(audio_url).content
                st.download_button(
                    label="⬇️ Tải file MP3 bài hát về máy",
                    data=audio_data,
                    file_name=f"{title_input}.mp3",
                    mime="audio/mp3"
                )
            else:
                status_box.error("Server tạo nhạc đang bận, vui lòng bấm thử lại sau vài giây!")

        except Exception as e:
            # Phương án dự phòng nếu API endpoint gặp sự cố mạng
            status_box.error("Đang kết nối lại tới Server Music Engine...")
            st.info("Hệ thống đang tải lại phiên làm việc. Hãy bấm nút '🚀 Tạo bài hát MP3' một lần nữa.")
