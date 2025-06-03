"""配置文件，用于存储全局配置"""
import os
import tempfile

# 文件路径配置
UPLOAD_FOLDER = tempfile.gettempdir()
DOWNLOAD_FOLDER = tempfile.gettempdir()
TEMP_FOLDER = tempfile.gettempdir()

# 确保必要的目录存在
for folder in [UPLOAD_FOLDER, DOWNLOAD_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# 文件大小限制
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 增加到 200MB

# 支持的文件类型
ALLOWED_EXTENSIONS = {
    'csv': ['.csv'],
    'excel': ['.xlsx', '.xls'],
} 