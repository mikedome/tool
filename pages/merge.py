import streamlit as st
import pandas as pd

def show():
    st.header("合并 CSV 文件")
    
    uploaded_files = st.file_uploader("选择多个CSV文件", type=['csv'], accept_multiple_files=True)
    
    if uploaded_files:
        try:
            dfs = [pd.read_csv(file) for file in uploaded_files]
            
            # 获取所有文件的列名
            all_columns = dfs[0].columns.tolist()
            
            sort_column = st.selectbox(
                "选择排序列（可选）",
                ["不排序"] + all_columns
            )
            
            sort_order = st.radio(
                "排序方式",
                ["升序", "降序"]
            )
            
            if st.button("合并文件"):
                # 合并所有数据框
                merged_df = pd.concat(dfs, ignore_index=True)
                
                # 如果选择了排序列，进行排序
                if sort_column != "不排序":
                    merged_df = merged_df.sort_values(
                        by=sort_column,
                        ascending=(sort_order == "升序")
                    )
                
                # 创建下载按钮
                csv = merged_df.to_csv(index=False)
                st.download_button(
                    label="下载合并后的文件",
                    data=csv,
                    file_name="merged.csv",
                    mime="text/csv"
                )
                
                st.success(f"成功合并 {len(dfs)} 个文件，共 {len(merged_df)} 行")
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")