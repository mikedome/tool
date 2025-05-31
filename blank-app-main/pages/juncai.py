import streamlit as st
import pandas as pd
import re
import os
import requests
import json
import chardet
import time
import subprocess
from typing import List, Dict
from utils.common import read_file, save_dataframe
from utils.components import file_uploader_with_preview

# ====================== 规则提取模块 ======================
class CompanyExtractor:
    """基于后缀向前查找的公司名称提取器"""
    
    def __init__(self, suffix_file: str = 'company_suffix.txt'):
        self.suffixes = self._load_suffixes(suffix_file)
        self.punctuation_pattern = re.compile(r'[，。、；：！？,.;:!?\s]')
        print(f"已加载 {len(self.suffixes)} 个公司后缀")
        
    def _load_suffixes(self, file_path: str) -> List[str]:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                suffixes = [line.strip() for line in f if line.strip()]
                print(f"从 {file_path} 加载的后缀: {suffixes[:5]}...")
                return suffixes
        default_suffixes = ['有限公司', '有限责任公司', '股份有限公司', '集团有限公司']
        print(f"使用默认后缀: {default_suffixes}")
        return default_suffixes

    def extract(self, text: str) -> List[str]:
        if not isinstance(text, str) or len(text.strip()) == 0:
            print("警告: 输入文本为空或非字符串类型")
            return []
            
        companies = []
        for suffix in self.suffixes:
            start_idx = 0
            while True:
                idx = text.find(suffix, start_idx)
                if idx == -1:
                    break
                end_idx = idx + len(suffix)
                punct_idx = -1
                for i in range(idx-1, -1, -1):
                    if self.punctuation_pattern.match(text[i]):
                        punct_idx = i
                        break
                if punct_idx != -1:
                    company_name = text[punct_idx+1:end_idx].strip()
                else:
                    company_name = text[:end_idx].strip()
                if len(company_name) >= 4 and re.search(r'[\u4e00-\u9fa5]', company_name):
                    companies.append(company_name)
                start_idx = end_idx
        return list({c for c in companies})  # 去重并返回

# ====================== 大模型清洗模块 ======================
class XFyunAPIClient:
    """讯飞大模型API客户端"""
    def __init__(self, apipassword: str, model: str = "Lite"):
        self.apipassword = apipassword
        self.model = model
        self.base_url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    
    def generate(self, messages: List[Dict]) -> Dict:
        """通用API调用方法"""
        headers = {
            "Authorization": f"Bearer {self.apipassword}",
            "Content-Type": "application/json",
            "host": "spark-api-open.xf-yun.com"
        }
        payload = {"model": self.model, "messages": messages, "temperature": 0.8}
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API请求失败: {e}")
            return {}

def find_url_column(df):
    """自动识别包含URL的列"""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    url_columns = []
    for column in df.columns:
        # 检查前5行是否包含URL
        sample = df[column].head().astype(str)
        if any(sample.str.contains(url_pattern)):
            url_columns.append(column)
    
    return url_columns

