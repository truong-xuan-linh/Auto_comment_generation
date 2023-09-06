import streamlit as st
from PIL import Image

#Trick to not init function multitime
if "get_comment" not in st.session_state:
    print("INIT MODEL")
    from src.comment import GetComment
    st.session_state.get_comment = GetComment()
    print("DONE INIT MODEL")

st.set_page_config(page_title="Auto Comment Generation", layout="wide", page_icon = "./storage/linhai.jpeg")
hide_menu_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html= True)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns(2)

#Sidebar
num_comments = st.sidebar.slider("Number of comments generated", 1, 10, 1)
type_generation = st.sidebar.radio("Type of comment generation", options=[0,1])

#LEFT COLUMN
with left_col:
    content = st.text_input("Enter your status", value="Hôm nay trời đẹp quá nhỉ")
    images = st.file_uploader("Choose an image file", key=1, accept_multiple_files=True, type=["jpg", "jpeg", "png", "webp", ])
    
if left_col.button("Generate"):
    info = {
        "content": content,
        "medias": images,
        "type_generation": type_generation,
        "num_comments": num_comments
    }
    
    #RIGHT COLUMN
    with right_col:
        st.write("**STATUS:** ", info["content"])
        st.write("**IMAGES:** ")
        st.image(info["medias"], width=100, caption=list(range(1, len(images) +1)))
        
        comments = st.session_state.get_comment.generator(info)
        for i, comment in enumerate(comments):
            st.write(f"**Comment {i+1}**: {comment}")        
