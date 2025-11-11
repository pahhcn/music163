"""图表构建器基类"""
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, Scatter
from pyecharts.globals import ThemeType
from typing import Optional
from utils.logger import get_logger

logger = get_logger()


class BaseChartBuilder:
    """图表构建器基类"""
    
    def __init__(self, db_manager, theme=ThemeType.MACARONS):
        """
        初始化图表构建器
        :param db_manager: 数据库管理器
        :param theme: 图表主题
        """
        self.db = db_manager
        self.theme = theme
        self.colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', 
                      '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
    
    def _create_empty_chart(self, title: str, message: str, chart_type='bar') -> Optional[Bar]:
        """
        创建空数据提示图表
        :param title: 标题
        :param message: 提示信息
        :param chart_type: 图表类型
        :return: 图表对象
        """
        try:
            if chart_type == 'bar':
                chart = (
                    Bar(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                    .add_xaxis(["暂无数据"])
                    .add_yaxis("", [0], label_opts=opts.LabelOpts(is_show=False))
                    .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title=title,
                            subtitle=message,
                            title_textstyle_opts=opts.TextStyleOpts(font_size=20),
                            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=14, color="#888")
                        ),
                        tooltip_opts=opts.TooltipOpts(is_show=False)
                    )
                )
            else:  # pie
                chart = (
                    Pie(init_opts=opts.InitOpts(theme=self.theme, width="100%", height="650px"))
                    .add("", [("暂无数据", 1)], radius=["40%", "70%"])
                    .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title=title,
                            subtitle=message,
                            title_textstyle_opts=opts.TextStyleOpts(font_size=20)
                        ),
                        legend_opts=opts.LegendOpts(is_show=False),
                        tooltip_opts=opts.TooltipOpts(is_show=False)
                    )
                )
            return chart
        except Exception as e:
            logger.error(f"创建空图表失败: {e}")
            return None
    
    def _format_large_number(self, num: int) -> str:
        """
        格式化大数字
        :param num: 数字
        :return: 格式化后的字符串
        """
        if num >= 100000000:
            return f"{num/100000000:.1f}亿"
        elif num >= 10000:
            return f"{num/10000:.1f}万"
        else:
            return str(num)
