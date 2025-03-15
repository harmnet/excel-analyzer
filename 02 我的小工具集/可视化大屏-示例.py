import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc

# 统一颜色主题
COLOR_SCHEME = {
    'background': '#1a1a1a',
    'card': '#2d2d2d',
    'text': '#ffffff',
    'primary': '#00ffcc',
    'secondary': '#4ECDC4',
    'warning': '#ff6b6b',
    'accent': '#2D7575'
}

# 创建示例数据
def create_sample_data():
    # 核心指标数据
    core_metrics = {
        'Total Sales': 1200000,
        'Total Orders': 15000,
        'Conversion Rate': 0.15
    }

    # 主分析区 - 趋势分析数据
    trend_data = pd.DataFrame({
        'Hour': [f"{i}:00" for i in range(24)],
        'Channel A': np.random.randint(1000, 5000, 24),
        'Channel B': np.random.randint(1000, 5000, 24),
        'Channel C': np.random.randint(1000, 5000, 24)
    })

    # 主分析区 - 地理分布数据
    geo_data = pd.DataFrame({
        '省份': ['广东', '江苏', '浙江', '山东', '河南', '四川', '湖北', '湖南', '河北', '福建'],
        '销售额': np.random.randint(100000, 500000, 10)
    })

    # 主分析区 - 排行榜数据
    rank_data = pd.DataFrame({
        'Product': [f"Product {i}" for i in range(1, 11)],
        'Sales': np.random.randint(10000, 100000, 10)
    })

    # 辅助分析区 - 构成分析数据
    sunburst_data = pd.DataFrame({
        'Category': ['Electronics', 'Clothing', 'Home & Kitchen'],
        'SubCategory': ['Phones', 'Shirts', 'Furniture'],
        'Sales': [500000, 300000, 200000]
    })

    # 辅助分析区 - 关联分析数据
    scatter_data = pd.DataFrame({
        'Price': np.random.randint(10, 100, 50),
        'Sales': np.random.randint(100, 1000, 50),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Home & Kitchen'], 50)
    })

    # 预警监控区数据
    alerts = pd.DataFrame({
        'Time': [datetime.now().strftime('%H:%M:%S') for _ in range(3)],
        'Alert': ['Low Inventory', 'High Refund Rate', 'Payment Failure'],
        'Severity': ['High', 'Medium', 'Low']
    })

    return core_metrics, trend_data, geo_data, rank_data, sunburst_data, scatter_data, alerts

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 获取示例数据
core_metrics, trend_data, geo_data, rank_data, sunburst_data, scatter_data, alerts = create_sample_data()

# 主标题区
title_area = html.Div(
    children=[
        html.Img(src="https://via.placeholder.com/100x50", style={'height': '50px'}),
        html.H1("电子商务数据可视化大屏", style={
            'fontSize': '48pt',
            'fontFamily': 'sans-serif',
            'margin': '0 auto',
            'color': COLOR_SCHEME['primary'],
            'textShadow': '0 0 10px rgba(0,255,204,0.5)'
        }),
        html.Div(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), style={
            'fontSize': '24pt',
            'fontFamily': 'sans-serif',
            'color': COLOR_SCHEME['text']
        })
    ],
    style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'height': '108px',
        'backgroundColor': COLOR_SCHEME['background'],
        'padding': '0 20px',
        'borderBottom': f'2px solid {COLOR_SCHEME["accent"]}'
    }
)

