"""现代化HTML报告构建器"""
from datetime import datetime
from typing import List, Dict, Any


class ModernHTMLBuilder:
    """现代化HTML报告构建器"""
    
    @staticmethod
    def get_css_styles() -> str:
        """获取网易云风格CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --netease-red: #EC4141;
            --netease-dark: #2C2C2C;
            --netease-gray: #F5F5F7;
            --netease-text: #333333;
            --netease-text-light: #666666;
            --card-shadow: 0 2px 8px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
        }
        
        body {
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
            background: #F5F5F7;
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            background: #ffffff;
            min-height: 100vh;
        }
        
        /* 网易云风格头部 */
        .modern-header {
            background: var(--netease-red);
            color: white;
            padding: 40px 40px 30px;
            position: relative;
        }
        
        .modern-header h1 {
            font-size: 28px;
            font-weight: 500;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .modern-header p {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 300;
        }
        
        /* 统计卡片网格 */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            padding: 30px 40px;
            background: #FAFAFA;
        }
        
        .stat-card {
            background: white;
            padding: 24px 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            border: 1px solid #EEEEEE;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-color: var(--netease-red);
        }
        
        .stat-card .icon {
            font-size: 32px;
            margin-bottom: 10px;
            display: inline-block;
        }
        
        .stat-card .value {
            font-size: 32px;
            font-weight: 600;
            color: var(--netease-red);
            margin: 8px 0;
        }
        
        .stat-card .label {
            font-size: 13px;
            color: var(--netease-text-light);
            font-weight: 400;
        }
        
        /* 网易云风格导航栏 */
        .sidebar-nav {
            position: sticky;
            top: 0;
            background: white;
            z-index: 1000;
            border-bottom: 1px solid #E5E5E5;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .nav-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 16px 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .nav-item {
            padding: 8px 16px;
            background: white;
            color: var(--netease-text);
            border: 1px solid #E5E5E5;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 400;
            transition: var(--transition);
            white-space: nowrap;
        }
        
        .nav-item:hover {
            background: #FFF5F5;
            border-color: var(--netease-red);
            color: var(--netease-red);
        }
        
        .nav-item.active {
            background: var(--netease-red);
            color: white;
            border-color: var(--netease-red);
        }
        
        /* 内容区域 */
        .content-area {
            padding: 30px 40px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
            background: #FAFAFA;
            min-height: calc(100vh - 300px);
        }
        
        .page-section {
            display: none;
            width: 100%;
        }
        
        .page-section.active {
            display: block;
        }
        
        .chart-card {
            background: white;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            border: 1px solid #EEEEEE;
            width: 100%;
        }
        
        .chart-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .chart-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #F5F5F5;
        }
        
        .chart-header .icon {
            font-size: 20px;
        }
        
        .chart-header h3 {
            font-size: 16px;
            font-weight: 500;
            color: var(--netease-text);
            flex-grow: 1;
        }
        
        /* 图表容器 - 确保图表充分展开 */
        .chart-card > div {
            width: 100% !important;
            min-height: 650px !important;
        }
        
        .chart-card > div > div {
            width: 100% !important;
            height: 650px !important;
        }
        
        /* ECharts容器优化 */
        div[_echarts_instance_] {
            width: 100% !important;
            height: 650px !important;
        }
        
        /* 强制图表容器展开 */
        [id^="chart"] {
            width: 100% !important;
            height: 650px !important;
        }
        
        /* Canvas元素优化 */
        .chart-card canvas {
            width: 100% !important;
            height: auto !important;
        }
        
        /* 页脚 */
        .modern-footer {
            background: var(--netease-dark);
            color: #999999;
            padding: 30px 40px;
            text-align: center;
            font-size: 13px;
        }
        
        .modern-footer p {
            margin: 6px 0;
        }
        
        /* 返回顶部按钮 */
        .back-top-btn {
            position: fixed;
            bottom: 40px;
            right: 40px;
            width: 48px;
            height: 48px;
            background: var(--netease-red);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            box-shadow: 0 4px 12px rgba(236, 65, 65, 0.3);
            transition: var(--transition);
            opacity: 0;
            visibility: hidden;
            z-index: 1001;
        }
        
        .back-top-btn.show {
            opacity: 1;
            visibility: visible;
        }
        
        .back-top-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(236, 65, 65, 0.4);
        }
        
        /* 响应式设计 */
        @media (max-width: 1200px) {
            .nav-container {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 8px;
                padding: 16px 24px;
            }
            
            .nav-item {
                font-size: 12px;
                padding: 12px 16px;
            }
        }
        
        @media (max-width: 768px) {
            body {
                padding: 12px;
            }
            
            .main-container {
                border-radius: 16px;
            }
            
            .modern-header {
                padding: 32px 24px;
            }
            
            .modern-header h1 {
                font-size: 28px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 16px;
                padding: 24px;
            }
            
            .stat-card {
                padding: 20px;
            }
            
            .stat-card .value {
                font-size: 28px;
            }
            
            .content-area {
                padding: 20px;
            }
            
            .chart-card {
                padding: 24px;
            }
            
            .nav-container {
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 6px;
                padding: 12px 16px;
            }
            
            .nav-item {
                padding: 10px 12px;
                font-size: 11px;
            }
        }
        
        /* 加载动画 */
        .loading-spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f4f6;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* 概览页面样式 */
        .overview-content {
            padding: 20px;
            line-height: 1.8;
        }
        
        .overview-content h3 {
            color: var(--netease-red);
            margin: 24px 0 12px;
            font-size: 16px;
            font-weight: 500;
        }
        
        .overview-content h3:first-child {
            margin-top: 0;
        }
        
        .overview-content p {
            margin: 10px 0;
            color: var(--netease-text-light);
            font-size: 14px;
        }
        
        .overview-content strong {
            color: var(--netease-text);
            font-weight: 500;
        }
        """
    
    @staticmethod
    def get_javascript() -> str:
        """获取JavaScript交互代码"""
        return """
        // 页面导航
        function navigateTo(pageIndex) {
            // 隐藏所有页面
            document.querySelectorAll('.page-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // 显示目标页面
            const targetPage = document.getElementById('page-' + pageIndex);
            if (targetPage) {
                targetPage.classList.add('active');
            }
            
            // 更新导航按钮状态
            document.querySelectorAll('.nav-item').forEach((btn, index) => {
                if (index === pageIndex) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
            
            // 不自动滚动到顶部，保持当前滚动位置
            // window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // 调整当前页面的图表大小
            resizeCurrentPageCharts();
        }
        
        // 返回顶部
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // 监听滚动事件
        window.addEventListener('scroll', () => {
            const backBtn = document.querySelector('.back-top-btn');
            if (window.pageYOffset > 300) {
                backBtn.classList.add('show');
            } else {
                backBtn.classList.remove('show');
            }
        });
        
        // 键盘导航支持
        document.addEventListener('keydown', (e) => {
            const pages = document.querySelectorAll('.page-section');
            const currentIndex = Array.from(pages).findIndex(page => 
                page.classList.contains('active')
            );
            
            if (e.key === 'ArrowRight' && currentIndex < pages.length - 1) {
                navigateTo(currentIndex + 1);
            } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                navigateTo(currentIndex - 1);
            }
        });
        
        // 页面加载完成后的初始化
        document.addEventListener('DOMContentLoaded', () => {
            console.log('📊 网易云音乐数据分析报告已加载');
            
            // 添加图表加载动画
            const charts = document.querySelectorAll('.chart-card');
            charts.forEach((chart, index) => {
                setTimeout(() => {
                    chart.style.animation = 'fadeInUp 0.5s ease-out';
                }, index * 100);
            });
            
            // 强制调整所有ECharts图表大小
            setTimeout(() => {
                if (window.echarts) {
                    const echartsInstances = document.querySelectorAll('[_echarts_instance_]');
                    echartsInstances.forEach(dom => {
                        const instance = echarts.getInstanceByDom(dom);
                        if (instance) {
                            instance.resize();
                        }
                    });
                }
            }, 500);
        });
        
        // 监听窗口大小变化，自动调整图表
        window.addEventListener('resize', () => {
            if (window.echarts) {
                const echartsInstances = document.querySelectorAll('[_echarts_instance_]');
                echartsInstances.forEach(dom => {
                    const instance = echarts.getInstanceByDom(dom);
                    if (instance) {
                        instance.resize();
                    }
                });
            }
        });
        
        // 页面切换时也调整图表大小
        function resizeCurrentPageCharts() {
            setTimeout(() => {
                const activePage = document.querySelector('.page-section.active');
                if (activePage && window.echarts) {
                    const charts = activePage.querySelectorAll('[_echarts_instance_]');
                    charts.forEach(dom => {
                        const instance = echarts.getInstanceByDom(dom);
                        if (instance) {
                            instance.resize();
                        }
                    });
                }
            }, 100);
        }
        """
    
    @staticmethod
    def build_html(stats: Dict[str, Any], charts_html: List[str], nav_items: List[str]) -> str:
        """
        构建完整的HTML报告
        :param stats: 统计数据
        :param charts_html: 图表HTML列表
        :param nav_items: 导航项列表
        :return: 完整HTML字符串
        """
        # 构建统计卡片 - 修复数据显示问题
        total_play = stats.get('total_playlist_play_count', 0)
        total_sub = stats.get('total_playlist_subscribe_count', 0)
        
        stats_cards = [
            ('📊', stats.get('total_playlists', 0), '总歌单数'),
            ('🎵', stats.get('total_song_records', 0), '总歌曲数'),
            ('🎤', stats.get('total_artists', 0), '歌手数量'),
            ('💿', stats.get('total_albums', 0), '专辑数量'),
            ('🔥', round(stats.get('avg_popularity', 0), 1), '平均热度'),
            ('⭐', stats.get('unique_songs', 0), '唯一歌曲'),
            ('👥', f"{total_play / 100000000:.1f}亿" if total_play > 0 else '0', '总播放量'),
            ('💖', f"{total_sub / 10000000:.1f}千万" if total_sub > 0 else '0', '总收藏数'),
        ]
        
        stats_html = '\n'.join([
            f'''
            <div class="stat-card">
                <div class="icon">{icon}</div>
                <div class="value">{value if not isinstance(value, (int, float)) else f"{value:,}"}</div>
                <div class="label">{label}</div>
            </div>
            '''
            for icon, value, label in stats_cards
        ])
        
        # 构建导航按钮 - 简化文字
        nav_items_short = []
        for item in nav_items:
            # 移除emoji后的文字，只保留emoji和关键词
            if '概览' in item:
                nav_items_short.append('📋 概览')
            elif '播放量' in item:
                nav_items_short.append('🏆 播放榜')
            elif '收藏数' in item:
                nav_items_short.append('⭐ 收藏榜')
            elif '对比' in item:
                nav_items_short.append('📊 对比')
            elif '标签分布' in item:
                nav_items_short.append('🏷️ 标签')
            elif '创建者' in item:
                nav_items_short.append('👥 创建者')
            elif '关系' in item:
                nav_items_short.append('💫 关系')
            elif '规模' in item:
                nav_items_short.append('📦 规模')
            elif '词云' in item:
                nav_items_short.append('☁️ 词云')
            elif '热门歌曲' in item:
                nav_items_short.append('🎵 热歌')
            elif '歌手排行' in item:
                nav_items_short.append('🎤 歌手')
            elif '时长' in item:
                nav_items_short.append('⏱️ 时长')
            elif '跨歌单' in item:
                nav_items_short.append('🔥 热门')
            elif '专辑' in item:
                nav_items_short.append('💿 专辑')
            elif '热度分布' in item:
                nav_items_short.append('📈 热度')
            elif '雷达' in item:
                nav_items_short.append('🌟 雷达')
            else:
                nav_items_short.append(item)
        
        nav_html = '\n'.join([
            f'<button class="nav-item{" active" if i == 0 else ""}" onclick="navigateTo({i})" title="{nav_items[i]}">{nav_items_short[i]}</button>'
            for i in range(len(nav_items))
        ])
        
        # 构建概览页面
        overview_html = f'''
        <div class="chart-card">
            <div class="chart-header">
                <span class="icon">📋</span>
                <h3>数据概览</h3>
            </div>
            <div class="overview-content">
                <h3>数据来源</h3>
                <p>本报告数据来自网易云音乐热门歌单，通过Python爬虫采集并分析。</p>
                <p>采集时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
                
                <h3>数据规模</h3>
                <p>• 歌单总数：<strong>{stats.get('total_playlists', 0):,}</strong> 个</p>
                <p>• 歌曲记录：<strong>{stats.get('total_song_records', 0):,}</strong> 条</p>
                <p>• 唯一歌曲：<strong>{stats.get('unique_songs', 0):,}</strong> 首</p>
                <p>• 歌手数量：<strong>{stats.get('total_artists', 0):,}</strong> 位</p>
                <p>• 专辑数量：<strong>{stats.get('total_albums', 0):,}</strong> 张</p>
                
                <h3>播放统计</h3>
                <p>• 总播放量：<strong>{stats.get('total_playlist_play_count', 0) / 100000000:.1f}</strong> 亿次</p>
                <p>• 总收藏数：<strong>{stats.get('total_playlist_subscribe_count', 0) / 10000000:.1f}</strong> 千万</p>
                <p>• 平均播放量：<strong>{stats.get('avg_playlist_play_count', 0):,.0f}</strong> 次/歌单</p>
                <p>• 平均收藏数：<strong>{stats.get('avg_subscribed_count', 0):,.0f}</strong> 人/歌单</p>
                <p>• 最高播放量：<strong>{stats.get('max_playlist_play_count', 0):,}</strong> 次</p>
                
                <h3>图表说明</h3>
                <p><strong>歌单分析（8个）</strong></p>
                <p>播放排行、收藏排行、对比分析、标签分布、创建者排行、关系分析、规模分布、标签词云</p>
                <p><strong>歌曲分析（7个）</strong></p>
                <p>热门歌曲、歌手排行、时长分布、跨歌单热歌、专辑热度、热度分布、歌手雷达</p>
                
                <h3>数据特点</h3>
                <p>本报告采用"跨歌单出现次数"作为歌曲热度的补充指标。</p>
                <p>统计方法：计算每首歌在多少个不同歌单中出现，出现次数越多说明该歌曲越受欢迎。</p>
                <p>这个指标能够反映歌曲在用户歌单中的流行程度，是衡量歌曲受欢迎度的有效方式。</p>
                
                <h3>使用说明</h3>
                <p>• 点击顶部导航按钮切换图表</p>
                <p>• 支持键盘左右箭头键切换</p>
                <p>• 图表支持缩放和数据查看</p>
            </div>
        </div>
        '''
        
        # 构建图表页面
        charts_pages_html = '\n'.join([
            f'''
            <div class="page-section" id="page-{i+1}">
                <div class="chart-card">
                    {chart_html}
                </div>
            </div>
            '''
            for i, chart_html in enumerate(charts_html)
        ])
        
        # 完整HTML
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="网易云音乐热门歌单数据分析可视化报告">
    <title>🎵 网易云音乐数据分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts-wordcloud@2/dist/echarts-wordcloud.min.js"></script>
    <style>{ModernHTMLBuilder.get_css_styles()}</style>
