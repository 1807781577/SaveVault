# Game Save Manager

A simple and elegant tool for backing up and managing game saves on Windows. Perfect for gamers who want multiple save slots for games that don't natively support them.

[中文说明](#中文说明)

## Features

- **Multi-Game Support** - Manage saves for unlimited games
- **Auto-Detect Save Paths** - Automatically finds save locations from:
  - Built-in database of 25+ popular games
  - Game installation directory scanning
  - AppData/AppData.Local/AppData.LocalLow directories
  - Steam Cloud save directory
- **Easy Backup Management** - Create, restore, rename, and delete backups
- **Dark Theme UI** - Modern and clean interface
- **Portable** - All data stored locally, no installation required

## Screenshots

Main Interface:
```
┌─────────────────────────────────────────────────────────────┐
│  Game Save Manager - 游戏存档备份管理工具                      │
├──────────────────────┬──────────────────────────────────────┤
│     游戏列表          │         存档备份                      │
│  ┌────────────────┐  │  当前存档: C:\Users\...\Save         │
│  │ 艾尔登法环      │  │  ┌─────────────────────────────────┐│
│  │ 黑神话：悟空    │  │  │ 备份名称    │ 创建时间   │ 大小  ││
│  │ 博德之门3      │  │  │ 一周目通关  │ 2024-01-15 │ 12MB ││
│  │ ...           │  │  │ 二周目开始  │ 2024-01-20 │ 15MB ││
│  └────────────────┘  │  └─────────────────────────────────┘│
│  [添加游戏] [删除]    │  [创建备份] [恢复] [删除] [重命名]   │
└──────────────────────┴──────────────────────────────────────┘
```

## Installation

### Option 1: Download Release (Recommended)
Download the latest `GameSaveManager.exe` from [Releases](../../releases)

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/game-save-manager.git
cd game-save-manager

# Run with Python
python game_save_manager.py
```

### Option 3: Build from Source
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GameSaveManager" game_save_manager.py
```

## Usage

### Adding a Game
1. Click "添加游戏" (Add Game)
2. Enter the game name OR select from the dropdown
3. Optionally, browse to the game's installation directory
4. Click "扫描存档" (Scan Saves) to auto-detect save locations
5. Select the correct save path from the results
6. Click "确定" (OK)

### Creating a Backup
1. Select a game from the list
2. Click "创建备份" (Create Backup)
3. Enter a name for the backup
4. Wait for the backup to complete

### Restoring a Backup
1. Select a game from the list
2. Select a backup from the list
3. Click "恢复" (Restore)
4. Confirm the restore (this will overwrite current save)

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
| ... and more | |

## Data Storage

- Configuration: `%USERPROFILE%/.game_save_manager/games.json`
- Backups: `%USERPROFILE%/.game_save_manager/backups/`

## Requirements

- Windows 10/11
- Python 3.7+ (if running from source)

## License

MIT License - feel free to use, modify, and distribute.

---

## 中文说明

一个简单优雅的 Windows 游戏存档备份管理工具。适合那些想要多存档但游戏本身不支持的游戏。

### 功能特点

- **多游戏支持** - 管理无限数量的游戏存档
- **自动识别存档路径** - 智能扫描以下位置：
  - 内置 25+ 款热门游戏的存档路径数据库
  - 游戏安装目录
  - AppData/AppData.Local/AppData.LocalLow 目录
  - Steam 云存档目录
- **备份管理** - 创建、恢复、重命名、删除备份
- **深色主题** - 现代简洁的界面
- **绿色便携** - 数据本地存储，无需安装

### 使用方法

1. **添加游戏** - 输入游戏名或从列表选择，点击扫描自动识别存档位置
2. **创建备份** - 选择游戏后点击创建备份，输入名称
3. **恢复存档** - 选择备份后点击恢复，当前存档会被覆盖

### 常见游戏存档位置

| 游戏 | 存档位置 |
|-----|---------|
| 艾尔登法环 | %APPDATA%/EldenRing |
| 黑神话：悟空 | %LOCALAPPDATA%/b1/Saved/SaveGames |
| 博德之门3 | %LOCALAPPDATA%/Larian Studios/... |
| 赛博朋克2077 | %USERPROFILE%/Saved Games/CD Projekt Red/... |
| 怪物猎人：世界 | %USERPROFILE%/Documents/CAPCOM/MHW |

### 自行编译

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "游戏存档备份工具" game_save_manager.py
```

### 注意事项

- 恢复存档会**覆盖**当前存档，请谨慎操作
- 某些游戏需要在关闭状态下才能正确备份/恢复
- Steam 云存档可能需要在游戏设置中关闭
