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
        """创建TOP热门歌曲柱状图（使用跨歌单出现次数）"""
        try:
            songs = self.db.get_songs_with_cross_playlist_count(top_n)
            if not songs:
                return self._create_empty_chart("热门歌曲排行", "暂无歌曲数据，请先爬取")
            
            names = [s['song_name'][:18] + '...' if len(s['song_name']) > 18 
                    else s['song_name'] for s in songs]
            values = [s.get('cross_playlist_count', 0) for s in songs]
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(names)
                .add_yaxis(
                    "出现次数",
                    values,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=10),
                    itemstyle_opts=opts.ItemStyleOpts(color=self.colors[0])
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🎵 TOP{top_n} 热门歌曲排行",
                        subtitle="按跨歌单出现次数排序 | 出现次数越多说明越受欢迎",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=10)
                    ),
                    yaxis_opts=opts.AxisOpts(name="出现次数（个歌单）"),
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
                    legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
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
    
    def create_album_scatter(self, top_n: int = 30):
        """创建专辑热度分析图（现代化柱状图）"""
        try:
            album_stats = self.db.get_album_stats_with_cross_count(top_n)
            if not album_stats:
                return self._create_empty_chart("专辑热度分析", "暂无专辑数据")
            
            if not album_stats:
                return self._create_empty_chart("专辑热度分析", "数据不足")
            
            # 准备数据
            album_names = []
            song_counts = []
            cross_counts = []
            
            for album in album_stats:
                # 截断专辑名，添加歌手信息
                album_display = album['album'][:15]
                if len(album['album']) > 15:
                    album_display += '...'
                album_display += f"\n({album['artist'][:8]})"
                
                album_names.append(album_display)
                song_counts.append(album['song_count'])
                cross_counts.append(round(album['total_cross_count'], 0))
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(album_names)
                .add_yaxis(
                    "收录歌曲数",
                    song_counts,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=9),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#667eea',
                        opacity=0.8
                    ),
                    stack="stack1"
                )
                .add_yaxis(
                    "总出现次数",
                    cross_counts,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=9),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#f093fb',
                        opacity=0.8
                    ),
                    yaxis_index=1
                )
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        name="总出现次数",
                        type_="value",
                        position="right",
                        axislabel_opts=opts.LabelOpts(formatter="{value}次")
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"💿 热门专辑分析 TOP{top_n}",
                        subtitle="左轴: 专辑收录歌曲数（蓝色） | 右轴: 专辑歌曲总出现次数（粉色）\n总出现次数越高说明专辑越受欢迎",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight="bold"),
                        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=10, color="#666"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(rotate=45, interval=0, font_size=9)
                    ),
                    yaxis_opts=opts.AxisOpts(
                        name="收录歌曲数",
                        type_="value",
                        position="left",
                        axislabel_opts=opts.LabelOpts(formatter="{value}首")
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    legend_opts=opts.LegendOpts(
                        pos_top="12%",
                        pos_left="center"
                    ),
                    datazoom_opts=[opts.DataZoomOpts(type_="slider", range_end=60)]
                )
            )
        except Exception as e:
            logger.error(f"创建专辑图表失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def create_popularity_distribution_bar(self):
        """创建歌曲热度分布柱状图（基于跨歌单次数）"""
        try:
            # 获取所有歌曲的跨歌单统计
            songs = self.db.get_all_songs()
            if not songs:
                return self._create_empty_chart("热度分布", "暂无歌曲数据")
            
            import pandas as pd
            
            # 计算每首歌的跨歌单次数
            df = pd.DataFrame(songs)
            cross_counts = df.groupby('song_id')['playlist_id'].nunique().reset_index()
            cross_counts.columns = ['song_id', 'cross_count']
            
            # 定义热度区间（基于跨歌单次数）
            bins = [0, 1, 2, 3, 5, 100]
            labels = ['仅1个歌单', '2个歌单', '3个歌单', '4-5个歌单', '6个以上歌单']
            cross_counts['range'] = pd.cut(cross_counts['cross_count'], bins=bins, labels=labels, include_lowest=True)
            
            counts = cross_counts['range'].value_counts().sort_index()
            categories = counts.index.tolist()
            values = counts.values.tolist()
            
            return (
                Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_xaxis(categories)
                .add_yaxis(
                    "歌曲数量",
                    values,
                    label_opts=opts.LabelOpts(is_show=True, position="top", font_size=12),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color='#667eea',
                        opacity=0.8
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="📊 歌曲热度分布",
                        subtitle=f"总计 {len(cross_counts)} 首唯一歌曲 | 按跨歌单出现次数统计",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(font_size=11, rotate=15)
                    ),
                    yaxis_opts=opts.AxisOpts(name="歌曲数量"),
                    tooltip_opts=opts.TooltipOpts(
                        trigger="axis",
                        formatter="{b}<br/>歌曲数: {c}"
                    )
                )
            )
        except Exception as e:
            logger.error(f"创建热度分布图失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def create_artist_radar(self, top_n: int = 8):
        """创建TOP歌手综合能力雷达图（优化版）"""
        try:
            artist_stats = self.db.get_artist_comprehensive_stats(top_n)
            if not artist_stats:
                return self._create_empty_chart("歌手能力雷达", "暂无歌曲数据")
            
            import pandas as pd
            import numpy as np
            
            df = pd.DataFrame(artist_stats)
            
            # 使用对数归一化处理数量类指标
            for col in ['song_count', 'avg_cross_count', 'max_cross_count']:
                values = df[col].values
                log_values = np.log1p(values)  # log(1+x)
                min_val, max_val = log_values.min(), log_values.max()
                if max_val > min_val:
                    df[col + '_norm'] = ((log_values - min_val) / (max_val - min_val)) * 100
                else:
                    df[col + '_norm'] = 50
            
            # 时长范围归一化（作品多样性）
            values = df['duration_range'].values
            min_val, max_val = values.min(), values.max()
            if max_val > min_val:
                df['diversity_norm'] = ((values - min_val) / (max_val - min_val)) * 100
            else:
                df['diversity_norm'] = 50
            
            indicators = [
                {"name": "作品量", "max": 100},
                {"name": "受欢迎度", "max": 100},
                {"name": "爆款能力", "max": 100},
                {"name": "作品多样性", "max": 100}
            ]
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            radar_data = []
            for i, (_, row) in enumerate(df.iterrows()):
                radar_data.append({
                    "value": [
                        round(row['song_count_norm'], 1),
                        round(row['avg_cross_count_norm'], 1),
                        round(row['max_cross_count_norm'], 1),
                        round(row['diversity_norm'], 1)
                    ],
                    "name": row['artist'][:10],
                    "itemStyle": {"color": colors[i % len(colors)]}
                })
            
            return (
                Radar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                .add_schema(
                    schema=indicators,
                    shape="polygon",
                    center=["50%", "58%"],
                    radius="65%",
                    splitarea_opt=opts.SplitAreaOpts(
                        is_show=True,
                        areastyle_opts=opts.AreaStyleOpts(opacity=0.1)
                    )
                )
                .add("", radar_data, areastyle_opts=opts.AreaStyleOpts(opacity=0.25))
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"🌟 TOP{top_n} 歌手综合能力雷达图",
                        subtitle="四个维度：作品量（产出能力）| 受欢迎度（传播广度）| 爆款能力（制造爆款）| 作品多样性（风格多样）",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight="bold"),
                        subtitle_textstyle_opts=opts.TextStyleOpts(font_size=10, color="#666"),
                        pos_left="center",
                        pos_top="2%"
                    ),
                    legend_opts=opts.LegendOpts(
                        pos_top="10%",
                        pos_left="center",
                        orient="horizontal",
                        item_width=25,
                        item_height=14
                    ),
                    tooltip_opts=opts.TooltipOpts(is_show=False)
                )
            )
        except Exception as e:
            logger.error(f"创建雷达图失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
