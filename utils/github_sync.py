import os
from github import Github
import streamlit as st
from datetime import datetime

def sync_all_files_to_github():
    try:
        # 从环境变量获取GitHub token
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            st.error("未找到GitHub访问令牌，请检查环境配置")
            return False
            
        # 初始化GitHub客户端
        g = Github(github_token)
        
        # 获取仓库 (替换为您的仓库名)
        repo = g.get_repo("your_username/your_repo")
        
        # 要同步的目录列表
        dirs_to_sync = ['src', 'pages', 'utils', 'data']
        # 要排除的文件和目录
        exclude_patterns = [
            '.git', '__pycache__', '.env', '.pyc', 
            '.DS_Store', '.idea', '.vscode'
        ]
        
        # 同步进度条
        progress_text = "正在同步文件..."
        progress_bar = st.progress(0)
        
        total_files = sum([len(files) for r, d, files in os.walk('.') 
                          if not any(ex in r for ex in exclude_patterns)])
        processed_files = 0
        
        # 同步所有文件
        for root, dirs, files in os.walk('.'):
            # 跳过排除的目录
            dirs[:] = [d for d in dirs if not any(ex in d for ex in exclude_patterns)]
            
            for file in files:
                # 跳过排除的文件
                if any(ex in file for ex in exclude_patterns):
                    continue
                    
                file_path = os.path.join(root, file)
                # 跳过二进制文件和特定格式文件
                if file.endswith(('.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe')):
                    continue
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 获取相对路径（去掉开头的./或.\）
                    github_path = file_path.replace('\\', '/')
                    if github_path.startswith('./') or github_path.startswith('.\\'):
                        github_path = github_path[2:]
                    
                    try:
                        # 检查文件是否存在
                        existing_file = repo.get_contents(github_path)
                        # 更新文件
                        repo.update_file(
                            github_path,
                            f"更新 {github_path} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            content,
                            existing_file.sha,
                            branch="main"
                        )
                        st.write(f"已更新: {github_path}")
                    except:
                        # 文件不存在，创建新文件
                        repo.create_file(
                            github_path,
                            f"创建 {github_path} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            content,
                            branch="main"
                        )
                        st.write(f"已创建: {github_path}")
                except Exception as e:
                    st.warning(f"处理文件 {file_path} 时出错: {str(e)}")
                    continue
                
                # 更新进度
                processed_files += 1
                progress_bar.progress(processed_files / total_files)
        
        progress_bar.progress(100)
        st.success("所有文件已成功同步到GitHub！")
        return True
        
    except Exception as e:
        st.error(f"同步到GitHub时发生错误: {str(e)}")
        return False 