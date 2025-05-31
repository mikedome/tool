import streamlit as st
import pandas as pd
import io

def show():
    st.header("格式转换")
    
    # 转换类型选择
    convert_type = st.radio(
        "选择转换类型",
        ["XLSX 转 CSV", "CSV 转 XLSX"]
    )
    
    if convert_type == "XLSX 转 CSV":
        uploaded_file = st.file_uploader("选择XLSX文件", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                # 读取Excel文件的所有sheet
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # 如果有多个sheet，让用户选择
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox("选择要转换的工作表", sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write(f"文件包含 {len(df)} 行数据")
                
                # 转换并下载
                csv = df.to_csv(index=False)
                st.download_button(
                    label="下载CSV文件",
                    data=csv,
                    file_name="converted.csv",
                    mime="text/csv"
                )
                
                st.success("转换完成！")
                
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")
    
    else:  # CSV 转 XLSX
        uploaded_file = st.file_uploader("选择CSV文件", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write(f"文件包含 {len(df)} 行数据")
                
                # 转换为Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                
                # 下载按钮
                st.download_button(
                    label="下载Excel文件",
                    data=output.getvalue(),
                    file_name="converted.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                st.success("转换完成！")
                
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")