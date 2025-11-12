"""歌单相关图表构建器"""
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Scatter, WordCloud
from .base_builder import BaseChartBuilder
from utils.logger import get_logger

logger = get_logger()


class PlaylistChartsBuilder(BaseChartBuilder):
    """歌单图表构建器"""
    
    def create_top_bar(self, top_n: int = 30, order_by: str = 'play_count'):
        """创建TOP歌单柱状图"""
        try:
            playlists = self.db.get_top_playlists(top_n, order_by)
            if not playlists:
                return self._create_empty_chart("热门歌单排行", "暂无数据，请先爬取歌单")
            
            names = [p['playlist_name'][:18] + '...' if len(p['playlist_name']) > 18 
                    else p['playlist_name'] for p in playlists]
            values = [p.get(order_by, 0) for p in playlists]
            
            title_map = {'play_count': '播放量', 'subscribed_count': '收藏数', 'track_count': '歌曲数'}
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(names)
                .add_yaxis(
                    title_map.get(order_by, '数值'),
                    values,
                    label_opts=opts.LabelOpts(
                        is_show=True,
                        position="top",
                        font_size=10
                    ),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[0])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🏆 TOP{top_n} 热门歌单{title_map.get(order_by, '')}排行",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name=title_map.get(order_by, '')),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider", range_end=60)],
                    legend_opts=opts.LegendOpts(pos_top="8%")
                )
            )
        except Exception as e:
            logger.error(f"创建TOP歌单图表失败: {e}")
            return None
    
    def create_comparison_bar(self, top_n: int = 20):
        """创建播放量与收藏数对比图"""
        try:
            playlists = self.db.get_top_playlists(top_n, 'play_count')
            if not playlists:
                return self._create_empty_chart("歌单对比分析", "暂无数据")
            
            names = [p['playlist_name'][:15] + '...' if len(p['playlist_name']) > 15 
                    else p['playlist_name'] for p in playlists]
            plays = [p['play_count'] for p in playlists]
            subs = [p['subscribed_count'] for p in playlists]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(names)
                .add_yaxis(
                    "播放量", 
                    plays, 
                    color=self.colors[0],
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=9)
                )
                .add_yaxis(
                    "收藏数", 
                    subs, 
                    color=self.colors[1],
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=9)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"📊 TOP{top_n} 歌单播放量 vs 收藏数",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=9)
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    legend_opts=opts.LegendOpts(pos_top="5%"),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider")]
                )
            )
        except Exception as e:
            logger.error(f"创建对比图失败: {e}")
            return None
    
    def create_tags_pie(self, top_n: int = 15):
        """创建标签分布饼图"""
        try:
            playlists = self.db.get_all_playlists()
            if not playlists:
                return self._create_empty_chart("标签分布", "暂无数据", 'pie')
            
            tags_count = {}
            for p in playlists:
                if p.get('tags'):
                    for tag in p['tags'].split(','):
                        tag = tag.strip()
                        if tag:
                            tags_count[tag] = tags_count.get(tag, 0) + 1
            
            sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            return (
                Pie(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add(
                    "",
                    sorted_tags,
                    radius=["35%", "70%"],
                    center=["55%", "55%"],
                    rosetype="area",
                    label_opts=opts.LabelOpts(formatter="{b}: {d}%", font_size=11)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🏷️ 热门标签分布 TOP{top_n}",
                        subtitle=f"共 {len(tags_count)} 个标签",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    legend_opts=opts.LegendOpts(
                        orient="vertical", pos_left="2%", pos_top="15%"
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
                .set_colors(self.colors)
            )
        except Exception as e:
            logger.error(f"创建标签饼图失败: {e}")
            return None
    
    def create_creator_bar(self, top_n: int = 20):
        """创建创建者贡献度柱状图"""
        try:
            playlists = self.db.get_all_playlists()
            if not playlists:
                return self._create_empty_chart("创建者排行", "暂无数据")
            
            creator_stats = {}
            for p in playlists:
                creator = p.get('creator_name', '未知')
                creator_stats[creator] = creator_stats.get(creator, 0) + 1
            
            sorted_creators = sorted(creator_stats.items(), key=lambda x: x[1], reverse=True)[:top_n]
            creators = [c[0] for c in sorted_creators]
            counts = [c[1] for c in sorted_creators]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(creators)
                .add_yaxis(
                    "歌单数量",
                    counts,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=10),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[2])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"👥 TOP{top_n} 热门创建者",
                        subtitle="按歌单数量排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=30, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌单数量"),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
        except Exception as e:
            logger.error(f"创建创建者图表失败: {e}")
            return None
    
    def create_relation_scatter(self, sample_size: int = 200):
        """创建播放量与收藏数关系散点图"""
        try:
            playlists = self.db.get_all_playlists()[:sample_size]
            if not playlists:
                return self._create_empty_chart("关系分析", "暂无数据")
            
            data = [[p['play_count'], p['subscribed_count']] for p in playlists]
            
            return (
                Scatter(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis([d[0] for d in data])
                .add_yaxis(
                    "歌单",
                    [d[1] for d in data],
                    symbol_size=10,
                    label_opts=opts.LabelOpts(is_show=False)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="💫 播放量与收藏数关系分析",
                        subtitle=f"样本数: {len(data)}",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    xaxis_opts=opts.AxisOpts(name="播放量", type_="value"),
                    yaxis_opts=opts.AxisOpts(name="收藏数", type_="value"),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    visualmap_opts=opts.VisualMapOpts(
                        type_="size", 
                        max_=max([d[1] for d in data]) if data else 100,
                        min_=min([d[1] for d in data]) if data else 0, 
                        dimension=1,
                        pos_right="2%",
                        pos_bottom="10%"
                    ),
                    legend_opts=opts.LegendOpts(pos_top="8%")
                )
            )
        except Exception as e:
            logger.error(f"创建散点图失败: {e}")
            return None
    
    def create_scale_pie(self):
        """创建歌单规模分布饼图"""
        try:
            playlists = self.db.get_all_playlists()
            if not playlists:
                return self._create_empty_chart("规模分布", "暂无数据", 'pie')
            
            categories = {
                '超大型(500+首)': 0,
                '大型(200-500首)': 0,
                '中型(100-200首)': 0,
                '小型(50-100首)': 0,
                '迷你型(<50首)': 0
            }
            
            for p in playlists:
                count = p.get('track_count', 0)
                if count >= 500:
                    categories['超大型(500+首)'] += 1
                elif count >= 200:
                    categories['大型(200-500首)'] += 1
                elif count >= 100:
                    categories['中型(100-200首)'] += 1
                elif count >= 50:
                    categories['小型(50-100首)'] += 1
                else:
                    categories['迷你型(<50首)'] += 1
            
            data = [(k, v) for k, v in categories.items() if v > 0]
            
            return (
                Pie(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add(
                    "",
                    data,
                    radius=["40%", "70%"],
                    center=["55%", "55%"],
                    label_opts=opts.LabelOpts(formatter="{b}\n{c}个 ({d}%)")
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="📦 歌单规模分布",
                        subtitle=f"总计 {len(playlists)} 个歌单",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
                .set_colors(self.colors)
            )
        except Exception as e:
            logger.error(f"创建规模饼图失败: {e}")
            return None
    
    def create_tags_wordcloud(self):
        """创建标签词云"""
        try:
            playlists = self.db.get_all_playlists()
            if not playlists:
                return None
            
            tags_count = {}
            for p in playlists:
                if p.get('tags'):
                    for tag in p['tags'].split(','):
                        tag = tag.strip()
                        if tag:
                            tags_count[tag] = tags_count.get(tag, 0) + 1
            
            # 只显示前50个最热门标签，避免词云过于拥挤
            sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:50]
            word_data = [(tag, count) for tag, count in sorted_tags]
            
            return (
                WordCloud(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add(
                    "",
                    word_data,
                    word_size_range=[18, 80],
                    shape='circle'
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="☁️ 热门标签词云 TOP50",
                        subtitle=f"展示前50个热门标签（总计 {len(tags_count)} 个标签）",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
        except Exception as e:
            logger.error(f"创建词云失败: {e}")
            return None