# 核心指标区
core_metrics_area = html.Div(
    children=[
        html.Div(
            children=[
                html.H3("总销售额", style={'color': COLOR_SCHEME['text']}),
                html.P(f"${core_metrics['Total Sales']:,}", style={
                    'fontSize': '24px',
                    'color': COLOR_SCHEME['primary'],
                    'textShadow': '0 0 5px rgba(0,255,204,0.3)'
                })
            ],
            style={
                'width': '600px',
                'height': '100px',
                'backgroundColor': COLOR_SCHEME['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
            }
        ),
        html.Div(
            children=[
                html.H3("总订单数", style={'color': COLOR_SCHEME['text']}),
                html.P(f"{core_metrics['Total Orders']:,}", style={
                    'fontSize': '24px',
                    'color': COLOR_SCHEME['primary'],
                    'textShadow': '0 0 5px rgba(0,255,204,0.3)'
                })
            ],
            style={
                'width': '600px',
                'height': '100px',
                'backgroundColor': COLOR_SCHEME['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
            }
        ),
        html.Div(
            children=[
                html.H3("转化率", style={'color': COLOR_SCHEME['text']}),
                html.P(f"{core_metrics['Conversion Rate'] * 100:.1f}%", style={
                    'fontSize': '24px',
                    'color': COLOR_SCHEME['primary'],
                    'textShadow': '0 0 5px rgba(0,255,204,0.3)'
                })
            ],
            style={
                'width': '600px',
                'height': '100px',
                'backgroundColor': COLOR_SCHEME['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'textAlign': 'center',
                'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
            }
        )
    ],
    style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '38px',
        'margin': '20px 0'
    }
)

# 主分析区 - 趋势分析
trend_fig = go.Figure()

# 定义更贴合实际的渠道名称
channels = {
    'Channel A': '移动端',
    'Channel B': 'PC端',
    'Channel C': '小程序'
}

# 添加平滑曲线
for channel, name in channels.items():
    trend_fig.add_trace(go.Scatter(
        x=trend_data['Hour'],
        y=trend_data[channel],
        mode='lines',
        name=name,
        line=dict(
            shape='spline',  # 使曲线平滑
            width=3,
            smoothing=1.3
        ),
        hoverinfo='x+y+name',
        hovertemplate='<b>%{x}</b><br>销售额: %{y:,}元<extra></extra>'
    ))

# 添加平均值线
trend_fig.add_hline(
    y=trend_data[['Channel A', 'Channel B', 'Channel C']].values.mean(),
    line=dict(
        dash='dot',
        width=2,
        color='rgba(255, 99, 71, 0.8)'
    ),
    annotation_text="平均值",
    annotation_position="top right",
    annotation=dict(
        font=dict(
            size=14,
            color='rgba(255, 99, 71, 1)'
        ),
        bgcolor='rgba(0, 0, 0, 0.5)'
    )
)

# 更新布局
trend_fig.update_layout(
    title={
        'text': "过去24小时各渠道销售额趋势",
        'font': {
            'size': 24,
            'color': COLOR_SCHEME['primary'],
            'family': 'sans-serif'
        },
        'x': 0.05
    },
    xaxis_title="时间",
    yaxis_title="销售额（元）",
    paper_bgcolor=COLOR_SCHEME['card'],
    plot_bgcolor=COLOR_SCHEME['card'],
    font={'color': COLOR_SCHEME['text']},
    xaxis={
        'gridcolor': COLOR_SCHEME['accent'],
        'showgrid': True,
        'tickangle': -45
    },
    yaxis={
        'gridcolor': COLOR_SCHEME['accent'],
        'showgrid': True,
        'tickformat': ',.0f'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'right',
        'x': 1,
        'font': {
            'size': 14,
            'color': COLOR_SCHEME['text']
        }
    },
    hovermode='x unified',
    margin=dict(l=50, r=50, t=80, b=50)
)

# 主分析区 - 地理分布
geo_fig = px.choropleth(
    geo_data, 
    locations='省份', 
    locationmode='geojson-id', 
    color='销售额',
    color_continuous_scale=["#2D7575", "#4ECDC4"],
    title="中国各省销售额分布"
).update_layout(
    paper_bgcolor=COLOR_SCHEME['card'],
    plot_bgcolor=COLOR_SCHEME['card'],
    font={'color': COLOR_SCHEME['text']},
    title={'font': {'color': COLOR_SCHEME['primary']}},
    margin=dict(l=0, r=0, t=50, b=0),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        showframe=False,
        showcoastlines=True,
        projection_type='mercator'
    )
)

# 主分析区 - 排行榜
rank_fig = go.Figure()
# 添加排序逻辑
sorted_rank_data = rank_data.sort_values('Sales', ascending=False)
rank_fig.add_trace(go.Bar(
    y=sorted_rank_data['Product'],
    x=sorted_rank_data['Sales'],
    marker_color='#4ECDC4',
    orientation='h'
))
rank_fig.update_layout(
    title={
        'text': "Top10 产品销售排行榜",
        'font': {'color': COLOR_SCHEME['primary']}
    },
    yaxis_title="产品",
    xaxis_title="销售额",
    paper_bgcolor=COLOR_SCHEME['card'],
    plot_bgcolor=COLOR_SCHEME['card'],
    font={'color': COLOR_SCHEME['text']},
    margin=dict(l=0, r=0, t=50, b=0),
    yaxis={
        'categoryorder':'total ascending',
        'gridcolor': COLOR_SCHEME['accent']
    },
    xaxis={'gridcolor': COLOR_SCHEME['accent']}
)

# 主分析区布局
main_analysis_area = html.Div(
    children=[
        dcc.Graph(figure=trend_fig, style={'width': '50%', 'height': '400px'}),
        dcc.Graph(figure=geo_fig, style={'width': '30%', 'height': '400px'}),
        dcc.Graph(figure=rank_fig, style={'width': '20%', 'height': '400px'})
    ],
    style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '20px',
        'margin': '20px 0'
    }
)
# 辅助分析区 - 构成分析
sunburst_fig = px.sunburst(
    sunburst_data, 
    path=['Category', 'SubCategory'], 
    values='Sales',
    title="销售构成分析"
).update_layout(
    paper_bgcolor=COLOR_SCHEME['card'],
    plot_bgcolor=COLOR_SCHEME['card'],
    font={'color': COLOR_SCHEME['text']},
    title={'font': {'color': COLOR_SCHEME['primary']}},
    margin=dict(l=0, r=0, t=50, b=0)
)

