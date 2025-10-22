"""
网易云音乐爬虫模块 - 热门歌单数据采集
使用API接口方式爬取热门歌单数据
支持分页、分类、排序等功能
"""
import time
import random
import requests
from typing import List, Dict, Any, Optional

from config.settings import SPIDER_CONFIG
from utils.logger import get_logger

logger = get_logger()


class MusicSpider:
    """网易云音乐爬虫类 - 热门歌单数据采集"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        self._setup_session()
        logger.info("热门歌单爬虫初始化成功")
    
    def _setup_session(self):
        """配置请求会话"""
        # 设置请求头
        self.session.headers.update({
            'User-Agent': random.choice(SPIDER_CONFIG['user_agents']),
            'Referer': 'https://music.163.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://music.163.com',
        })
        
        # 设置Cookie
        self.session.cookies.set('appver', '8.7.01')
        self.session.cookies.set('os', 'pc')
    
    def _random_delay(self):
        """随机延时"""
        time.sleep(random.uniform(SPIDER_CONFIG['min_delay'], SPIDER_CONFIG['max_delay']))
    
    def crawl_hot_playlists(self, max_pages: int = 20, category: str = '全部', order: str = 'hot') -> List[Dict[str, Any]]:
        """
        爬取热门歌单（支持分页）
        :param max_pages: 最大页数（每页50个歌单）
        :param category: 歌单分类
        :param order: 排序方式（hot=最热、new=最新）
        :return: 歌单数据列表
        """
        playlists_data = []
        
        try:
            logger.info(f"开始爬取热门歌单，目标页数: {max_pages}，分类: {category}，排序: {order}")
            
            # 网易云音乐热门歌单API
            # 每页50个歌单，offset = (page - 1) * 50
            for page in range(1, max_pages + 1):
                offset = (page - 1) * 50
                limit = 50
                
                try:
                    # 使用网易云音乐的歌单广场API
                    url = 'https://music.163.com/api/playlist/list'
                    params = {
                        'cat': category,  # 分类
                        'order': order,  # 排序方式
                        'offset': offset,  # 偏移量
                        'limit': limit,  # 每页数量
                        'total': 'true'  # 返回总数
                    }
                    
                    response = self.session.get(url, params=params, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get('code') == 200 and 'playlists' in data:
                            playlists = data['playlists']
                            
                            if not playlists:
                                logger.info(f"第 {page} 页没有更多歌单，停止爬取")
                                break
                            
                            logger.info(f"正在爬取第 {page}/{max_pages} 页，获取到 {len(playlists)} 个歌单")
                            
                            # 解析每个歌单
                            for idx, playlist_info in enumerate(playlists, 1):
                                try:
                                    playlist_data = self._parse_playlist_data(playlist_info, offset + idx)
                                    if playlist_data:
                                        playlists_data.append(playlist_data)
                                        
                                        # 打印简要信息
                                        logger.info(
                                            f"  [{offset + idx}] {playlist_data['playlist_name'][:30]} | "
                                            f"播放:{playlist_data['play_count']:,} | "
                                            f"收藏:{playlist_data['subscribed_count']:,} | "
                                            f"歌曲:{playlist_data['track_count']}"
                                        )
                                        
                                except Exception as e:
                                    logger.error(f"解析歌单 {idx} 失败: {e}")
                                    continue
                            
                            # 每页之后延时
                            if page < max_pages:
                                self._random_delay()
                        else:
                            logger.warning(f"第 {page} 页API返回错误: {data.get('msg', 'Unknown error')}")
                            break
                    else:
                        logger.warning(f"第 {page} 页请求失败，状态码: {response.status_code}")
                        break
                        
                except Exception as e:
                    logger.error(f"爬取第 {page} 页失败: {e}")
                    continue
            
            logger.info(f"热门歌单爬取完成，共 {len(playlists_data)} 个歌单")
            
        except Exception as e:
            logger.error(f"爬取热门歌单失败: {e}")
        
        return playlists_data
    
    def _parse_playlist_data(self, playlist_info: Dict, rank: int) -> Optional[Dict[str, Any]]:
        """
        解析歌单数据
        :param playlist_info: API返回的歌单信息
        :param rank: 排名/序号
        :return: 格式化的歌单数据
        """
        try:
            playlist_data = {
                'rank': rank,
                'playlist_id': str(playlist_info.get('id', '')),
                'playlist_name': playlist_info.get('name', ''),
                'description': playlist_info.get('description', ''),
                'cover_url': playlist_info.get('coverImgUrl', ''),
                'creator_name': playlist_info.get('creator', {}).get('nickname', ''),
                'creator_id': str(playlist_info.get('creator', {}).get('userId', '')),
                'play_count': playlist_info.get('playCount', 0),
                'subscribed_count': playlist_info.get('subscribedCount', 0),
                'track_count': playlist_info.get('trackCount', 0),
                'share_count': playlist_info.get('shareCount', 0),
                'comment_count': playlist_info.get('commentCount', 0),
                'playlist_url': f"https://music.163.com/#/playlist?id={playlist_info.get('id', '')}",
            }
            
            # 标签
            tags = playlist_info.get('tags', [])
            playlist_data['tags'] = ','.join(tags) if tags else ''
            
            # 创建时间
            create_time = playlist_info.get('createTime', 0)
            if create_time:
                from datetime import datetime
                date = datetime.fromtimestamp(create_time / 1000)
                playlist_data['create_time'] = date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                playlist_data['create_time'] = ''
            
            # 更新频率
            playlist_data['update_frequency'] = playlist_info.get('updateFrequency', '')
            
            return playlist_data
            
        except Exception as e:
            logger.error(f"解析歌单数据失败: {e}")
            return None
    
    def get_hot_playlist_categories(self) -> List[str]:
        """
        获取热门歌单分类列表
        :return: 分类列表
        """
        # 网易云音乐的主要分类
        categories = [
            '全部', '华语', '欧美', '日语', '韩语', '粤语',
            '流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐',
            '爵士', '乡村', 'R&B/Soul', '古典', '民族',
            '清晨', '夜晚', '学习', '工作', '午休', '下午茶',
            '地铁', '驾车', '运动', '旅行', '散步', '酒吧'
        ]
        return categories
    
    def get_playlist_detail(self, playlist_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定歌单的详细信息
        :param playlist_id: 歌单ID
        :return: 歌单详细信息
        """
        try:
            url = f'https://music.163.com/api/playlist/detail?id={playlist_id}'
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 200 and 'result' in data:
                    playlist = data['result']
                    
                    playlist_data = {
                        'playlist_id': str(playlist.get('id', '')),
                        'playlist_name': playlist.get('name', ''),
                        'description': playlist.get('description', ''),
                        'cover_url': playlist.get('coverImgUrl', ''),
                        'creator_name': playlist.get('creator', {}).get('nickname', ''),
                        'creator_id': str(playlist.get('creator', {}).get('userId', '')),
                        'play_count': playlist.get('playCount', 0),
                        'subscribed_count': playlist.get('subscribedCount', 0),
                        'track_count': playlist.get('trackCount', 0),
                        'share_count': playlist.get('shareCount', 0),
                        'comment_count': playlist.get('commentCount', 0),
                        'playlist_url': f"https://music.163.com/#/playlist?id={playlist_id}",
                    }
                    
                    # 标签
                    tags = playlist.get('tags', [])
                    playlist_data['tags'] = ','.join(tags) if tags else ''
                    
                    # 创建时间
                    create_time = playlist.get('createTime', 0)
                    if create_time:
                        from datetime import datetime
                        date = datetime.fromtimestamp(create_time / 1000)
                        playlist_data['create_time'] = date.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        playlist_data['create_time'] = ''
                    
                    playlist_data['update_frequency'] = playlist.get('updateFrequency', '')
                    
                    logger.info(f"获取歌单详情成功: {playlist_data['playlist_name']}")
                    return playlist_data
            
        except Exception as e:
            logger.error(f"获取歌单详情失败: {e}")
        
        return None
    
    def get_playlist_songs(self, playlist_id: str) -> List[Dict[str, Any]]:
        """
        获取歌单中的所有歌曲
        :param playlist_id: 歌单ID
        :return: 歌曲列表
        """
        try:
            url = f'https://music.163.com/api/playlist/detail?id={playlist_id}'
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 200 and 'result' in data:
                    playlist = data['result']
                    tracks = playlist.get('tracks', [])
                    
                    songs_data = []
                    for idx, track in enumerate(tracks, 1):
                        song_data = self._parse_song_data(track, playlist_id, idx)
                        if song_data:
                            songs_data.append(song_data)
                    
                    logger.info(f"获取歌单 {playlist_id} 的 {len(songs_data)} 首歌曲")
                    return songs_data
            
        except Exception as e:
            logger.error(f"获取歌单歌曲失败: {e}")
        
        return []
    
    def _parse_song_data(self, track: Dict, playlist_id: str, position: int) -> Optional[Dict[str, Any]]:
        """
        解析歌曲数据
        :param track: API返回的歌曲信息
        :param playlist_id: 所属歌单ID
        :param position: 在歌单中的位置
        :return: 格式化的歌曲数据
        """
        try:
            song_data = {
                'song_id': str(track.get('id', '')),
                'song_name': track.get('name', ''),
                'playlist_id': playlist_id,
                'position': position,
                'duration': track.get('duration', 0),  # 毫秒
                'popularity': track.get('popularity', 0),  # 热度值
            }
            
            # 歌手信息
            artists = track.get('artists', [])
            if artists:
                artist_names = [artist.get('name', '') for artist in artists]
                song_data['artist'] = ', '.join(artist_names)
                song_data['artist_id'] = str(artists[0].get('id', '')) if artists else ''
            else:
                song_data['artist'] = ''
                song_data['artist_id'] = ''
            
            # 专辑信息
            album = track.get('album', {})
            song_data['album'] = album.get('name', '')
            song_data['album_id'] = str(album.get('id', ''))
            
            # 封面
            song_data['cover_url'] = album.get('picUrl', '')
            
            # 发行时间
            publish_time = album.get('publishTime', 0)
            if publish_time:
                from datetime import datetime
                date = datetime.fromtimestamp(publish_time / 1000)
                song_data['publish_time'] = date.strftime('%Y-%m-%d')
            else:
                song_data['publish_time'] = ''
            
            # 歌曲URL
            song_data['song_url'] = f"https://music.163.com/#/song?id={track.get('id', '')}"
            
            # 格式化时长
            duration_sec = track.get('duration', 0) // 1000
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            song_data['duration_format'] = f"{minutes}:{seconds:02d}"
            
            return song_data
            
        except Exception as e:
            logger.error(f"解析歌曲数据失败: {e}")
            return None
    
    def crawl_playlist_songs_batch(self, playlist_ids: List[str], max_songs_per_playlist: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        批量爬取多个歌单的歌曲
        :param playlist_ids: 歌单ID列表
        :param max_songs_per_playlist: 每个歌单最多爬取的歌曲数（None表示全部）
        :return: {playlist_id: [songs]} 字典
        """
        result = {}
        
        try:
            logger.info(f"开始批量爬取 {len(playlist_ids)} 个歌单的歌曲")
            
            for i, playlist_id in enumerate(playlist_ids, 1):
                try:
                    logger.info(f"正在爬取第 {i}/{len(playlist_ids)} 个歌单的歌曲 (ID: {playlist_id})")
                    
                    songs = self.get_playlist_songs(playlist_id)
                    
                    if max_songs_per_playlist and len(songs) > max_songs_per_playlist:
                        songs = songs[:max_songs_per_playlist]
                    
                    result[playlist_id] = songs
                    logger.info(f"  获取到 {len(songs)} 首歌曲")
                    
                    # 延时避免请求过快
                    if i < len(playlist_ids):
                        self._random_delay()
                        
                except Exception as e:
                    logger.error(f"爬取歌单 {playlist_id} 的歌曲失败: {e}")
                    result[playlist_id] = []
                    continue
            
            total_songs = sum(len(songs) for songs in result.values())
            logger.info(f"批量爬取完成，共获取 {total_songs} 首歌曲")
            
        except Exception as e:
            logger.error(f"批量爬取歌曲失败: {e}")
        
        return result
    
    def close(self):
        """关闭会话"""
        if self.session:
            self.session.close()
            logger.info("爬虫会话已关闭")
    
    def __del__(self):
        """析构函数"""
        self.close()


if __name__ == '__main__':
    # 测试爬虫
    print("=" * 70)
    print("网易云音乐热门歌单爬虫测试")
    print("=" * 70)
    
    spider = MusicSpider()
    
    # 测试1: 爬取热门歌单（前2页，共100个）
    print("\n[测试1] 爬取热门歌单 (前2页，共100个)")
    print("-" * 70)
    hot_playlists = spider.crawl_hot_playlists(max_pages=2, category='全部', order='hot')
    
    if hot_playlists:
        print(f"\n[成功] 成功爬取 {len(hot_playlists)} 个热门歌单")
        print(f"\n前10个热门歌单:\n")
        for i, playlist in enumerate(hot_playlists[:10], 1):
            print(f"[{i:2d}] {playlist['playlist_name'][:40]}")
            print(f"     创建者: {playlist['creator_name']}")
            print(f"     播放: {playlist['play_count']:,} | 收藏: {playlist['subscribed_count']:,} | 歌曲: {playlist['track_count']}")
            if playlist['tags']:
                print(f"     标签: {playlist['tags']}")
            print()
    else:
        print("[失败] 爬取热门歌单失败")
    
    # 测试2: 获取指定歌单详情
    if hot_playlists:
        print("\n[测试2] 获取第一个歌单的详细信息")
        print("-" * 70)
        
        first_playlist_id = hot_playlists[0]['playlist_id']
        detail = spider.get_playlist_detail(first_playlist_id)
        
        if detail:
            print(f"\n歌单名称: {detail['playlist_name']}")
            print(f"创建者: {detail['creator_name']}")
            print(f"播放次数: {detail['play_count']:,}")
            print(f"收藏次数: {detail['subscribed_count']:,}")
            print(f"歌曲总数: {detail['track_count']}")
            print(f"创建时间: {detail['create_time']}")
            print(f"标签: {detail['tags']}")
            print(f"描述: {detail['description'][:100]}...")
        else:
            print("[失败] 获取歌单详情失败")
    
    # 测试3: 获取分类列表
    print("\n[测试3] 获取歌单分类列表")
    print("-" * 70)
    categories = spider.get_hot_playlist_categories()
    print(f"\n支持的分类 ({len(categories)}个):")
    for i in range(0, len(categories), 6):
        row = categories[i:i+6]
        print("  " + " | ".join(f"{cat:10s}" for cat in row))
    
    spider.close()
    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)
