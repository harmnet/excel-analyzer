import os
import pandas as pd
import requests
from flask import Flask, request, render_template, jsonify, Response
import json
import io
import sys
import logging
import datetime
import time
import socket
from openai import OpenAI

# 修改模块导入路径部分
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# from 硅基流动API示例 import call_ai_api, API_KEY, API_URL

# 配置日志
log_dir = os.path.join(current_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'data_analysis_{datetime.datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# 配置火山引擎API参数
API_CONFIG = {
    "api_key": "026f661d-3948-42e1-acdd-81e64e62da1b",
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "model": "deepseek-r1-250120"
}

# 全局client实例
client = OpenAI(
    api_key=API_CONFIG["api_key"],
    base_url=API_CONFIG["base_url"],
)

def analyze_with_ai(prompt, stream=False):
    """通用AI分析函数，支持流式输出"""
    logger.info("开始调用AI分析...")
    start_time = time.time()
    
    try:
        logger.info(f"请求AI模型: {API_CONFIG['model']}")
        logger.info(f"提示词长度: {len(prompt)} 字符")
        
        if stream:
            # 流式输出模式
            def generate():
                response = client.chat.completions.create(
                    model=API_CONFIG["model"],
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    stream=True,
                    response_format={"type": "json_object"}
                )
                
                full_content = ""
                for chunk in response:
                    if not chunk.choices:
                        continue
                    
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_content += delta
                        yield f"data: {json.dumps({'content': delta, 'full': full_content})}\n\n"
                
                # 发送完成信号
                elapsed_time = time.time() - start_time
                logger.info(f"AI流式分析完成，耗时: {elapsed_time:.2f}秒")
                yield f"data: {json.dumps({'content': '[DONE]', 'time': elapsed_time})}\n\n"
            
            return generate
        else:
            # 非流式输出模式
            response = client.chat.completions.create(
                model=API_CONFIG["model"],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"AI分析完成，耗时: {elapsed_time:.2f}秒")
            return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"AI分析失败: {str(e)}")
        return f"AI分析失败: {str(e)}"

@app.route('/')
def index():
    logger.info("访问首页")
    return get_upload_template()

