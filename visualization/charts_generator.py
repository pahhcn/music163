"""
网易云音乐热门歌单数据可视化模块
使用Pyecharts生成交互式图表
"""
import os
from typing import List, Dict, Any
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, Scatter, Radar, WordCloud as PyWordCloud, Page, Funnel
from pyecharts.globals import ThemeType

from config.settings import VISUALIZATION_CONFIG, OUTPUT_CONFIG
from utils.logger import get_logger

logger = get_logger()


class ChartsGenerator:
    """热门歌单可视化图表生成器"""
    
    def __init__(self, db_manager):
        """
        初始化图表生成器
        :param db_manager: 数据库管理器实例
        """
        self.db = db_manager
        self.theme = self._get_theme()
        self.colors = VISUALIZATION_CONFIG['colors']
    
    def _get_theme(self):
        """获取主题"""
        theme_map = {
            'vintage': ThemeType.VINTAGE,
            'macarons': ThemeType.MACARONS,
            'infographic': ThemeType.INFOGRAPHIC,
            'shine': ThemeType.SHINE,
            'roma': ThemeType.ROMA,
        }
        theme_name = VISUALIZATION_CONFIG['theme']
        return theme_map.get(theme_name, ThemeType.MACARONS)
    
    def _create_no_data_chart(self, title: str, subtitle: str, message: str) -> Bar:
        """
        创建无数据提示图表
        :param title: 图表标题
        :param subtitle: 副标题
        :param message: 提示信息
        :return: Bar图表对象
        """
        try:
            # 创建一个简单的柱状图显示提示信息
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(["提示"])
                .add_yaxis(
                    "数据状态",
                    [0],
                    color='#E0E0E0',
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(color='#E0E0E0')
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"📊 {title}",
                        subtitle=f"{subtitle}\n\n{message}",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold"),
                        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=16, color="#666")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(is_show=False),
                        axisline_opts=opts.AxisLineOpts(is_show=False),
                        axistick_opts=opts.AxisTickOpts(is_show=False)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(is_show=False),
                        axisline_opts=opts.AxisLineOpts(is_show=False),
                        axistick_opts=opts.AxisTickOpts(is_show=False),
                        splitline_opts=opts.SplitLineOpts(is_show=False)
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    legend_opts=opts.LegendOpts(is_show=False)
                )
            )
            return bar
        except Exception as e:
            logger.error(f"创建无数据图表失败: {e}")
            return None
    
    def _create_no_data_pie(self, title: str, subtitle: str, message: str) -> Pie:
        """
        创建无数据提示饼图
        :param title: 图表标题
        :param subtitle: 副标题
        :param message: 提示信息
        :return: Pie图表对象
        """
        try:
            # 创建一个简单的饼图显示提示信息
            pie = (
                Pie(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add(
                    "",
                    [("暂无数据", 1)],
                    radius=["30%", "75%"],
                    center=["50%", "50%"],
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(color='#E0E0E0')
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"📊 {title}",
                        subtitle=f"{subtitle}\n\n{message}",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold"),
                        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=16, color="#666"),
                        pos_left="center",
                        pos_top="5%"
                    ),
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
            return pie
        except Exception as e:
            logger.error(f"创建无数据饼图失败: {e}")
            return None
    
    def create_top_playlists_bar(self, top_n: int = 30, order_by: str = 'play_count') -> Bar:
        """
        创建TOP热门歌单柱状图
        :param top_n: TOP N
        :param order_by: 排序字段
        :return: Bar图表对象
        """
        try:
            top_playlists = self.db.get_top_playlists(top_n, order_by)
            
            if not top_playlists:
                logger.warning("没有歌单数据,无法生成柱状图")
                return None
            
            # 提取数据
            playlist_names = [f"{p['playlist_name'][:20]}..." if len(p['playlist_name']) > 20 
                            else p['playlist_name'] for p in top_playlists]
            values = [p.get(order_by, 0) for p in top_playlists]
            
            title_map = {
                'play_count': '播放量',
                'subscribed_count': '收藏数',
                'track_count': '歌曲数'
            }
            
            # 创建柱状图
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(playlist_names)
                .add_yaxis(
                    title_map.get(order_by, order_by),
                    values,
                    color=self.colors[0],
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#5470c6'
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"TOP {top_n} 热门歌单{title_map.get(order_by, '')}排行",
                        subtitle="数据来源: 网易云音乐",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name=title_map.get(order_by, ''),
                        axislabel_opts=opts.LabelOpts(formatter="{value}")
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="axis",
                        axis_pointer_type="shadow",
                        formatter="{b}<br/>{a}: {c}"
                    ),
                    datazoom_opts=[
                        opts.DataZoomOpts(type_="slider", range_start=0, range_end=50),
                        opts.DataZoomOpts(type_="inside")
                    ],
                )
            )
            
            logger.info(f"TOP歌单{title_map.get(order_by, '')}柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建柱状图失败: {e}")
            return None
    
    def create_playlist_comparison_bar(self, top_n: int = 20) -> Bar:
        """
        创建歌单播放量与收藏数对比柱状图
        :param top_n: TOP N
        :return: Bar图表对象
        """
        try:
            top_playlists = self.db.get_top_playlists(top_n, 'play_count')
            
            if not top_playlists:
                logger.warning("没有歌单数据")
                return None
            
            playlist_names = [f"{p['playlist_name'][:15]}..." if len(p['playlist_name']) > 15 
                            else p['playlist_name'] for p in top_playlists]
            play_counts = [p['play_count'] for p in top_playlists]
            subscribe_counts = [p['subscribed_count'] for p in top_playlists]
            
            bar = (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="1400px", height="700px"))
                .add_xaxis(playlist_names)
                .add_yaxis("播放量", play_counts, color=self.colors[0])
                .add_yaxis("收藏数", subscribe_counts, color=self.colors[1])
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"TOP {top_n} 热门歌单 播放量 vs 收藏数",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=9)
                    ),
                    yaxis_opts=opts.AxisOpts(name="数量"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider")],
                )
            )
            
            logger.info("歌单对比柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建对比柱状图失败: {e}")
            return None
    
    def create_tags_pie(self, top_n: int = 15) -> Pie:
        """
        创建歌单标签分布饼图
        :param top_n: TOP N 标签
        :return: Pie图表对象
        """
        try:
            playlists = self.db.get_all_playlists()
            
            if not playlists:
                logger.warning("没有歌单数据")
                return None
            
            # 统计标签
            tags_count = {}
            for playlist in playlists:
                tags_str = playlist.get('tags', '')
                if tags_str:
                    tags_list = tags_str.split(',')
                    for tag in tags_list:
                        tag = tag.strip()
                        if tag:
                            tags_count[tag] = tags_count.get(tag, 0) + 1
            
            # 排序并取TOP N
            sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            if not sorted_tags:
                logger.warning("没有标签数据")
                return None
            
            pie = (
                Pie(init_opts=opts.InitOpts(theme=self.theme, width="1200px", height="700px"))
                .add(
                    "",
                    sorted_tags,
                    radius=["30%", "75%"],
                    rosetype="area",
                    label_opts=opts.LabelOpts(formatter="{b}: {d}%", font_size=12)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"热门歌单标签分布 TOP {top_n}",
                        subtitle=f"共统计 {len(tags_count)} 个标签",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    legend_opts=opts.LegendOpts(
                        orient="vertical",
                        pos_left="left",
                        pos_top="15%"
                    ),
                    tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} 个歌单 ({d}%)")
                )
                .set_colors(self.colors)
            )
            
            logger.info("标签饼图创建成功")
            return pie
            
        except Exception as e:
            logger.error(f"创建饼图失败: {e}")
            return None
    
    def create_creator_contribution_bar(self, top_n: int = 20) -> Bar:
        """
        创建歌单创建者贡献度柱状图
        :param top_n: TOP N 创建者
        :return: Bar图表对象
        """
        try:
            playlists = self.db.get_all_playlists()
            
            if not playlists:
                logger.warning("没有歌单数据")
                return None
            
            # 统计创建者
            creator_stats = {}
            for playlist in playlists:
                creator = playlist.get('creator_name', '未知')
                if creator not in creator_stats:
                    creator_stats[creator] = {
                        'count': 0,
                        'total_play': 0,
                        'total_subscribe': 0
                    }
                creator_stats[creator]['count'] += 1
                creator_stats[creator]['total_play'] += playlist.get('play_count', 0)
                creator_stats[creator]['total_subscribe'] += playlist.get('subscribed_count', 0)
            
            # 排序并取TOP N
            sorted_creators = sorted(creator_stats.items(), 
                                   key=lambda x: x[1]['count'], 
                                   reverse=True)[:top_n]
            
            creators = [item[0] for item in sorted_creators]
            counts = [item[1]['count'] for item in sorted_creators]
            
            bar = (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="1400px", height="700px"))
                .add_xaxis(creators)
                .add_yaxis(
                    "歌单数量",
                    counts,
                    color=self.colors[2],
                    label_opts=opts.LabelOpts(position="top"),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#91cc75'
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"TOP {top_n} 热门歌单创建者",
                        subtitle="按上榜歌单数量排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=30, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌单数量"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
                )
            )
            
            logger.info("创建者贡献度柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建创建者柱状图失败: {e}")
            return None
    
    def create_play_subscribe_scatter(self, sample_size: int = 200) -> Scatter:
        """
        创建播放量与收藏数关系散点图
        :param sample_size: 采样数量
        :return: Scatter图表对象
        """
        try:
            playlists = self.db.get_all_playlists()[:sample_size]
            
            if not playlists:
                logger.warning("没有歌单数据")
                return None
            
            data = []
            for p in playlists:
                play = p.get('play_count', 0)
                subscribe = p.get('subscribed_count', 0)
                name = p.get('playlist_name', '')[:20]
                data.append({
                    "value": [play, subscribe],
                    "name": name
                })
            
            scatter = (
                Scatter(init_opts=opts.InitOpts(theme=self.theme, width="1200px", height="700px"))
                .add_xaxis([d['value'][0] for d in data])
                .add_yaxis(
                    "歌单",
                    [d['value'][1] for d in data],
                    symbol_size=12,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .set_series_opts(
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#5470c6'
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="歌单播放量与收藏数关系分析",
                        subtitle=f"样本数: {len(data)}",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        name="播放量",
                        type_="value",
                        splitline_opts=opts.SplitLineOpts(is_show=True)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="收藏数",
                        type_="value",
                        splitline_opts=opts.SplitLineOpts(is_show=True)
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        formatter="{b}<br/>播放: {c[0]}<br/>收藏: {c[1]}"
                    ),
                    visualmap_opts=opts.VisualMapOpts(
                        type_="size",
                        max_=max([d['value'][1] for d in data]) if data else 100,
                        min_=min([d['value'][1] for d in data]) if data else 0,
                        dimension=1
                    ),
                )
            )
            
            logger.info("播放量收藏数散点图创建成功")
            return scatter
            
        except Exception as e:
            logger.error(f"创建散点图失败: {e}")
            return None
    
    def create_playlist_scale_pie(self) -> Pie:
        """
        创建歌单规模分布饼图（按歌曲数量分类）
        :return: Pie图表对象
        """
        try:
            playlists = self.db.get_all_playlists()
            
            if not playlists:
                logger.warning("没有歌单数据")
                return None
            
            # 分类统计
            scale_categories = {
                '超大型(500+首)': 0,
                '大型(200-500首)': 0,
                '中型(100-200首)': 0,
                '小型(50-100首)': 0,
                '迷你型(<50首)': 0
            }
            
            for p in playlists:
                track_count = p.get('track_count', 0)
                if track_count >= 500:
                    scale_categories['超大型(500+首)'] += 1
                elif track_count >= 200:
                    scale_categories['大型(200-500首)'] += 1
                elif track_count >= 100:
                    scale_categories['中型(100-200首)'] += 1
                elif track_count >= 50:
                    scale_categories['小型(50-100首)'] += 1
                else:
                    scale_categories['迷你型(<50首)'] += 1
            
            data_pair = [(k, v) for k, v in scale_categories.items() if v > 0]
            
            pie = (
                Pie(init_opts=opts.InitOpts(theme=self.theme, width="1000px", height="600px"))
                .add(
                    "",
                    data_pair,
                    radius=["40%", "70%"],
                    label_opts=opts.LabelOpts(formatter="{b}\n{c}个 ({d}%)", font_size=12)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="歌单规模分布",
                        subtitle=f"总计 {len(playlists)} 个歌单",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight="bold")
                    ),
                    legend_opts=opts.LegendOpts(
                        orient="vertical",
                        pos_left="left",
                        pos_top="20%"
                    ),
                    tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} 个 ({d}%)")
                )
                .set_colors(self.colors)
            )
            
            logger.info("歌单规模饼图创建成功")
            return pie
            
        except Exception as e:
            logger.error(f"创建规模饼图失败: {e}")
            return None
    
    def create_tags_wordcloud(self) -> PyWordCloud:
        """
        创建歌单标签词云图
        :return: WordCloud图表对象
        """
        try:
            playlists = self.db.get_all_playlists()
            
            if not playlists:
                logger.warning("没有歌单数据")
                return None
            
            # 统计标签
            tags_count = {}
            for playlist in playlists:
                tags_str = playlist.get('tags', '')
                if tags_str:
                    tags_list = tags_str.split(',')
                    for tag in tags_list:
                        tag = tag.strip()
                        if tag:
                            tags_count[tag] = tags_count.get(tag, 0) + 1
            
            if not tags_count:
                logger.warning("没有标签数据")
                return None
            
            # 转换为词云需要的格式
            word_data = [(tag, count) for tag, count in tags_count.items()]
            
            wordcloud = (
                PyWordCloud(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1200px",
                    height="700px"
                ))
                .add(
                    "",
                    word_data,
                    word_size_range=[20, 120],
                    shape='circle',
                    textstyle_opts=opts.TextStyleOpts(font_family="Microsoft YaHei")
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="热门歌单标签词云",
                        subtitle=f"共 {len(tags_count)} 个标签",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b}: {c} 个歌单")
                )
            )
            
            logger.info("标签词云图创建成功")
            return wordcloud
            
        except Exception as e:
            logger.error(f"创建词云图失败: {e}")
            return None
    
    # ==================== 歌曲相关图表 ====================
    
    def create_top_songs_bar(self, top_n: int = 30) -> Bar:
        """
        创建TOP热门歌曲柱状图
        :param top_n: TOP N
        :return: Bar图表对象
        """
        try:
            top_songs = self.db.get_top_songs(top_n, 'popularity')
            
            if not top_songs:
                logger.warning("没有歌曲数据")
                return self._create_no_data_chart("热门歌曲排行", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            # 提取数据
            song_names = [f"{s['song_name'][:20]}..." if len(s['song_name']) > 20 
                         else s['song_name'] for s in top_songs]
            popularities = [s.get('popularity', 0) for s in top_songs]
            
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(song_names)
                .add_yaxis(
                    "热度",
                    popularities,
                    color=self.colors[3],
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"TOP {top_n} 热门歌曲排行",
                        subtitle="按热度值排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="热度值"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
                    datazoom_opts=[
                        opts.DataZoomOpts(type_="slider", range_start=0, range_end=50),
                        opts.DataZoomOpts(type_="inside")
                    ],
                )
            )
            
            logger.info("TOP歌曲柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建歌曲柱状图失败: {e}")
            return None
    
    def create_artist_bar(self, top_n: int = 20) -> Bar:
        """
        创建TOP歌手柱状图
        :param top_n: TOP N
        :return: Bar图表对象
        """
        try:
            # 使用数据库查询歌手统计
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_no_data_chart("歌手排行榜", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            # 统计歌手歌曲数
            from collections import Counter
            artist_counts = Counter([s['artist'] for s in songs if s.get('artist')])
            top_artists = artist_counts.most_common(top_n)
            
            artists = [a[0] for a in top_artists]
            counts = [a[1] for a in top_artists]
            
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(artists)
                .add_yaxis(
                    "歌曲数量",
                    counts,
                    color=self.colors[1],
                    label_opts=opts.LabelOpts(position="top")
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"TOP {top_n} 热门歌手",
                        subtitle="按歌曲数量排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=30, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌曲数量"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
                )
            )
            
            logger.info("歌手柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建歌手柱状图失败: {e}")
            return None
    
    def create_song_duration_pie(self) -> Pie:
        """
        创建歌曲时长分布饼图
        :return: Pie图表对象
        """
        try:
            songs = self.db.get_all_songs()
            if not songs:
                # 对于饼图，我们创建一个特殊的无数据饼图
                return self._create_no_data_pie("歌曲时长分布", "暂无歌曲数据", 
                    "请先爬取歌曲数据：运行 python main.py，选择 '2 - 爬取歌单歌曲'")
            
            # 统计时长分布
            import pandas as pd
            df = pd.DataFrame(songs)
            durations_sec = df['duration'] / 1000
            
            very_short = len(durations_sec[durations_sec <= 120])
            short = len(durations_sec[(durations_sec > 120) & (durations_sec <= 180)])
            medium = len(durations_sec[(durations_sec > 180) & (durations_sec <= 300)])
            long_duration = len(durations_sec[(durations_sec > 300) & (durations_sec <= 420)])
            very_long = len(durations_sec[durations_sec > 420])
            
            data = [
                ("极短(≤2分钟)", very_short),
                ("短(2-3分钟)", short),
                ("中等(3-5分钟)", medium),
                ("长(5-7分钟)", long_duration),
                ("超长(>7分钟)", very_long)
            ]
            
            # 过滤掉数量为0的分类
            data = [(name, count) for name, count in data if count > 0]
            
            pie = (
                Pie(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add(
                    "时长分布",
                    data,
                    radius=["30%", "75%"],
                    center=["50%", "50%"],
                    rosetype="area",
                    label_opts=opts.LabelOpts(
                        formatter="{b}\n{c}首 ({d}%)",
                        font_size=14,
                        font_weight="bold"
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="🎵 歌曲时长分布",
                        subtitle=f"总计 {len(df)} 首歌曲",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold"),
                        pos_left="center",
                        pos_top="5%"
                    ),
                    legend_opts=opts.LegendOpts(
                        orient="vertical", 
                        pos_top="20%", 
                        pos_left="2%",
                        textstyle_opts=opts.TextStyleOpts(font_size=12)
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="item",
                        formatter="{b}: {c}首歌曲 ({d}%)"
                    )
                )
                .set_colors(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
            )
            
            logger.info("歌曲时长饼图创建成功")
            return pie
            
        except Exception as e:
            logger.error(f"创建时长饼图失败: {e}")
            return None
    
    def create_cross_playlist_songs_bar(self, min_count: int = 3, top_n: int = 30) -> Bar:
        """
        创建跨歌单热门歌曲柱状图
        :param min_count: 最少出现的歌单数
        :param top_n: TOP N
        :return: Bar图表对象
        """
        try:
            cross_songs = self.db.get_cross_playlist_songs(min_count)
            
            if not cross_songs:
                logger.warning("没有跨歌单歌曲数据")
                return self._create_no_data_chart("跨歌单热门歌曲", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            # 取TOP N
            cross_songs = cross_songs[:top_n]
            
            song_names = [f"{s['song_name'][:25]}..." if len(s['song_name']) > 25 
                         else s['song_name'] for s in cross_songs]
            playlist_counts = [s['playlist_count'] for s in cross_songs]
            
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(song_names)
                .add_yaxis(
                    "出现次数",
                    playlist_counts,
                    color=self.colors[4],
                    label_opts=opts.LabelOpts(position="top")
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"跨歌单热门歌曲 TOP {top_n}",
                        subtitle=f"至少出现在{min_count}个歌单中",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=9)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌单数量"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
                    datazoom_opts=[
                        opts.DataZoomOpts(type_="slider", range_start=0, range_end=50),
                        opts.DataZoomOpts(type_="inside")
                    ],
                )
            )
            
            logger.info("跨歌单歌曲柱状图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建跨歌单歌曲柱状图失败: {e}")
            return None
    
    def create_album_popularity_scatter(self, top_n: int = 100) -> Scatter:
        """
        创建专辑热度散点图
        :param top_n: TOP N 专辑
        :return: Scatter图表对象
        """
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_no_data_chart("专辑热度分析", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            # 过滤有效专辑数据
            df = df[df['album'].notna() & (df['album'] != '')]
            
            if df.empty:
                return None
            
            # 按专辑统计
            album_stats = df.groupby('album').agg({
                'song_id': 'count',
                'popularity': 'mean',
                'artist': 'first'
            }).reset_index()
            
            album_stats.columns = ['album', 'song_count', 'avg_popularity', 'artist']
            album_stats = album_stats.sort_values('avg_popularity', ascending=False).head(top_n)
            
            # 准备散点图数据
            data = []
            for _, row in album_stats.iterrows():
                data.append({
                    "value": [row['song_count'], row['avg_popularity']],
                    "name": f"{row['album'][:20]}...",
                    "symbolSize": min(max(row['song_count'] * 3, 8), 30)
                })
            
            scatter = (
                Scatter(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis([d['value'][0] for d in data])
                .add_yaxis(
                    "专辑",
                    [{"value": d['value'], "name": d['name'], "symbolSize": d['symbolSize']} for d in data],
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .set_series_opts(
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#FF6B6B',
                        opacity=0.8
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="💿 专辑热度分析",
                        subtitle=f"TOP {top_n} 专辑 - 歌曲数量 vs 平均热度",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        name="歌曲数量",
                        type_="value",
                        splitline_opts=opts.SplitLineOpts(is_show=True)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="平均热度",
                        type_="value",
                        splitline_opts=opts.SplitLineOpts(is_show=True)
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        formatter="{b}<br/>歌曲数: {c[0]}<br/>平均热度: {c[1]:.1f}"
                    ),
                    visualmap_opts=opts.VisualMapOpts(
                        type_="size",
                        max_=max([d['value'][0] for d in data]) if data else 10,
                        min_=min([d['value'][0] for d in data]) if data else 1,
                        dimension=0,
                        pos_left="left",
                        pos_bottom="10%"
                    )
                )
            )
            
            logger.info("专辑热度散点图创建成功")
            return scatter
            
        except Exception as e:
            logger.error(f"创建专辑散点图失败: {e}")
            return None
    
    def create_artist_song_heatmap(self, top_artists: int = 20, top_albums: int = 15) -> Bar:
        """
        创建歌手-专辑热力图（用柱状图模拟）
        :param top_artists: TOP N 歌手
        :param top_albums: TOP N 专辑
        :return: Bar图表对象
        """
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_no_data_chart("歌手专辑热度分析", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            # 过滤有效数据
            df = df[df['artist'].notna() & df['album'].notna() & 
                   (df['artist'] != '') & (df['album'] != '')]
            
            if df.empty:
                return None
            
            # 获取TOP歌手
            top_artist_list = df['artist'].value_counts().head(top_artists).index.tolist()
            df_filtered = df[df['artist'].isin(top_artist_list)]
            
            # 按歌手-专辑组合统计
            artist_album_stats = df_filtered.groupby(['artist', 'album']).agg({
                'song_id': 'count',
                'popularity': 'mean'
            }).reset_index()
            
            artist_album_stats.columns = ['artist', 'album', 'song_count', 'avg_popularity']
            artist_album_stats = artist_album_stats.sort_values('song_count', ascending=False).head(50)
            
            # 创建组合标签
            labels = [f"{row['artist'][:10]}-{row['album'][:15]}" for _, row in artist_album_stats.iterrows()]
            song_counts = artist_album_stats['song_count'].tolist()
            popularities = artist_album_stats['avg_popularity'].tolist()
            
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1600px",
                    height="800px"
                ))
                .add_xaxis(labels)
                .add_yaxis(
                    "歌曲数量",
                    song_counts,
                    yaxis_index=0,
                    color='#4ECDC4',
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .add_yaxis(
                    "平均热度",
                    popularities,
                    yaxis_index=1,
                    color='#FF6B6B',
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        name="平均热度",
                        type_="value",
                        position="right"
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="🎤 歌手专辑热度分析",
                        subtitle="TOP歌手专辑组合的歌曲数量与热度",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="歌曲数量",
                        type_="value"
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="axis",
                        axis_pointer_type="cross"
                    ),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
                    datazoom_opts=[
                        opts.DataZoomOpts(type_="slider", range_start=0, range_end=60),
                        opts.DataZoomOpts(type_="inside")
                    ]
                )
            )
            
            logger.info("歌手专辑热力图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建歌手专辑热力图失败: {e}")
            return None
    
    def create_song_popularity_distribution(self) -> Bar:
        """
        创建歌曲热度分布柱状图
        :return: Bar图表对象
        """
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_no_data_chart("歌曲热度分布", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            # 定义热度区间
            bins = [0, 20, 40, 60, 80, 100]
            labels = ['低热度(0-20)', '中低热度(21-40)', '中等热度(41-60)', '中高热度(61-80)', '高热度(81-100)']
            
            # 分组统计
            df['popularity_range'] = pd.cut(df['popularity'], bins=bins, labels=labels, include_lowest=True)
            popularity_counts = df['popularity_range'].value_counts().sort_index()
            
            categories = popularity_counts.index.tolist()
            counts = popularity_counts.values.tolist()
            
            bar = (
                Bar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1400px",
                    height="700px"
                ))
                .add_xaxis(categories)
                .add_yaxis(
                    "歌曲数量",
                    counts,
                    color='#45B7D1',
                    label_opts=opts.LabelOpts(
                        position="top",
                        font_size=14,
                        font_weight="bold"
                    ),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color=opts.JsCode("""
                            function(params) {
                                var colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'];
                                return colors[params.dataIndex % colors.length];
                            }
                        """)
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="🔥 歌曲热度分布",
                        subtitle=f"总计 {len(df)} 首歌曲的热度分布情况",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(font_size=12)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="歌曲数量",
                        axislabel_opts=opts.LabelOpts(formatter="{value}")
                    ),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="axis",
                        formatter="{b}: {c}首歌曲"
                    )
                )
            )
            
            logger.info("歌曲热度分布图创建成功")
            return bar
            
        except Exception as e:
            logger.error(f"创建热度分布图失败: {e}")
            return None
    
    def create_top_artists_radar(self, top_n: int = 8) -> Radar:
        """
        创建TOP歌手雷达图
        :param top_n: TOP N 歌手
        :return: Radar图表对象
        """
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_no_data_chart("歌手能力雷达图", "暂无歌曲数据", 
                    "请先爬取歌曲数据：\n1. 运行 python main.py\n2. 选择 '2 - 爬取歌单歌曲'")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            # 按歌手统计多维度数据
            artist_stats = df.groupby('artist').agg({
                'song_id': 'count',
                'popularity': ['mean', 'max'],
                'duration': 'mean'
            }).reset_index()
            
            artist_stats.columns = ['artist', 'song_count', 'avg_popularity', 'max_popularity', 'avg_duration']
            
            # 取TOP N歌手
            artist_stats = artist_stats.sort_values('song_count', ascending=False).head(top_n)
            
            # 数据标准化（0-100）
            try:
                from sklearn.preprocessing import MinMaxScaler
                scaler = MinMaxScaler(feature_range=(0, 100))
                features = ['song_count', 'avg_popularity', 'max_popularity', 'avg_duration']
                artist_stats[features] = scaler.fit_transform(artist_stats[features])
            except ImportError:
                # 如果sklearn不可用，使用简单的最大最小值标准化
                features = ['song_count', 'avg_popularity', 'max_popularity', 'avg_duration']
                for feature in features:
                    min_val = artist_stats[feature].min()
                    max_val = artist_stats[feature].max()
                    if max_val > min_val:
                        artist_stats[feature] = ((artist_stats[feature] - min_val) / (max_val - min_val)) * 100
                    else:
                        artist_stats[feature] = 50  # 如果所有值相同，设为中间值
            
            # 雷达图指标
            indicators = [
                {"name": "歌曲数量", "max": 100},
                {"name": "平均热度", "max": 100},
                {"name": "最高热度", "max": 100},
                {"name": "平均时长", "max": 100}
            ]
            
            # 准备数据
            radar_data = []
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            for i, (_, row) in enumerate(artist_stats.iterrows()):
                radar_data.append({
                    "value": [
                        round(row['song_count'], 1),
                        round(row['avg_popularity'], 1),
                        round(row['max_popularity'], 1),
                        round(row['avg_duration'], 1)
                    ],
                    "name": row['artist'][:10],
                    "itemStyle": {"color": colors[i % len(colors)]}
                })
            
            radar = (
                Radar(init_opts=opts.InitOpts(
                    theme=self.theme,
                    width="1200px",
                    height="700px"
                ))
                .add_schema(
                    schema=indicators,
                    shape="polygon",
                    center=["50%", "50%"],
                    radius="75%",
                    angleaxis_opts=opts.AngleAxisOpts(
                        min_=0,
                        max_=100,
                        is_clockwise=False,
                        interval=5,
                        axistick_opts=opts.AxisTickOpts(is_show=False),
                        axislabel_opts=opts.LabelOpts(is_show=False)
                    ),
                    radiusaxis_opts=opts.RadiusAxisOpts(
                        min_=0,
                        max_=100,
                        interval=20,
                        splitarea_opts=opts.SplitAreaOpts(
                            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.1)
                        )
                    ),
                    polar_opts=opts.PolarOpts(),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                )
                .add(
                    series_name="歌手能力",
                    data=radar_data,
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
                    linestyle_opts=opts.LineStyleOpts(width=2)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="🌟 TOP歌手能力雷达图",
                        subtitle=f"TOP {top_n} 歌手多维度能力分析",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24, font_weight="bold")
                    ),
                    legend_opts=opts.LegendOpts(
                        pos_top="10%",
                        pos_left="center",
                        orient="horizontal"
                    ),
                    tooltip_opts=opts.TooltipOpts(trigger="item")
                )
            )
            
            logger.info("歌手雷达图创建成功")
            return radar
            
        except Exception as e:
            logger.error(f"创建歌手雷达图失败: {e}")
            return None
    
    def _generate_html_template(self, charts_html: List[str], stats: Dict) -> str:
        """
        生成美观的HTML模板（带菜单导航和分页）
        :param charts_html: 图表HTML列表
        :param stats: 统计数据
        :return: 完整HTML字符串
        """
        from datetime import datetime
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网易云音乐热门歌单数据分析报告</title>
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/v5/echarts.min.js"></script>
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/v5/echarts-wordcloud.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        /* 头部样式 */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
        }}
        
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        /* 统计卡片 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #666;
        }}
        
        /* 导航菜单 */
        .nav-menu {{
            background: white;
            padding: 20px 40px;
            border-bottom: 2px solid #eee;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .nav-btn {{
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        .nav-btn.active {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        /* 图表容器 */
        .charts-container {{
            padding: 40px;
        }}
        
        .chart-page {{
            display: none;
            animation: fadeIn 0.5s;
        }}
        
        .chart-page.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .chart-wrapper {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        
        .chart-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .chart-title::before {{
            content: '📊';
            font-size: 28px;
        }}
        
        /* 页脚 */
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer p {{
            margin: 5px 0;
            opacity: 0.8;
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                padding: 20px;
            }}
            
            .nav-menu {{
                padding: 15px 20px;
            }}
            
            .nav-btn {{
                padding: 10px 18px;
                font-size: 12px;
            }}
            
            .charts-container {{
                padding: 20px;
            }}
        }}
        
        /* 加载动画 */
        .loading {{
            display: none;
            text-align: center;
            padding: 50px;
            font-size: 18px;
            color: #667eea;
        }}
        
        /* 顶部返回按钮 */
        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s;
            opacity: 0;
            visibility: hidden;
        }}
        
        .back-to-top.show {{
            opacity: 1;
            visibility: visible;
        }}
        
        .back-to-top:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>🎵 网易云音乐热门歌单数据分析报告</h1>
            <p>NetEase Cloud Music Hot Playlists Data Analysis Report</p>
            <p style="margin-top: 10px; font-size: 14px;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">总歌单数</div>
                <div class="value">{stats.get('total_playlists', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">总播放量</div>
                <div class="value">{stats.get('total_playlist_play_count', 0) // 100000000:.1f}亿</div>
            </div>
            <div class="stat-card">
                <div class="label">总收藏数</div>
                <div class="value">{stats.get('total_playlist_subscribe_count', 0) // 10000000:.1f}千万</div>
            </div>
            <div class="stat-card">
                <div class="label">总歌曲数</div>
                <div class="value">{stats.get('total_song_records', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">唯一歌曲</div>
                <div class="value">{stats.get('unique_songs', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">歌手数量</div>
                <div class="value">{stats.get('total_artists', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">专辑数量</div>
                <div class="value">{stats.get('total_albums', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="label">平均热度</div>
                <div class="value">{stats.get('avg_popularity', 0) or 0:.1f}</div>
            </div>
        </div>
        
        <!-- 导航菜单 -->
        <div class="nav-menu">
            <button class="nav-btn active" onclick="showPage(0)">📈 概览</button>
            <button class="nav-btn" onclick="showPage(1)">🏆 播放排行</button>
            <button class="nav-btn" onclick="showPage(2)">⭐ 收藏排行</button>
            <button class="nav-btn" onclick="showPage(3)">📊 对比分析</button>
            <button class="nav-btn" onclick="showPage(4)">🏷️ 标签分布</button>
            <button class="nav-btn" onclick="showPage(5)">👥 创建者排行</button>
            <button class="nav-btn" onclick="showPage(6)">💫 关系分析</button>
            <button class="nav-btn" onclick="showPage(7)">📦 规模分布</button>
            <button class="nav-btn" onclick="showPage(8)">☁️ 标签词云</button>
            <button class="nav-btn" onclick="showPage(9)">🎵 热门歌曲</button>
            <button class="nav-btn" onclick="showPage(10)">🎤 歌手排行</button>
            <button class="nav-btn" onclick="showPage(11)">⏱️ 时长分布</button>
            <button class="nav-btn" onclick="showPage(12)">🔥 跨歌单热歌</button>
            <button class="nav-btn" onclick="showPage(13)">💿 专辑热度</button>
            <button class="nav-btn" onclick="showPage(14)">🎶 歌手专辑</button>
            <button class="nav-btn" onclick="showPage(15)">📊 热度分布</button>
            <button class="nav-btn" onclick="showPage(16)">🌟 歌手雷达</button>
        </div>
        
        <!-- 图表容器 -->
        <div class="charts-container">
            <!-- 概览页 -->
            <div class="chart-page active" id="page-0">
                <div class="chart-wrapper">
                    <div class="chart-title">数据概览与说明</div>
                    <div style="padding: 20px; line-height: 2;">
                        <h3 style="color: #667eea; margin-bottom: 15px;">📊 报告说明</h3>
                        <p>• 本报告基于网易云音乐热门歌单数据生成</p>
                        <p>• 共采集 <strong>{stats.get('total_playlists', 0)}</strong> 个热门歌单，<strong>{stats.get('total_song_records', 0)}</strong> 首歌曲</p>
                        <p>• 包含 <strong>{stats.get('unique_songs', 0)}</strong> 首唯一歌曲，<strong>{stats.get('total_artists', 0)}</strong> 位歌手，<strong>{stats.get('total_albums', 0)}</strong> 张专辑</p>
                        <p>• 数据包含播放量、收藏数、标签、创建者、歌曲热度等多个维度</p>
                        <p>• 点击上方菜单按钮可切换查看不同维度的数据可视化图表</p>
                        
                        <h3 style="color: #667eea; margin: 30px 0 15px;">📈 歌单分析图表</h3>
                        <p><strong>🏆 播放排行:</strong> TOP30热门歌单播放量排行榜</p>
                        <p><strong>⭐ 收藏排行:</strong> TOP30热门歌单收藏数排行榜</p>
                        <p><strong>📊 对比分析:</strong> 播放量与收藏数双维度对比</p>
                        <p><strong>🏷️ 标签分布:</strong> 热门歌单标签分类统计</p>
                        <p><strong>👥 创建者排行:</strong> 歌单创建者贡献度分析</p>
                        <p><strong>💫 关系分析:</strong> 播放量与收藏数关系散点图</p>
                        <p><strong>📦 规模分布:</strong> 歌单大小规模分类统计</p>
                        <p><strong>☁️ 标签词云:</strong> 热门标签词云可视化</p>
                        
                        <h3 style="color: #667eea; margin: 30px 0 15px;">🎵 歌曲分析图表</h3>
                        <p><strong>🎵 热门歌曲:</strong> TOP30热门歌曲排行榜（按热度值）</p>
                        <p><strong>🎤 歌手排行:</strong> TOP20歌手排行榜（按歌曲数量）</p>
                        <p><strong>⏱️ 时长分布:</strong> 歌曲时长分布饼图</p>
                        <p><strong>🔥 跨歌单热歌:</strong> 在多个歌单中出现的热门歌曲</p>
                        <p><strong>💿 专辑热度:</strong> 专辑热度散点分析图</p>
                        <p><strong>🎶 歌手专辑:</strong> 歌手专辑组合热度分析</p>
                        <p><strong>📊 热度分布:</strong> 歌曲热度区间分布统计</p>
                        <p><strong>🌟 歌手雷达:</strong> TOP歌手多维度能力雷达图</p>
                        
                        <h3 style="color: #667eea; margin: 30px 0 15px;">💡 使用提示</h3>
                        <p>• 所有图表支持鼠标悬停查看详细数据</p>
                        <p>• 部分图表支持缩放和拖拽操作</p>
                        <p>• 建议使用Chrome、Firefox等现代浏览器浏览</p>
                    </div>
                </div>
            </div>
            
            {chr(10).join(f'''
            <div class="chart-page" id="page-{i+1}">
                <div class="chart-wrapper">
                    {chart_html}
                </div>
            </div>
            ''' for i, chart_html in enumerate(charts_html))}
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>📊 网易云音乐热门歌单数据分析报告</p>
            <p>数据来源: 网易云音乐 | 分析工具: Python + Pyecharts</p>
            <p>© 2025 Music Data Analysis Project</p>
        </div>
    </div>
    
    <!-- 返回顶部按钮 -->
    <button class="back-to-top" onclick="scrollToTop()">↑</button>
    
    <script>
        // 页面切换
        function showPage(pageIndex) {{
            // 隐藏所有页面
            const pages = document.querySelectorAll('.chart-page');
            pages.forEach(page => page.classList.remove('active'));
            
            // 显示指定页面
            const targetPage = document.getElementById('page-' + pageIndex);
            if (targetPage) {{
                targetPage.classList.add('active');
            }}
            
            // 更新按钮状态
            const buttons = document.querySelectorAll('.nav-btn');
            buttons.forEach((btn, index) => {{
                if (index === pageIndex) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            
            // 滚动到顶部
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        // 返回顶部
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        // 监听滚动显示返回顶部按钮
        window.addEventListener('scroll', function() {{
            const backToTop = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {{
                backToTop.classList.add('show');
            }} else {{
                backToTop.classList.remove('show');
            }}
        }});
        
        // 键盘导航
        document.addEventListener('keydown', function(e) {{
            const pages = document.querySelectorAll('.chart-page');
            const currentIndex = Array.from(pages).findIndex(page => 
                page.classList.contains('active')
            );
            
            if (e.key === 'ArrowRight' && currentIndex < pages.length - 1) {{
                showPage(currentIndex + 1);
            }} else if (e.key === 'ArrowLeft' && currentIndex > 0) {{
                showPage(currentIndex - 1);
            }}
        }});
    </script>
</body>
</html>
"""
        return html_template
    
    def generate_report(self, output_path: str = None) -> str:
        """
        生成完整的热门歌单数据分析HTML报告（带菜单导航）
        :param output_path: 输出文件路径
        :return: 报告文件路径
        """
        try:
            stats = self.db.get_statistics()
            
            if not stats or stats.get('total_playlists', 0) == 0:
                logger.warning("没有歌单数据,无法生成报告")
                return ""
            
            if output_path is None:
                output_dir = OUTPUT_CONFIG['reports_dir']
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, 'hot_playlists_report.html')
            
            logger.info("开始生成热门歌单可视化图表...")
            
            # 生成各个图表并保存为临时HTML
            charts_html = []
            temp_dir = os.path.join(OUTPUT_CONFIG['reports_dir'], 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            chart_configs = [
                ("播放量排行图", lambda: self.create_top_playlists_bar(30, 'play_count')),
                ("收藏数排行图", lambda: self.create_top_playlists_bar(30, 'subscribed_count')),
                ("对比图", lambda: self.create_playlist_comparison_bar(20)),
                ("标签分布图", lambda: self.create_tags_pie(15)),
                ("创建者排行图", lambda: self.create_creator_contribution_bar(20)),
                ("关系散点图", lambda: self.create_play_subscribe_scatter(200)),
                ("规模分布图", lambda: self.create_playlist_scale_pie()),
                ("标签词云", lambda: self.create_tags_wordcloud()),
                ("热门歌曲排行", lambda: self.create_top_songs_bar(30)),
                ("歌手排行图", lambda: self.create_artist_bar(20)),
                ("歌曲时长分布", lambda: self.create_song_duration_pie()),
                ("跨歌单热门歌曲", lambda: self.create_cross_playlist_songs_bar(3, 30)),
                ("专辑热度分析", lambda: self.create_album_popularity_scatter(100)),
                ("歌手专辑热度", lambda: self.create_artist_song_heatmap(20, 15)),
                ("歌曲热度分布", lambda: self.create_song_popularity_distribution()),
                ("歌手能力雷达图", lambda: self.create_top_artists_radar(8)),
            ]
            
            for i, (name, chart_func) in enumerate(chart_configs):
                logger.info(f"生成{name}...")
                chart = chart_func()
                if chart:
                    temp_file = os.path.join(temp_dir, f'chart_{i}.html')
                    chart.render(temp_file)
                    
                    # 读取图表HTML
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        chart_html = f.read()
                    
                    # 提取图表内容（包括div和script标签）
                    import re
                    # 提取从 <div id=... 到最后一个 </script> 的内容
                    pattern = r'(<div id="[^"]*" class="chart-container".*?</div>\s*<script>.*?</script>)'
                    match = re.search(pattern, chart_html, re.DOTALL)
                    if match:
                        charts_html.append(match.group(1))
                    else:
                        # 如果正则匹配失败，尝试更宽松的匹配
                        pattern2 = r'(<div id="[^"]*".*?var chart_[^=]*=.*?;.*?</script>)'
                        match2 = re.search(pattern2, chart_html, re.DOTALL)
                        if match2:
                            charts_html.append(match2.group(1))
            
            # 生成最终HTML
            final_html = self._generate_html_template(charts_html, stats)
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            # 清理临时文件
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            logger.info(f"热门歌单可视化报告已生成: {output_path}")
            logger.info(f"共生成 {len(charts_html)} 个图表")
            return output_path
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""


if __name__ == '__main__':
    # 测试图表生成
    from database.db_manager import DatabaseManager
    
    print("测试热门歌单可视化模块")
    print("="*60)
    
    db = DatabaseManager()
    generator = ChartsGenerator(db)
    
    # 生成报告
    print("\n开始生成可视化报告...")
    report_path = generator.generate_report()
    
    if report_path:
        print(f"\n[成功] 报告已生成: {report_path}")
        print("\n提示: 在浏览器中打开该HTML文件即可查看完整报告")
    else:
        print("\n[失败] 报告生成失败，请先爬取歌单数据")
    
    db.close()
