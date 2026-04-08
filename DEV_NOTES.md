# SaveVault - 开发笔记

## 项目信息
- **位置**: D:\game_save_manager
- **GitHub**: https://github.com/1807781577/SaveVault (私有)
- **EXE文件**: D:\game_save_manager\dist\SaveVault.exe
- **当前版本**: v1.2.1

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.2.1 | 修复 LocalLow 路径识别问题 |
| v1.2.0 | 添加中英文语言切换功能 |
| v1.1.1 | 中英双语 Release 说明 |
| v1.1.0 | 重命名为 SaveVault，恢复前自动备份 |
| v1.0.1 | 恢复前自动备份当前存档 |
| v1.0.0 | 首个正式版本 |

## 已完成功能

### 核心功能
1. 游戏存档备份/恢复/删除/重命名
2. 自动识别存档路径（支持多种方式）：
   - 内置数据库（25+款热门游戏）
   - 游戏安装目录扫描
   - AppData/Roaming、AppData/Local、AppData/LocalLow 扫描
   - 支持 `厂商\游戏名` 两层目录结构（如 Unity 游戏）
   - Steam 云存档检测
3. 深色主题 UI
4. 打包成独立 EXE 文件（无需安装 Python）

### 安全功能
- 恢复前自动备份当前存档，防止误操作丢失数据
- 自动备份命名为 `_auto_backup_before_restore_时间戳`
- 操作前确认提示

### 国际化
- 中英文语言切换（点击右上角「语言」按钮）
- 语言设置自动保存
- Issue 模板中英双语
- Release 说明中英双语

### 扫描覆盖范围
| 路径 | 说明 |
|------|------|
| AppData/Roaming | 常见游戏存档 |
| AppData/Local | 部分游戏 |
| AppData/LocalLow | Unity 游戏常用 |
| Documents/My Games | Xbox/微软游戏 |
| Saved Games | 部分大型游戏 |
| Steam/userdata | Steam 云存档 |

## 技术栈
- Python 3.14 + tkinter
- PyInstaller 打包

## 项目结构
```
D:\game_save_manager\
├── savevault.py           # 主程序源码
├── README.md              # 项目说明（中英双语）
├── build.bat              # 打包脚本
├── DEV_NOTES.md           # 开发笔记
├── .gitignore             # Git 忽略配置
├── .github\
│   └── ISSUE_TEMPLATE\    # Issue 模板（中英双语）
│       ├── bug_report.md
│       ├── feature_request.md
│       └── config.yml
└── dist\
    └── SaveVault.exe      # 打包后的 EXE
```

## 常用命令

### 运行程序
```bash
python D:\game_save_manager\savevault.py
```

### 打包 EXE
```bash
cd D:\game_save_manager
pyinstaller --onefile --windowed --name "SaveVault" savevault.py --clean -y
```

### Git 操作
```bash
cd D:\game_save_manager
git status
git add .
git commit -m "描述"
git push
```

### 发布 Release
```bash
gh release create v1.x.x "D:\game_save_manager\dist\SaveVault.exe" --title "v1.x.x" --notes "更新说明"
```

## 数据存储位置
- 配置文件: `%USERPROFILE%\.savevault\config.json`
- 游戏列表: `%USERPROFILE%\.savevault\games.json`（旧版本）
- 备份数据: `%USERPROFILE%\.savevault\backups\`

## 已修复的 Bug
- [x] LocalLow 路径识别错误（之前错误使用 `AppData/Local/Low`，现在正确使用 `AppData/LocalLow`）

## 已更新
- [x] README.md 添加详细使用指南（中英双语）
  - 英文部分：Features, Download & Installation, Usage Guide, Safety Features, Supported Games, Data Storage, Notes
  - 中文部分：功能特点、使用指南（详细操作步骤）、安全特性、常见游戏存档位置、注意事项、数据存储位置

## 待优化/待办
- [ ] 用户测试反馈
- [ ] 可能需要添加更多游戏到数据库
- [ ] 考虑添加备份备注功能
- [ ] 添加数字签名（避免 Windows SmartScreen 警告）

## 绿色便携特性
- 无需安装 Python 或任何运行时
- 双击 EXE 即可运行
- 可复制到任意位置（桌面、U盘）
- 数据完全本地存储，不联网

---

## 开发日志

### 2026-04-08

**项目创建**
- 创建游戏存档备份工具项目
- 实现基本功能：备份、恢复、删除、重命名
- 添加游戏存档路径自动识别功能

**UI 美化**
- 深色主题 UI
- 现代简洁的界面设计

**安全功能**
- 恢复前自动备份当前存档

**国际化**
- 添加中英文语言切换功能
- Issue 模板中英双语
- Release 说明中英双语

**项目重命名**
- 从 game-save-manager 重命名为 SaveVault

**Bug 修复**
- 修复 LocalLow 路径识别错误（AppData/Local/Low → AppData/LocalLow）

**文档完善**
- README.md 添加详细使用指南（中英双语）

---

**创建时间**: 2026-04-08  
**最后更新**: 2026-04-08

---

## 下次继续开发

只需告诉我：
- 项目位置：`D:\game_save_manager`
- GitHub：`https://github.com/1807781577/SaveVault`
- 想要做什么修改/优化

然后告诉我你想修改什么，我会根据项目代码继续帮你开发。