@app.route('/analyze', methods=['POST'])
def analyze_data():
    session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(hash(request.remote_addr))[:4]
    logger.info(f"[{session_id}] 开始处理上传文件请求")
    upload_start_time = time.time()
    
    try:
        # 文件处理逻辑
        file = request.files['file']
        logger.info(f"[{session_id}] 上传文件: {file.filename}, 大小: {len(file.read())/1024:.2f} KB")
        file.seek(0)  # 重置文件指针位置
        
        file_ext = file.filename.split('.')[-1].lower()
        
        # 读取数据
        logger.info(f"[{session_id}] 开始读取{file_ext}文件")
        if file_ext == 'csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        upload_end_time = time.time()
        logger.info(f"[{session_id}] 文件上传和读取完成，耗时: {upload_end_time - upload_start_time:.2f}秒")
        logger.info(f"[{session_id}] 数据集维度: {df.shape[0]}行 x {df.shape[1]}列")
        
        # 自定义JSON编码器处理特殊类型如Timestamp
        class CustomJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'isoformat'):  # 处理日期时间类型
                    return obj.isoformat()
                elif pd.isna(obj):  # 处理NaN、None等
                    return None
                else:
                    return str(obj)  # 其他类型转为字符串
        
        # 构建分析报告
        logger.info(f"[{session_id}] 开始数据集分析")
        analysis_start_time = time.time()
        
        report = {
            "shape": df.shape,
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "sample": df.head().to_dict(orient='records')
        }
        
        # 记录缺失值情况
        missing_count = df.isnull().sum().sum()
        missing_percentage = (missing_count / (df.shape[0] * df.shape[1])) * 100
        logger.info(f"[{session_id}] 数据集缺失值: {missing_count}个 ({missing_percentage:.2f}%)")
        
        # 生成AI提示
        analysis_prompt = f"""
        请分析以下数据集质量：
        1. 数据维度：{report['shape']}
        2. 数据类型：{json.dumps(report['dtypes'], indent=2)}
        3. 缺失值统计：{json.dumps(report['missing'], indent=2)}
        4. 数据样例：{json.dumps(report['sample'], indent=2, cls=CustomJSONEncoder)}
        
        请用中文给出详细的质量评估和改进建议，使用Markdown格式。
        """
        
        # 获取AI分析结果
        logger.info(f"[{session_id}] 开始调用AI进行质量分析")
        ai_result = analyze_with_ai(analysis_prompt)
        
        analysis_end_time = time.time()
        logger.info(f"[{session_id}] 数据分析完成，总耗时: {analysis_end_time - analysis_start_time:.2f}秒")
        
        # 保留思考过程，确保正确格式化
        # 如果有必要，可以标记但不移除思考过程
        if "思考中..." in ai_result:
            # 仅做日志记录，不改变内容
            logger.info(f"[{session_id}] AI返回包含思考过程的分析")
        
        # 使用自定义编码器处理整个响应
        response = json.dumps({
            "report": report,
            "analysis": ai_result
        }, cls=CustomJSONEncoder)
        
        logger.info(f"[{session_id}] 返回分析结果，处理完成")
        return jsonify(json.loads(response))
        
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"[{session_id}] 处理错误: {str(e)}\n{error_msg}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def handle_upload():
    try:
        file = request.files['file']
        # 保存文件到临时目录
        temp_dir = os.path.join(current_dir, 'temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        
        return jsonify({
            "status": "success",
            "filename": file.filename,
            "size": os.path.getsize(file_path)
        })
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_stream', methods=['POST'])
def analyze_data_stream():
    # 从临时目录读取文件
    filename = request.json.get('filename')
    file_path = os.path.join(current_dir, 'temp_uploads', filename)
    
    try:
        with open(file_path, 'rb') as f:
            # 文件处理逻辑（需要保持4空格缩进）
            file_ext = filename.split('.')[-1].lower()
            
            # 读取数据
            if file_ext == 'csv':
                df = pd.read_csv(f)
            else:
                df = pd.read_excel(f)
            
            # 后续处理代码（保持原有逻辑）
            # ... [原有生成报告、调用AI等代码] ...
            
            return Response(combined_generator(), mimetype="text/event-stream")
            
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"流式处理错误: {str(e)}\n{error_msg}")
        return Response(f"data: {json.dumps({'error': str(e)})}\n\n", 
                        mimetype="text/event-stream")

