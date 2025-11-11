"""
网易云音乐热门歌单数据爬取与可视化分析
主程序入口
"""
import os
import sys
import time
from datetime import datetime

from config.settings import create_directories, SPIDER_CONFIG
from database.db_manager import DatabaseManager
from spider.music_spider import MusicSpider
from utils.logger import get_logger

logger = get_logger()


class MusicAnalysisApp:
    """音乐分析应用主类"""
    
    def __init__(self):
        """初始化应用"""
        self.db = None
        self.spider = None
        
        # 创建必要的目录
        create_directories()
        
        # 初始化数据库
        try:
            self.db = DatabaseManager()
            logger.info("应用初始化成功")
        except Exception as e:
            logger.error(f"应用初始化失败: {e}")
            sys.exit(1)
    
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("  网易云音乐热门歌单数据分析系统")
        print("="*60)
        print("\n主菜单:")
        print("  1. 爬取热门歌单数据")
        print("  2. 爬取歌单内的歌曲")
        print("  3. 数据分析")
        print("  4. 生成可视化报告 ⭐")
        print("  5. 查看数据库统计")
        print("  6. 导出数据为CSV")
        print("  7. 清空数据库")
        print("  0. 退出程序")
        print("-"*60)
    
    def crawl_hot_playlists(self):
        """爬取热门歌单功能"""
        print("\n【爬取热门歌单】")
        print("-"*60)
        
        try:
            # 初始化爬虫
            if not self.spider:
                self.spider = MusicSpider()
            
            # 显示分类选项
            categories = self.spider.get_hot_playlist_categories()
            print("\n可选分类:")
            for i in range(0, len(categories), 6):
                row = categories[i:i+6]
                print("  " + " | ".join(f"{j+i+1:2d}.{cat:8s}" for j, cat in enumerate(row)))
            
            print(f"\n  默认: 全部")
            
            category_choice = input("\n请选择分类序号 (直接回车使用默认): ").strip()
            
            category = SPIDER_CONFIG['default_playlist_category']
            if category_choice.isdigit():
                idx = int(category_choice) - 1
                if 0 <= idx < len(categories):
                    category = categories[idx]
            
            print(f"已选择分类: {category}")
            
            # 获取爬取参数
            print(f"\n默认爬取页数: {SPIDER_CONFIG['max_playlist_pages']} (每页50个，共约{SPIDER_CONFIG['max_playlist_pages'] * 50}个歌单)")
            user_input = input("请输入要爬取的页数 (1-50, 直接回车使用默认): ").strip()
            
            max_pages = SPIDER_CONFIG['max_playlist_pages']
            if user_input and user_input.isdigit():
                max_pages = min(int(user_input), 50)  # 限制最多50页
            
            total_playlists = max_pages * 50
            print(f"\n将爬取 {max_pages} 页，约 {total_playlists} 个热门歌单")
            print("[注意] 爬取较多歌单需要较长时间，建议从2-5页开始测试")
            
            confirm = input("\n是否继续? (y/n, 默认y): ").strip().lower()
            if confirm and confirm != 'y':
                print("已取消爬取")
                return
            
            print(f"\n开始爬取热门歌单...")
            print("提示: 爬取过程可能需要较长时间，请耐心等待...")
            
            # 爬取热门歌单
            start_time = time.time()
            
            playlists_data = self.spider.crawl_hot_playlists(
                max_pages=max_pages,
                category=category,
                order='hot'
            )
            
            if not playlists_data:
                print("[失败] 爬取失败，没有获取到数据")
                return
            
            print(f"\n[成功] 成功爬取 {len(playlists_data)} 个热门歌单")
            
            # 保存到数据库
            print("\n正在保存到数据库...")
            success_count = self.db.insert_playlists_batch(playlists_data)
            print(f"[成功] 已保存 {success_count} 个歌单到数据库")
            
            # 显示统计信息
            if playlists_data:
                total_play = sum(p.get('play_count', 0) for p in playlists_data)
                total_subscribe = sum(p.get('subscribed_count', 0) for p in playlists_data)
                avg_play = total_play // len(playlists_data) if playlists_data else 0
                avg_subscribe = total_subscribe // len(playlists_data) if playlists_data else 0
                
                print(f"\n[统计] 统计信息:")
                print(f"  总播放量: {total_play:,}")
                print(f"  总收藏数: {total_subscribe:,}")
                print(f"  平均播放量: {avg_play:,}")
                print(f"  平均收藏数: {avg_subscribe:,}")
            
            elapsed_time = time.time() - start_time
            print(f"\n爬取完成! 耗时: {elapsed_time:.2f} 秒")
            
        except KeyboardInterrupt:
            print("\n\n用户中断爬取")
        except Exception as e:
            logger.error(f"爬取热门歌单失败: {e}")
            print(f"[失败] 爬取失败: {e}")
        finally:
            # 清理爬虫资源
            if self.spider:
                self.spider.close()
                self.spider = None
    
    def crawl_playlist_songs(self):
        """爬取歌单内的歌曲功能"""
        print("\n【爬取歌单内的歌曲】")
        print("-"*60)
        
        try:
            # 检查是否有歌单数据
            stats = self.db.get_statistics()
            if not stats or stats.get('total_playlists', 0) == 0:
                print("\n[提示] 数据库中暂无歌单数据，请先爬取热门歌单")
                return
            
            print(f"\n数据库中有 {stats.get('total_playlists', 0)} 个歌单")
            
            # 获取用户选择
            print("\n爬取选项:")
            print("  1. 爬取所有歌单的歌曲")
            print("  2. 爬取前N个歌单的歌曲")
            print("  3. 爬取指定歌单的歌曲")
            print("  0. 返回主菜单")
            
            choice = input("\n请选择 (0-3): ").strip()
            
            if choice == '0':
                return
            
            # 初始化爬虫
            if not self.spider:
                self.spider = MusicSpider()
            
            playlist_ids = []
            max_songs_per_playlist = None
            
            if choice == '1':
                # 爬取所有歌单
                confirm = input(f"\n将爬取所有 {stats.get('total_playlists', 0)} 个歌单的歌曲，可能需要很长时间。是否继续? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("已取消")
                    return
                
                playlists = self.db.get_all_playlists()
                playlist_ids = [p['playlist_id'] for p in playlists]
                
                # 询问是否限制每个歌单的歌曲数
                limit_input = input("\n是否限制每个歌单爬取的歌曲数? (输入数字或直接回车不限制): ").strip()
                if limit_input.isdigit():
                    max_songs_per_playlist = int(limit_input)
                    print(f"将限制每个歌单爬取前 {max_songs_per_playlist} 首歌曲")
            
            elif choice == '2':
                # 爬取前N个歌单
                n_input = input(f"\n请输入要爬取的歌单数量 (1-{stats.get('total_playlists', 0)}): ").strip()
                if not n_input.isdigit():
                    print("[错误] 无效的输入")
                    return
                
                n = min(int(n_input), stats.get('total_playlists', 0))
                
                # 按播放量排序获取TOP N
                top_playlists = self.db.get_top_playlists(n, 'play_count')
                playlist_ids = [p['playlist_id'] for p in top_playlists]
                
                print(f"\n将爬取播放量TOP {n} 的歌单:")
                for i, p in enumerate(top_playlists[:5], 1):
                    print(f"  {i}. {p['playlist_name'][:30]} (播放: {p['play_count']:,})")
                if n > 5:
                    print(f"  ...")
                
                # 询问是否限制每个歌单的歌曲数
                limit_input = input("\n是否限制每个歌单爬取的歌曲数? (输入数字或直接回车不限制): ").strip()
                if limit_input.isdigit():
                    max_songs_per_playlist = int(limit_input)
                    print(f"将限制每个歌单爬取前 {max_songs_per_playlist} 首歌曲")
            
            elif choice == '3':
                # 爬取指定歌单
                playlist_id = input("\n请输入歌单ID: ").strip()
                if not playlist_id:
                    print("[错误] 歌单ID不能为空")
                    return
                
                playlist = self.db.get_playlist_by_id(playlist_id)
                if not playlist:
                    print(f"[错误] 找不到歌单ID: {playlist_id}")
                    return
                
                print(f"\n将爬取歌单: {playlist['playlist_name']}")
                print(f"  创建者: {playlist['creator_name']}")
                print(f"  歌曲数: {playlist['track_count']}")
                
                playlist_ids = [playlist_id]
            
            else:
                print("[错误] 无效的选择")
                return
            
            if not playlist_ids:
                print("[错误] 没有找到可爬取的歌单")
                return
            
            # 开始爬取
            print(f"\n开始爬取 {len(playlist_ids)} 个歌单的歌曲...")
            start_time = time.time()
            
            batch_songs = self.spider.crawl_playlist_songs_batch(playlist_ids, max_songs_per_playlist)
            
            # 保存到数据库
            print("\n保存歌曲到数据库...")
            total_saved = 0
            for playlist_id, songs_list in batch_songs.items():
                if songs_list:
                    count = self.db.insert_songs_batch(songs_list)
                    total_saved += count
            
            elapsed_time = time.time() - start_time
            print(f"\n[成功] 爬取完成!")
            print(f"  共爬取: {sum(len(songs) for songs in batch_songs.values())} 首歌曲")
            print(f"  已保存: {total_saved} 首歌曲")
            print(f"  耗时: {elapsed_time:.2f} 秒")
            
            # 显示歌曲统计
            song_stats = self.db.get_song_statistics()
            if song_stats:
                print(f"\n[统计] 数据库中现有:")
                print(f"  歌曲记录数: {song_stats.get('total_song_records', 0)}")
                print(f"  唯一歌曲数: {song_stats.get('unique_songs', 0)}")
                print(f"  歌手数: {song_stats.get('total_artists', 0)}")
                print(f"  专辑数: {song_stats.get('total_albums', 0)}")
            
        except KeyboardInterrupt:
            print("\n\n用户中断爬取")
        except Exception as e:
            logger.error(f"爬取歌曲失败: {e}")
            print(f"[失败] 爬取失败: {e}")
        finally:
            # 清理爬虫资源
            if self.spider:
                self.spider.close()
                self.spider = None
    
    def analyze_data(self):
        """热门歌单数据分析功能"""
        print("\n【热门歌单数据分析】")
        print("-"*60)
        
        try:
            stats = self.db.get_statistics()
            
            if not stats or stats.get('total_playlists', 0) == 0:
                print("\n[提示] 数据库中暂无歌单数据，请先爬取数据")
                return
            
            # 歌单基础统计
            print("\n【基础统计】")
            print(f"  总歌单数: {stats.get('total_playlists', 0)}")
            print(f"  总播放量: {stats.get('total_playlist_play_count', 0):,}")
            print(f"  总收藏数: {stats.get('total_playlist_subscribe_count', 0):,}")
            print(f"  平均播放量: {stats.get('avg_playlist_play_count', 0):.0f}")
            print(f"  平均收藏数: {stats.get('avg_subscribed_count', 0):.0f}")
            print(f"  最高播放量: {stats.get('max_playlist_play_count', 0):,}")
            
            # TOP歌单
            print("\n【TOP 10 热门歌单】")
            top_playlists = self.db.get_top_playlists(10, 'play_count')
            for i, playlist in enumerate(top_playlists, 1):
                print(f"  {i:2d}. {playlist['playlist_name'][:35]}")
                print(f"      创建者: {playlist['creator_name']} | 播放: {playlist['play_count']:,} | 收藏: {playlist['subscribed_count']:,}")
            
            # 按收藏数排序
            print("\n【TOP 10 收藏最多歌单】")
            top_subscribed = self.db.get_top_playlists(10, 'subscribed_count')
            for i, playlist in enumerate(top_subscribed, 1):
                print(f"  {i:2d}. {playlist['playlist_name'][:35]}")
                print(f"      创建者: {playlist['creator_name']} | 收藏: {playlist['subscribed_count']:,} | 播放: {playlist['play_count']:,}")
            
            print("\n[OK] 分析完成")
            
        except Exception as e:
            logger.error(f"数据分析失败: {e}")
            print(f"[X] 分析失败: {e}")
    
    def generate_modern_report(self):
        """生成可视化报告功能"""
        print("\n【生成可视化报告】")
        print("-"*60)
        
        try:
            stats = self.db.get_statistics()
            
            if not stats or stats.get('total_playlists', 0) == 0:
                print("\n[提示] 数据库中暂无歌单数据，请先爬取数据")
                return
            
            print(f"\n📊 当前数据库统计:")
            print(f"  • 歌单总数: {stats.get('total_playlists', 0):,}")
            print(f"  • 歌曲总数: {stats.get('total_song_records', 0):,}")
            print(f"  • 唯一歌曲: {stats.get('unique_songs', 0):,}")
            print(f"  • 歌手数量: {stats.get('total_artists', 0):,}")
            print(f"  • 专辑数量: {stats.get('total_albums', 0):,}")
            
            print("\n✨ 报告特点:")
            print("  • 现代化渐变色UI设计")
            print("  • 响应式布局，适配各种屏幕")
            print("  • 流畅的页面切换动画")
            print("  • 顶部横向导航菜单")
            print("  • 支持键盘左右箭头快速切换")
            print("  • 8个统计卡片展示关键指标")
            print("  • 所有图表支持交互、缩放、悬停提示")
            
            print("\n📈 包含的15个可视化图表:")
            print("\n  【歌单分析】(8个)")
            print("    1. 🏆 播放量排行 - TOP30热门歌单")
            print("    2. ⭐ 收藏数排行 - TOP30热门歌单")
            print("    3. 📊 对比分析 - 播放量vs收藏数")
            print("    4. 🏷️  标签分布 - 热门标签饼图")
            print("    5. 👥 创建者排行 - 贡献度分析")
            print("    6. 💫 关系分析 - 散点图")
            print("    7. 📦 规模分布 - 歌单大小分类")
            print("    8. ☁️  标签词云 - 可视化")
            
            print("\n  【歌曲分析】(7个)")
            print("    9.  🎵 热门歌曲 - TOP30排行榜")
            print("    10. 🎤 歌手排行 - TOP20歌手")
            print("    11. ⏱️  时长分布 - 歌曲时长饼图")
            print("    12. 🔥 跨歌单热歌 - 多歌单热门歌曲")
            print("    13. 💿 专辑热度 - 散点分析")
            print("    14. 📊 热度分布 - 区间统计")
            print("    15. 🌟 歌手雷达 - 多维度能力分析")
            
            print("\n⏱️  提示: 生成过程约需10-20秒...")
            
            confirm = input("\n是否开始生成? (y/n, 默认y): ").strip().lower()
            if confirm and confirm != 'y':
                print("已取消生成")
                return
            
            print("\n" + "-"*60)
            print("正在生成报告，请稍候...")
            print("-"*60)
            
            # 导入现代化可视化模块
            from visualization.modern_report_generator import ModernReportGenerator
            
            # 生成报告
            generator = ModernReportGenerator(self.db)
            report_path = generator.generate_report()
            
            if report_path and os.path.exists(report_path):
                file_size = os.path.getsize(report_path) / 1024
                print("\n" + "="*60)
                print("🎉 报告生成成功！")
                print("="*60)
                print(f"\n📄 文件信息:")
                print(f"  • 路径: {report_path}")
                print(f"  • 大小: {file_size:.1f} KB")
                print(f"\n💡 使用提示:")
                print(f"  1. 在浏览器中打开该HTML文件")
                print(f"  2. 使用顶部导航按钮切换不同图表")
                print(f"  3. 支持键盘左右箭头快速切换页面")
                print(f"  4. 鼠标悬停可查看详细数据")
                
                # 询问是否打开报告
                open_report = input("\n是否在浏览器中打开报告? (y/n, 默认y): ").strip().lower()
                if not open_report or open_report == 'y':
                    import webbrowser
                    webbrowser.open(f'file:///{os.path.abspath(report_path)}')
                    print("✓ 已在浏览器中打开报告")
            else:
                print("\n❌ 报告生成失败，请查看日志文件")
            
        except ImportError as e:
            logger.error(f"导入可视化模块失败: {e}")
            print(f"\n❌ 缺少依赖库")
            print(f"   请运行: pip install pyecharts pandas")
        except Exception as e:
            logger.error(f"生成现代化报告失败: {e}")
            print(f"\n❌ 生成报告失败: {e}")
            import traceback
            traceback.print_exc()
    
    def show_statistics(self):
        """显示数据库统计信息"""
        print("\n【数据库统计】")
        print("-"*60)
        
        try:
            stats = self.db.get_statistics()
            
            if not stats:
                print("数据库中暂无数据")
                return
            
            print("\n 数据统计:")
            
            # 歌单统计
            if stats.get('total_playlists', 0) > 0:
                print(f"\n【热门歌单】")
                print(f"  总歌单数: {stats.get('total_playlists', 0)}")
                print(f"  总播放量: {stats.get('total_playlist_play_count', 0):,}")
                print(f"  平均播放量: {stats.get('avg_playlist_play_count', 0):.0f}")
                print(f"  平均收藏数: {stats.get('avg_subscribed_count', 0):.0f}")
                print(f"  最高播放量: {stats.get('max_playlist_play_count', 0):,}")
            
            # 歌曲统计
            if stats.get('total_songs', 0) > 0:
                print(f"\n【歌曲数据】")
                print(f"  总歌曲数: {stats.get('total_songs', 0)}")
                print(f"  总评论数: {stats.get('total_comments', 0)}")
                print(f"  歌手数量: {stats.get('total_artists', 0)}")
                print(f"  总播放量: {stats.get('total_play_count', 0):,}")
                print(f"  平均播放量: {stats.get('avg_play_count', 0):.0f}")
                print(f"  最高播放量: {stats.get('max_play_count', 0):,}")
                print(f"  平均评论数: {stats.get('avg_comment_count', 0):.0f}")
                
                if stats.get('top_artist'):
                    print(f"\n  最热门歌手: {stats['top_artist']} ({stats.get('top_artist_song_count', 0)} 首歌)")
            
        except Exception as e:
            logger.error(f"获取统计失败: {e}")
            print(f"[X] 获取统计失败: {e}")
    
    def export_csv(self):
        """导出热门歌单数据为CSV"""
        print("\n【导出热门歌单数据为CSV】")
        print("-"*60)
        
        try:
            playlists = self.db.get_all_playlists()
            
            if not playlists:
                print("\n[提示] 数据库中暂无歌单数据，请先爬取数据")
                return
            
            # 导出CSV
            import csv
            from config.settings import OUTPUT_CONFIG
            
            csv_path = OUTPUT_CONFIG.get('csv_export_path', 'output/playlists_data.csv')
            csv_dir = os.path.dirname(csv_path)
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
            
            print(f"\n正在导出 {len(playlists)} 个歌单数据...")
            
            with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                fieldnames = ['rank', 'playlist_id', 'playlist_name', 'creator_name', 
                             'play_count', 'subscribed_count', 'track_count', 
                             'tags', 'create_time', 'description']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for playlist in playlists:
                    writer.writerow({
                        'rank': playlist.get('rank', ''),
                        'playlist_id': playlist.get('playlist_id', ''),
                        'playlist_name': playlist.get('playlist_name', ''),
                        'creator_name': playlist.get('creator_name', ''),
                        'play_count': playlist.get('play_count', 0),
                        'subscribed_count': playlist.get('subscribed_count', 0),
                        'track_count': playlist.get('track_count', 0),
                        'tags': playlist.get('tags', ''),
                        'create_time': playlist.get('create_time', ''),
                        'description': playlist.get('description', '')[:200]  # 限制描述长度
                    })
            
            print(f"[OK] 数据已导出到: {csv_path}")
            print(f"     共导出 {len(playlists)} 条记录")
            
        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            print(f"[X] 导出失败: {e}")
    
    def clear_database(self):
        """清空数据库"""
        print("\n【清空数据库】")
        print("-"*60)
        
        confirm = input("\n[!]  警告: 此操作将清空所有数据,是否继续? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            try:
                self.db.clear_all_data()
                print("[OK] 数据库已清空")
                
            except Exception as e:
                logger.error(f"清空数据库失败: {e}")
                print(f"[X] 清空失败: {e}")
        else:
            print("已取消操作")
    
    def run(self):
        """运行主程序"""
        print("\n" + "🎵"*30)
        print("    欢迎使用网易云音乐数据分析系统!")
        print("🎵"*30)
        logger.info("程序启动")
        
        while True:
            try:
                self.show_menu()
                choice = input("\n请选择功能 (0-8): ").strip()
                
                if choice == '1':
                    self.crawl_hot_playlists()
                elif choice == '2':
                    self.crawl_playlist_songs()
                elif choice == '3':
                    self.analyze_data()
                elif choice == '4':
                    self.generate_modern_report()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '6':
                    self.export_csv()
                elif choice == '7':
                    self.clear_database()
                elif choice == '0':
                    print("\n" + "="*60)
                    print("  感谢使用，再见！")
                    print("="*60)
                    logger.info("程序正常退出")
                    break
                else:
                    print("\n[X] 无效的选择，请重新输入")
                
                # 暂停以便查看结果
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n检测到中断信号，退出程序")
                logger.info("程序被用户中断")
                break
            except Exception as e:
                logger.error(f"程序运行错误: {e}")
                print(f"\n[X] 发生错误: {e}")
                input("\n按回车键继续...")
        
        # 清理资源
        self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.spider:
                self.spider.close()
            if self.db:
                self.db.close()
            logger.info("资源清理完成")
        except Exception as e:
            logger.error(f"清理资源失败: {e}")


def main():
    """主函数"""
    try:
        app = MusicAnalysisApp()
        app.run()
    except Exception as e:
        logger.critical(f"程序启动失败: {e}")
        print(f"[X] 程序启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

