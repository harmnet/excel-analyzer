import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# 创建示例数据
def create_sample_data():
    # 销售数据
    sales_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
        'Sales': [10000 + i * 500 for i in range(30)]
    })

    # 品类销售数据
    category_sales = pd.DataFrame({
        'Category': ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys'],
        'Sales': [500000, 300000, 200000, 100000, 100000]
    })

    return sales_data, category_sales

# 创建Dash应用
app = dash.Dash(__name__)

# 获取示例数据
sales_data, category_sales = create_sample_data()

# 布局
app.layout = html.Div(
    children=[
        html.H1("交互式数据可视化报告 - 视觉呼吸感设计", style={'textAlign': 'center', 'marginBottom': '40px'}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3("每日销售额趋势", style={'marginBottom': '20px'}),
                        dcc.Graph(
                            figure=px.line(sales_data, x='Date', y='Sales', title="").update_layout(
                                plot_bgcolor='#F8F9FA', paper_bgcolor='#F8F9FA', margin=dict(t=0)
                            )
                        )
                    ],
                    style={
                        'backgroundColor': '#F8F9FA',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '60px'  # 模块间距 ≥ 模块高度的30%
                    }
                ),
                html.Div(
                    children=[
                        html.H3("各品类销售额", style={'marginBottom': '20px'}),
                        dcc.Graph(
                            figure=px.bar(category_sales, x='Category', y='Sales', title="").update_layout(
                                plot_bgcolor='#F8F9FA', paper_bgcolor='#F8F9FA', margin=dict(t=0)
                            )
                        )
                    ],
                    style{
                        'backgroundColor': '#F8F9FA',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'marginBottom': '60px'  # 模块间距 ≥ 模块高度的30%
                    }
                )
            ],
            style={'maxWidth': '1200px', 'margin': '0 auto'}
        )
    ],
    style={'backgroundColor': 'white', 'padding': '40px'}
)

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