def auto_update():
    """一键更新军采数据流程"""
    st.subheader("军采数据一键更新")
    
    # 1. 上传新数据和历史数据
    col1, col2 = st.columns(2)
    with col1:
        new_file = st.file_uploader("上传新采集的数据", type=['csv'], key="new_data")
    with col2:
        history_file = st.file_uploader("上传历史数据(可选)", type=['csv'], key="history_data")
    
    if st.button("开始更新", key="start_update"):
        if not new_file:
            st.error("请上传新采集的数据文件")
            return
            
        with st.spinner("正在处理..."):
            try:
                # 读取新数据
                new_df = pd.read_csv(new_file)
                st.info(f"新数据包含 {len(new_df)} 条记录")
                
                # 2. 链接爬取
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 获取未爬取的链接
                empty_content = new_df[new_df['内容'].isna() | (new_df['内容'] == '')]
                total_links = len(empty_content)
                
                if total_links > 0:
                    st.warning(f"发现 {total_links} 个未爬取的链接")
                    
                    # 爬取进度跟踪
                    processed = 0
                    while True:
                        empty_content = new_df[new_df['内容'].isna() | (new_df['内容'] == '')]
                        if len(empty_content) == 0:
                            break
                            
                        for idx, row in empty_content.iterrows():
                            try:
                                # 这里调用您的链接爬取函数
                                # content = crawl_link(row['标题链接'])
                                # new_df.at[idx, '内容'] = content
                                
                                processed += 1
                                progress = processed / total_links
                                progress_bar.progress(progress)
                                status_text.text(f"已处理: {processed}/{total_links}")
                                
                                # 每10条保存一次
                                if processed % 10 == 0:
                                    temp_file = save_dataframe(new_df, "temp_crawled.csv")
                                    st.info(f"已保存临时文件: {temp_file}")
                                
                            except Exception as e:
                                st.error(f"处理链接失败: {row['标题链接']}, 错误: {str(e)}")
                                continue
                            
                        time.sleep(1)  # 避免请求过快
                
                # 3. 合并历史数据
                if history_file:
                    history_df = pd.read_csv(history_file)
                    st.info(f"历史数据包含 {len(history_df)} 条记录")
                    
                    # 合并数据
                    merged_df = pd.concat([history_df, new_df], ignore_index=True)
                    st.success(f"合并后共 {len(merged_df)} 条记录")
                    
                    # 4. 全字段去重
                    dedup_df = merged_df.drop_duplicates()
                    removed = len(merged_df) - len(dedup_df)
                    st.success(f"去重完成，删除了 {removed} 条重复记录")
                    
                    # 保存结果
                    final_file = save_dataframe(dedup_df, "updated_data.csv")
                    st.success(f"更新完成！结果已保存至: {final_file}")
                    
                    # 下载按钮
                    st.download_button(
                        label="下载更新后的数据",
                        data=dedup_df.to_csv(index=False),
                        file_name="updated_data.csv",
                        mime="text/csv"
                    )
                else:
                    # 如果没有历史数据，直接保存新数据
                    final_file = save_dataframe(new_df, "new_data.csv")
                    st.success(f"处理完成！结果已保存至: {final_file}")
                    
                    # 下载按钮
                    st.download_button(
                        label="下载处理后的数据",
                        data=new_df.to_csv(index=False),
                        file_name="new_data.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"处理过程中出错: {str(e)}")

def show():
    st.header("军采项目工具")
    
    # 使用选项卡布局
    tab1, tab2, tab3, tab4 = st.tabs(["一键更新", "启动程序", "链接解析", "API调用"])
    
    # 选项卡1：一键更新
    with tab1:
        auto_update()
    
    # 选项卡2：启动程序
    with tab2:
        st.subheader("启动后羿采集器")
        
        # 程序路径配置
        program_path = st.session_state.get('program_path', '')
        
        # 文件选择按钮
        exe_file = st.file_uploader("选择后羿采集器程序", type=['exe'], key="exe_selector")
        if exe_file:
            program_path = exe_file.name
            st.session_state['program_path'] = program_path
            st.success(f"已选择程序: {program_path}")
        
        # 手动输入路径
        program_path = st.text_input("或手动输入程序路径", value=program_path)
        
        if st.button("启动程序", key="start_program"):
            try:
                if os.path.exists(program_path):
                    subprocess.Popen(program_path)
                    st.success("程序已启动！")
                else:
                    st.error("找不到程序文件，请检查路径是否正确。")
            except Exception as e:
                st.error(f"启动程序时出错: {str(e)}")
    
    # 选项卡3：链接解析
    with tab3:
        st.subheader("链接解析")
        
        # 添加CSV文件上传功能
        csv_file = st.file_uploader("上传包含链接的CSV文件", type=['csv'], key="csv_uploader")
        
        if csv_file is not None:
            try:
                # 读取CSV文件
                df = pd.read_csv(csv_file)
                
                # 自动识别包含URL的列
                url_columns = find_url_column(df)
                
                if url_columns:
                    # 如果找到包含URL的列，让用户选择
                    selected_column = st.selectbox(
                        "选择包含链接的列",
                        url_columns,
                        key="url_column_selector"
                    )
                    
                    # 显示链接数量
                    num_urls = df[selected_column].count()
                    st.info(f"找到 {num_urls} 个链接")
                    
                    # 显示链接预览
                    if st.checkbox("预览链接", key="preview_urls"):
                        st.write(df[selected_column].head())
                    
                    # 解析按钮
                    if st.button("开始解析链接", key="parse_urls"):
                        urls = df[selected_column].dropna().tolist()
                        for url in urls:
                            try:
                                st.info(f"正在解析: {url}")
                                # 这里可以添加具体的链接解析逻辑
                            except Exception as e:
                                st.error(f"解析链接 {url} 时出错: {str(e)}")
                else:
                    st.warning("未在CSV文件中找到包含链接的列")
                
            except Exception as e:
                st.error(f"读取CSV文件时出错: {str(e)}")
        
        # 手动输入链接选项
        st.markdown("---")
        st.markdown("或手动输入链接：")
        input_url = st.text_area(
            "请输入需要解析的链接（每行一个）",
            height=100,
            key="url_input"
        )
        
        if st.button("解析手动输入的链接", key="parse_manual_urls"):
            if input_url:
                urls = input_url.strip().split('\n')
                for url in urls:
                    try:
                        st.info(f"正在解析: {url}")
                        # 这里可以添加具体的链接解析逻辑
                    except Exception as e:
                        st.error(f"解析链接 {url} 时出错: {str(e)}")
            else:
                st.warning("请输入需要解析的链接")
    
    # 选项卡4：API调用
    with tab4:
        st.subheader("中标公司名称提取(95%准确)")
        
        # API配置
        with st.expander("API配置", expanded=True):
            api_password = st.text_input(
                "API密钥", 
                value="epclnWKUULFRJAfzCbnv:pqhwjskGVgfwdPYqYcLL",
                type="password"
            )
        
        # 文件上传
        uploaded_file = st.file_uploader("上传CSV文件", type=['csv'], key="api_csv_uploader")
        
        if uploaded_file is not None:
            try:
                # 读取CSV预览
                df = pd.read_csv(uploaded_file)
                st.write("文件预览：")
                st.dataframe(df.head())
                
                # 选择内容列
                content_column = st.selectbox(
                    "选择内容列",
                    df.columns.tolist(),
                    index=df.columns.tolist().index("内容") if "内容" in df.columns else 0,
                    key="content_column_selector"
                )
                
                # 批处理设置
                batch_size = st.number_input("批处理大小", min_value=1, value=100, key="batch_size")
                
                if st.button("开始处理", key="start_processing"):
                    # 初始化工具
                    rule_extractor = CompanyExtractor()
                    
                    # 初始化进度条
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 初始化结果存储
                    results = []
                    total_rows = len(df)
                    
                    # 分批处理
                    for batch_start in range(0, total_rows, batch_size):
                        batch_end = min(batch_start + batch_size, total_rows)
                        batch_texts = df.iloc[batch_start:batch_end][content_column].tolist()
                        
                        status_text.text(f"处理批次：{batch_start+1}-{batch_end}/{total_rows}")
                        
                        # 规则提取
                        for text in batch_texts:
                            companies = rule_extractor.extract(str(text))
                            results.append("; ".join(companies))
                        
                        # 更新进度
                        progress = (batch_end) / total_rows
                        progress_bar.progress(progress)
                    
                    # 添加结果列
                    df['提取的公司'] = results
                    
                    # 显示结果预览
                    st.write("处理结果预览：")
                    st.dataframe(df.head())
                    
                    # 提供下载按钮
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="下载处理结果",
                        data=csv,
                        file_name="processed_results.csv",
                        mime="text/csv"
                    )
                    
                    status_text.text("处理完成！")
                    
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")

if __name__ == "__main__":
    show()
