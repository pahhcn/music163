"""现代化可视化报告生成器 - 模块化版本"""
import os
import re
import shutil
from typing import List, Dict, Any, Optional
from pyecharts.globals import ThemeType

from database.db_manager import DatabaseManager
from config.settings import VISUALIZATION_CONFIG, OUTPUT_CONFIG
from utils.logger import get_logger
from .templates.html_builder import ModernHTMLBuilder
from .chart_builders import PlaylistChartsBuilder, SongChartsBuilder

logger = get_logger()


class ModernReportGenerator:
    """现代化可视化报告生成器"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        初始化报告生成器
        :param db_manager: 数据库管理器实例
        """
        self.db = db_manager if db_manager else DatabaseManager()
        self.theme = self._get_theme()
        
        # 初始化图表构建器
        self.playlist_builder = PlaylistChartsBuilder(self.db, self.theme)
        self.song_builder = SongChartsBuilder(self.db, self.theme)
        
        logger.info("现代化报告生成器初始化完成")
    
    def _get_theme(self) -> ThemeType:
        """获取图表主题"""
        theme_map = {
            'vintage': ThemeType.VINTAGE,
            'macarons': ThemeType.MACARONS,
            'infographic': ThemeType.INFOGRAPHIC,
            'shine': ThemeType.SHINE,
            'roma': ThemeType.ROMA,
        }
        theme_name = VISUALIZATION_CONFIG.get('theme', 'macarons')
        return theme_map.get(theme_name, ThemeType.MACARONS)
    
    def _extract_chart_content(self, html: str) -> Optional[str]:
        """
        从完整HTML中提取图表内容
        :param html: 完整HTML字符串
        :return: 图表内容（div + script）
        """
        try:
            # 匹配 <div id=... 到 </script> 的内容
            pattern = r'(<div id="[^"]*"[^>]*>.*?</div>\s*<script>.*?</script>)'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                return match.group(1)
            
            # 备用匹配方案
            pattern2 = r'(<div[^>]*class="chart-container"[^>]*>.*?</div>.*?<script>.*?</script>)'
            match2 = re.search(pattern2, html, re.DOTALL)
            if match2:
                return match2.group(1)
            
            logger.warning("无法提取图表内容")
            return None
        except Exception as e:
            logger.error(f"提取图表内容失败: {e}")
            return None
    
    def _generate_chart_html(self, chart, temp_file: str) -> Optional[str]:
        """
        生成图表HTML内容
        :param chart: 图表对象
        :param temp_file: 临时文件路径
        :return: 图表HTML内容
        """
        try:
            if chart is None:
                return None
            
            # 渲染图表到临时文件
            chart.render(temp_file)
            
            # 读取并提取内容
            with open(temp_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            return self._extract_chart_content(html_content)
        except Exception as e:
            logger.error(f"生成图表HTML失败: {e}")
            return None
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        生成完整的现代化可视化报告
        :param output_path: 输出文件路径
        :return: 报告文件路径
        """
        try:
            # 获取统计数据
            stats = self.db.get_statistics()
            if not stats or stats.get('total_playlists', 0) == 0:
                logger.warning("没有歌单数据，无法生成报告")
                return ""
            
            # 确定输出路径
            if output_path is None:
                output_dir = OUTPUT_CONFIG['reports_dir']
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, 'music_analysis_report.html')
            
            logger.info("="*60)
            logger.info("开始生成现代化可视化报告...")
            logger.info("="*60)
            
            # 创建临时目录
            temp_dir = os.path.join(OUTPUT_CONFIG['reports_dir'], 'temp_charts')
            os.makedirs(temp_dir, exist_ok=True)
            
            # 定义图表配置
            chart_configs = [
                # 歌单相关图表
                {
                    'name': '播放量排行',
                    'icon': '🏆',
                    'func': lambda: self.playlist_builder.create_top_bar(30, 'play_count')
                },
                {
                    'name': '收藏数排行',
                    'icon': '⭐',
                    'func': lambda: self.playlist_builder.create_top_bar(30, 'subscribed_count')
                },
                {
                    'name': '对比分析',
                    'icon': '📊',
                    'func': lambda: self.playlist_builder.create_comparison_bar(20)
                },
                {
                    'name': '标签分布',
                    'icon': '🏷️',
                    'func': lambda: self.playlist_builder.create_tags_pie(15)
                },
                {
                    'name': '创建者排行',
                    'icon': '👥',
                    'func': lambda: self.playlist_builder.create_creator_bar(20)
                },
                {
                    'name': '关系分析',
                    'icon': '💫',
                    'func': lambda: self.playlist_builder.create_relation_scatter(200)
                },
                {
                    'name': '规模分布',
                    'icon': '📦',
                    'func': lambda: self.playlist_builder.create_scale_pie()
                },
                {
                    'name': '标签词云',
                    'icon': '☁️',
                    'func': lambda: self.playlist_builder.create_tags_wordcloud()
                },
                # 歌曲相关图表
                {
                    'name': '热门歌曲',
                    'icon': '🎵',
                    'func': lambda: self.song_builder.create_top_songs_bar(30)
                },
                {
                    'name': '歌手排行',
                    'icon': '🎤',
                    'func': lambda: self.song_builder.create_artist_bar(20)
                },
                {
                    'name': '时长分布',
                    'icon': '⏱️',
                    'func': lambda: self.song_builder.create_duration_pie()
                },
                {
                    'name': '跨歌单热歌',
                    'icon': '🔥',
                    'func': lambda: self.song_builder.create_cross_playlist_bar(3, 30)
                },
                {
                    'name': '专辑热度',
                    'icon': '💿',
                    'func': lambda: self.song_builder.create_album_scatter(30)
                },
                {
                    'name': '热度分布',
                    'icon': '📊',
                    'func': lambda: self.song_builder.create_popularity_distribution_bar()
                },
                {
                    'name': '歌手雷达',
                    'icon': '🌟',
                    'func': lambda: self.song_builder.create_artist_radar(8)
                },
            ]
            
            # 生成所有图表
            charts_html = []
            nav_items = ['📋 概览']
            
            for i, config in enumerate(chart_configs):
                name = config['name']
                icon = config['icon']
                func = config['func']
                
                logger.info(f"[{i+1}/{len(chart_configs)}] 生成 {name} 图表...")
                
                try:
                    chart = func()
                    if chart:
                        temp_file = os.path.join(temp_dir, f'chart_{i}.html')
                        chart_html = self._generate_chart_html(chart, temp_file)
                        
                        if chart_html:
                            charts_html.append(chart_html)
                            nav_items.append(f"{icon} {name}")
                            logger.info(f"    ✓ {name} 生成成功")
                        else:
                            logger.warning(f"    ✗ {name} 提取内容失败")
                    else:
                        logger.warning(f"    ✗ {name} 生成失败（无数据）")
                except Exception as e:
                    logger.error(f"    ✗ {name} 生成失败: {e}")
            
            logger.info("="*60)
            logger.info(f"成功生成 {len(charts_html)} 个图表")
            logger.info("="*60)
            
            # 构建最终HTML
            logger.info("正在构建HTML报告...")
            final_html = ModernHTMLBuilder.build_html(stats, charts_html, nav_items)
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            # 清理临时文件
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info("临时文件已清理")
            
            logger.info("="*60)
            logger.info(f"✓ 报告生成成功: {output_path}")
            logger.info(f"✓ 共包含 {len(charts_html)} 个可视化图表")
            logger.info("="*60)
            
            return output_path
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""
    
    def get_report_summary(self) -> Dict[str, Any]:
        """
        获取报告摘要信息
        :return: 摘要字典
        """
        try:
            stats = self.db.get_statistics()
            return {
                'total_playlists': stats.get('total_playlists', 0),
                'total_songs': stats.get('total_song_records', 0),
                'unique_songs': stats.get('unique_songs', 0),
                'total_artists': stats.get('total_artists', 0),
                'total_albums': stats.get('total_albums', 0),
                'avg_popularity': stats.get('avg_popularity', 0),
            }
        except Exception as e:
            logger.error(f"获取报告摘要失败: {e}")
            return {}


if __name__ == '__main__':
    # 测试报告生成
    print("\n" + "="*60)
    print("现代化可视化报告生成器测试")
    print("="*60 + "\n")
    
    db = DatabaseManager()
    generator = ModernReportGenerator(db)
    
    # 显示摘要
    summary = generator.get_report_summary()
    print("数据摘要:")
    print(f"  歌单数量: {summary.get('total_playlists', 0):,}")
    print(f"  歌曲数量: {summary.get('total_songs', 0):,}")
    print(f"  唯一歌曲: {summary.get('unique_songs', 0):,}")
    print(f"  歌手数量: {summary.get('total_artists', 0):,}")
    print(f"  专辑数量: {summary.get('total_albums', 0):,}")
    print(f"  平均热度: {summary.get('avg_popularity', 0):.1f}\n")
    
    # 生成报告
    report_path = generator.generate_report()
    
    if report_path:
        print(f"\n✓ 成功！报告已生成: {report_path}")
        print("  在浏览器中打开该文件即可查看\n")
    else:
        print("\n✗ 失败！请检查日志信息\n")
    
    db.close()
