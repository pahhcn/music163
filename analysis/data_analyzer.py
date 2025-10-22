"""
热门歌单数据分析模块
对网易云音乐热门歌单数据进行统计分析
"""
import pandas as pd
import jieba
from collections import Counter
from typing import List, Dict, Any, Tuple, Optional
import os

from database.db_manager import DatabaseManager
from config.settings import ANALYSIS_CONFIG, OUTPUT_CONFIG
from utils.logger import get_logger

logger = get_logger()


class DataAnalyzer:
    """热门歌单数据分析器"""
    
    def __init__(self, db_manager: DatabaseManager = None):
        """
        初始化数据分析器
        :param db_manager: 数据库管理器实例
        """
        self.db = db_manager if db_manager else DatabaseManager()
        self.playlists_df = None
        self.songs_df = None
        self._load_data()
    
    def _load_data(self):
        """从数据库加载歌单和歌曲数据到DataFrame"""
        try:
            # 加载歌单数据
            playlists = self.db.get_all_playlists()
            if playlists:
                self.playlists_df = pd.DataFrame(playlists)
                logger.info(f"加载了 {len(self.playlists_df)} 个歌单数据")
            else:
                self.playlists_df = pd.DataFrame()
                logger.warning("没有歌单数据")
            
            # 加载歌曲数据
            songs = self.db.get_all_songs()
            if songs:
                self.songs_df = pd.DataFrame(songs)
                logger.info(f"加载了 {len(self.songs_df)} 首歌曲数据")
            else:
                self.songs_df = pd.DataFrame()
                logger.warning("没有歌曲数据")
                
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            self.playlists_df = pd.DataFrame()
            self.songs_df = pd.DataFrame()
    
    def get_basic_statistics(self) -> Dict[str, Any]:
        """
        获取歌单基础统计数据
        :return: 统计数据字典
        """
        try:
            if self.playlists_df.empty:
                return {}
            
            stats = {
                'total_playlists': len(self.playlists_df),
                'total_play_count': int(self.playlists_df['play_count'].sum()),
                'total_subscribed_count': int(self.playlists_df['subscribed_count'].sum()),
                'avg_play_count': int(self.playlists_df['play_count'].mean()),
                'avg_subscribed_count': int(self.playlists_df['subscribed_count'].mean()),
                'avg_track_count': int(self.playlists_df['track_count'].mean()),
                'max_play_count': int(self.playlists_df['play_count'].max()),
                'max_subscribed_count': int(self.playlists_df['subscribed_count'].max()),
                'total_creators': self.playlists_df['creator_name'].nunique(),
            }
            
            logger.info(f"歌单基础统计: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"获取基础统计失败: {e}")
            return {}
    
    def get_top_playlists(self, n: int = 30, by: str = 'play_count') -> List[Dict[str, Any]]:
        """
        获取TOP N 热门歌单
        :param n: TOP N
        :param by: 排序字段 (play_count, subscribed_count, track_count)
        :return: 歌单列表
        """
        try:
            if self.playlists_df.empty:
                return []
            
            # 确保排序字段存在
            if by not in self.playlists_df.columns:
                by = 'play_count'
            
            top_playlists = self.playlists_df.nlargest(n, by)
            
            # 选择关键字段
            columns = ['playlist_name', 'creator_name', 'play_count', 
                      'subscribed_count', 'track_count', 'tags']
            result = top_playlists[columns].to_dict('records')
            
            logger.info(f"获取TOP {n} 歌单 (按 {by})")
            return result
            
        except Exception as e:
            logger.error(f"获取TOP歌单失败: {e}")
            return []
    
    def get_creator_distribution(self, n: int = 20) -> List[Dict[str, Any]]:
        """
        获取歌单创建者分布统计
        :param n: TOP N 创建者
        :return: 创建者统计列表
        """
        try:
            if self.playlists_df.empty:
                return []
            
            # 按创建者分组统计
            creator_stats = self.playlists_df.groupby('creator_name').agg({
                'playlist_id': 'count',
                'play_count': ['sum', 'mean'],
                'subscribed_count': ['sum', 'mean']
            }).reset_index()
            
            creator_stats.columns = ['creator_name', 'playlist_count', 
                                    'total_play_count', 'avg_play_count',
                                    'total_subscribed_count', 'avg_subscribed_count']
            
            # 转换为整数
            for col in ['total_play_count', 'avg_play_count', 
                       'total_subscribed_count', 'avg_subscribed_count']:
                creator_stats[col] = creator_stats[col].astype(int)
            
            # 排序并取TOP N
            creator_stats = creator_stats.sort_values('playlist_count', ascending=False).head(n)
            
            result = creator_stats.to_dict('records')
            logger.info(f"获取TOP {n} 创建者分布")
            return result
            
        except Exception as e:
            logger.error(f"获取创建者分布失败: {e}")
            return []
    
    def get_tag_distribution(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """
        获取歌单标签分布统计
        :return: 标签统计列表
        """
        try:
            if self.playlists_df.empty:
                return []
            
            # 提取所有标签
            all_tags = []
            for tags_str in self.playlists_df['tags'].dropna():
                if tags_str:
                    tags = tags_str.split(',')
                    all_tags.extend([tag.strip() for tag in tags if tag.strip()])
            
            if not all_tags:
                logger.warning("没有标签数据")
                return []
            
            # 统计标签频率
            tag_counter = Counter(all_tags)
            top_tags = tag_counter.most_common(top_n)
            
            result = [{'tag': tag, 'count': count} for tag, count in top_tags]
            logger.info(f"获取到 {len(result)} 个热门标签")
            return result
            
        except Exception as e:
            logger.error(f"获取标签分布失败: {e}")
            return []
    
    def get_playlist_scale_distribution(self) -> Dict[str, int]:
        """
        获取歌单规模分布（按歌曲数量分类）
        :return: 规模分布字典
        """
        try:
            if self.playlists_df.empty:
                return {}
            
            # 定义规模分类
            small = len(self.playlists_df[self.playlists_df['track_count'] <= 20])
            medium = len(self.playlists_df[(self.playlists_df['track_count'] > 20) & 
                                           (self.playlists_df['track_count'] <= 50)])
            large = len(self.playlists_df[(self.playlists_df['track_count'] > 50) & 
                                          (self.playlists_df['track_count'] <= 100)])
            extra_large = len(self.playlists_df[self.playlists_df['track_count'] > 100])
            
            result = {
                '小型(<=20首)': small,
                '中型(21-50首)': medium,
                '大型(51-100首)': large,
                '超大型(>100首)': extra_large
            }
            
            logger.info(f"歌单规模分布: {result}")
            return result
            
        except Exception as e:
            logger.error(f"获取规模分布失败: {e}")
            return {}
    
    def get_play_subscribe_correlation(self) -> Tuple[List[int], List[int]]:
        """
        获取播放量与收藏数的相关性数据
        :return: (播放量列表, 收藏数列表)
        """
        try:
            if self.playlists_df.empty:
                return [], []
            
            # 过滤掉0值
            valid_df = self.playlists_df[
                (self.playlists_df['play_count'] > 0) & 
                (self.playlists_df['subscribed_count'] > 0)
            ]
            
            play_counts = valid_df['play_count'].tolist()
            subscribed_counts = valid_df['subscribed_count'].tolist()
            
            logger.info(f"获取到 {len(play_counts)} 组播放量与收藏数相关性数据")
            return play_counts, subscribed_counts
            
        except Exception as e:
            logger.error(f"获取相关性数据失败: {e}")
            return [], []
    
    def analyze_playlist_description(self, top_n: int = 50) -> List[Tuple[str, int]]:
        """
        分析歌单描述关键词
        :param top_n: TOP N 关键词
        :return: (关键词, 频率)列表
        """
        try:
            if self.playlists_df.empty:
                return []
            
            # 合并所有歌单描述
            descriptions = self.playlists_df['description'].dropna().tolist()
            if not descriptions:
                logger.warning("没有歌单描述数据")
                return []
            
            descriptions_text = ' '.join(descriptions)
            
            # 使用jieba分词
            words = jieba.cut(descriptions_text)
            
            # 停用词
            stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', 
                        '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
                        '你', '会', '着', '没有', '看', '好', '自己', '这', '啊', '吗',
                        '歌单', '音乐', '歌曲'}
            
            # 过滤短词和停用词
            filtered_words = [word for word in words 
                            if len(word) >= 2 and word not in stopwords]
            
            # 统计词频
            word_freq = Counter(filtered_words)
            top_words = word_freq.most_common(top_n)
            
            logger.info(f"提取了 {len(top_words)} 个描述关键词")
            return top_words
            
        except Exception as e:
            logger.error(f"分析歌单描述失败: {e}")
            return []
    
    def get_popularity_analysis(self) -> Dict[str, Any]:
        """
        综合热度分析（播放量、收藏数综合评估）
        :return: 热度分析结果
        """
        try:
            if self.playlists_df.empty:
                return {}
            
            # 计算综合热度指数 (播放量权重0.6 + 收藏数权重0.4)
            df = self.playlists_df.copy()
            
            # 归一化处理
            max_play = df['play_count'].max()
            max_subscribe = df['subscribed_count'].max()
            
            if max_play > 0 and max_subscribe > 0:
                df['normalized_play'] = df['play_count'] / max_play
                df['normalized_subscribe'] = df['subscribed_count'] / max_subscribe
                df['popularity_score'] = df['normalized_play'] * 0.6 + df['normalized_subscribe'] * 0.4
                
                # 获取TOP10综合热度歌单
                top_by_score = df.nlargest(10, 'popularity_score')
                
                result = {
                    'top_playlists': top_by_score[['playlist_name', 'creator_name', 
                                                   'play_count', 'subscribed_count']].to_dict('records'),
                    'avg_popularity_score': float(df['popularity_score'].mean()),
                    'high_popularity_count': len(df[df['popularity_score'] > 0.5]),  # 高热度歌单数量
                }
                
                logger.info("综合热度分析完成")
                return result
            else:
                return {}
            
        except Exception as e:
            logger.error(f"综合热度分析失败: {e}")
            return {}
    
    # ==================== 歌曲相关分析方法 ====================
    
    def get_song_statistics(self) -> Dict[str, Any]:
        """
        获取歌曲基础统计
        :return: 统计数据字典
        """
        try:
            if self.songs_df.empty:
                return {}
            
            stats = {
                'total_songs': len(self.songs_df),
                'unique_songs': self.songs_df['song_id'].nunique(),
                'total_artists': self.songs_df['artist'].nunique(),
                'total_albums': self.songs_df['album'].nunique(),
                'avg_duration': int(self.songs_df['duration'].mean()),
                'avg_popularity': float(self.songs_df['popularity'].mean()),
                'max_popularity': int(self.songs_df['popularity'].max()),
            }
            
            logger.info(f"歌曲统计: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"获取歌曲统计失败: {e}")
            return {}
    
    def get_top_songs(self, n: int = 30, by: str = 'popularity') -> List[Dict[str, Any]]:
        """
        获取TOP N 热门歌曲
        :param n: TOP N
        :param by: 排序字段 (popularity, duration)
        :return: 歌曲列表
        """
        try:
            if self.songs_df.empty:
                return []
            
            if by not in self.songs_df.columns:
                by = 'popularity'
            
            top_songs = self.songs_df.nlargest(n, by)
            columns = ['song_name', 'artist', 'album', 'duration_format', 'popularity', 'playlist_id']
            result = top_songs[columns].to_dict('records')
            
            logger.info(f"获取TOP {n} 歌曲 (按 {by})")
            return result
            
        except Exception as e:
            logger.error(f"获取TOP歌曲失败: {e}")
            return []
    
    def get_artist_distribution(self, n: int = 20) -> List[Dict[str, Any]]:
        """
        获取歌手分布统计
        :param n: TOP N 歌手
        :return: 歌手统计列表
        """
        try:
            if self.songs_df.empty:
                return []
            
            # 按歌手分组统计
            artist_stats = self.songs_df.groupby('artist').agg({
                'song_id': 'count',
                'popularity': 'mean',
                'duration': 'mean'
            }).reset_index()
            
            artist_stats.columns = ['artist', 'song_count', 'avg_popularity', 'avg_duration']
            
            # 转换为整数
            artist_stats['avg_popularity'] = artist_stats['avg_popularity'].astype(int)
            artist_stats['avg_duration'] = artist_stats['avg_duration'].astype(int)
            
            # 排序并取TOP N
            artist_stats = artist_stats.sort_values('song_count', ascending=False).head(n)
            
            result = artist_stats.to_dict('records')
            logger.info(f"获取TOP {n} 歌手分布")
            return result
            
        except Exception as e:
            logger.error(f"获取歌手分布失败: {e}")
            return []
    
    def get_album_distribution(self, n: int = 20) -> List[Dict[str, Any]]:
        """
        获取专辑分布统计
        :param n: TOP N 专辑
        :return: 专辑统计列表
        """
        try:
            if self.songs_df.empty:
                return []
            
            # 过滤空专辑
            album_df = self.songs_df[self.songs_df['album'].notna() & (self.songs_df['album'] != '')]
            
            if album_df.empty:
                return []
            
            # 按专辑分组统计
            album_stats = album_df.groupby('album').agg({
                'song_id': 'count',
                'artist': 'first',
                'popularity': 'mean'
            }).reset_index()
            
            album_stats.columns = ['album', 'song_count', 'artist', 'avg_popularity']
            album_stats['avg_popularity'] = album_stats['avg_popularity'].astype(int)
            
            # 排序并取TOP N
            album_stats = album_stats.sort_values('song_count', ascending=False).head(n)
            
            result = album_stats.to_dict('records')
            logger.info(f"获取TOP {n} 专辑分布")
            return result
            
        except Exception as e:
            logger.error(f"获取专辑分布失败: {e}")
            return []
    
    def get_song_duration_distribution(self) -> Dict[str, int]:
        """
        获取歌曲时长分布
        :return: 时长分布字典
        """
        try:
            if self.songs_df.empty:
                return {}
            
            # 将时长从毫秒转换为秒
            durations_sec = self.songs_df['duration'] / 1000
            
            # 定义时长区间（秒）
            very_short = len(durations_sec[durations_sec <= 120])  # ≤2分钟
            short = len(durations_sec[(durations_sec > 120) & (durations_sec <= 180)])  # 2-3分钟
            medium = len(durations_sec[(durations_sec > 180) & (durations_sec <= 300)])  # 3-5分钟
            long_duration = len(durations_sec[(durations_sec > 300) & (durations_sec <= 420)])  # 5-7分钟
            very_long = len(durations_sec[durations_sec > 420])  # >7分钟
            
            result = {
                '极短(≤2分钟)': very_short,
                '短(2-3分钟)': short,
                '中等(3-5分钟)': medium,
                '长(5-7分钟)': long_duration,
                '超长(>7分钟)': very_long
            }
            
            logger.info(f"歌曲时长分布: {result}")
            return result
            
        except Exception as e:
            logger.error(f"获取时长分布失败: {e}")
            return {}
    
    def get_cross_playlist_songs(self, min_playlists: int = 2) -> List[Dict[str, Any]]:
        """
        获取跨歌单热门歌曲（在多个歌单中出现的歌曲）
        :param min_playlists: 最少出现的歌单数
        :return: 跨歌单歌曲列表
        """
        try:
            if self.songs_df.empty:
                return []
            
            # 按song_id分组统计
            cross_songs = self.songs_df.groupby('song_id').agg({
                'song_name': 'first',
                'artist': 'first',
                'album': 'first',
                'popularity': 'mean',
                'playlist_id': 'count'  # 出现的歌单数量
            }).reset_index()
            
            cross_songs.columns = ['song_id', 'song_name', 'artist', 'album', 'avg_popularity', 'playlist_count']
            
            # 筛选出现在多个歌单中的歌曲
            cross_songs = cross_songs[cross_songs['playlist_count'] >= min_playlists]
            
            # 按出现次数排序
            cross_songs = cross_songs.sort_values('playlist_count', ascending=False)
            
            cross_songs['avg_popularity'] = cross_songs['avg_popularity'].astype(int)
            
            result = cross_songs.to_dict('records')
            logger.info(f"找到 {len(result)} 首跨歌单歌曲 (至少出现在 {min_playlists} 个歌单)")
            return result
            
        except Exception as e:
            logger.error(f"获取跨歌单歌曲失败: {e}")
            return []
    
    def get_unique_songs(self) -> List[Dict[str, Any]]:
        """
        获取去重后的唯一歌曲列表
        :return: 唯一歌曲列表
        """
        try:
            if self.songs_df.empty:
                return []
            
            # 按song_id去重，保留popularity最高的记录
            unique_songs = self.songs_df.sort_values('popularity', ascending=False).drop_duplicates('song_id')
            
            columns = ['song_id', 'song_name', 'artist', 'album', 'duration_format', 'popularity']
            result = unique_songs[columns].to_dict('records')
            
            logger.info(f"获取 {len(result)} 首唯一歌曲")
            return result
            
        except Exception as e:
            logger.error(f"获取唯一歌曲失败: {e}")
            return []
    
    def export_to_csv(self, output_path: str = None) -> bool:
        """
        导出歌单数据为CSV
        :param output_path: 输出文件路径
        :return: 是否成功
        """
        try:
            if output_path is None:
                output_path = OUTPUT_CONFIG['csv_export_path']
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.playlists_df.empty:
                self.playlists_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                logger.info(f"歌单数据已导出到: {output_path}")
                return True
            else:
                logger.warning("没有数据可导出")
                return False
                
        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            return False


if __name__ == '__main__':
    # 测试热门歌单数据分析
    analyzer = DataAnalyzer()
    
    print("="*60)
    print("热门歌单数据分析测试")
    print("="*60)
    
    # 1. 基础统计
    stats = analyzer.get_basic_statistics()
    print("\n【基础统计】")
    for key, value in stats.items():
        print(f"  {key}: {value:,}" if isinstance(value, int) else f"  {key}: {value}")
    
    # 2. TOP歌单
    print("\n【TOP 10 热门歌单（按播放量）】")
    top_playlists = analyzer.get_top_playlists(10, 'play_count')
    for i, playlist in enumerate(top_playlists, 1):
        print(f"  {i}. {playlist.get('playlist_name', 'N/A')[:30]}")
        print(f"     创建者: {playlist.get('creator_name', 'N/A')}")
        print(f"     播放: {playlist.get('play_count', 0):,} | "
              f"收藏: {playlist.get('subscribed_count', 0):,}")
    
    # 3. 创建者分布
    print("\n【TOP 10 热门创建者】")
    creators = analyzer.get_creator_distribution(10)
    for i, creator in enumerate(creators, 1):
        print(f"  {i}. {creator.get('creator_name', 'N/A')}")
        print(f"     歌单数: {creator.get('playlist_count', 0)} | "
              f"总播放: {creator.get('total_play_count', 0):,}")
    
    # 4. 标签分布
    print("\n【TOP 15 热门标签】")
    tags = analyzer.get_tag_distribution(15)
    for i, tag in enumerate(tags, 1):
        print(f"  {i}. {tag.get('tag', 'N/A')}: {tag.get('count', 0)} 次")
    
    # 5. 规模分布
    print("\n【歌单规模分布】")
    scale_dist = analyzer.get_playlist_scale_distribution()
    for scale, count in scale_dist.items():
        print(f"  {scale}: {count} 个")
    
    # 6. 综合热度分析
    print("\n【综合热度分析】")
    popularity = analyzer.get_popularity_analysis()
    if popularity:
        print(f"  平均热度分数: {popularity.get('avg_popularity_score', 0):.3f}")
        print(f"  高热度歌单数量: {popularity.get('high_popularity_count', 0)}")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)

