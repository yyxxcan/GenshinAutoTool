# 原神多账号辅助工具 v5.4

自动切换多个原神账号，逐号调用 BetterGI 完成每日委托、清体力等自动化操作。

## 依赖

- **BetterGI** — 游戏内自动化执行（请自行搜索下载，配置一条龙任务）
- **原神** — 窗口化运行
- **胡桃工具箱**（可选）— 仅切号功能需要（请自行搜索下载）
- **Tesseract OCR** — 压缩包已自带，无需安装

## 部署

解压 `GenshinMultiAccountTool.zip` 到任意目录（路径不要含中文或空格）。确保 `tesseract-ocr/` 文件夹与 `GenshinMultiAccountTool.exe` 同级。

## 配置要点

首次运行后点「设置」，必填项：

| 配置项 | 说明 |
|--------|------|
| BetterGI 可执行文件 | 选择 `BetterGI.exe` |
| BetterGI 配置文件 | 选择 BetterGI 的 `User/config.json` |
| 原神可执行文件 | 选择 `YuanShen.exe`（国际服选 `GenshinImpact.exe`） |
| Tesseract OCR 目录 | 指向自带的 `tesseract-ocr/` 文件夹 |

其余项按需调整。`config.json` 由程序自动管理，不要手动编辑。

## config.json 配置项详解

配置文件位于程序同级目录。运行时自动生成默认值，无需手动创建。本节列出所有字段含义，供查阅。

### bettergi

| 字段 | 含义 | 示例值 |
|------|------|--------|
| `exe` | BetterGI 主程序路径 | `D:\BetterGI\BetterGI.exe` |
| `config` | BetterGI 的 User 配置文件路径 | `D:\BetterGI\User\config.json` |

### snap_hutao

| 字段 | 含义 | 示例值 |
|------|------|--------|
| `exe` | 胡桃工具箱主程序路径 | `D:\Hutao\Snap.Hutao.exe` |
| `app_id` | 胡桃 MSIX 应用 ID（固定值，无需修改） | `E8B6E2B3-...` |

### genshin

| 字段 | 含义 | 示例值 |
|------|------|--------|
| `exe` | 原神主程序路径 | `D:\Genshin Impact\YuanShen.exe` |
| `process_name` | 游戏进程名 | `YuanShen.exe`（国际服 `GenshinImpact.exe`） |

### monitor

| 字段 | 含义 | 默认值 |
|------|------|--------|
| `max_wait_seconds` | BetterGI 一条龙最大等待时长（秒） | `7200`（2 小时） |

### tesseract

| 字段 | 含义 | 默认值 |
|------|------|--------|
| `path` | Tesseract OCR 目录路径 | 空字符串（未配置） |

### hotkeys

| 字段 | 含义 | 默认值 |
|------|------|--------|
| `stop` | 全局停止快捷键 | `ctrl+shift+q` |
| `pause` | 全局暂停/继续快捷键 | `ctrl+shift+p` |

### uid

| 字段 | 含义 | 可选值 | 默认值 |
|------|------|--------|--------|
| `method` | UID 识别方式 | `tesseract` / `bettergi` | `tesseract` |
| `bettergi_group` | BetterGI 配置组名（method=bettergi 时生效） | 任意组名 | 空字符串 |

### settings

| 字段 | 含义 | 默认值 |
|------|------|--------|
| `auto_minimize` | 启动定时器后自动最小化到托盘 | `true` |
| `minimize_on_close` | 关闭窗口时最小化到托盘（而非退出） | `true` |
| `auto_shutdown` | 全部账号完成后自动关机 | `false` |

### accounts

账号数组，每项字段：

| 字段 | 含义 | 可选值 |
|------|------|--------|
| `name` | 账号显示名称 | 任意字符串 |
| `launch_method` | 启动方式 | `direct` / `hutao` |
| `config_name` | BetterGI 一条龙配置名 | BetterGI User 目录下配置文件名（不含 `.json`） |
| `uid` | 游戏 UID | 9 位数字字符串 |
| `enabled` | 是否勾选（批量执行时生效） | `true` / `false` |

