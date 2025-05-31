import streamlit as st
import pandas as pd
from typing import List
from utils.common import read_file

def file_uploader_with_preview(label: str, 
                             file_type: List[str],
                             key: str = None):
    """带预览的文件上传组件"""
    file = st.file_uploader(label, type=file_type, key=key)
    if file:
        df = read_file(file, file_type[0])
        if df is not None:
            st.write("文件预览：")
            st.dataframe(df.head())
        return df
    return None

def download_button_with_preview(df: pd.DataFrame,
                               filename: str,
                               label: str = "下载文件"):
    """带预览的下载按钮"""
    if df is not None:
        st.write("结果预览：")
        st.dataframe(df.head())
        csv = df.to_csv(index=False)
        st.download_button(
            label=label,
            data=csv,
            file_name=filename,
            mime="text/csv"
        ) 