import streamlit as st
from rembg import remove
from PIL import Image
from streamlit_image_comparison import image_comparison
import easyocr as ocr  #OCR
import numpy as np

# set page config
st.set_page_config(page_title='My_First_Image_App', layout="centered")
st.subheader('[미니프로젝트] 이미지 배경제거 + 글자추출 웹서비스')
st.markdown('### :arrow_forward::sunglasses: Remove Background - `rembg`')
st.markdown("#### sample result")
image_comparison(
    img1 = "https://raw.githubusercontent.com/jaygil8755/first_app/3ccd1f9edd28745c8c7f63f1c839f87d29d46ab8/src/animal-1.jpg",
    img2 = "https://raw.githubusercontent.com/jaygil8755/first_app/3ccd1f9edd28745c8c7f63f1c839f87d29d46ab8/src/animal_rmbg.png",
    label1 = "원본 이미지",
    label2 = "배경제거 이미지",
    show_labels=True,
    make_responsive=True,
    in_memory=True)

st.markdown("### :arrow_forward: :ab:글자 추출(OCR) - `easyocr`")

option = st.selectbox(
    '어떤 서비스를 원하시나요?',
    ('배경제거', '글자추출'))

st.success(f'당신의 선택은: {option}')
if option == '배경제거':
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        input_ = Image.open(uploaded_file)
        st.image(input_, caption='원본 이미지', use_column_width=True)
        with st.spinner("🤖 열심히 작업 중..... "):
            output = remove(input_)
            st.image(output, caption='배경 제거 이미지', use_column_width=True)

if option == '글자추출':
    image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])
    @st.cache
    def load_model(): 
        reader = ocr.Reader(['ko', 'en'], model_storage_directory='.')
        return reader 
    
    reader = load_model() #load model
    
    if image is not None:
    
        input_image = Image.open(image) #read image
        st.image(input_image, caption='업로드한 이미지', use_column_width=True)
    
        with st.spinner("🤖 AI is at Work! "):

            # result = reader.readtext(image, detail = 0)    
            result = reader.readtext(np.array(input_image))
            result_text = [] #empty list for results
            for text in result:
                result_text.append(text[1])
    
            st.write(result_text)
        st.balloons()
    else:
        st.write("Upload an Image")

st.caption("감사합니다. 궁금하신 사항은 e-mail로 문의해주세요")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
