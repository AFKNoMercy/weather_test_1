import streamlit as st
import requests
import os

# Lấy API key từ biến môi trường (Streamlit secrets)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --- Hàm lấy dữ liệu thời tiết ---
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tomorrow_data = data['list'][1]  # Dự báo gần nhất của ngày mai (3h một bản)
        return {
            "temp": tomorrow_data["main"]["temp"],
            "desc": tomorrow_data["weather"][0]["description"],
            "humidity": tomorrow_data["main"]["humidity"],
            "wind": tomorrow_data["wind"]["speed"]
        }
    else:
        return None

# --- Hàm gợi ý trang phục ---
def suggest_outfit(temp):
    if temp < 15:
        return "🌬️ Trời lạnh, bạn nên mặc áo khoác dày, khăn và nón ấm."
    elif 15 <= temp < 25:
        return "🍂 Thời tiết mát mẻ, áo dài tay hoặc áo khoác nhẹ là phù hợp."
    else:
        return "☀️ Trời nóng, mặc đồ mát, áo thun và quần short là hợp lý."

# --- Hàm gợi ý biện pháp thời tiết ---
def weather_advice(desc):
    if "mưa" in desc:
        return "☔ Mang theo ô và áo mưa khi ra ngoài nhé."
    elif "nắng" in desc:
        return "🧴 Dùng kem chống nắng và đeo kính râm để bảo vệ da."
    elif "gió" in desc:
        return "💨 Cẩn thận gió mạnh, tránh ra ngoài nếu không cần thiết."
    else:
        return "✅ Không có hiện tượng thời tiết đặc biệt cần lo lắng."

# --- Gợi ý món ăn theo nhiệt độ ---
def food_suggestion(temp):
    if temp < 15:
        return "🍜 Một tô phở, lẩu hoặc cháo nóng sẽ rất tuyệt!"
    elif 15 <= temp < 25:
        return "🥘 Hãy thử bún bò, hủ tiếu hoặc cơm tấm nhé."
    else:
        return "🍹 Trời nóng, trà sữa, sinh tố hoặc gỏi cuốn sẽ mát lành."

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Trợ lý thời tiết AI", page_icon="🌤️")
st.title("🌤️ Trợ Lý Thời Tiết AI")

city = st.text_input("🌍 Nhập tên thành phố (VD: Hanoi, Ho Chi Minh)    (* Nên viết không dấu)", "Hanoi")

if st.button("Xem dự báo"):
    weather = get_weather(city)
    if weather:
        st.subheader(f"📆 Dự báo thời tiết ngày mai tại {city.title()}:")
        st.write(f"🌡️ Nhiệt độ: {weather['temp']}°C")
        st.write(f"🌦️ Thời tiết: {weather['desc']}")
        st.write(f"💧 Độ ẩm: {weather['humidity']}%")
        st.write(f"💨 Gió: {weather['wind']} m/s")

        st.subheader("👕 Gợi ý trang phục:")
        st.info(suggest_outfit(weather['temp']))

        st.subheader("🛡️ Biện pháp phòng tránh:")
        st.warning(weather_advice(weather['desc']))

        st.subheader("🍽️ Gợi ý món ăn phù hợp:")
        st.success(food_suggestion(weather['temp']))
    else:
        st.error("❌ Không thể lấy dữ liệu. Kiểm tra tên thành phố hoặc API key.")