@app.route('/templates/upload.html')
def get_upload_template():
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>智能数据集分析平台</title>
        <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {
                --primary: #1E88E5;
                --secondary: #26A69A;
                --light: #F5F5F5;
            }
            body {
                background: var(--light);
                min-height: 100vh;
            }
            .main-container {
                max-width: 800px;
                margin: 2rem auto;
                padding: 2rem;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .upload-area {
                border: 2px dashed #ced4da;
                border-radius: 8px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s;
            }
            .upload-area:hover {
                border-color: var(--primary);
                background: rgba(30, 136, 229, 0.05);
            }
            .progress-container {
                height: 20px;
                border-radius: 10px;
                overflow: hidden;
            }
            .analysis-tabs .nav-link {
                color: #495057;
                font-weight: 500;
            }
            .analysis-tabs .nav-link.active {
                color: var(--primary);
                border-bottom: 3px solid var(--primary);
            }
            .preview-table {
                max-height: 400px;
                overflow: auto;
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            <h2 class="text-center mb-4"><i class="fas fa-database me-2"></i>智能数据集分析平台</h2>
            
            <!-- 上传区域 -->
            <div class="upload-area" id="uploadArea">
                <input type="file" id="fileUpload" class="d-none" accept=".csv,.xlsx">
                <button class="btn btn-lg btn-primary" onclick="document.getElementById('fileUpload').click()">
                    <i class="fas fa-cloud-upload-alt me-2"></i>选择数据集文件
                </button>
                <p class="text-muted mt-3 mb-0">支持格式：CSV、Excel</p>
            </div>

            <!-- 进度显示 -->
            <div class="mt-4" id="progressSection" style="display:none;">
                <div class="d-flex justify-content-between mb-2">
                    <span id="statusText">准备上传...</span>
                    <span id="progressPercent">0%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" 
                         role="progressbar" style="width: 0%"></div>
                </div>
            </div>

            <!-- 分析结果 -->
            <div class="mt-4" id="resultSection" style="display:none;">
                <ul class="nav analysis-tabs" id="resultTabs">
                    <li class="nav-item">
                        <a class="nav-link active" data-bs-toggle="tab" href="#rawData">原始数据</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-bs-toggle="tab" href="#analysisResult">分析结论</a>
                    </li>
                </ul>
                
                <div class="tab-content mt-3">
                    <div class="tab-pane fade show active" id="rawData">
                        <div class="preview-table"></div>
                    </div>
                    <div class="tab-pane fade" id="analysisResult">
                        <div class="card p-3"></div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
        <script>
            // 文件选择后自动上传
            document.getElementById('fileUpload').addEventListener('change', function(e) {
                uploadFile();
            });

            // 实时进度更新处理
            const progressBar = document.querySelector('.progress-bar');
            const progressPercent = document.getElementById('progressPercent');
            const statusText = document.getElementById('statusText');

            function updateProgress(percentage, message) {
                progressBar.style.width = percentage + '%';
                progressPercent.textContent = percentage + '%';
                statusText.textContent = message;
            }

            // 修改结果处理逻辑
            function processAnalysisResult(result) {
                // 直接提取总结部分
                const summaryStart = result.indexOf('## 数据质量分析总结');
                const finalSummary = summaryStart !== -1 ? result.substring(summaryStart) : result;

                // 更新结果展示
                document.getElementById('analysisResult').innerHTML = marked.parse(finalSummary);
                
                // 隐藏思考过程标签
                document.querySelectorAll('.nav-item').forEach(item => {
                    if (item.textContent.includes('思考过程')) {
                        item.style.display = 'none';
                    }
                });
            }

            // 修改文件上传处理逻辑
            function uploadFile() {
                const fileInput = document.getElementById('fileUpload');
                const file = fileInput.files[0];
                
                // 显示进度区域
                document.getElementById('progressSection').style.display = 'block';
                document.getElementById('resultSection').style.display = 'none';
                
                // 重置进度条
                updateProgress(0, '开始上传文件...');

                const xhr = new XMLHttpRequest();
                const formData = new FormData();
                formData.append('file', file);

                // 实时上传进度监听
                xhr.upload.addEventListener('progress', (event) => {
                    if (event.lengthComputable) {
                        const percent = Math.round((event.loaded / event.total) * 100);
                        updateProgress(percent, `上传中... (${percent}%)`);
                    }
                });

                // 处理响应
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === XMLHttpRequest.DONE) {
                        if (xhr.status === 200) {
                            // 开始分析流程
                            startAnalysis();
                        } else {
                            showError(`上传失败: ${xhr.statusText}`);
                        }
                    }
                };

                xhr.open('POST', '/upload');
                xhr.send(formData);
            }

            // 新增分析启动函数
            function startAnalysis() {
                const eventSource = new EventSource('/analyze_stream');
                
                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.type === 'progress') {
                        updateProgress(data.percentage, data.message);
                    } else if (data.type === 'result') {
                        processAnalysisResult(data.content);
                        document.getElementById('resultSection').style.display = 'block';
                        eventSource.close();
                    }
                };
                
                eventSource.onerror = (err) => {
                    showError('分析连接中断');
                    eventSource.close();
                };
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    logger.info("===== 数据集质量分析服务启动 =====")
    # 关键修改：必须使用0.0.0.0作为host，并更改为8080端口
    app.run(debug=True, host='0.0.0.0', port=8080)
    logger.info("服务已启动，可通过以下方式访问：")
    
    # 获取本机IP地址并显示
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        logger.info(f"1. 本地访问: http://127.0.0.1:8080")
        logger.info(f"2. 局域网访问: http://{local_ip}:8080")
        
        # 提示如何获取公网访问
        logger.info("如需外网访问，请考虑以下方式：")
        logger.info("1. 确保防火墙已允许8080端口的TCP连接")
        logger.info("2. 如需公网访问，可使用内网穿透工具如ngrok: ngrok http 8080")
    except:
        logger.info("无法获取本机IP地址，请使用 http://127.0.0.1:8080 访问")
