import dash
from dash import dcc, html
import plotly.graph_objects as go

# 创建 Mermaid 图表数据
nodes = [
    {'id': 'SO', 'label': 'SO战略-扩张型', 'x': 0, 'y': 0},
    {'id': '1', 'label': '加速欧洲工厂建设', 'x': 1, 'y': -0.5},
    {'id': '2', 'label': '开发V2G储能产品线', 'x': 1, 'y': 0.5},
    {'id': 'WO', 'label': 'WO战略-改进型', 'x': 0, 'y': 2},
    {'id': '3', 'label': '与宁德时代合资建电池厂', 'x': 1, 'y': 1.5},
    {'id': '4', 'label': '引入丰田精益生产体系', 'x': 1, 'y': 2.5},
    {'id': 'ST', 'label': 'ST战略-防御型', 'x': 0, 'y': 4},
    {'id': '5', 'label': '建立锂资源战略储备', 'x': 1, 'y': 3.5},
    {'id': '6', 'label': '自研车规级芯片', 'x': 1, 'y': 4.5},
    {'id': 'WT', 'label': 'WT战略-保守型', 'x': 0, 'y': 6},
    {'id': '7', 'label': '聚焦高端市场差异化', 'x': 1, 'y': 5.5},
    {'id': '8', 'label': '申请欧盟碳关税豁免', 'x': 1, 'y': 6.5}
]

edges = [
    {'from': 'SO', 'to': '1'},
    {'from': 'SO', 'to': '2'},
    {'from': 'WO', 'to': '3'},
    {'from': 'WO', 'to': '4'},
    {'from': 'ST', 'to': '5'},
    {'from': 'ST', 'to': '6'},
    {'from': 'WT', 'to': '7'},
    {'from': 'WT', 'to': '8'}
]

# 创建图表
fig = go.Figure()

# 添加节点
for node in nodes:
    fig.add_trace(go.Scatter(
        x=[node['x']],
        y=[node['y']],
        mode='markers+text',
        name=node['id'],
        text=node['label'],
        textposition='middle right',
        hoverinfo='text',
        marker=dict(size=20, color='lightblue')
    ))

# 添加边
for edge in edges:
    start = next(node for node in nodes if node['id'] == edge['from'])
    end = next(node for node in nodes if node['id'] == edge['to'])
    fig.add_trace(go.Scatter(
        x=[start['x'], end['x']],
        y=[start['y'], end['y']],
        mode='lines',
        line=dict(color='gray'),
        hoverinfo='none'
    ))

# 更新布局
fig.update_layout(
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white',
    margin=dict(l=0, r=0, t=0, b=0),
    height=800
)

# 创建 Dash 应用
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
