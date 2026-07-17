#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GenshinMultiAccountTool 打包脚本（--onefile + Inno Setup staging）

- PyInstaller --onefile：所有 Python 代码、依赖、小资源嵌入单个 exe
- tesseract-ocr 因体积过大（114MB）保留为独立目录
- 只暴露 exe + tesseract-ocr + 配置文件 给用户
"""

import shutil, os, sys, subprocess, json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DIST_DIR = SCRIPT_DIR / "dist"          # PyInstaller onefile 输出
BUILD_DIR = SCRIPT_DIR / "build"        # PyInstaller 构建缓存
STAGING_DIR = SCRIPT_DIR / "dist_onedir" / "GenshinMultiAccountTool"  # Inno Setup staging
EXE_NAME = "GenshinMultiAccountTool"

def run(cmd_args):
    print(f"\n>>> {' '.join(cmd_args)}")
    subprocess.run(cmd_args, check=True)

def main():
    os.chdir(str(SCRIPT_DIR))

    # 清理旧构建产物
    for d in [DIST_DIR, BUILD_DIR, STAGING_DIR.parent]:
        if d.exists():
            try:
                shutil.rmtree(d)
                print(f"[信息] 清理: {d}")
            except PermissionError as e:
                print(f"[警告] 无法清理 {d}: {e}，跳过")

    # ==== 第一步：PyInstaller --onefile 打包 ====
    print("\n========== 第一步：PyInstaller --onefile ==========")
    run([sys.executable, "-m", "PyInstaller",
         "--onefile",
         "--noconsole",
         "--name", EXE_NAME,
         "--icon", "icon.ico",
         "--add-data", f"BetterGI-UID识别脚本;BetterGI-UID识别脚本",
         "--add-data", f"BetterGI-主界面检测脚本;BetterGI-主界面检测脚本",
         "--add-data", "logo.png;.",
         "--add-data", "icon.ico;.",
         "--distpath", str(DIST_DIR),
         "--workpath", str(BUILD_DIR),
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

    exe_path = DIST_DIR / f"{EXE_NAME}.exe"
    if not exe_path.is_file():
        print(f"[错误] 未找到输出文件: {exe_path}")
        sys.exit(1)

    print(f"\n[信息] --onefile 构建完成: {exe_path}")
    exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"[信息] exe 大小: {exe_size_mb:.1f} MB")

    # ==== 第二步：创建 Inno Setup staging 目录 ====
    print("\n========== 第二步：创建安装包 staging 目录 ==========")
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    # 2a. 复制 onefile exe
    shutil.copy2(exe_path, STAGING_DIR / f"{EXE_NAME}.exe")
    print(f"[信息] 复制 exe → staging")

    # 2b. 复制 tesseract-ocr（不嵌入 exe，太大 114MB）
    tess_src = SCRIPT_DIR / "tesseract-ocr"
    if tess_src.is_dir():
        tess_dest = STAGING_DIR / "tesseract-ocr"
        if tess_dest.exists():
            shutil.rmtree(tess_dest)
        shutil.copytree(tess_src, tess_dest)
        print(f"[信息] 复制: tesseract-ocr")
    else:
        print(f"[警告] 未找到 tesseract-ocr")

    # 2c. 创建空配置文件（首次安装用，不含任何用户数据）
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
    config_path = STAGING_DIR / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(empty_config, f, ensure_ascii=False, indent=2)
    print(f"[信息] 创建空配置: config.json")

    # 2d. 复制调度配置（首次安装用空模板）
    scheduler_config = {"schedules": []}
    sched_path = STAGING_DIR / "scheduler_config.json"
    with open(sched_path, "w", encoding="utf-8") as f:
        json.dump(scheduler_config, f, ensure_ascii=False, indent=2)
    print(f"[信息] 创建空调度配置: scheduler_config.json")

    print("\n" + "=" * 50)
    print(f"打包完成!")
    print(f"  onefile exe : {exe_path}")
    print(f"  staging 目录: {STAGING_DIR}")
    print(f"  → 下一步: ISCC.exe setup.iss")
    print("=" * 50)

if __name__ == "__main__":
    main()
