import streamlit as st
from PIL import Image

# Display header image
header_image = Image.open("header.png")
st.image(header_image, width='stretch')


st.title("AI Tư vấn Bảo Hiểm Xã Hội Việt Nam")
st.subheader("Chào mừng bạn đến với ứng dụng tư vấn bảo hiểm xã hội!")
st.markdown("""
            Ứng dụng này sử dụng trí tuệ nhân tạo để cung cấp thông tin và tư vấn về các chính sách bảo hiểm xã hội tại Việt Nam.
            Bạn có thể hỏi về các loại bảo hiểm, quyền lợi, quy trình tham gia và nhiều hơn nữa. Vui lòng nhập từ khóa hoặc câu hỏi của bạn bên dưới để bắt đầu
            """)
