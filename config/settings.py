"""
配置文件
包含项目所有配置参数
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库配置
DATABASE_CONFIG = {
    'db_path': os.path.join(BASE_DIR, 'data', 'music163.db'),
}

# 爬虫配置
SPIDER_CONFIG = {
    # 网易云音乐热歌榜URL
    'hot_songs_url': 'https://music.163.com/#/discover/toplist?id=3778678',
    # 所有榜单URL (飙升榜、新歌榜、热歌榜等)
    'all_playlist_url': 'https://music.163.com/#/discover/toplist',
    # 热门歌单广场URL
    'hot_playlists_url': 'https://music.163.com/#/discover/playlist',
    
    # 爬取设置 - 歌曲
    'max_songs': 100,  # 最大爬取歌曲数量
    'max_comments_per_song': 20,  # 每首歌最大评论数
    
    # 爬取设置 - 热门歌单
    'max_playlist_pages': 20,  # 最大爬取歌单页数（每页50个，20页=1000个歌单）
    'playlists_per_page': 50,  # 每页歌单数量
    'default_playlist_category': '全部',  # 默认歌单分类
    'default_playlist_order': 'hot',  # 默认排序方式（hot=最热，new=最新）
    
    # 超时设置
    'page_load_timeout': 30,  # 页面加载超时时间(秒)
    'element_wait_timeout': 10,  # 元素等待超时时间(秒)
    
    # 反爬策略
    'min_delay': 1,  # 最小延时(秒)
    'max_delay': 3,  # 最大延时(秒)
    'scroll_pause': 0.5,  # 滚动暂停时间(秒)
    
    # User-Agent列表
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ],
}

# API请求配置
API_CONFIG = {
    'base_url': 'https://music.163.com',
    'timeout': 10,  # 请求超时时间（秒）
    'max_retries': 3,  # 最大重试次数
    'retry_delay': 2,  # 重试延迟（秒）
}

# 输出目录配置
OUTPUT_CONFIG = {
    'data_dir': os.path.join(BASE_DIR, 'data'),
    'output_dir': os.path.join(BASE_DIR, 'output'),
    'reports_dir': os.path.join(BASE_DIR, 'output', 'reports'),
    'logs_dir': os.path.join(BASE_DIR, 'logs'),
    'csv_export_path': os.path.join(BASE_DIR, 'output', 'music_data.csv'),
}

# 可视化配置
VISUALIZATION_CONFIG = {
    # Pyecharts主题
    'theme': 'macarons',  # 可选: vintage, macarons, infographic, shine, roma
    
    # 图表配置
    'chart_width': '1400px',
    'chart_height': '600px',
    
    # 颜色方案
    'colors': [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
        '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
    ],
    
    # 报告配置
    'report_title': '网易云音乐数据分析报告',
    'report_filename': 'music_analysis_report.html',
}

# 日志配置
LOG_CONFIG = {
    'log_dir': os.path.join(BASE_DIR, 'logs'),
    'log_filename': 'music163.log',
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,  # 保留5个备份
}

# 数据分析配置
ANALYSIS_CONFIG = {
    'top_n_songs': 20,  # TOP N 热歌
    'top_n_artists': 15,  # TOP N 歌手
    'min_comment_length': 5,  # 最小评论长度(用于词云)
    'wordcloud_max_words': 200,  # 词云最大词数
    'wordcloud_width': 1200,
    'wordcloud_height': 600,
}

# 创建必要的目录
def create_directories():
    """创建项目所需的目录"""
    dirs = [
        OUTPUT_CONFIG['data_dir'],
        OUTPUT_CONFIG['output_dir'],
        OUTPUT_CONFIG['reports_dir'],
        OUTPUT_CONFIG['logs_dir'],
    ]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"创建目录: {dir_path}")

if __name__ == '__main__':
    create_directories()