</head>
<body>
    <div class="main-container">
        <!-- 头部 -->
        <div class="modern-header">
            <h1>🎵 网易云音乐数据分析报告</h1>
            <p>NetEase Cloud Music Data Analysis Report</p>
            <p style="margin-top: 12px; font-size: 14px;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid">
            {stats_html}
        </div>
        
        <!-- 导航栏 -->
        <div class="sidebar-nav">
            <div class="nav-container">
                {nav_html}
            </div>
        </div>
        
        <!-- 内容区域 -->
        <div class="content-area">
            <!-- 概览页 -->
            <div class="page-section active" id="page-0">
                {overview_html}
            </div>
            
            <!-- 图表页 -->
            {charts_pages_html}
        </div>
        
        <!-- 页脚 -->
        <div class="modern-footer">
            <p>📊 网易云音乐热门歌单数据分析报告</p>
            <p>数据来源: 网易云音乐 | 分析工具: Python + Pyecharts</p>
            <p>© 2025 Music Data Analysis Project</p>
        </div>
    </div>
    
    <!-- 返回顶部按钮 -->
    <button class="back-top-btn" onclick="scrollToTop()">↑</button>
    
    <script>{ModernHTMLBuilder.get_javascript()}</script>
</body>
</html>'''
        
        return html
