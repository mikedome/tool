import streamlit as st
import pandas as pd
from utils.csv_operations import CSVOperations
import io

def show():
    st.header("拆分 CSV 文件")
    
    uploaded_file = st.file_uploader("选择CSV文件", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"文件总行数: {len(df)}")
            
            rows_per_file = st.number_input(
                "每个文件的行数",
                min_value=1,
                max_value=len(df),
                value=min(1000, len(df))
            )
            
            if st.button("拆分文件"):
                split_dfs = CSVOperations.split_csv(df, rows_per_file)
                
                for i, split_df in enumerate(split_dfs, 1):
                    # 创建下载按钮
                    csv = split_df.to_csv(index=False)
                    st.download_button(
                        label=f"下载第 {i} 个文件",
                        data=csv,
                        file_name=f"split_{i}.csv",
                        mime="text/csv"
                    )
                
                st.success(f"成功将文件拆分为 {len(split_dfs)} 个部分")
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")