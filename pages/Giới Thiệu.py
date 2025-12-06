import streamlit as st
import base64
from pathlib import Path


@st.cache_data
def get_base64_of_bin_file(bin_file: str) -> str:
		with open(bin_file, 'rb') as f:
				data = f.read()
		return base64.b64encode(data).decode()


st.set_page_config(page_title="Giới Thiệu", layout="wide")

# Path to the main image
IMG_PATH = Path(r"D:\UIT\AI\LegiSearch\Source\LawAI.jpg")
img_b64 = get_base64_of_bin_file(IMG_PATH)
# Path to the circular logo to show in the top-right of the visual
LOGO_PATH = Path(r"D:\UIT\AI\LegiSearch\Source\BHXHlogo.jpeg")
logo_b64 = get_base64_of_bin_file(LOGO_PATH)

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
	.hero .visual {{
		flex: 0 0 45%;
		height: 72vh;
		border-radius: 6px;
		background-image: url("data:image/jpg;base64,{img_b64}");
		background-size: cover;
		background-position: center right;
		box-shadow: 0 6px 24px rgba(0,0,0,0.4);
		border: 6px solid rgba(0,0,0,0.15);
		position: relative;
		overflow: hidden;
	}}
	/* small circular overlay logo in top-right of visual (placeholder) */
	.hero .visual:before {{
		content: '';
		position: absolute;
		top: 12px;
		right: 12px;
		width: 68px;
		height: 68px;
		border-radius: 50%;
		box-shadow: 0 4px 12px rgba(0,0,0,0.25);
		background-image: url("data:image/jpeg;base64,{logo_b64}");
		background-size: cover;
		background-position: center;
		border: 2px solid rgba(255,255,255,0.35);
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
		<h1>Chào mừng đến với AI Tư vấn Bảo Hiểm Xã Hội Việt Nam!</h1>
		<p class="lead">AI tư vấn bảo hiểm xã hội Việt Nam là hệ thống trợ lý thông minh giúp người dân tra cứu nhanh các thông tin về chế độ BHXH, BHYT, BHTN như mức đóng – hưởng, điều kiện nhận lương hưu, thời gian tham gia, hay thủ tục giải quyết hồ sơ.</p>
		<p class="small">Nhờ khả năng phân tích dữ liệu và trả lời tự động, AI giúp giảm thời gian chờ đợi, hạn chế sai sót khi tìm thông tin và hỗ trợ người lao động hiểu rõ quyền lợi của mình.</p>
	</div>
	<div class="visual"></div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

st.markdown("\n\n", unsafe_allow_html=True)

