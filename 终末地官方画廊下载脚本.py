import subprocess
import sys
import importlib.util

# 需要检测的库列表
REQUIRED_PACKAGES = ['requests']

def check_and_install_packages():
    """检查并安装必要的Python包"""
    print("=" * 60)
    print("检查依赖库...")
    print("=" * 60)
    
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        # 检查包是否已安装
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
            print(f"❌ 未找到: {package}")
        else:
            print(f"✅ 已安装: {package}")
    
    if missing_packages:
        print(f"\n发现 {len(missing_packages)} 个缺失的依赖库")
        print("-" * 40)
        
        # 询问用户是否安装
        choice = input(f"是否自动安装缺失的库 {', '.join(missing_packages)}？(y/n，默认y): ").strip().lower()
        
        if choice != 'n':
            print("\n开始安装依赖库...")
            for package in missing_packages:
                print(f"正在安装 {package}...")
                try:
                    # 使用pip安装包
                    cmd = [sys.executable, "-m", "pip", "install", package]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"✅ {package} 安装成功！")
                    else:
                        print(f"❌ {package} 安装失败")
                        print(f"错误信息: {result.stderr}")
                        print(f"\n你可以手动安装: {sys.executable} -m pip install {package}")
                        return False
                except Exception as e:
                    print(f"❌ 安装 {package} 时出错: {str(e)}")
                    return False
            
            # 重新导入已安装的库
            print("\n重新加载依赖库...")
            for package in missing_packages:
                try:
                    importlib.import_module(package)
                    print(f"✅ {package} 加载成功")
                except ImportError as e:
                    print(f"❌ {package} 加载失败: {str(e)}")
                    return False
            
            print("\n✅ 所有依赖库安装完成！")
            return True
        else:
            print("用户取消安装，程序退出")
            return False
    else:
        print("\n✅ 所有依赖库已就绪")
        return True

def show_manual_install_commands():
    """显示手动安装命令"""
    print("\n" + "=" * 60)
    print("手动安装命令")
    print("=" * 60)
    print("\n如果自动安装失败，请按以下方法手动安装：")
    print("\n方法1：使用pip直接安装")
    for package in REQUIRED_PACKAGES:
        print(f"  pip install {package}")
    
    print("\n方法2：使用Python模块方式")
    for package in REQUIRED_PACKAGES:
        print(f"  {sys.executable} -m pip install {package}")
    
    print("\n方法3：使用镜像源（国内用户推荐）")
    for package in REQUIRED_PACKAGES:
        print(f"  pip install {package} -i https://pypi.tuna.tsinghua.edu.cn/simple")
    
    print("\n方法4：升级pip后再安装")
    print(f"  {sys.executable} -m pip install --upgrade pip")
    for package in REQUIRED_PACKAGES:
        print(f"  pip install {package}")

# 导入必要的库（如果已安装）
def safe_imports():
    """安全导入必要的库"""
    global re, requests, os, urlparse, time
    
    try:
        import re
        print("✅ 导入 re 成功")
    except ImportError:
        print("❌ 导入 re 失败（这是Python内置库，不应该失败）")
        return False
    
    try:
        import requests
        print("✅ 导入 requests 成功")
    except ImportError:
        print("❌ 导入 requests 失败")
        return False
    
    try:
        import os
        print("✅ 导入 os 成功")
    except ImportError:
        print("❌ 导入 os 失败（这是Python内置库，不应该失败）")
        return False
    
    try:
        from urllib.parse import urlparse
        print("✅ 导入 urlparse 成功")
    except ImportError:
        print("❌ 导入 urlparse 失败（这是Python内置库，不应该失败）")
        return False
    
    try:
        import time
        print("✅ 导入 time 成功")
    except ImportError:
        print("❌ 导入 time 失败（这是Python内置库，不应该失败）")
        return False
    
    return True

# 主程序入口修改
def main():
    print("=" * 60)
    print("图片链接提取与下载工具")
    print("=" * 60)
    print(f"从pic.txt文件中提取所有以https开头、以后引号结尾的链接")
    print(f"比如： \"https://web.hycdn.cn/endfield/special/over-the-frontier/assets/imgs/0201.5fe42f.jpg\"")
    
    # 第一步：检查并安装依赖
    if not check_and_install_packages():
        print("\n❌ 依赖库安装失败或用户取消")
        show_manual_install_commands()
        input("\n按回车键退出...")
        return
    
    # 第二步：导入所有库
    print("\n" + "=" * 60)
    print("导入依赖库...")
    print("=" * 60)
    
    if not safe_imports():
        print("\n❌ 库导入失败，请检查安装")
        show_manual_install_commands()
        input("\n按回车键退出...")
        return
    
    # 原有的main函数代码
    original_main()

