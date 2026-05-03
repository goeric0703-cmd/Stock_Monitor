import akshare as ak
import pandas as pd
from datetime import datetime

# 1. 设置你的股票池
my_stocks = ["600519", "000001", "300750"]

def generate_html():
    # 获取实时行情
    df_all = ak.stock_zh_a_spot_em()
    df_selected = df_all[df_all['代码'].isin(my_stocks)].copy()
    
    # 获取行业新闻 (财联社电报)
    news_df = ak.stock_telegraph_cls()
    news_html = "".join([f"<li><b>[{row['time']}]</b> {row['content']}</li>" for _, row in news_df.head(10).iterrows()])

    # 构建极简 HTML 模板
    html_content = f"""
    <html>
    <head><meta charset="utf-8"><title>A股实时监控</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>📈 核心股票监控 (更新: {datetime.now().strftime('%Y-%m-%d %H:%M')})</h1>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background: #f2f2f2;">
                <th>代码</th><th>名称</th><th>最新价</th><th>涨跌幅</th><th>涨停参考</th><th>跌停参考</th>
            </tr>
    """
    
    for _, row in df_selected.iterrows():
        limit_up = round(row['昨收'] * 1.1, 2)
        limit_down = round(row['昨收'] * 0.9, 2)
        html_content += f"""
            <tr>
                <td>{row['代码']}</td><td>{row['名称']}</td>
                <td>{row['最新价']}</td><td>{row['涨跌幅']}%</td>
                <td style="color:red;">{limit_up}</td><td style="color:green;">{limit_down}</td>
            </tr>
        """
    
    html_content += f"""
        </table>
        <h2>📰 行业全球新闻 (9:00 播报)</h2>
        <ul>{news_html}</ul>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html()
