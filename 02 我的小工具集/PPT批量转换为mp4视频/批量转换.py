from moviepy import ImageSequenceClip
import os
import tempfile
import subprocess
from PIL import Image
import glob
import time

def ppt_to_pdf(ppt_path, pdf_path):
    """使用LibreOffice将PPT转换为PDF"""
    print(f"正在将PPT转换为PDF: {ppt_path}")
    
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
        return False
    
    # 使用LibreOffice转换为PDF
    try:
        cmd = [
            soffice,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_path),
            ppt_path
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 检查生成的PDF文件名（LibreOffice可能会修改文件名）
        expected_pdf = os.path.join(
            os.path.dirname(pdf_path),
            os.path.splitext(os.path.basename(ppt_path))[0] + '.pdf'
        )
        
        if os.path.exists(expected_pdf):
            # 如果文件名不匹配，重命名为期望的文件名
            if expected_pdf != pdf_path:
                os.rename(expected_pdf, pdf_path)
            
            print(f"PDF已成功生成: {pdf_path}")
            return True
        else:
            print(f"PDF生成失败，文件不存在: {expected_pdf}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"LibreOffice转换失败: {e}")
        return False
    except Exception as e:
        print(f"转换过程出错: {str(e)}")
        return False

def pdf_to_images(pdf_path, output_folder):
    """将PDF转换为图片序列"""
    print(f"正在将PDF转换为图片: {pdf_path}")
    
    # 使用macOS自带的sips命令将PDF转换为图片
    try:
        # 创建临时目录存放每一页的PDF
        temp_dir = os.path.join(output_folder, "temp_pdf_pages")
        os.makedirs(temp_dir, exist_ok=True)
        
        # 使用pdfseparate分割PDF页面（需要安装poppler）
        pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
        page_pattern = os.path.join(temp_dir, f"{pdf_basename}-%d.pdf")
        
        try:
            subprocess.run(['pdfseparate', pdf_path, page_pattern], check=True)
        except:
            print("pdfseparate命令失败，请确保已安装poppler: brew install poppler")
            return []
        
        # 获取所有PDF页面文件
        pdf_pages = glob.glob(os.path.join(temp_dir, "*.pdf"))
        
        # 按页码数字排序（而非字符串排序）
        pdf_pages.sort(key=lambda x: int(os.path.basename(x).split('-')[-1].split('.')[0]))
        
        # 将每一页PDF转换为PNG
        images = []
        for i, pdf_page in enumerate(pdf_pages):
            # 使用序号确保顺序正确
            output_image = os.path.join(output_folder, f"slide_{str(i+1).zfill(3)}.png")
            
            # 使用sips转换
            subprocess.run(['sips', '-s', 'format', 'png', pdf_page, '--out', output_image], check=True)
            
            if os.path.exists(output_image):
                images.append(output_image)
        
        # 清理临时文件
        for f in glob.glob(os.path.join(temp_dir, "*.pdf")):
            os.remove(f)
        os.rmdir(temp_dir)
        
        # 确保按数字顺序排序
        images.sort(key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))
        
        return images
    except Exception as e:
        print(f"PDF转图片失败: {str(e)}")
        return []

def ppt_to_images(ppt_path, output_folder):
    """将PPT转换为图片（通过LibreOffice和PDF）"""
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取PPT文件名（不含扩展名）
    ppt_name = os.path.splitext(os.path.basename(ppt_path))[0]
    
    # 设置PDF路径
    pdf_path = os.path.join(tempfile.gettempdir(), f"{ppt_name}.pdf")
    
    try:
        # 第一步：将PPT转换为PDF
        if not ppt_to_pdf(ppt_path, pdf_path):
            print("PPT转PDF失败")
            return []
        
        # 第二步：将PDF转换为图片
        images = pdf_to_images(pdf_path, output_folder)
        
        # 检查图片数量
        if len(images) < 1:
            print("生成的图片数量为0，请检查PPT文件内容")
            return []
            
        print(f"成功生成 {len(images)} 张图片")
        return images
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return []
    finally:
        # 清理临时PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

def convert_ppt_to_video(ppt_path, video_path, temp_folder):
    """将单个PPT文件转换为视频"""
    print(f"\n开始处理: {os.path.basename(ppt_path)}")
    
    # 创建临时文件夹
    ppt_temp_folder = os.path.join(temp_folder, os.path.splitext(os.path.basename(ppt_path))[0])
    os.makedirs(ppt_temp_folder, exist_ok=True)
    
    # 转换PPT为图片
    images = ppt_to_images(ppt_path, ppt_temp_folder)
    
    if not images:
        print(f"无法生成图片，跳过: {ppt_path}")
        return False
    
    # 生成视频
    try:
        print(f"正在生成视频，共 {len(images)} 帧...")
        clip = ImageSequenceClip(images, fps=0.5)  # 降低帧率，每页显示2秒
        clip.write_videofile(video_path, codec='libx264')
        print(f"转换完成，视频已保存至：{video_path}")
        
        # 清理临时文件
        for img in images:
            if os.path.exists(img):
                os.remove(img)
        
        # 尝试删除临时文件夹
        try:
            os.rmdir(ppt_temp_folder)
        except:
            pass
            
        return True
    except Exception as e:
        print(f"视频生成失败: {str(e)}")
        return False

# 文件路径配置
ppt_folder = "/Users/harmnet/Desktop/PPT"  # PPT文件夹路径
video_folder = "/Users/harmnet/Desktop/PPT视频"  # 视频输出文件夹
temp_folder = "/Users/harmnet/Desktop/PPT_Images_Temp"  # 临时文件夹

# 创建输出目录
os.makedirs(video_folder, exist_ok=True)
os.makedirs(temp_folder, exist_ok=True)

# 获取所有PPT文件
ppt_files = glob.glob(os.path.join(ppt_folder, "*.pptx"))

if not ppt_files:
    print(f"在 {ppt_folder} 中未找到任何.pptx文件")
    exit(1)

print(f"找到 {len(ppt_files)} 个PPT文件，开始批量转换...")

# 批量处理所有PPT文件
success_count = 0
for i, ppt_file in enumerate(ppt_files):
    print(f"\n[{i+1}/{len(ppt_files)}] 处理文件: {os.path.basename(ppt_file)}")
    
    # 生成视频文件路径
    video_filename = os.path.splitext(os.path.basename(ppt_file))[0] + ".mp4"
    video_path = os.path.join(video_folder, video_filename)
    
    # 如果视频已存在，跳过处理
    if os.path.exists(video_path):
        print(f"视频文件已存在: {video_filename}，跳过处理")
        continue
    
    # 转换PPT为视频
    if convert_ppt_to_video(ppt_file, video_path, temp_folder):
        success_count += 1

# 打印总结
print(f"\n批量转换完成！成功转换 {success_count}/{len(ppt_files)} 个文件")
print(f"视频文件保存在: {video_folder}")

# 清理主临时文件夹（如果为空）
try:
    os.rmdir(temp_folder)
except:
    pass






