# 网易云音乐数据分析系统

基于Python的网易云音乐热门歌单数据爬取、分析和可视化工具。

## 功能

- 爬取网易云音乐热门歌单数据
- 爬取歌单内的歌曲信息
- 生成15个可视化图表的HTML报告
- 数据导出为CSV格式

## 环境要求

- Windows系统
- Python 3.7+

## 安装

1. 克隆项目
```bash
git clone https://github.com/pahhcn/music163.git
cd music163
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用

运行主程序：
```bash
python main.py
```

按照菜单提示操作：
1. 爬取热门歌单数据（建议2-5页测试）
2. 爬取歌单内的歌曲
3. 数据分析
4. 生成可视化报告
5. 查看数据库统计
6. 导出数据为CSV
7. 清空数据库

## 可视化图表

报告包含15个图表：

**歌单分析（8个）**
- 播放量排行
- 收藏数排行
- 对比分析
- 标签分布
- 创建者排行
- 关系分析
- 规模分布
- 标签词云

**歌曲分析（7个）**
- 热门歌曲（按跨歌单出现次数）
- 歌手排行
- 时长分布
- 跨歌单热歌
- 专辑热度
- 热度分布
- 歌手雷达图

## 项目结构

```
music163/
├── analysis/          # 数据分析
├── config/            # 配置文件
├── data/              # SQLite数据库
├── database/          # 数据库管理
├── logs/              # 日志文件
├── output/            # 输出文件
│   └── reports/       # HTML报告
├── spider/            # 爬虫模块
├── utils/             # 工具函数
├── visualization/     # 可视化
├── main.py            # 主程序
└── requirements.txt   # 依赖包
```

## 技术栈

- requests - HTTP请求
- SQLite - 数据存储
- pandas - 数据处理
- pyecharts - 图表生成
- jieba - 中文分词

## 数据字段

**歌单数据**
- playlist_id, playlist_name, creator_name
- play_count, subscribed_count, track_count
- tags, description

**歌曲数据**
- song_id, song_name, artist, album
- duration, popularity, playlist_id
