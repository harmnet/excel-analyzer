import os
import pandas as pd
import requests
import logging
import json
import PyPDF2
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def validate_question(question):
    """验证题目是否包含所有必要字段"""
    required_fields = {
        '题目类型': question['题目类型'],
        '题干': question['题干'],
        '正确答案': question['正确答案'],
        '题目解析': question['题目解析'],
        '难度': question['难度'],
        '选项A': question['选项A'],
        '选项B': question['选项B']
    }
    
    # 如果不是判断题，还需要验证选项C和D
    if question['题目类型'] != '判断题':
        required_fields['选项C'] = question['选项C']
        required_fields['选项D'] = question['选项D']
    
    # 检查所有必要字段是否都有内容
    empty_fields = [field for field, value in required_fields.items() if not value or value.isspace()]
    
    if empty_fields:
        logging.warning(f"题目缺少必要字段: {', '.join(empty_fields)}")
        return False
        
    # 验证答案格式
    if question['题目类型'] == '单选题' and question['正确答案'] not in ['A', 'B', 'C', 'D']:
        logging.warning(f"单选题答案格式错误: {question['正确答案']}")
        return False
    elif question['题目类型'] == '多选题' and not all(c in 'ABCD' for c in question['正确答案']):
        logging.warning(f"多选题答案格式错误: {question['正确答案']}")
        return False
    elif question['题目类型'] == '判断题' and question['正确答案'] not in ['A', 'B']:
        logging.warning(f"判断题答案格式错误: {question['正确答案']}")
        return False
        
    return True

def parse_markdown_questions(markdown_text):
    """解析 Markdown 格式的题目"""
    questions = []
    current_question = None
    current_type = ""
    
    lines = markdown_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 处理题型
        if line.startswith('### '):
            current_type = line.replace('### ', '').replace('：', '').replace('第1批', '').replace('第2批', '').replace('第3批', '').strip()
            continue
            
        # 处理题目开始
        if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.') or line.startswith('6.') or line.startswith('7.') or line.startswith('8.') or line.startswith('9.'):
            if current_question:
                if validate_question(current_question):
                    questions.append(current_question)
            current_question = {
                "序号": "",
                "题目类型": current_type,
                "题干": "",
                "正确答案": "",
                "题目解析": "",
                "分类": "",
                "标签": "",
                "难度": "易",
                "选项A": "",
                "选项B": "",
                "选项C": "",
                "选项D": ""
            }
            continue
            
        # 处理字段
        if '**' in line:
            parts = line.split('**')
            if len(parts) >= 3:
                field = parts[1].replace(':', '').strip()
                value = parts[2].replace(':', '').strip()
                
                if field == '序号':
                    current_question['序号'] = value
                elif field == '题目类型':
                    current_question['题目类型'] = value
                elif field == '题干':
                    current_question['题干'] = value
                elif field == '正确答案':
                    current_question['正确答案'] = value
                elif field == '题目解析':
                    current_question['题目解析'] = value
                elif field == '选项A':
                    current_question['选项A'] = value
                elif field == '选项B':
                    current_question['选项B'] = value
                elif field == '选项C':
                    current_question['选项C'] = value if value != '-' else ''
                elif field == '选项D':
                    current_question['选项D'] = value if value != '-' else ''
    
    # 添加最后一个题目
    if current_question and validate_question(current_question):
        questions.append(current_question)
        
    return questions

class ModelAPI:
    def __init__(self, model_type="siliconflow"):
        self.model_type = model_type
        if model_type == "siliconflow":
            self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
            self.api_key = "sk-bivnwauskdbvpspvmdorrgkrpwlyfxbfcezqsfsevowzubdj"
            self.model_name = "Pro/deepseek-ai/DeepSeek-V3"
        elif model_type == "deepseek":
            self.api_url = "https://api.deepseek.com/v1/chat/completions"
            self.api_key = "your_deepseek_api_key"  # 替换为实际的 API key
            self.model_name = "deepseek-chat"
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")

    def generate(self, prompt, max_retries=3):
        """调用API生成内容"""
        for retry in range(max_retries):
            try:
                if self.model_type == "siliconflow":
                    return self._call_siliconflow_api(prompt)
                else:
                    return self._call_deepseek_api(prompt)
            except Exception as e:
                logging.error(f"API调用失败 (尝试 {retry + 1}/{max_retries}): {str(e)}")
                if retry < max_retries - 1:
                    logging.info("等待5秒后重试...")
                    time.sleep(5)
                else:
                    raise

    def _call_siliconflow_api(self, prompt):
        """调用硅基流动API"""
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的教育工作者"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "stream": False,
            "max_tokens": 4096,
            "stop": ["null"],
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0,
            "n": 1,
            "response_format": {"type": "text"}
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.api_url, json=payload, headers=headers, timeout=180)
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.text}")
            
        return response.json()["choices"][0]["message"]["content"]

    def _call_deepseek_api(self, prompt):
        """调用DeepSeek API"""
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的教育工作者"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 0.7,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.api_url, json=payload, headers=headers, timeout=180)
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.text}")
            
        return response.json()["choices"][0]["message"]["content"]

