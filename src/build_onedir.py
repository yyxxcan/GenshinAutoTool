#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GenshinMultiAccountTool onedir 模式打包脚本（供 Inno Setup 封装用）"""

import shutil, os, sys, subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DIST_ONEDIR = SCRIPT_DIR / "dist_onedir"
BUILD_ONEDIR = SCRIPT_DIR / "build_onedir"
EXE_NAME = "GenshinMultiAccountTool"

def run(cmd_args):
    print(f"\n>>> {' '.join(cmd_args)}")
    subprocess.run(cmd_args, check=True)

def main():
    os.chdir(str(SCRIPT_DIR))

    # 清理旧 onedir 构建产物
    for d in [DIST_ONEDIR, BUILD_ONEDIR]:
        if d.exists():
            try:
                shutil.rmtree(d)
                print(f"[信息] 清理: {d}")
            except PermissionError as e:
                print(f"[警告] 无法清理 {d}: {e}，跳过")

    # ==== 第一步：PyInstaller onedir 打包 ====
    print("\n========== 第一步：PyInstaller onedir ==========")
    run([sys.executable, "-m", "PyInstaller",
         "--onedir",                          # 目录模式，非单文件
         "--noconsole",
         "--name", EXE_NAME,
         "--icon", "icon.ico",
         "--add-data", "icon.ico;.",
         "--distpath", str(DIST_ONEDIR),      # 输出到 dist_onedir
         "--workpath", str(BUILD_ONEDIR),     # 构建缓存到 build_onedir
         "--collect-all", "pystray",
         "--hidden-import", "numpy",
         "--hidden-import", "PIL._imaging",
         "--hidden-import", "PIL._tkinter_finder",
         "--hidden-import", "PIL.Image",
         "--hidden-import", "PIL.ImageDraw",
         "main.py"])

    exe_dir = DIST_ONEDIR / EXE_NAME
    if not exe_dir.is_dir():
        print(f"[错误] 未找到输出目录: {exe_dir}")
        sys.exit(1)

    # ==== 第二步：收集附加文件到发布目录 ====
    print("\n========== 第二步：收集附加文件 ==========")

    # 复制配置文件模板
    for f in ["config.json", "config_template.json", "scheduler_config.json",
              "requirements.txt"]:
        src = SCRIPT_DIR / f
        if src.exists():
            shutil.copy2(src, exe_dir / f)
            print(f"[信息] 复制: {f}")

    # 复制使用说明
    for doc in ["使用说明.md", "使用说明.txt"]:
        src = SCRIPT_DIR / doc
        if src.exists():
            shutil.copy2(src, exe_dir / doc)
            print(f"[信息] 复制: {doc}")

    # 复制 scheduler.py
    src = SCRIPT_DIR / "scheduler.py"
    if src.exists():
        shutil.copy2(src, exe_dir / "scheduler.py")
        print(f"[信息] 复制: scheduler.py")

    # 复制 Logo
    src = SCRIPT_DIR / "logo.png"
    if src.exists():
        shutil.copy2(src, exe_dir / "logo.png")
        print(f"[信息] 复制: logo.png")

    # 复制 Tesseract OCR
    tess = SCRIPT_DIR / "tesseract-ocr"
    if tess.is_dir():
        dest = exe_dir / "tesseract-ocr"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(tess, dest)
        print(f"[信息] 复制: tesseract-ocr")
    else:
        print(f"[警告] 未找到 tesseract-ocr，如需要 OCR 功能请手动放置")

    # 复制 BetterGI-UID识别脚本
    uid_script = SCRIPT_DIR / "BetterGI-UID识别脚本"
    if uid_script.is_dir():
        dest = exe_dir / "BetterGI-UID识别脚本"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(uid_script, dest)
        print(f"[信息] 复制: BetterGI-UID识别脚本")
    elif uid_script.is_file():
        shutil.copy2(uid_script, exe_dir / "BetterGI-UID识别脚本")
        print(f"[信息] 复制: BetterGI-UID识别脚本")

    print("\n" + "=" * 50)
    print(f"onedir 打包完成!")
    print(f"  {exe_dir}")
    print(f"  → 下一步: 用 Inno Setup 编译 setup.iss")
    print("=" * 50)

if __name__ == "__main__":
    main()
