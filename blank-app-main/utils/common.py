import pandas as pd
import streamlit as st
from typing import Optional, Union, List
import os
from config import ALLOWED_EXTENSIONS
import tempfile

def validate_file(file, file_type: str) -> bool:
    """验证文件类型"""
    if file is None:
        return False
    ext = os.path.splitext(file.name)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, [])

def read_file(file, file_type: str) -> Optional[pd.DataFrame]:
    """统一的文件读取函数"""
    try:
        if file_type == 'csv':
            return pd.read_csv(file)
        elif file_type == 'excel':
            return pd.read_excel(file)
        return None
    except Exception as e:
        st.error(f"读取文件失败: {str(e)}")
        return None

def save_dataframe(df: pd.DataFrame, 
                  filename: str,
                  file_type: str = 'csv') -> Optional[str]:
    """统一的数据保存函数"""
    try:
        # 使用临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as tmp:
            if file_type == 'csv':
                df.to_csv(tmp.name, index=False)
            elif file_type == 'excel':
                df.to_excel(tmp.name, index=False)
            return tmp.name
    except Exception as e:
        st.error(f"保存文件失败: {str(e)}")
        return None 