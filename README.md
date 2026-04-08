# SaveVault

[![Release](https://img.shields.io/github/v/release/1807781577/SaveVault?include_prereleases)](https://github.com/1807781577/SaveVault/releases)
[![Downloads](https://img.shields.io/github/downloads/1807781577/SaveVault/total)](https://github.com/1807781577/SaveVault/releases)
[![License](https://img.shields.io/github/license/1807781577/SaveVault)](LICENSE)

A simple and elegant tool for backing up and managing game saves on Windows. Perfect for gamers who want multiple save slots for games that don't natively support them.

**[⬇️ Download Latest Version](https://github.com/1807781577/SaveVault/releases/latest)**

[中文说明](#中文说明)

## Features

- **Multi-Game Support** - Manage saves for unlimited games
- **Auto-Detect Save Paths** - Automatically finds save locations from:
  - Built-in database of 25+ popular games
  - Game installation directory scanning
  - AppData/AppData.Local/AppData.LocalLow directories (supports `Publisher\Game` format)
  - Steam Cloud save directory
- **Easy Backup Management** - Create, restore, rename, and delete backups
- **Safety First** - Auto-backup current save before restore
- **Dark Theme UI** - Modern and clean interface
- **Portable EXE** - No installation required, just download and run

## Download & Installation

### Quick Start (Recommended)
1. Download `SaveVault.exe` from [Releases](https://github.com/1807781577/SaveVault/releases/latest)
2. Double-click to run
3. No Python or additional software needed

### Run from Source
```bash
git clone https://github.com/1807781577/SaveVault.git
cd SaveVault
python savevault.py
```

## Usage

### Adding a Game
1. Click "添加游戏" (Add Game)
2. Enter game name OR browse to game installation directory
3. Click "扫描存档" (Scan Saves) - paths will be auto-detected
4. Select the correct save path and confirm

### Creating a Backup
1. Select a game from the list
2. Click "创建备份" (Create Backup)
3. Enter a name for the backup

### Restoring a Backup
1. Select a game from the list
2. Select a backup to restore
3. Click "恢复" (Restore)
4. **Current save is auto-backed up** before restore

## Safety Features

| Feature | Description |
|---------|-------------|
| Auto-backup before restore | Automatically saves current game state before overwriting |
| Restore confirmation | Clear warning before any destructive operation |
| Local data only | No network requests, all data stays on your computer |

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
| ... and 15+ more | |

## Data Storage

- Configuration: `%USERPROFILE%/.savevault/games.json`
- Backups: `%USERPROFILE%/.savevault/backups/`

## Requirements

- Windows 10/11

## License

MIT License

---

## 中文说明

一个简单优雅的 Windows 游戏存档备份管理工具。适合那些想要多存档但游戏本身不支持的游戏。

**[⬇️ 下载最新版本](https://github.com/1807781577/SaveVault/releases/latest)**

### 功能特点

- **多游戏支持** - 管理无限数量的游戏存档
- **自动识别存档路径** - 智能扫描：
  - 内置 25+ 款热门游戏数据库
  - 游戏安装目录
  - AppData/LocalLow 目录（支持 `厂商\游戏名` 格式）
  - Steam 云存档
- **安全恢复** - 恢复前自动备份当前存档
- **深色主题** - 现代简洁的界面
- **绿色便携** - 下载即用，无需安装

### 快速开始

1. 下载 `SaveVault.exe`
2. 双击运行
3. 添加游戏 → 扫描存档 → 创建备份

### 安全特性

- ✅ 恢复前自动备份当前存档，防止误操作丢失
- ✅ 操作前确认提示
- ✅ 数据完全本地存储，不联网

### 常见游戏存档位置

| 游戏 | 存档位置 |
|-----|---------|
| 艾尔登法环 | %APPDATA%/EldenRing |
| 黑神话：悟空 | %LOCALAPPDATA%/b1/Saved/SaveGames |
| 博德之门3 | %LOCALAPPDATA%/Larian Studios/... |
| 赛博朋克2077 | %USERPROFILE%/Saved Games/CD Projekt Red/... |
| 怪物猎人：世界 | %USERPROFILE%/Documents/CAPCOM/MHW |
| GTA5 | %USERPROFILE%/Documents/Rockstar Games/GTA V |

### 注意事项

- 某些游戏需要在关闭状态下才能正确备份/恢复
- Steam 云存档可能需要在游戏设置中关闭
- 恢复操作会自动备份当前存档，可放心使用
