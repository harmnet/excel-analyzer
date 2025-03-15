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

# 配置硅基API参数（实际值需要替换）
API_CONFIG = {
    "url": "https://api.siliconflow.cn/v1/chat/completions",
    "key": "sk-bivnwauskdbvpspvmdorrgkrpwlyfxbfcezqsfsevowzubdj",
    "model": "Pro/deepseek-ai/DeepSeek-V3"
}

def analyze_with_ai(prompt, stream=False):
    """通用AI分析函数，支持流式输出"""
    logger.info("开始调用AI分析...")
    start_time = time.time()
    
    headers = {
        "Authorization": f"Bearer {API_CONFIG['key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": API_CONFIG['model'],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": stream
    }
    
    try:
        logger.info(f"请求AI模型: {API_CONFIG['model']}")
        logger.info(f"提示词长度: {len(prompt)} 字符")
        
        if stream:
            # 流式输出模式
            def generate():
                response = requests.post(
                    API_CONFIG['url'], 
                    headers=headers, 
                    json=payload, 
                    stream=True
                )
                response.raise_for_status()
                
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data.strip() == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                delta = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if delta:
                                    full_content += delta
                                    yield f"data: {json.dumps({'content': delta, 'full': full_content})}\n\n"
                            except Exception as e:
                                logger.error(f"解析流式响应出错: {str(e)}")
                
                # 发送完成信号
                elapsed_time = time.time() - start_time
                logger.info(f"AI流式分析完成，耗时: {elapsed_time:.2f}秒")
                yield f"data: {json.dumps({'content': '[DONE]', 'time': elapsed_time})}\n\n"
            
            return generate
        else:
            # 非流式输出模式
            response = requests.post(API_CONFIG['url'], headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            elapsed_time = time.time() - start_time
            token_count = result.get('usage', {}).get('total_tokens', 'N/A')
            logger.info(f"AI分析完成，耗时: {elapsed_time:.2f}秒，使用tokens: {token_count}")
            return result['choices'][0]['message']['content']
        
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

@app.route('/analyze_stream', methods=['POST'])
def analyze_data_stream():
    session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(hash(request.remote_addr))[:4]
    logger.info(f"[{session_id}] 开始处理流式分析请求")
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
        
        # 自定义JSON编码器处理特殊类型
        class CustomJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                elif pd.isna(obj):
                    return None
                else:
                    return str(obj)
        
        # 构建数据报告
        report = {
            "shape": df.shape,
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "sample": df.head().to_dict(orient='records')
        }
        
        # 修改提示词，让AI生成清晰的思考过程和精炼总结
        analysis_prompt = f"""
        请分析以下数据集质量：
        1. 数据维度：{report['shape']}
        2. 数据类型：{json.dumps(report['dtypes'], indent=2)}
        3. 缺失值统计：{json.dumps(report['missing'], indent=2)}
        4. 数据样例：{json.dumps(report['sample'], indent=2, cls=CustomJSONEncoder)}
        
        请用中文给出详细的质量评估和改进建议，使用Markdown格式。
        我希望你的回答分为两个部分：
        
        第一部分是思考过程，请在每个思考步骤前标记"思考中..."，包含以下内容：
        1. 首先分析数据维度和基本结构
        2. 然后详细检查每列的数据类型是否合适
        3. 接着分析缺失值情况及其对数据质量的影响
        4. 根据数据样例分析，找出可能存在的异常值或数据问题
        5. 最后给出整体数据质量评分和具体改进建议
        
        第二部分是总结结果，以"## 数据质量分析总结"为标题，简明扼要地总结分析发现和关键建议，不超过300字。请在总结前使用"---"分隔线将两部分内容分开。
        """
        
        # 获取流式分析结果
        logger.info(f"[{session_id}] 开始流式调用AI")
        generate = analyze_with_ai(analysis_prompt, stream=True)
        
        response = Response(generate(), mimetype="text/event-stream")
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        return response
        
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"[{session_id}] 流式处理错误: {str(e)}\n{error_msg}")
        return Response(f"data: {json.dumps({'error': str(e)})}\n\n", 
                        mimetype="text/event-stream")