# 辅助分析区 - 关联分析
scatter_fig = px.scatter(
    scatter_data, 
    x='Price', 
    y='Sales', 
    color='Category',
    title="价格与销售额关联分析"
).update_layout(
    paper_bgcolor=COLOR_SCHEME['card'],
    plot_bgcolor=COLOR_SCHEME['card'],
    font={'color': COLOR_SCHEME['text']},
    title={'font': {'color': COLOR_SCHEME['primary']}},
    xaxis={'gridcolor': COLOR_SCHEME['accent']},
    yaxis={'gridcolor': COLOR_SCHEME['accent']}
)

# 辅助分析区布局
auxiliary_analysis_area = html.Div(
    children=[
        dcc.Graph(figure=sunburst_fig, style={
            'width': '20%',
            'height': '400px',
            'borderRadius': '10px',
            'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
        }),
        dcc.Graph(figure=scatter_fig, style={
            'width': '40%',
            'height': '400px',
            'borderRadius': '10px',
            'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
        }),
        html.Div(style={'width': '40%', 'height': '400px'}, children=[
            html.H3("预警监控", style={'color': COLOR_SCHEME['text']}),
            dash_table.DataTable(
                id='alerts-table',
                columns=[{"name": i, "id": i} for i in alerts.columns],
                data=alerts.to_dict('records'),
                style_table={'backgroundColor': COLOR_SCHEME['card'], 'color': COLOR_SCHEME['text'], 'height': '360px'},
                style_header={'backgroundColor': COLOR_SCHEME['accent'], 'color': COLOR_SCHEME['text']},
                style_cell={'backgroundColor': COLOR_SCHEME['card'], 'color': COLOR_SCHEME['text']}
            )
        ])
    ],
    style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '20px',
        'margin': '20px 0'
    }
)
# 整体布局
app.layout = html.Div(
    children=[
        title_area,
        core_metrics_area,
        main_analysis_area,
        auxiliary_analysis_area
    ],
    style={
        'width': '1920px',
        'height': '1080px',
        'backgroundColor': COLOR_SCHEME['background'],
        'color': COLOR_SCHEME['text'],
        'padding': '20px',
        'fontFamily': 'sans-serif'
    }
)
if __name__ == '__main__':
    app.run_server(debug=True)