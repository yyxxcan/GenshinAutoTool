#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GenshinMultiAccountTool 单版本打包脚本"""

import shutil, os, sys, subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DIST_DIR = SCRIPT_DIR / "dist"
BUILD_DIR = SCRIPT_DIR / "build"
EXE_NAME = "GenshinMultiAccountTool"
ARCHIVE_NAME = "GenshinMultiAccountTool"
PACKAGE_DIR = DIST_DIR / ARCHIVE_NAME

def run(cmd_args):
    print(f"\n>>> {' '.join(cmd_args)}")
    subprocess.run(cmd_args, check=True)

def main():
    os.chdir(str(SCRIPT_DIR))

    # 清理旧构建产物（忽略被锁定的文件）
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            try:
                shutil.rmtree(d)
                print(f"[信息] 清理: {d}")
            except PermissionError as e:
                print(f"[警告] 无法清理 {d}: {e}，跳过")

    # 打包
    print("\n========== 打包 ==========")
    run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
         "--name", EXE_NAME,
         "--icon", "icon.ico",
         "--add-data", "icon.ico;.",
         "--collect-all", "pystray",
         "--hidden-import", "numpy",
         "--hidden-import", "psutil",
         "--hidden-import", "pyautogui",
         "--hidden-import", "pygetwindow",
         "--hidden-import", "pytesseract",
         "--hidden-import", "uiautomation",
         "--hidden-import", "PIL._imaging",
         "--hidden-import", "PIL._tkinter_finder",
         "--hidden-import", "PIL.Image",
         "--hidden-import", "PIL.ImageDraw",
         "--hidden-import", "websocket",
         "--hidden-import", "requests",
         "main.py"])

    exe_src = DIST_DIR / f"{EXE_NAME}.exe"
    if not exe_src.exists():
        print(f"[错误] 未找到输出文件: {exe_src}")
        sys.exit(1)

    # 创建发布目录
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(exe_src, PACKAGE_DIR / f"{EXE_NAME}.exe")
    print(f"[成功] 复制: {EXE_NAME}.exe")

    # 复制文档
    for doc in ["使用说明.md", "使用说明.txt"]:
        src = SCRIPT_DIR / doc
        if src.exists():
            shutil.copy2(src, PACKAGE_DIR / doc)
            print(f"[信息] 复制文档: {doc}")

    # 创建空配置文件（不含用户数据）
    import json as _json
    empty_config = {
        "accounts": [],
        "bettergi": {"exe": "", "config": ""},
        "snap_hutao": {"exe": "", "app_id": "E8B6E2B3-D2A0-4435-A81D-2A16AAF405C8_k3erpsn8bwzzy!App"},
        "genshin": {"exe": "", "process_name": "YuanShen.exe"},
        "monitor": {"max_wait_seconds": 7200},
        "tesseract": {"path": ""},
        "hotkeys": {"stop": "ctrl+shift+q", "pause": "ctrl+shift+p", "start": ""},
        "uid": {"method": "tesseract", "bettergi_group": ""},
        "settings": {
            "auto_minimize": True,
            "minimize_on_close": True,
            "auto_shutdown": False,
            "launch_apps_enabled": False,
            "launch_apps_after_all": [],
            "stop_closes_all_processes": True,
        },
    }
    config_path = PACKAGE_DIR / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        _json.dump(empty_config, f, ensure_ascii=False, indent=2)
    print(f"[信息] 创建空配置: config.json")

    # 创建空调度配置文件
    scheduler_config = {"schedules": []}
    sched_path = PACKAGE_DIR / "scheduler_config.json"
    with open(sched_path, "w", encoding="utf-8") as f:
        _json.dump(scheduler_config, f, ensure_ascii=False, indent=2)
    print(f"[信息] 创建空调度配置: scheduler_config.json")

    # 复制 Tesseract OCR 便携版
    tess = SCRIPT_DIR / "tesseract-ocr"
    if tess.is_dir():
        dest = PACKAGE_DIR / "tesseract-ocr"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(tess, dest)
        print(f"[信息] 复制: tesseract-ocr")
    else:
        print(f"[警告] 未找到 tesseract-ocr，请手动放置")

    # 检查并复制 BetterGI-UID识别脚本
    uid_script = SCRIPT_DIR / "BetterGI-UID识别脚本"
    if uid_script.is_dir():
        dest = PACKAGE_DIR / "BetterGI-UID识别脚本"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(uid_script, dest)
        print(f"[信息] 复制: BetterGI-UID识别脚本")
    elif uid_script.is_file():
        shutil.copy2(uid_script, PACKAGE_DIR / "BetterGI-UID识别脚本")
        print(f"[信息] 复制: BetterGI-UID识别脚本")

    # 复制 BetterGI-主界面检测脚本
    main_script = SCRIPT_DIR / "BetterGI-主界面检测脚本"
    if main_script.is_dir():
        dest = PACKAGE_DIR / "BetterGI-主界面检测脚本"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(main_script, dest)
        print(f"[信息] 复制: BetterGI-主界面检测脚本")

    # 打包 zip
    archive = DIST_DIR / ARCHIVE_NAME
    shutil.make_archive(str(archive), "zip", DIST_DIR, ARCHIVE_NAME)
    print(f"\n[成功] 压缩包: {archive}.zip")

    print("\n" + "=" * 50)
    print("打包完成!")
    print(f"  {PACKAGE_DIR}")
    print(f"  {archive}.zip")
    print("=" * 50)

if __name__ == "__main__":
    main()