@app.route('/templates/upload.html')
def get_upload_template():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>数据集质量分析</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .upload-container {
                border: 2px dashed #ccc;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
                border-radius: 5px;
            }
            .upload-container:hover {
                border-color: #007bff;
            }
            .btn {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            }
            .btn:hover {
                background-color: #0056b3;
            }
            .btn:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
            #result {
                margin-top: 30px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                display: none;
            }
            .loading {
                text-align: center;
                display: none;
            }
            .error {
                color: red;
                margin-top: 10px;
            }
            .progress-container {
                width: 100%;
                margin-top: 10px;
                display: none;
            }
            .progress-bar {
                width: 100%;
                height: 20px;
                background-color: #f3f3f3;
                border-radius: 5px;
                overflow: hidden;
            }
            .progress {
                height: 100%;
                background-color: #4CAF50;
                width: 0%;
                transition: width 0.3s;
                text-align: center;
                line-height: 20px;
                color: white;
            }
            .file-info {
                font-size: 14px;
                margin-top: 5px;
                color: #666;
            }
            #thinking {
                background-color: #f8f9fa;
                border-left: 3px solid #28a745;
                padding: 10px 15px;
                margin: 15px 0;
                display: none;
                font-style: italic;
                color: #6c757d;
            }
            .thinking-step {
                margin: 10px 0;
                padding-left: 15px;
                border-left: 2px solid #17a2b8;
            }
            .blink {
                animation: blink-animation 1s steps(5, start) infinite;
            }
            @keyframes blink-animation {
                to { visibility: hidden; }
            }
            .ai-status {
                background-color: #e9ecef;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 10px 0;
                font-size: 14px;
                color: #495057;
                display: none;
            }
            .status-icon {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-waiting {
                background-color: #ffc107;
            }
            .status-processing {
                background-color: #17a2b8;
            }
            .status-completed {
                background-color: #28a745;
            }
            #resultSummary {
                background-color: #f8fff8;
                border-left: 4px solid #28a745;
                padding: 15px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .tab-container {
                margin-top: 20px;
                border-bottom: 1px solid #ddd;
            }
            .tab {
                display: inline-block;
                padding: 10px 20px;
                cursor: pointer;
                background-color: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                margin-right: 5px;
                border-radius: 5px 5px 0 0;
            }
            .tab.active {
                background-color: white;
                border-bottom: 2px solid white;
                margin-bottom: -1px;
                font-weight: bold;
            }
            .tab-content {
                display: none;
                padding: 15px;
                border: 1px solid #ddd;
                border-top: none;
            }
            .tab-content.active {
                display: block;
            }
        </style>
    </head>
    <body>
        <h1>数据集质量分析工具</h1>
        <div class="upload-container">
            <h2>上传数据集文件</h2>
            <p>支持的格式: Excel (.xlsx, .xls) 或 CSV (.csv)</p>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" id="fileInput" accept=".xlsx,.xls,.csv">
                <br>
                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar">
                        <div class="progress" id="progressBar">0%</div>
                    </div>
                    <div class="file-info" id="fileInfo"></div>
                </div>
                <br>
                <button type="submit" class="btn" id="analyzeBtn" disabled>分析数据集</button>
            </form>
            <p class="error" id="errorMsg"></p>
        </div>
        
        <div class="ai-status" id="aiStatus">
            <span class="status-icon status-waiting" id="statusIcon"></span>
            <span id="statusText">准备分析...</span>
        </div>
        
        <div id="thinking">
            <h3>AI思考过程：</h3>
            <div id="thinkingSteps"></div>
        </div>
        
        <div class="loading" id="loading">
            <p>正在分析数据集，请稍候...</p>
            <img src="https://i.stack.imgur.com/kOnzy.gif" width="50" height="50">
        </div>
        
        <div id="result">
            <h2>分析结果</h2>
            <div class="tab-container">
                <div class="tab active" data-tab="summary">分析总结</div>
                <div class="tab" data-tab="detail">详细分析</div>
                <div class="tab" data-tab="thinking">思考过程</div>
            </div>
            <div id="resultSummary" class="tab-content active" data-content="summary"></div>
            <div id="analysisResult" class="tab-content" data-content="detail"></div>
            <div id="thinking" class="tab-content" data-content="thinking">
                <h3>AI思考过程：</h3>
                <div id="thinkingSteps"></div>
            </div>
        </div>
        
        <script>
            // 文件选择和验证
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const file = this.files[0];
                const analyzeBtn = document.getElementById('analyzeBtn');
                const errorMsg = document.getElementById('errorMsg');
                const progressContainer = document.getElementById('progressContainer');
                const fileInfo = document.getElementById('fileInfo');
                
                if (!file) {
                    analyzeBtn.disabled = true;
                    errorMsg.textContent = '';
                    progressContainer.style.display = 'none';
                    return;
                }
                
                const validExtensions = ['.xlsx', '.xls', '.csv'];
                const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
                
                if (!validExtensions.includes(fileExtension)) {
                    analyzeBtn.disabled = true;
                    errorMsg.textContent = '请上传Excel或CSV格式的文件';
                    progressContainer.style.display = 'none';
                    return;
                }
                
                // 显示文件信息
                const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
                fileInfo.textContent = `文件名: ${file.name} (${fileSizeMB} MB)`;
                progressContainer.style.display = 'block';
                errorMsg.textContent = '';
                
                // 模拟文件上传进度
                simulateUploadProgress();
            });
            
            // 模拟文件上传进度
            function simulateUploadProgress() {
                const progressBar = document.getElementById('progressBar');
                const analyzeBtn = document.getElementById('analyzeBtn');
                
                let progress = 0;
                const interval = setInterval(() => {
                    progress += 5;
                    if (progress > 100) {
                        clearInterval(interval);
                        progress = 100;
                        // 上传完成，启用分析按钮
                        analyzeBtn.disabled = false;
                    }
                    
                    progressBar.style.width = progress + '%';
                    progressBar.textContent = progress + '%';
                }, 150);
            }
            
            document.getElementById('uploadForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const fileInput = document.getElementById('fileInput');
                if (!fileInput.files.length) {
                    document.getElementById('errorMsg').textContent = '请选择文件';
                    return;
                }
                
                const file = fileInput.files[0];
                const validExtensions = ['.xlsx', '.xls', '.csv'];
                const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
                
                if (!validExtensions.includes(fileExtension)) {
                    document.getElementById('errorMsg').textContent = '请上传Excel或CSV格式的文件';
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                // 禁用分析按钮，显示状态
                document.getElementById('analyzeBtn').disabled = true;
                document.getElementById('errorMsg').textContent = '';
                document.getElementById('result').style.display = 'none';
                document.getElementById('thinking').style.display = 'none';
                document.getElementById('thinkingSteps').innerHTML = '';
                
                // 显示AI状态
                const aiStatus = document.getElementById('aiStatus');
                const statusIcon = document.getElementById('statusIcon');
                const statusText = document.getElementById('statusText');
                
                aiStatus.style.display = 'block';
                statusIcon.className = 'status-icon status-waiting';
                statusText.textContent = '正在上传数据集...';
                
                // 使用流式输出API
                fetch('/analyze_stream', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('网络响应错误');
                    }
                    
                    statusIcon.className = 'status-icon status-processing';
                    statusText.textContent = '正在执行分析...';
                    
                    // 加载Markdown渲染器
                    if (!window.markdownit) {
                        const script = document.createElement('script');
                        script.src = 'https://cdn.jsdelivr.net/npm/markdown-it@12/dist/markdown-it.min.js';
                        document.head.appendChild(script);
                    }
                    
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    let content = '';
                    let markdown = '';
                    let thinking = document.getElementById('thinking');
                    let thinkingSteps = document.getElementById('thinkingSteps');
                    
                    thinking.style.display = 'block';
                    document.getElementById('result').style.display = 'block';
                    
                    function processStream({ done, value }) {
                        if (done) {
                            return;
                        }
                        
                        const chunk = decoder.decode(value, { stream: true });
                        const lines = chunk.split('\\n\\n');
                        
                        lines.forEach(line => {
                            if (line.startsWith('data: ')) {
                                try {
                                    const data = JSON.parse(line.substring(6));
                                    
                                    if (data.error) {
                                        document.getElementById('errorMsg').textContent = data.error;
                                        statusIcon.className = 'status-icon status-error';
                                        statusText.textContent = '分析错误';
                                        return;
                                    }
                                    
                                    if (data.content === '[DONE]') {
                                        // 分析完成
                                        statusIcon.className = 'status-icon status-completed';
                                        statusText.textContent = `分析完成 (${data.time.toFixed(2)}秒)`;
                                        document.getElementById('analyzeBtn').disabled = false;
                                        return;
                                    }
                                    
                                    // 更新内容
                                    content += data.content;
                                    
                                    // 处理分隔符，分离思考过程和总结
                                    if (content.includes('---')) {
                                        const parts = content.split('---');
                                        const thinkingPart = parts[0];
                                        const summaryPart = parts.length > 1 ? parts[1] : '';
                                        
                                        // 处理思考过程
                                        if (thinkingPart.includes('思考中...')) {
                                            // 重新构建思考步骤
                                            thinkingSteps.innerHTML = '';
                                            const steps = thinkingPart.split('思考中...');
                                            for (let i = 0; i < steps.length; i++) {
                                                const step = document.createElement('div');
                                                step.className = 'thinking-step';
                                                let stepContent = steps[i];
                                                
                                                // 如果是最后一步还在进行中，添加闪烁光标
                                                if (i === steps.length - 1) {
                                                    stepContent += ' <span class="blink">|</span>';
                                                }
                                                
                                                step.innerHTML = `<strong>步骤 ${i + 1}:</strong> ${stepContent}`;
                                                thinkingSteps.appendChild(step);
                                            }
                                            
                                            // 构建Markdown内容（去除思考过程）
                                            markdown = content.replace(/思考中\.\.\./g, '');
                                        } else {
                                            markdown = content;
                                        }
                                        
                                        // 渲染总结部分
                                        if (window.markdownit && summaryPart) {
                                            const md = window.markdownit();
                                            document.getElementById('resultSummary').innerHTML = md.render(summaryPart);
                                            // 显示详细分析（没有思考中标记的完整内容）
                                            document.getElementById('analysisResult').innerHTML = md.render(markdown);
                                        }
                                    } else {
                                        // 检测思考过程
                                        if (content.includes('思考中...')) {
                                            const parts = content.split('思考中...');
                                            
                                            // 重新构建思考步骤
                                            thinkingSteps.innerHTML = '';
                                            for (let i = 0; i < parts.length; i++) {
                                                const step = document.createElement('div');
                                                step.className = 'thinking-step';
                                                let stepContent = parts[i];
                                                
                                                // 如果是最后一步还在进行中，添加闪烁光标
                                                if (i === parts.length - 1) {
                                                    stepContent += ' <span class="blink">|</span>';
                                                }
                                                
                                                step.innerHTML = `<strong>步骤 ${i + 1}:</strong> ${stepContent}`;
                                                thinkingSteps.appendChild(step);
                                            }
                                            
                                            // 构建Markdown内容（去除思考过程）
                                            markdown = content.replace(/思考中\.\.\./g, '');
                                        }
                                        
                                        // 渲染Markdown结果
                                        if (window.markdownit) {
                                            const md = window.markdownit();
                                            document.getElementById('analysisResult').innerHTML = md.render(markdown);
                                        } else {
                                            document.getElementById('analysisResult').textContent = markdown;
                                        }
                                    }
                                } catch (e) {
                                    console.error('解析流数据错误:', e);
                                }
                            }
                        });
                        
                        // 继续读取下一块数据
                        reader.read().then(processStream);
                    }
                    
                    // 开始读取流
                    reader.read().then(processStream);
                })
                .catch((error) => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('analyzeBtn').disabled = false;
                    document.getElementById('aiStatus').style.display = 'none';
                    document.getElementById('errorMsg').textContent = '请求失败: ' + error.message;
                });
            });

            // 添加标签切换功能
            document.addEventListener('DOMContentLoaded', function() {
                const tabs = document.querySelectorAll('.tab');
                
                tabs.forEach(tab => {
                    tab.addEventListener('click', function() {
                        const tabId = this.getAttribute('data-tab');
                        
                        // 激活点击的标签
                        tabs.forEach(t => t.classList.remove('active'));
                        this.classList.add('active');
                        
                        // 显示对应内容
                        document.querySelectorAll('.tab-content').forEach(content => {
                            content.classList.remove('active');
                            if(content.getAttribute('data-content') === tabId) {
                                content.classList.add('active');
                            }
                        });
                    });
                });
            });
        </script>
    </body>
    </html>
    """

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
