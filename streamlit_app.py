import streamlit as st
from pages import split, merge, deduplicate, convert, filter, juncai, policy
from utils.error_handler import handle_errors
from utils.github_sync import sync_all_files_to_github
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面配置
def init_page():
    st.set_page_config(
        page_title="Ethan的工具集",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 隐藏默认的页面导航菜单
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        div[data-testid="stSidebarNav"] {display: none;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # 设置调试模式
    if 'debug' not in st.session_state:
        st.session_state.debug = os.getenv('DEBUG', 'False').lower() == 'true'

@handle_errors
def main():
    init_page()
    
    # 添加GitHub同步按钮
    with st.sidebar:
        st.title("功能选择")
        if st.button("同步所有文件到GitHub"):
            with st.spinner('正在同步文件...'):
                sync_all_files_to_github()
        
        # 修改选择功能的顺序，确保政策申报显示在正确位置
        page = st.selectbox(
            "选择功能",
            [
                "军采项目",
                "政策申报",  # 确保这个选项存在
                "拆分 CSV",
                "合并 CSV",
                "CSV 去重",
                "格式转换",
                "筛选导出"
            ]
        )
    
    # 页面标题
    st.title("Ethan的工具集")
    
    # 页面路由
    if page == "政策申报":
        policy.show()
    elif page == "军采项目":
        juncai.show()
    elif page == "拆分 CSV":
        split.show()
    elif page == "合并 CSV":
        merge.show()
    elif page == "CSV 去重":
        deduplicate.show()
    elif page == "格式转换":
        convert.show()
    elif page == "筛选导出":
        filter.show()

if __name__ == "__main__":
    main() 
