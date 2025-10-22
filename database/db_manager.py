"""
数据库管理模块
使用SQLite存储歌单和歌曲数据
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import DATABASE_CONFIG
from utils.logger import get_logger

logger = get_logger()


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库管理器
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path if db_path else DATABASE_CONFIG['db_path']
        self.conn = None
        self.cursor = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库连接和表结构"""
        try:
            # 确保数据目录存在
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # 连接数据库
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
            self.cursor = self.conn.cursor()
            
            # 创建表
            self._create_tables()
            
            logger.info(f"数据库初始化成功: {self.db_path}")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def _create_tables(self):
        """创建数据库表"""
        try:
            # 歌单表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playlist_id TEXT UNIQUE NOT NULL,
                    playlist_name TEXT NOT NULL,
                    creator_name TEXT,
                    creator_id TEXT,
                    play_count INTEGER DEFAULT 0,
                    subscribed_count INTEGER DEFAULT 0,
                    track_count INTEGER DEFAULT 0,
                    share_count INTEGER DEFAULT 0,
                    comment_count INTEGER DEFAULT 0,
                    tags TEXT,
                    description TEXT,
                    cover_img_url TEXT,
                    playlist_url TEXT,
                    create_time TIMESTAMP,
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 歌曲表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_id TEXT NOT NULL,
                    song_name TEXT NOT NULL,
                    artist TEXT,
                    artist_id TEXT,
                    album TEXT,
                    album_id TEXT,
                    duration INTEGER DEFAULT 0,
                    duration_format TEXT,
                    popularity INTEGER DEFAULT 0,
                    position INTEGER DEFAULT 0,
                    publish_time TEXT,
                    song_url TEXT,
                    cover_url TEXT,
                    playlist_id TEXT NOT NULL,
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
                )
            """)
            
            # 评论表（可选，暂时保留结构）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment_id TEXT UNIQUE NOT NULL,
                    song_id TEXT NOT NULL,
                    user_name TEXT,
                    user_id TEXT,
                    content TEXT,
                    like_count INTEGER DEFAULT 0,
                    comment_time TIMESTAMP,
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (song_id) REFERENCES songs(song_id)
                )
            """)
            
            # 创建索引
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_playlist_id 
                ON playlists(playlist_id)
            """)
            
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_playlist_play_count 
                ON playlists(play_count DESC)
            """)
            
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_song_id 
                ON songs(song_id)
            """)
            
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_artist 
                ON songs(artist)
            """)
            
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_song_playlist_id 
                ON songs(playlist_id)
            """)
            
            self.conn.commit()
            logger.info("数据库表创建成功")
            
        except Exception as e:
            logger.error(f"创建数据库表失败: {e}")
            raise
    
    # ==================== 歌单相关方法 ====================
    
    def insert_playlist(self, playlist_data: Dict[str, Any]) -> bool:
        """
        插入单个歌单数据
        :param playlist_data: 歌单数据字典
        :return: 是否成功
        """
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO playlists (
                    playlist_id, playlist_name, creator_name, creator_id,
                    play_count, subscribed_count, track_count,
                    share_count, comment_count, tags, description,
                    cover_img_url, playlist_url, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                playlist_data.get('playlist_id'),
                playlist_data.get('playlist_name'),
                playlist_data.get('creator_name'),
                playlist_data.get('creator_id'),
                playlist_data.get('play_count', 0),
                playlist_data.get('subscribed_count', 0),
                playlist_data.get('track_count', 0),
                playlist_data.get('share_count', 0),
                playlist_data.get('comment_count', 0),
                playlist_data.get('tags'),
                playlist_data.get('description'),
                playlist_data.get('cover_img_url'),
                playlist_data.get('playlist_url'),
                playlist_data.get('create_time')
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"插入歌单数据失败: {e}")
            self.conn.rollback()
            return False
    
    def insert_playlists_batch(self, playlists_data: List[Dict[str, Any]]) -> int:
        """
        批量插入歌单数据
        :param playlists_data: 歌单数据列表
        :return: 成功插入的数量
        """
        success_count = 0
        for playlist_data in playlists_data:
            if self.insert_playlist(playlist_data):
                success_count += 1
        
        logger.info(f"批量插入歌单: 成功 {success_count}/{len(playlists_data)}")
        return success_count
    
    def get_all_playlists(self) -> List[Dict[str, Any]]:
        """获取所有歌单"""
        try:
            self.cursor.execute("SELECT * FROM playlists ORDER BY play_count DESC")
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"获取所有歌单失败: {e}")
            return []
    
    def get_playlist_by_id(self, playlist_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取歌单"""
        try:
            self.cursor.execute("SELECT * FROM playlists WHERE playlist_id = ?", (playlist_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"获取歌单失败: {e}")
            return None
    
    def get_top_playlists(self, n: int = 30, order_by: str = 'play_count') -> List[Dict[str, Any]]:
        """
        获取TOP N歌单
        :param n: TOP N
        :param order_by: 排序字段
        :return: 歌单列表
        """
        try:
            valid_columns = ['play_count', 'subscribed_count', 'track_count', 'comment_count']
            if order_by not in valid_columns:
                order_by = 'play_count'
            
            query = f"SELECT * FROM playlists ORDER BY {order_by} DESC LIMIT ?"
            self.cursor.execute(query, (n,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"获取TOP歌单失败: {e}")
            return []
    
    # ==================== 歌曲相关方法 ====================
    
    def insert_song(self, song_data: Dict[str, Any]) -> bool:
        """
        插入单首歌曲数据
        :param song_data: 歌曲数据字典
        :return: 是否成功
        """
        try:
            self.cursor.execute("""
                INSERT INTO songs (
                    song_id, song_name, artist, artist_id, album, album_id,
                    duration, duration_format, popularity, position,
                    publish_time, song_url, cover_url, playlist_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                song_data.get('song_id'),
                song_data.get('song_name'),
                song_data.get('artist'),
                song_data.get('artist_id'),
                song_data.get('album'),
                song_data.get('album_id'),
                song_data.get('duration', 0),
                song_data.get('duration_format'),
                song_data.get('popularity', 0),
                song_data.get('position', 0),
                song_data.get('publish_time'),
                song_data.get('song_url'),
                song_data.get('cover_url'),
                song_data.get('playlist_id')
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"插入歌曲数据失败: {e}")
            self.conn.rollback()
            return False
    
    def insert_songs_batch(self, songs_data: List[Dict[str, Any]]) -> int:
        """
        批量插入歌曲数据
        :param songs_data: 歌曲数据列表
        :return: 成功插入的数量
        """
        success_count = 0
        for song_data in songs_data:
            if self.insert_song(song_data):
                success_count += 1
        
        logger.info(f"批量插入歌曲: 成功 {success_count}/{len(songs_data)}")
        return success_count
    
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """获取所有歌曲"""
        try:
            self.cursor.execute("SELECT * FROM songs ORDER BY popularity DESC")
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"获取所有歌曲失败: {e}")
            return []
    
    def get_songs_by_playlist(self, playlist_id: str) -> List[Dict[str, Any]]:
        """根据歌单ID获取歌曲列表"""
        try:
            self.cursor.execute("""
                SELECT * FROM songs 
                WHERE playlist_id = ? 
                ORDER BY position ASC
            """, (playlist_id,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"获取歌单歌曲失败: {e}")
            return []
    
    def get_top_songs(self, n: int = 30, order_by: str = 'popularity') -> List[Dict[str, Any]]:
        """
        获取TOP N歌曲
        :param n: TOP N
        :param order_by: 排序字段
        :return: 歌曲列表
        """
        try:
            valid_columns = ['popularity', 'duration']
            if order_by not in valid_columns:
                order_by = 'popularity'
            
            query = f"SELECT * FROM songs ORDER BY {order_by} DESC LIMIT ?"
            self.cursor.execute(query, (n,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"获取TOP歌曲失败: {e}")
            return []
    
    def get_song_statistics(self) -> Dict[str, Any]:
        """获取歌曲统计数据"""
        try:
            stats = {}
            
            # 基础统计
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_song_records,
                    COUNT(DISTINCT song_id) as unique_songs,
                    COUNT(DISTINCT artist) as total_artists,
                    COUNT(DISTINCT album) as total_albums,
                    AVG(duration) as avg_duration,
                    AVG(popularity) as avg_popularity,
                    MAX(popularity) as max_popularity
                FROM songs
            """)
            row = self.cursor.fetchone()
            stats.update(dict(row))
            
            # 歌单分布
            self.cursor.execute("""
                SELECT COUNT(DISTINCT playlist_id) as playlists_with_songs
                FROM songs
            """)
            row = self.cursor.fetchone()
            stats.update(dict(row))
            
            return stats
            
        except Exception as e:
            logger.error(f"获取歌曲统计失败: {e}")
            return {}
    
    def get_unique_songs(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        获取去重后的唯一歌曲
        :param limit: 限制数量
        :return: 唯一歌曲列表
        """
        try:
            # 使用子查询获取每首歌曲popularity最高的记录
            query = """
                SELECT * FROM songs
                WHERE id IN (
                    SELECT id FROM (
                        SELECT id, song_id, popularity,
                               ROW_NUMBER() OVER (PARTITION BY song_id ORDER BY popularity DESC) as rn
                        FROM songs
                    ) WHERE rn = 1
                )
                ORDER BY popularity DESC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            result = [dict(row) for row in rows]
            
            logger.info(f"获取 {len(result)} 首唯一歌曲")
            return result
            
        except Exception as e:
            # 如果ROW_NUMBER不支持，使用备用方案
            logger.warning(f"使用备用去重方案: {e}")
            try:
                query = """
                    SELECT s1.* FROM songs s1
                    LEFT JOIN songs s2 ON s1.song_id = s2.song_id AND s1.popularity < s2.popularity
                    WHERE s2.song_id IS NULL
                    ORDER BY s1.popularity DESC
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                return [dict(row) for row in rows]
            except Exception as e2:
                logger.error(f"获取唯一歌曲失败: {e2}")
                return []
    
    def get_cross_playlist_songs(self, min_count: int = 2) -> List[Dict[str, Any]]:
        """
        获取跨歌单出现的歌曲
        :param min_count: 最少出现的歌单数
        :return: 跨歌单歌曲列表
        """
        try:
            query = """
                SELECT 
                    song_id,
                    song_name,
                    artist,
                    album,
                    AVG(popularity) as avg_popularity,
                    COUNT(DISTINCT playlist_id) as playlist_count
                FROM songs
                GROUP BY song_id, song_name, artist, album
                HAVING COUNT(DISTINCT playlist_id) >= ?
                ORDER BY playlist_count DESC, avg_popularity DESC
            """
            
            self.cursor.execute(query, (min_count,))
            rows = self.cursor.fetchall()
            result = [dict(row) for row in rows]
            
            logger.info(f"找到 {len(result)} 首跨歌单歌曲 (至少 {min_count} 个歌单)")
            return result
            
        except Exception as e:
            logger.error(f"获取跨歌单歌曲失败: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        try:
            stats = {}
            
            # 歌单统计
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_playlists,
                    SUM(play_count) as total_playlist_play_count,
                    AVG(play_count) as avg_playlist_play_count,
                    SUM(subscribed_count) as total_playlist_subscribe_count,
                    AVG(subscribed_count) as avg_subscribed_count,
                    AVG(track_count) as avg_track_count,
                    MAX(play_count) as max_playlist_play_count,
                    MAX(subscribed_count) as max_playlist_subscribe_count
                FROM playlists
            """)
            row = self.cursor.fetchone()
            if row:
                stats.update(dict(row))
            
            # 歌曲统计
            song_stats = self.get_song_statistics()
            stats.update(song_stats)
            
            return stats
            
        except Exception as e:
            logger.error(f"获取统计数据失败: {e}")
            return {}
    
    def clear_all_data(self):
        """清空所有数据"""
        try:
            self.cursor.execute("DELETE FROM comments")
            self.cursor.execute("DELETE FROM songs")
            self.cursor.execute("DELETE FROM playlists")
            self.conn.commit()
            logger.info("已清空所有数据")
        except Exception as e:
            logger.error(f"清空数据失败: {e}")
            self.conn.rollback()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")


