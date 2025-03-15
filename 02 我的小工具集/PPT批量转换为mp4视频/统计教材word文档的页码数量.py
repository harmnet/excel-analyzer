import os
import glob
import subprocess
import tempfile
import time

# 文件路径配置
doc_folder = "/Users/harmnet/Desktop/教材"  # 教材文件夹路径

# 获取所有docx文件
doc_files = glob.glob(os.path.join(doc_folder, "*.docx"))

if not doc_files:
    print(f"在 {doc_folder} 中未找到任何.docx文件")
    exit(1)

print(f"找到 {len(doc_files)} 个Word文档，开始统计页数...")

# 初始化总页数计数器
total_pages = 0

# 使用LibreOffice将Word转换为PDF并获取页数
def get_pdf_page_count(doc_file):
    print(f"正在转换 {os.path.basename(doc_file)} 为PDF...")
    
    # 创建临时PDF文件名
    pdf_basename = os.path.splitext(os.path.basename(doc_file))[0] + ".pdf"
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_basename)
    
    # 尝试多个可能的LibreOffice路径
    libreoffice_paths = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',  # 标准安装路径
        '/usr/local/bin/soffice',     # Homebrew (Intel)
        '/opt/homebrew/bin/soffice'    # Homebrew (Apple Silicon)
    ]
    
    # 查找可用的LibreOffice路径
    soffice = None
    for path in libreoffice_paths:
        if os.path.exists(path):
            soffice = path
            break
    
    if not soffice:
        print("未找到LibreOffice，请确保已安装")
        return 0
    
    # 使用LibreOffice转换为PDF
    try:
        subprocess.run([
            soffice,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', tempfile.gettempdir(),
            doc_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待转换完成
        time.sleep(2)
        
        if not os.path.exists(pdf_path):
            print(f"PDF生成失败: {pdf_path}")
            return 0
        
        # 使用pdfinfo获取页数
        try:
            result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Pages:' in line:
                    pages = int(line.split(':')[1].strip())
                    return pages
        except:
            # 如果pdfinfo不可用，尝试使用其他方法
            try:
                # 使用pdftk
                result = subprocess.run(['pdftk', pdf_path, 'dump_data'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'NumberOfPages:' in line:
                        pages = int(line.split(':')[1].strip())
                        return pages
            except:
                print("无法获取PDF页数，请安装poppler-utils或pdftk")
                return 0
        
        return 0
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return 0
    finally:
        # 清理临时PDF
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except:
                pass

# 统计每个文档的页数
for doc_file in doc_files:
    try:
        # 使用PDF方法获取准确页数
        page_count = get_pdf_page_count(doc_file)
        
        if page_count > 0:
            print(f"{os.path.basename(doc_file)}: {page_count} 页 (PDF方法)")
            total_pages += page_count
        else:
            print(f"{os.path.basename(doc_file)}: 无法获取页数")
    except Exception as e:
        print(f"{os.path.basename(doc_file)}: 处理失败 ({str(e)})")

print(f"\n统计完成！总页码数: {total_pages} 页")
