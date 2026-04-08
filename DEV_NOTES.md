# Game Save Manager - 开发笔记

## 项目信息
- **位置**: D:\game_save_manager
- **GitHub**: https://github.com/1807781577/game-save-manager (私有)
- **EXE文件**: D:\game_save_manager\dist\GameSaveManager.exe

## 已完成功能
1. 游戏存档备份/恢复/删除/重命名
2. 自动识别存档路径（支持多种方式）：
   - 内置数据库（25+款热门游戏）
   - 游戏安装目录扫描
   - AppData/LocalLow 扫描（支持 厂商\游戏名 格式）
   - Steam 云存档检测
3. 深色主题 UI
4. 打包成 EXE 文件

## 技术栈
- Python 3.14 + tkinter
- PyInstaller 打包

## 常用命令

### 运行程序
```bash
python D:\game_save_manager\game_save_manager.py
```

### 打包 EXE
```bash
cd D:\game_save_manager
pyinstaller --onefile --windowed --name "GameSaveManager" game_save_manager.py --clean -y
```

### Git 操作
```bash
cd D:\game_save_manager
git status
git add .
git commit -m "描述"
git push
```

## 待优化/待办
- [ ] 用户测试反馈
- [ ] 可能需要添加更多游戏到数据库
- [ ] 考虑添加备份备注功能

## 数据存储位置
- 配置文件: `%USERPROFILE%\.game_save_manager\games.json`
- 备份数据: `%USERPROFILE%\.game_save_manager\backups\`

---
创建时间: 2026-04-08