### 定时计划 (scheduler_config.json)

独立文件，存储计划任务数组，每项字段：

| 字段 | 含义 | 可选值 |
|------|------|--------|
| `name` | 任务名称 | 任意字符串 |
| `type` | 触发类型 | `daily` / `weekly` / `once` / `date` |
| `time` | 触发时间 | `HH:MM` 格式（如 `08:00`） |
| `weekdays` | 每周哪几天（type=weekly 时生效） | `[0,1,...,6]`（0=周一） |
| `date` | 指定日期（type=date 时生效） | `YYYY-MM-DD` |
| `enabled` | 是否启用 | `true` / `false` |

## 账号管理

「+ 添加账号」→ 填写名称、启动方式（直接启动/胡桃启动）、BetterGI 一条龙配置名、游戏 UID。勾选后「开始」即逐号执行。

## 核心功能

- **快捷键**：全局停止 `Ctrl+Shift+Q` / 暂停继续 `Ctrl+Shift+P`（可在设置中自定义）
- **定时计划**：支持每天/每周/一次性/指定日期，到点自动触发一条龙。「一键启动全部」一次性启用所有定时任务
- **系统托盘**：关闭窗口最小化到托盘，右键菜单可控制开始/暂停/停止/定时器
- **开机自启**：勾选后注册表写入，重启自动运行
- **自动关机**：全部账号完成后 60 秒倒计时关机（可取消）

## 注意事项

- 游戏必须窗口化，全屏无法识别 UID
- 一条龙执行期间不要动鼠标键盘
- 首次使用只勾一个号试运行
- 电脑不要休眠/睡眠，否则定时任务无法触发
- `tesseract-ocr/` 必须和 exe 同级

## 常见问题

### Tesseract OCR 识别失败或报错"找不到 tesseract"

**原因**：`tesseract-ocr/` 未与 exe 同级，或目录结构不完整。

**解决**：
1. 确认 exe 同级有 `tesseract-ocr/` 文件夹，内含 `tesseract.exe`
2. 在设置中重新选择 Tesseract OCR 目录
3. 若仍无法使用，在设置中将「UID 识别方式」改为 `bettergi`，由 BetterGI 内部完成 UID 读取（无需 tesseract）

### 提示"程序已在运行中"

**原因**：工具已有一个实例在运行（通过文件锁防重复启动）。

**解决**：检查系统托盘是否已有工具图标，双击打开；或通过任务管理器结束旧进程。

### 检测不到游戏窗口 / 账号登录失败

**原因**：游戏进程未启动、窗口标题异常、或游戏处于全屏。

**解决**：
1. 确认游戏为**窗口化**模式（全屏无法操作）
2. 确认 `genshin.process_name` 与实际进程名一致（国际服为 `GenshinImpact.exe`）
3. 首次使用只勾一个号测试，日志窗口可看到详细错误信息

### 托盘图标不显示

**原因**：Windows 可能隐藏了托盘图标，或旧实例残留僵尸图标影响新实例。

**解决**：
1. 展开系统托盘折叠区（点击任务栏 `^` 箭头），检查图标是否在其中
2. 若仍无，在任务管理器中结束所有 `GenshinMultiAccountTool.exe` 进程后重开
3. 若旧图标残留（不可点击），工具启动时已自动触发托盘刷新；如无效，重启 Windows 资源管理器

### 定时任务到点不执行

**原因**：定时器未启动、电脑休眠、或任务 `enabled` 为 `false`。

**解决**：
1. 确认定时计划窗口中「定时器」状态为「运行中」，任务列表勾选项已启用
2. 电脑**不能休眠/睡眠**，否则定时器线程挂起
3. 若到点未触发，检查系统时间是否正确，手动点「一键启动全部」看是否能正常执行一次性任务
4. 若需要电脑无人值守运行，搭配「开机自启」+ 电源选项「永不睡眠」
