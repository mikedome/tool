import streamlit as st
import pandas as pd

def show():
    st.header("筛选导出")
    
    uploaded_file = st.file_uploader("选择CSV文件", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"原始文件行数: {len(df)}")
            
            # 获取所有列名
            columns = df.columns.tolist()
            
            # 创建筛选条件
            st.subheader("设置筛选条件")
            
            filter_conditions = []
            for i in range(4):  # 最多4个筛选条件
                col1, col2 = st.columns(2)
                
                with col1:
                    column = st.selectbox(
                        f"选择列 {i+1}",
                        ["不筛选"] + columns,
                        key=f"col_{i}"
                    )
                
                if column != "不筛选":
                    with col2:
                        keyword = st.text_input(
                            f"输入关键词 {i+1}",
                            key=f"keyword_{i}"
                        )
                        if keyword:
                            filter_conditions.append((column, keyword))
            
            if st.button("开始筛选"):
                # 应用筛选条件
                filtered_df = df.copy()
                for column, keyword in filter_conditions:
                    filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(keyword, case=False, na=False)]
                
                st.write(f"筛选后行数: {len(filtered_df)}")
                
                # 预览筛选结果
                if len(filtered_df) > 0:
                    st.write("预览前5行：")
                    st.write(filtered_df.head())
                    
                    # 下载按钮
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="下载筛选结果",
                        data=csv,
                        file_name="filtered.csv",
                        mime="text/csv"
                    )
                    
                    st.success("筛选完成！")
                else:
                    st.warning("筛选结果为空！")
                
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")