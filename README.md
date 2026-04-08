# SaveVault

[![Release](https://img.shields.io/github/v/release/1807781577/SaveVault?include_prereleases)](https://github.com/1807781577/SaveVault/releases)
[![Downloads](https://img.shields.io/github/downloads/1807781577/SaveVault/total)](https://github.com/1807781577/SaveVault/releases)
[![License](https://img.shields.io/github/license/1807781577/SaveVault)](LICENSE)

A simple and elegant tool for backing up and managing game saves on Windows. Perfect for gamers who want multiple save slots for games that don't natively support them.

**[⬇️ Download Latest Version](https://github.com/1807781577/SaveVault/releases/latest)**

[中文说明](#中文说明)

---

## Features

- **Multi-Game Support** - Manage saves for unlimited games
- **Auto-Detect Save Paths** - Automatically finds save locations from:
  - Built-in database of 25+ popular games
  - Game installation directory scanning
  - AppData/AppData.Local/AppData.LocalLow directories
  - Steam Cloud save directory
- **Easy Backup Management** - Create, restore, rename, and delete backups
- **Safety First** - Auto-backup current save before restore
- **Language Toggle** - Chinese/English interface
- **Dark Theme UI** - Modern and clean interface
- **Portable EXE** - No installation required, just download and run

---

## Download & Installation

### Quick Start (Recommended)
1. Download `SaveVault.exe` from [Releases](https://github.com/1807781577/SaveVault/releases/latest)
2. Double-click to run
3. No Python or additional software needed

### System Requirements
- Windows 10/11

---

## Usage Guide

### Adding a Game

**Method 1: Auto-Scan**
1. Click "Add Game" / "添加游戏"
2. Enter game name (e.g., `Elden Ring`)
3. OR browse to game installation directory
4. Click "Scan Saves" / "扫描存档"
5. Select the correct save path from results
6. Click "OK" / "确定"

**Method 2: Manual Selection**
1. Click "Add Game" / "添加游戏"
2. Click "Browse Save Dir" / "浏览存档目录"
3. Select your save folder manually
4. Click "OK" / "确定"

### Creating a Backup

1. Select a game from the left panel
2. Click "Create Backup" / "创建备份"
3. Enter a name for the backup (e.g., `Chapter 1 Complete`)
4. Wait for completion

### Restoring a Backup

1. Select a game from the left panel
2. Select a backup from the right panel
3. Click "Restore" / "恢复"
4. Confirm the dialog
5. **Current save is auto-backed up** before restore
6. Wait for completion

### Other Features

| Button | Function |
|--------|----------|
| Delete / 删除 | Delete selected backup |
| Rename / 重命名 | Rename backup |
| Open Folder / 打开目录 | Open backup folder in Explorer |
| Language / 语言 | Toggle Chinese/English interface |

---

## Safety Features

| Feature | Description |
|---------|-------------|
| Auto-backup before restore | Automatically saves current game state before overwriting |
| Restore confirmation | Clear warning before any destructive operation |
| Local data only | No network requests, all data stays on your computer |

---

## Supported Games (Built-in Detection)

| Game | Save Location |
|------|---------------|
| Elden Ring | %APPDATA%/EldenRing |
| Black Myth: Wukong | %LOCALAPPDATA%/b1/Saved/SaveGames |
| Baldur's Gate 3 | %LOCALAPPDATA%/Larian Studios/... |
| Cyberpunk 2077 | %USERPROFILE%/Saved Games/CD Projekt Red/... |
| Monster Hunter: World | %USERPROFILE%/Documents/CAPCOM/MHW |
| GTA V | %USERPROFILE%/Documents/Rockstar Games/GTA V |
| Minecraft | %APPDATA%/.minecraft |
| Stardew Valley | %APPDATA%/StardewValley |
| Terraria | %USERPROFILE%/Documents/My Games/Terraria |
| Hollow Knight | %LOCALAPPDATA%/../LocalLow/Team Cherry/Hollow Knight |
| Hades | %USERPROFILE%/Documents/Hades |
| ... and more | |

---

## Data Storage

- Config: `%USERPROFILE%/.savevault/config.json`
- Backups: `%USERPROFILE%/.savevault/backups/`

---

## Notes

- Close the game before backup/restore for best results
- Steam Cloud saves may need to be disabled in game settings
- Restore operation auto-backs up current save, safe to use

---

## License

MIT License

---

## 中文说明

一个简单优雅的 Windows 游戏存档备份管理工具。适合那些想要多存档但游戏本身不支持的游戏。

**[⬇️ 下载最新版本](https://github.com/1807781577/SaveVault/releases/latest)**

---

### 功能特点

- **多游戏支持** - 管理无限数量的游戏存档
- **自动识别存档路径** - 智能扫描：
  - 内置 25+ 款热门游戏数据库
  - 游戏安装目录
  - AppData/LocalLow 目录（支持 `厂商\游戏名` 格式）
  - Steam 云存档
- **安全恢复** - 恢复前自动备份当前存档
- **中英文切换** - 点击右上角「语言」按钮
- **深色主题** - 现代简洁的界面
- **绿色便携** - 下载即用，无需安装

---

### 使用指南

#### 添加游戏

**方法一：自动扫描**
1. 点击「添加游戏」
2. 输入游戏名称（如 `艾尔登法环`）
3. 或选择游戏安装目录
4. 点击「扫描存档」
5. 从扫描结果中选择正确的存档路径
6. 点击「确定」

**方法二：手动选择**
1. 点击「添加游戏」
2. 点击「浏览存档目录」直接选择存档位置
3. 点击「确定」

#### 创建备份

1. 在左侧游戏列表中选择游戏
2. 点击右侧「创建备份」
3. 输入备份名称（如 `一周目通关`）
4. 等待完成

#### 恢复备份

1. 在左侧选择游戏
2. 在右侧备份列表中选择要恢复的备份
3. 点击「恢复」
4. 确认对话框点击「是」
5. **当前存档会自动备份**（防止误操作丢失）
6. 等待恢复完成

#### 其他功能

| 按钮 | 功能 |
|------|------|
| 删除 | 删除选中的备份 |
| 重命名 | 重命名备份 |
| 打开目录 | 打开备份文件夹 |
| 语言 | 切换中/英文界面 |

---

### 安全特性

- ✅ 恢复前自动备份当前存档，防止误操作丢失
- ✅ 操作前确认提示
- ✅ 数据完全本地存储，不联网

---

### 常见游戏存档位置

| 游戏 | 存档位置 |
|-----|---------|
| 艾尔登法环 | %APPDATA%/EldenRing |
| 黑神话：悟空 | %LOCALAPPDATA%/b1/Saved/SaveGames |
| 博德之门3 | %LOCALAPPDATA%/Larian Studios/... |
| 赛博朋克2077 | %USERPROFILE%/Saved Games/CD Projekt Red/... |
| 怪物猎人：世界 | %USERPROFILE%/Documents/CAPCOM/MHW |
| GTA5 | %USERPROFILE%/Documents/Rockstar Games/GTA V |
| 我的世界 | %APPDATA%/.minecraft |
| 泰拉瑞亚 | %USERPROFILE%/Documents/My Games/Terraria |
| 星露谷物语 | %APPDATA%/StardewValley |
| 空洞骑士 | %LOCALAPPDATA%/../LocalLow/Team Cherry/Hollow Knight |
| 哈迪斯 | %USERPROFILE%/Documents/Hades |

---

### 注意事项

- 建议在游戏关闭状态下进行备份/恢复
- Steam 云存档可能需要在游戏设置中关闭
- 恢复操作会自动备份当前存档，可放心使用
- 无需安装 Python 或任何运行时，双击 EXE 即可运行

---

### 数据存储位置

- 配置文件: `%USERPROFILE%\.savevault\config.json`
- 备份数据: `%USERPROFILE%\.savevault\backups\`

---

## License

MIT License
