import streamlit as st
from PIL import Image
import sys
import os

# Add libs directory to path
sys.path.insert(0, os.path.dirname(__file__))

# # Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "UI.py"

# Display header image
header_image = Image.open("D:\\UIT\\AI\\LegiSearch\\Source\\header.png")
st.image(header_image, width='stretch')
#Header
st.title("AI Tư vấn Bảo Hiểm Xã Hội Việt Nam")
st.subheader("Chào mừng bạn đến với ứng dụng tư vấn bảo hiểm xã hội!")
st.markdown("""
            Ứng dụng này sử dụng trí tuệ nhân tạo để cung cấp thông tin và tư vấn về các chính sách bảo hiểm xã hội tại Việt Nam.
            Bạn có thể hỏi về các loại bảo hiểm, quyền lợi, quy trình tham gia và nhiều hơn nữa. Vui lòng nhập từ khóa hoặc câu hỏi của bạn bên dưới để bắt đầu
            """)


## Sidebar menu
with st.sidebar:
    st.markdown("---")
    
    # col1, col2, col3 = st.columns([1, 1, 1])
    # # with col1:
    # #     if st.button("Hỏi đáp AI",icon =":material/psychology_alt:", use_container_width=True):
    # #         st.session_state.page = "hoi-dap"
    
    st.markdown("### Menu")

        
    if st.button("Hỏi đáp AI",key = "btn_hoi_dap",icon =":material/psychology_alt:", use_container_width=True):
        st.session_state.page = "hoi-dap"
    
    if st.button("Tra cứu văn bản", key="btn_tra_cuu", icon=":material/document_search:" , use_container_width=True):

        st.session_state.page = "tra-cuu"

    
    if st.button("Giới thiệu hệ thống", key="btn_gioi_thieu", icon=":material/stacks:", use_container_width=True):
        st.session_state.page = "gioi-thieu"
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #888;'>Phiên bản 1.0</p>", unsafe_allow_html=True)



# Display content based on selected page
if st.session_state.page == "tra-cuu":
    st.title("Tra cứu văn bản")
    st.switch_page("pages/tra-cuu.py")

elif st.session_state.page == "hoi-dap":
    st.title("Hỏi đáp AI")
    st.switch_page("pages/hoi-dap.py")
elif st.session_state.page == "gioi-thieu":
    st.title("Giới thiệu hệ thống")
    st.switch_page("pages/gioi-thieu.py")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Phiên bản 1.0</p>", unsafe_allow_html=True)   