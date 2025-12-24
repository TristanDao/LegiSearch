import streamlit as st
import base64 
from PIL import Image
import sys
import os
from pathlib import Path

#Gioi thieu
@st.cache_data
def get_base64_of_bin_file(bin_file: str) -> str:
		with open(bin_file, 'rb') as f:
				data = f.read()
		return base64.b64encode(data).decode()

BG_PATH = Path(r"D:\UIT\AI\LegiSearch\Source\LawAI.jpg")
bg_b64 = get_base64_of_bin_file(BG_PATH)
# Page configuration
st.set_page_config(page_title="Portfolio", layout="wide")
# HTML/CSS: hero layout with left text and right visual (image as background)
html = f"""
<style>
	.hero {{
		display: flex;
		gap: 2rem;
		align-items: center;
		justify-content: center;
		padding: 2rem;
		box-sizing: border-box;
		height: 82vh;
		background: linear-gradient(180deg, #0e4d66 0%, #1b5169 60%);
	}}
	.hero .content {{
		flex: 0 0 55%;
		color: #ffffff;
		padding: 2.2rem;
		border-radius: 8px;
		background: linear-gradient(180deg, rgba(0,0,0,0.45), rgba(0,0,0,0.35));
		box-shadow: 0 6px 18px rgba(0,0,0,0.35);
	}}
	.hero h1 {{
		font-family: 'Segoe UI', Roboto, Arial, sans-serif;
		font-size: 2.4rem;
		margin: 0 0 1rem 0;
		color: #ffd95a; /* warm yellow like design */
		font-style: italic;
		line-height: 1.1;
	}}
	.hero p.lead {{
		color: rgba(255,255,255,0.95);
		font-size: 1.05rem;
		margin-bottom: 1rem;
		line-height: 1.6;
	}}
	.hero p.small {{
		color: rgba(255,255,255,0.9);
		font-size: 0.98rem;
		line-height: 1.5;
	}}

	
	/* responsive: stack on small screens */
	@media (max-width: 900px) {{
		.hero {{
			flex-direction: column-reverse;
			height: auto;
			padding: 1rem;
		}}
		.hero .content, .hero .visual {{
			flex: 0 0 auto;
			width: 100%;
			height: auto;
		}}
		.hero .visual {{
			height: 38vh;
		}}
		.hero h1 {{ font-size: 1.6rem; }}
	}}
</style>

<div class="hero">
	<div class="content">
		<p class="lead">AI tư vấn bảo hiểm xã hội Việt Nam là hệ thống trợ lý thông minh giúp người dân tra cứu nhanh các thông tin về chế độ BHXH, BHYT, BHTN như mức đóng – hưởng, điều kiện nhận lương hưu, thời gian tham gia, hay thủ tục giải quyết hồ sơ.</p>
		<p class="small">Nhờ khả năng phân tích dữ liệu và trả lời tự động, AI giúp giảm thời gian chờ đợi, hạn chế sai sót khi tìm thông tin và hỗ trợ người lao động hiểu rõ quyền lợi của mình.</p>
	</div>
	<div class="visual"></div>
</div>
"""





# Title


st.markdown("""
<p style="color: #ffd95a; font-size: 1.2rem; line-height: 1.6; text-align: justify; padding: 1rem; background-color: rgba(0,0,0,0.45); border-radius: 10px;">
AI tư vấn bảo hiểm xã hội Việt Nam là hệ thống trợ lý thông minh giúp người dân tra cứu nhanh các thông tin về chế độ BHXH, BHYT, BHTN như mức đóng – hưởng, điều kiện nhận lương hưu, thời gian tham gia, hay thủ tục giải quyết hồ sơ. Nhờ khả năng phân tích dữ liệu và trả lời tự động, AI giúp giảm thời gian chờ đợi, hạn chế sai sót khi tìm thông tin và hỗ trợ người lao động hiểu rõ quyền lợi của mình.
</p>
""", unsafe_allow_html=True)
st.markdown(f"""
<style>
    .stMain {{
        background-image: url("data:image/jpg;base64,{bg_b64}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
            
    .main-title {{
        text-align: center;
        color: #0e4d66;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        padding: 1rem;
    }}
    
    .member-card {{
        display: flex;
        align-items: center;
        gap: 2rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .member-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    .member-image {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #0e4d66;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    .member-info {{
        color: white;
        flex: 1;
    }}
    
    .member-info h3 {{
        color: white;
        margin-bottom: 0.5rem;
        font-size: 1.5rem;
    }}
    
    .member-info ul {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}
    
    .member-info li {{
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        padding-left: 1.5rem;
        position: relative;
    }}
    
    .member-info li:before {{
        content: "•";
        position: absolute;
        left: 0;
        font-weight: bold;
        font-size: 1.5rem;
    }}
</style>

<h1 class="main-title"> Thành Viên Nhóm</h1>
""", unsafe_allow_html=True)

# Members data (you can customize this with actual data)
members = [
    {
        "name": "Ngô Phạm Thế Duy",
        "student_id": "25210013",
        "image_path": "Source\\Duy.jpg"
    },
    {
        "name": "Đào Phước Thịnh",
        "student_id": "25210038",
        "image_path": "Source\\DaoPhuocThinh.jpg"
    },
    {
        "name": "Trần Thị Tố Linh",
        "student_id": "25210018",
        "image_path": "Source\\TranThiToLinh.jpg"
    },
    {
        "name": "Lê Văn Mạnh",
        "student_id": "25210020",
        "image_path": "Source\\LeVanManh.jpg"
    },
    {
        "name": "Hoàng Tùng",
        "student_id": "25210049",
        "image_path": "Source\\Tung.jpg"
    },
    {
        "name": "Trần Xuân Hòa",
        "student_id": "25210016",
        "image_path": "Source\\Hoa.jpg"
    }
]

# Display members
for i, member in enumerate(members):
    # Create member card
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Try to load image, if not found use a placeholder
        try:
            img_path = Path(f"D:\\UIT\\AI\\LegiSearch\\{member['image_path']}")
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            else:
                # Placeholder if image doesn't exist
                st.markdown(f"""
                <div style="width: 150px; height: 150px; border-radius: 50%; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                display: flex; align-items: center; justify-content: center; 
                color: white; font-size: 3rem; font-weight: bold; margin: auto;">
                    {member['name'][0]}
                </div>
                """, unsafe_allow_html=True)
        except:
            # Fallback placeholder
            st.markdown(f"""
            <div style="width: 150px; height: 150px; border-radius: 50%; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            display: flex; align-items: center; justify-content: center; 
            color: white; font-size: 3rem; font-weight: bold; margin: auto;">
                {member['name'][0]}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="member-info">
            <ul>
                <li><strong>Họ và tên:</strong> {member['name']}</li>
                <li><strong>MSSV:</strong> {member['student_id']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Add some spacing between members
    st.markdown("<br>", unsafe_allow_html=True)
