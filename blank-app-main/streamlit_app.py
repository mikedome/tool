import streamlit as st
from pages import split, merge, deduplicate, convert, filter, juncai
from utils.error_handler import handle_errors
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面配置
def init_page():
    st.set_page_config(
        page_title="数据处理工具集",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 设置调试模式
    if 'debug' not in st.session_state:
        st.session_state.debug = os.getenv('DEBUG', 'False').lower() == 'true'

@handle_errors
def main():
    init_page()
    st.title("Ethan的工具集")
    
    # 侧边栏导航
    page = st.sidebar.selectbox(
        "选择功能",
        ["军采项目", "拆分 CSV", "合并 CSV", "CSV 去重", "格式转换", "筛选导出"]
    )
    
    # 页面路由
    pages = {
        "军采项目": juncai.show,
        "拆分 CSV": split.show,
        "合并 CSV": merge.show,
        "CSV 去重": deduplicate.show,
        "格式转换": convert.show,
        "筛选导出": filter.show
    }
    
    if page in pages:
        pages[page]()

if __name__ == "__main__":
    main() 