def generate_questions_batch(content, existing_questions, batch_num, model_type="siliconflow", max_retries=3):
    """生成一批题目"""
    logging.info(f"正在生成第 {batch_num}/6 批题目...")
    
    # 根据批次确定题目类型分布
    if batch_num <= 3:
        type_distribution = "单选题7道,多选题2道,判断题1道"
    else:
        type_distribution = "单选题3道,多选题4道,判断题3道"
    
    prompt = f"""
    阅读理解以下内容,帮我出10道试题。    
    题目要求:
    1. 题目类型及数量:
       本批需要生成{type_distribution}
    2. 每道题目需要和以下已有题目不重复:
    {[q['题干'] for q in existing_questions]}
    3. 输出格式要求:
       每道题目必须严格按照以下格式输出:
       ### 题目类型（单选题/多选题/判断题）
       1. **序号**: 1
          **题目类型**: 单选题
          **题干**: 这里是题目内容？
          **正确答案**: A
          **题目解析**: 这里是解析内容
          **选项A**: 这里是选项A内容
          **选项B**: 这里是选项B内容
          **选项C**: 这里是选项C内容（判断题填"-"）
          **选项D**: 这里是选项D内容（判断题填"-"）

    4. 格式说明:
       - 每个字段必须用**包围，如 **序号**: 1
       - 字段名称必须完全一致，包括冒号
       - 判断题的选项A表示"正确"，选项B表示"错误"，选项C和D统一填"-"
       - 答案格式：
         单选题：A/B/C/D
         多选题：ABC等组合
         判断题：A(正确)或B(错误)
       
    阅读理解内容如下：
    {content}
    """
    
    # logging.info(f"提示词内容:\n{prompt}")  # 注释掉这行
    
    try:
        model_api = ModelAPI(model_type)
        questions_str = model_api.generate(prompt)
        
        # 输出原始响应内容
        logging.info(f"API返回内容:\n{questions_str}")
        
        questions = parse_markdown_questions(questions_str)
        logging.info(f"解析后的题目内容:\n{json.dumps(questions, ensure_ascii=False, indent=2)}")
        
        if not questions:
            raise ValueError("解析结果为空")
            
        logging.info(f"成功解析第 {batch_num} 批题目，共 {len(questions)} 道题")
        return [q for q in questions if validate_question(q)]
        
    except Exception as e:
        logging.error(f"生成题目失败: {str(e)}")
        return []

def read_pdf_and_generate_questions(pdf_path, model_type="siliconflow"):
    # 读取PDF
    logging.info("开始读取PDF文件...")
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()
        logging.info("PDF文件读取完成")
    except Exception as e:
        logging.error(f"读取PDF失败: {str(e)}")
        return
    
    # 分批次生成题目
    all_questions = []
    for batch in range(1, 7):
        questions = generate_questions_batch(content, all_questions, batch, model_type)
        all_questions.extend(questions)
        logging.info(f"已完成 {len(all_questions)}/60 道题目")
    
    # 保存所有题目
    questions_data = {
        '序号': [],
        '题目类型': [],
        '题干': [],
        '正确答案': [],
        '题目解析': [],
        '分类': [],
        '标签': [],
        '难度': [],
        '选项A': [],
        '选项B': [],
        '选项C': [],
        '选项D': []
    }
    
    # 处理所有题目
    for i, q in enumerate(all_questions, 1):
        q['序号'] = str(i)  # 重新编号
        questions_data['序号'].append(q['序号'])
        questions_data['题目类型'].append(q['题目类型'])
        questions_data['题干'].append(q['题干'])
        questions_data['正确答案'].append(q['正确答案'])
        questions_data['题目解析'].append(q['题目解析'])
        questions_data['分类'].append(q['分类'])
        questions_data['标签'].append(q['标签'])
        questions_data['难度'].append(q['难度'])
        questions_data['选项A'].append(q['选项A'])
        questions_data['选项B'].append(q['选项B'])
        if q['题目类型'] == '判断题':
            questions_data['选项C'].append('')
            questions_data['选项D'].append('')
        else:
            questions_data['选项C'].append(q['选项C'])
            questions_data['选项D'].append(q['选项D'])
    
    # 保存到Excel
    try:
        df = pd.DataFrame(questions_data)
        desktop_path = '/Users/harmnet/Desktop'
        excel_path = os.path.join(desktop_path, '题库.xlsx')
        df.to_excel(excel_path, index=False)
        logging.info(f"题库已成功保存到: {excel_path}")
    except Exception as e:
        logging.error(f"保存题库失败: {str(e)}")

# 使用示例
pdf_path = "/Users/harmnet/Desktop/8.2 数据服务基础设施安全管理.pdf"
# 使用硅基流动API
read_pdf_and_generate_questions(pdf_path, "siliconflow")
# 或使用DeepSeek API
# read_pdf_and_generate_questions(pdf_path, "deepseek")