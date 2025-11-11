"""歌曲相关图表构建器"""
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Scatter, Radar
from collections import Counter
from .base_builder import BaseChartBuilder
from utils.logger import get_logger

logger = get_logger()


class SongChartsBuilder(BaseChartBuilder):
    """歌曲图表构建器"""
    
    def create_top_songs_bar(self, top_n: int = 30):
        """创建TOP热门歌曲柱状图"""
        try:
            songs = self.db.get_top_songs(top_n, 'popularity')
            if not songs:
                return self._create_empty_chart("热门歌曲排行", "暂无歌曲数据，请先爬取")
            
            names = [s['song_name'][:18] + '...' if len(s['song_name']) > 18 
                    else s['song_name'] for s in songs]
            values = [s.get('popularity', 0) for s in songs]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(names)
                .add_yaxis(
                    "热度值",
                    values,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=10),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[0])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🎵 TOP{top_n} 热门歌曲排行",
                        subtitle="按热度值排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="热度值"),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider", range_end=60)]
                )
            )
        except Exception as e:
            logger.error(f"创建歌曲排行图失败: {e}")
            return None
    
    def create_artist_bar(self, top_n: int = 20):
        """创建TOP歌手柱状图"""
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("歌手排行榜", "暂无歌曲数据")
            
            artist_counts = Counter([s['artist'] for s in songs if s.get('artist')])
            top_artists = artist_counts.most_common(top_n)
            
            artists = [a[0] for a in top_artists]
            counts = [a[1] for a in top_artists]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(artists)
                .add_yaxis(
                    "歌曲数量",
                    counts,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=10),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[1])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🎤 TOP{top_n} 热门歌手",
                        subtitle="按歌曲数量排序",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=30, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌曲数量"),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
        except Exception as e:
            logger.error(f"创建歌手图表失败: {e}")
            return None
    
    def create_duration_pie(self):
        """创建歌曲时长分布饼图"""
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("时长分布", "暂无歌曲数据", 'pie')
            
            import pandas as pd
            df = pd.DataFrame(songs)
            durations_sec = df['duration'] / 1000
            
            categories = [
                ("极短(≤2分钟)", len(durations_sec[durations_sec <= 120])),
                ("短(2-3分钟)", len(durations_sec[(durations_sec > 120) & (durations_sec <= 180)])),
                ("中等(3-5分钟)", len(durations_sec[(durations_sec > 180) & (durations_sec <= 300)])),
                ("长(5-7分钟)", len(durations_sec[(durations_sec > 300) & (durations_sec <= 420)])),
                ("超长(>7分钟)", len(durations_sec[durations_sec > 420]))
            ]
            
            data = [(name, count) for name, count in categories if count > 0]
            
            return (
                Pie(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add(
                    "",
                    data,
                    radius=["35%", "70%"],
                    center=["55%", "55%"],
                    rosetype="area",
                    label_opts=opts.LabelOpts(formatter="{b}\n{c}首 ({d}%)", font_size=12)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="⏱️ 歌曲时长分布",
                        subtitle=f"总计 {len(df)} 首歌曲",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%")
                )
                .set_colors(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
            )
        except Exception as e:
            logger.error(f"创建时长饼图失败: {e}")
            return None
    
    def create_cross_playlist_bar(self, min_count: int = 3, top_n: int = 30):
        """创建跨歌单热门歌曲柱状图"""
        try:
            cross_songs = self.db.get_cross_playlist_songs(min_count)
            if not cross_songs:
                return self._create_empty_chart("跨歌单热歌", "暂无歌曲数据")
            
            cross_songs = cross_songs[:top_n]
            names = [s['song_name'][:20] + '...' if len(s['song_name']) > 20 
                    else s['song_name'] for s in cross_songs]
            counts = [s['playlist_count'] for s in cross_songs]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(names)
                .add_yaxis(
                    "出现次数",
                    counts,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=10),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[4])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🔥 跨歌单热门歌曲 TOP{top_n}",
                        subtitle=f"至少出现在{min_count}个歌单中",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=9)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌单数量"),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider", range_end=60)]
                )
            )
        except Exception as e:
            logger.error(f"创建跨歌单图表失败: {e}")
            return None
    
    def create_album_scatter(self, top_n: int = 100):
        """创建专辑热度散点图"""
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("专辑热度分析", "暂无歌曲数据")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            df = df[df['album'].notna() & (df['album'] != '')]
            
            if df.empty:
                return self._create_empty_chart("专辑热度分析", "暂无专辑数据")
            
            album_stats = df.groupby('album').agg({
                'song_id': 'count',
                'popularity': 'mean'
            }).reset_index()
            album_stats.columns = ['album', 'song_count', 'avg_popularity']
            album_stats = album_stats.sort_values('avg_popularity', ascending=False).head(top_n)
            
            data = [[row['song_count'], row['avg_popularity']] for _, row in album_stats.iterrows()]
            
            return (
                Scatter(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis([d[0] for d in data])
                .add_yaxis(
                    "专辑",
                    [d[1] for d in data],
                    symbol_size=12,
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(color='#FF6B6B', opacity=0.7)
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"💿 专辑热度分析 TOP{top_n}",
                        subtitle="歌曲数量 vs 平均热度",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(name="歌曲数量", type_="value"),
                    yaxis_opts=opts.AxisOpts(name="平均热度", type_="value"),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    visualmap_opts=opts.VisualMapOpts(
                        type_="size", max_=max([d[0] for d in data]) if data else 10,
                        min_=min([d[0] for d in data]) if data else 1, dimension=0
                    )
                )
            )
        except Exception as e:
            logger.error(f"创建专辑散点图失败: {e}")
            return None
    
    def create_popularity_distribution_bar(self):
        """创建歌曲热度分布柱状图"""
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("热度分布", "暂无歌曲数据")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            bins = [0, 20, 40, 60, 80, 100]
            labels = ['低热度(0-20)', '中低(21-40)', '中等(41-60)', '中高(61-80)', '高热度(81-100)']
            df['range'] = pd.cut(df['popularity'], bins=bins, labels=labels, include_lowest=True)
            
            counts = df['range'].value_counts().sort_index()
            categories = counts.index.tolist()
            values = counts.values.tolist()
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(categories)
                .add_yaxis(
                    "歌曲数量",
                    values,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=12),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[5])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="📊 歌曲热度分布",
                        subtitle=f"总计 {len(df)} 首歌曲",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=12)),
                    yaxis_opts=opts.AxisOpts(name="歌曲数量"),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
        except Exception as e:
            logger.error(f"创建热度分布图失败: {e}")
            return None
    
    def create_artist_radar(self, top_n: int = 8):
        """创建TOP歌手雷达图"""
        try:
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("歌手能力雷达", "暂无歌曲数据")
            
            import pandas as pd
            df = pd.DataFrame(songs)
            
            artist_stats = df.groupby('artist').agg({
                'song_id': 'count',
                'popularity': ['mean', 'max'],
                'duration': 'mean'
            }).reset_index()
            artist_stats.columns = ['artist', 'song_count', 'avg_pop', 'max_pop', 'avg_dur']
            artist_stats = artist_stats.sort_values('song_count', ascending=False).head(top_n)
            
            # 简单归一化到0-100
            for col in ['song_count', 'avg_pop', 'max_pop', 'avg_dur']:
                min_val, max_val = artist_stats[col].min(), artist_stats[col].max()
                if max_val > min_val:
                    artist_stats[col] = ((artist_stats[col] - min_val) / (max_val - min_val)) * 100
                else:
                    artist_stats[col] = 50
            
            indicators = [
                {"name": "歌曲数量", "max": 100},
                {"name": "平均热度", "max": 100},
                {"name": "最高热度", "max": 100},
                {"name": "平均时长", "max": 100}
            ]
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            radar_data = []
            for i, (_, row) in enumerate(artist_stats.iterrows()):
                radar_data.append({
                    "value": [round(row['song_count'], 1), round(row['avg_pop'], 1),
                             round(row['max_pop'], 1), round(row['avg_dur'], 1)],
                    "name": row['artist'][:10],
                    "itemStyle": {"color": colors[i % len(colors)]}
                })
            
            return (
                Radar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_schema(
                    schema=indicators,
                    shape="polygon",
                    center=["50%", "58%"],
                    radius="65%"
                )
                .add("", radar_data, areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🌟 TOP{top_n} 歌手能力雷达图",
                        subtitle="多维度能力分析",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    legend_opts=opts.LegendOpts(pos_top="12%", pos_left="center", orient="horizontal")
                )
            )
        except Exception as e:
            logger.error(f"创建雷达图失败: {e}")
            return None
