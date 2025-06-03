import streamlit as st
from functools import wraps
import traceback

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"错误: {str(e)}")
            if st.session_state.get('debug', False):
                st.error(f"详细错误信息:\n{traceback.format_exc()}")
            return None
    return wrapper 