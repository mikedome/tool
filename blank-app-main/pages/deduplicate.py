import streamlit as st
import pandas as pd

def show():
    st.header("CSV 文件去重")
    
    uploaded_file = st.file_uploader("选择CSV文件", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"原始文件行数: {len(df)}")
            
            # 获取所有列名供用户选择
            columns = df.columns.tolist()
            
            # 选择用于去重的列
            dedup_columns = st.multiselect(
                "选择用于去重的列（默认使用所有列）",
                columns,
                default=columns
            )
            
            # 排序选项
            sort_column = st.selectbox(
                "选择排序列（可选）",
                ["不排序"] + columns
            )
            
            sort_order = st.radio(
                "排序方式",
                ["升序", "降序"]
            )
            
            if st.button("开始去重"):
                # 执行去重操作
                df_dedup = df.drop_duplicates(subset=dedup_columns)
                
                # 排序（如果选择了排序列）
                if sort_column != "不排序":
                    df_dedup = df_dedup.sort_values(
                        by=sort_column,
                        ascending=(sort_order == "升序")
                    )
                
                st.write(f"去重后行数: {len(df_dedup)}")
                st.write(f"删除重复行数: {len(df) - len(df_dedup)}")
                
                # 下载按钮
                csv = df_dedup.to_csv(index=False)
                st.download_button(
                    label="下载去重后的文件",
                    data=csv,
                    file_name="deduplicated.csv",
                    mime="text/csv"
                )
                
                st.success("去重完成！")
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")