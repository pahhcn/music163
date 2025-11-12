"""现代化HTML报告构建器"""
from datetime import datetime
from typing import List, Dict, Any


class ModernHTMLBuilder:
    """现代化HTML报告构建器"""
    
    @staticmethod
    def get_css_styles() -> str:
        """获取现代化CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --success-color: #10b981;
            --card-shadow: 0 4px 20px rgba(0,0,0,0.08);
            --card-shadow-hover: 0 8px 30px rgba(0,0,0,0.12);
            --border-radius: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 24px;
            line-height: 1.6;
        }
        
        .main-container {
            max-width: 1800px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 24px 80px rgba(0,0,0,0.25);
            overflow: hidden;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* 现代化头部 */
        .modern-header {
            background: var(--primary-gradient);
            color: white;
            padding: 48px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .modern-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 15s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.1) rotate(180deg); }
        }
        
        .modern-header h1 {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
            letter-spacing: -0.5px;
        }
        
        .modern-header p {
            font-size: 16px;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        /* 统计卡片网格 */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 24px;
            padding: 40px;
            background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
        }
        
        .stat-card {
            background: white;
            padding: 28px;
            border-radius: var(--border-radius);
            text-align: center;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            border: 1px solid #f0f0f0;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--primary-gradient);
            transform: scaleX(0);
            transition: transform 0.3s;
        }
        
        .stat-card:hover::before {
            transform: scaleX(1);
        }
        
        .stat-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--card-shadow-hover);
        }
        
        .stat-card .icon {
            font-size: 36px;
            margin-bottom: 12px;
            display: inline-block;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .stat-card .value {
            font-size: 36px;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 12px 0;
        }
        
        .stat-card .label {
            font-size: 14px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* 现代化导航栏 */
        .sidebar-nav {
            position: sticky;
            top: 0;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            z-index: 1000;
            border-bottom: 1px solid #e5e7eb;
            box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        }
        
        .nav-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
            padding: 20px 40px;
            max-width: 1800px;
            margin: 0 auto;
        }
        
        .nav-item {
            padding: 14px 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: #495057;
            border: 2px solid transparent;
            border-radius: 16px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: var(--transition);
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .nav-item:hover {
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            border-color: #667eea;
        }
        
        .nav-item.active {
            background: var(--primary-gradient);
            color: white;
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 6px 24px rgba(102, 126, 234, 0.5);
            border-color: #764ba2;
        }
        
        /* 内容区域 - 充分利用空间 */
        .content-area {
            padding: 40px;
            max-width: 1800px;
            margin: 0 auto;
            width: 100%;
        }
        
        .page-section {
            display: none;
            animation: fadeInUp 0.5s ease-out;
            width: 100%;
        }
        
        .page-section.active {
            display: block;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chart-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 40px;
            margin-bottom: 32px;
            box-shadow: var(--card-shadow);
            transition: var(--transition);
            border: 1px solid #f0f0f0;
            width: 100%;
        }
        
        .chart-card:hover {
            box-shadow: var(--card-shadow-hover);
        }
        
        .chart-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #f3f4f6;
        }
        
        .chart-header .icon {
            font-size: 32px;
        }
        
        .chart-header h3 {
            font-size: 24px;
            font-weight: 700;
            color: #111827;
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
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .modern-footer p {
            margin: 8px 0;
            opacity: 0.9;
        }
        
        /* 返回顶部按钮 */
        .back-top-btn {
            position: fixed;
            bottom: 32px;
            right: 32px;
            width: 56px;
            height: 56px;
            background: var(--primary-gradient);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
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
            transform: translateY(-8px) scale(1.1);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
        }
        
        /* 主题切换按钮 */
        .theme-toggle {
            position: fixed;
            top: 32px;
            right: 32px;
            width: 56px;
            height: 56px;
            background: white;
            border: 2px solid #667eea;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: var(--transition);
            z-index: 1002;
        }
        
        .theme-toggle:hover {
            transform: rotate(180deg) scale(1.1);
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
            padding: 24px;
            line-height: 1.8;
        }
        
        .overview-content h3 {
            color: #667eea;
            margin: 32px 0 16px;
            font-size: 20px;
            font-weight: 700;
        }
        
        .overview-content h3:first-child {
            margin-top: 0;
        }
        
        .overview-content p {
            margin: 12px 0;
            color: #4b5563;
        }
        
        .overview-content strong {
            color: #111827;
            font-weight: 600;
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
                <h3>📊 报告说明</h3>
                <p>• 本报告基于网易云音乐热门歌单数据生成</p>
                <p>• 共采集 <strong>{stats.get('total_playlists', 0):,}</strong> 个歌单，<strong>{stats.get('total_song_records', 0):,}</strong> 首歌曲</p>
                <p>• 包含 <strong>{stats.get('unique_songs', 0):,}</strong> 首唯一歌曲，<strong>{stats.get('total_artists', 0):,}</strong> 位歌手</p>
                <p>• 数据维度包括：播放量、收藏数、标签、创建者、歌曲热度等</p>
                
                <h3>📈 图表导航</h3>
                <p><strong>歌单分析：</strong>包含播放排行、收藏排行、标签分布、创建者贡献等维度</p>
                <p><strong>歌曲分析：</strong>包含热门歌曲、歌手排行、时长分布、热度分析等维度</p>
                
                <h3>💡 使用提示</h3>
                <p>• 使用顶部导航按钮切换不同图表</p>
                <p>• 所有图表支持鼠标悬停查看详细数据</p>
                <p>• 支持键盘左右箭头键快速切换页面</p>
                <p>• 建议使用Chrome、Edge等现代浏览器浏览</p>
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