def original_main():
    """原有的main函数代码"""
    # 设置文件路径
    filename = 'pic.txt'  # 如果你的文件在其他位置，修改这里
    
    print("\n" + "=" * 60)
    print("开始处理文件")
    print("=" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"错误：找不到文件 '{filename}'")
        print("\n请选择：")
        print("1. 将 pic.txt 放在当前目录")
        print("2. 输入文件的完整路径")
        
        choice = input("\n请选择 (1或2，默认1): ").strip()
        if choice == '2':
            filename = input("请输入pic.txt的完整路径: ").strip()
            if not os.path.exists(filename):
                print("文件不存在，程序退出")
                return
        else:
            print("请先将pic.txt文件复制到当前目录")
            print(f"当前目录: {os.getcwd()}")
            return
    
    # 提取链接
    print(f"\n正在从 {filename} 提取图片链接...")
    urls = extract_urls_from_file(filename)
    
    if not urls:
        print("没有找到任何图片链接！")
        print("\n可能的原因：")
        print("1. 文件格式与预期不符")
        print("2. 文件中确实没有图片链接")
        print("3. 编码问题")
        
        # 显示文件开头部分供检查
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                preview = f.read(500)
            print("\n文件开头500字符：")
            print("-" * 40)
            print(preview)
            print("-" * 40)
        except:
            pass
        return
    
    # 显示前几个链接
    print("\n找到的图片链接（前5个）：")
    for i, url in enumerate(urls[:5]):
        print(f"  {i+1}. {url}")
    if len(urls) > 5:
        print(f"  ... 共 {len(urls)} 个链接")
    
    # 询问是否下载
    print()
    choice = input(f"是否下载这 {len(urls)} 张图片到 'pic' 文件夹？(y/n，默认y): ").strip().lower()
    if choice == 'n':
        print("已取消下载")
        return
    
    # 下载图片
    download_images(urls)

# 原来的extract_urls_from_file和download_images函数保持不变
def extract_urls_from_file(filename):
    """从文件中提取所有以https开头、以引号结尾的链接"""
    urls = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"文件读取成功，总长度：{len(content)} 字符")
        
        # 方法1：直接搜索所有以 https 开头的内容
        start_idx = 0
        while True:
            # 查找 "https"
            start_idx = content.find('https', start_idx)
            if start_idx == -1:
                break
            
            # 找到链接结束位置（下一个引号）
            end_idx = content.find('"', start_idx)
            if end_idx == -1:
                end_idx = content.find("'", start_idx)
            if end_idx == -1:
                end_idx = content.find('}', start_idx)
            if end_idx == -1:
                end_idx = content.find(']', start_idx)
            if end_idx == -1:
                end_idx = content.find(',', start_idx)
            
            if end_idx != -1:
                url = content[start_idx:end_idx].strip()
                # 清理可能的结尾符号
                url = url.rstrip('"').rstrip("'").rstrip('}').rstrip(']').rstrip(',')
                
                # 检查是否是图片链接
                if url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    urls.append(url)
                    print(f"找到图片: {url}")
                else:
                    print(f"跳过非图片: {url}")
            
            start_idx = end_idx if end_idx != -1 else start_idx + 5
        
        # 方法2：使用正则表达式（作为备用）
        if len(urls) == 0:
            print("方法1未找到链接，尝试正则表达式...")
            # 更宽松的正则表达式
            pattern = r'https?://[^"\'\}\],\s]+\.(?:jpg|jpeg|png|gif|webp)'
            urls = re.findall(pattern, content, re.IGNORECASE)
            
        # 去重
        urls = list(dict.fromkeys(urls))
        
        print(f"\n总共找到 {len(urls)} 个图片链接")
        return urls
        
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        print(f"从文件中提取所有以https开头、以后引号结尾的链接")
        print(f"比如： \"https://web.hycdn.cn/endfield/special/over-the-frontier/assets/imgs/0201.5fe42f.jpg\"")
        return []
    except Exception as e:
        print(f"读取文件时出错：{str(e)}")
        return []

def download_images(urls, save_dir='pic'):
    """下载图片到指定文件夹"""
    if not urls:
        print("没有链接可下载")
        return
    
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"创建文件夹: {save_dir}")
    
    print(f"\n开始下载 {len(urls)} 张图片到 {save_dir} 文件夹...")
    print("-" * 50)
    
    success_count = 0
    fail_count = 0
    
    for i, url in enumerate(urls):
        try:
            # 从URL中提取文件名
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # 如果文件名无效，生成一个
            if not filename:
                ext = url.split('.')[-1].split('?')[0] if '.' in url else 'jpg'
                filename = f'image_{i+1:04d}.{ext}'
            
            filepath = os.path.join(save_dir, filename)
            
            # 如果文件已存在，跳过
            if os.path.exists(filepath):
                print(f"⏭️  [{i+1}/{len(urls)}] {filename} 已存在")
                success_count += 1
                continue
            
            # 下载图片
            print(f"⬇️  [{i+1}/{len(urls)}] 下载: {filename}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content) / 1024  # KB
            print(f"✅ 已保存: {filename} ({file_size:.1f}KB)")
            success_count += 1
            
            # 稍微停顿，避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ 下载失败 {url[:50]}...: {str(e)[:50]}")
            fail_count += 1
    
    print("-" * 50)
    print(f"下载完成！成功: {success_count} 张，失败: {fail_count} 张")
    print(f"图片保存在: {os.path.abspath(save_dir)}")

if __name__ == '__main__':
    main()