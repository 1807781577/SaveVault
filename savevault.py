#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaveVault - Game Save Manager
Supports multi-game, multi-save management with auto-detection
"""

import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
from pathlib import Path
import winreg

# ==================== 语言包 / Language Packs ====================

LANGUAGES = {
    "zh": {
        # 标题 / Titles
        "app_title": "SaveVault",
        "game_list": "游戏列表",
        "save_backup": "存档备份",
        "add_game": "添加游戏",
        
        # 按钮 / Buttons
        "add": "添加游戏",
        "delete": "删除",
        "edit_path": "编辑路径",
        "create_backup": "创建备份",
        "restore": "恢复",
        "rename": "重命名",
        "open_dir": "打开目录",
        "scan": "扫描存档",
        "db_detect": "数据库检测",
        "browse": "浏览",
        "browse_save": "浏览存档目录",
        "confirm": "确定",
        "cancel": "取消",
        
        # 标签 / Labels
        "game_name": "游戏名称:",
        "game_dir": "游戏目录:",
        "save_path": "存档路径:",
        "current_save": "当前存档:",
        "select_game": "请选择游戏",
        "scan_result": "扫描结果:",
        
        # 表头 / Table Headers
        "backup_name": "备份名称",
        "create_time": "创建时间",
        "size": "大小",
        
        # 消息 / Messages
        "select_game_first": "请先选择一个游戏",
        "select_backup_first": "请先选择一个备份",
        "enter_game_name": "请输入游戏名称",
        "select_save_path": "请选择存档路径",
        "game_exists": "游戏已存在",
        "save_path_not_exist": "存档路径不存在",
        "backup_created": "备份创建成功",
        "backup_failed": "备份失败",
        "restore_success": "存档恢复成功！\n\n当前存档已自动备份",
        "restore_failed": "恢复失败",
        "delete_success": "备份已删除",
        "delete_failed": "删除失败",
        "rename_success": "重命名成功",
        "rename_failed": "重命名失败",
        "path_updated": "路径已更新",
        "game_added": "已添加游戏",
        
        # 确认对话框 / Confirm Dialogs
        "confirm_delete_game": "确定要删除游戏 '{}' 吗？\n（备份文件不会被删除）",
        "confirm_restore": "确定恢复到 '{}' 吗？\n\n当前存档将被覆盖！\n（恢复前会自动备份当前存档）",
        "confirm_delete_backup": "确定删除备份 '{}' 吗？",
        "auto_backup_failed": "恢复前自动备份失败：{}\n\n是否仍要继续恢复？",
        
        # 对话框 / Dialogs
        "add_game_title": "添加游戏",
        "create_backup_title": "创建备份",
        "enter_backup_name": "请输入备份名称:",
        "rename_title": "重命名",
        "new_name": "新名称:",
        
        # 状态 / Status
        "scanning": "正在扫描...",
        "found_paths": "找到 {} 个可能的存档目录",
        "not_found": "未找到存档，请手动选择",
        "db_found": "已从数据库检测",
        "db_not_found": "数据库中未找到",
        "scan_hint": "选择游戏目录或输入名称后点击扫描",
        "games_count": "已添加 {} 款游戏 | 数据目录: {}",
        
        # 其他 / Others
        "language": "语言",
        "chinese": "中文",
        "english": "English",

        # 清空进度 / Clear Progress
        "clear_progress": "清空进度",
        "confirm_clear_progress": "确定清空「{}」的全部进度吗？\n\n此操作将删除当前存档的所有内容！\n（删除前会自动备份当前存档）",
        "clear_success": "进度已清空！\n\n当前存档已自动备份",
        "clear_failed": "清空失败",
        "clear_no_save": "存档目录不存在或为空",
    },
    "en": {
        # Titles
        "app_title": "SaveVault",
        "game_list": "Game List",
        "save_backup": "Save Backups",
        "add_game": "Add Game",
        
        # Buttons
        "add": "Add Game",
        "delete": "Delete",
        "edit_path": "Edit Path",
        "create_backup": "Create Backup",
        "restore": "Restore",
        "rename": "Rename",
        "open_dir": "Open Folder",
        "scan": "Scan Saves",
        "db_detect": "DB Detect",
        "browse": "Browse",
        "browse_save": "Browse Save Dir",
        "confirm": "OK",
        "cancel": "Cancel",
        
        # Labels
        "game_name": "Game Name:",
        "game_dir": "Game Directory:",
        "save_path": "Save Path:",
        "current_save": "Current Save:",
        "select_game": "Select a game",
        "scan_result": "Scan Results:",
        
        # Table Headers
        "backup_name": "Backup Name",
        "create_time": "Created",
        "size": "Size",
        
        # Messages
        "select_game_first": "Please select a game first",
        "select_backup_first": "Please select a backup first",
        "enter_game_name": "Please enter game name",
        "select_save_path": "Please select save path",
        "game_exists": "Game already exists",
        "save_path_not_exist": "Save path does not exist",
        "backup_created": "Backup created successfully",
        "backup_failed": "Backup failed",
        "restore_success": "Save restored successfully!\n\nCurrent save has been auto-backed up",
        "restore_failed": "Restore failed",
        "delete_success": "Backup deleted",
        "delete_failed": "Delete failed",
        "rename_success": "Renamed successfully",
        "rename_failed": "Rename failed",
        "path_updated": "Path updated",
        "game_added": "Game added",
        
        # Confirm Dialogs
        "confirm_delete_game": "Delete game '{}'?\n(Backup files will not be deleted)",
        "confirm_restore": "Restore to '{}'?\n\nCurrent save will be overwritten!\n(Current save will be auto-backed up)",
        "confirm_delete_backup": "Delete backup '{}'?",
        "auto_backup_failed": "Auto-backup failed: {}\n\nContinue with restore?",
        
        # Dialogs
        "add_game_title": "Add Game",
        "create_backup_title": "Create Backup",
        "enter_backup_name": "Enter backup name:",
        "rename_title": "Rename",
        "new_name": "New name:",
        
        # Status
        "scanning": "Scanning...",
        "found_paths": "Found {} possible save directories",
        "not_found": "No saves found, please select manually",
        "db_found": "Found in database",
        "db_not_found": "Not found in database",
        "scan_hint": "Select game directory or enter name, then click Scan",
        "games_count": "{} games added | Data: {}",
        
        # Others
        "language": "Language",
        "chinese": "中文",
        "english": "English",

        # Clear Progress
        "clear_progress": "Clear Progress",
        "confirm_clear_progress": "Clear all progress for '{}'?\n\nThis will delete all current save data!\n(Current save will be auto-backed up)",
        "clear_success": "Progress cleared!\n\nCurrent save has been auto-backed up",
        "clear_failed": "Clear failed",
        "clear_no_save": "Save directory does not exist or is empty",
    }
}

# ==================== 游戏数据库 / Game Database ====================

GAME_SAVE_PATHS = {
    "艾尔登法环": ["{APPDATA}/EldenRing"],
    "Elden Ring": ["{APPDATA}/EldenRing"],
    "只狼": ["{APPDATA}/Sekiro"],
    "Sekiro": ["{APPDATA}/Sekiro"],
    "黑暗之魂3": ["{APPDATA}/DarkSoulsIII"],
    "Dark Souls 3": ["{APPDATA}/DarkSoulsIII"],
    "赛博朋克2077": ["{SAVEDGAMES}/CD Projekt Red/Cyberpunk 2077"],
    "Cyberpunk 2077": ["{SAVEDGAMES}/CD Projekt Red/Cyberpunk 2077"],
    "巫师3": ["{SAVEDGAMES}/CD Projekt Red/The Witcher 3"],
    "The Witcher 3": ["{SAVEDGAMES}/CD Projekt Red/The Witcher 3"],
    "博德之门3": ["{LOCALAPPDATA}/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/Savegames"],
    "Baldur's Gate 3": ["{LOCALAPPDATA}/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/Savegames"],
    "霍格沃茨之遗": ["{LOCALAPPDATA}/Hogwarts Legacy/Saved/SaveGames"],
    "Hogwarts Legacy": ["{LOCALAPPDATA}/Hogwarts Legacy/Saved/SaveGames"],
    "黑神话：悟空": ["{LOCALAPPDATA}/b1/Saved/SaveGames"],
    "Black Myth: Wukong": ["{LOCALAPPDATA}/b1/Saved/SaveGames"],
    "荒野大镖客2": ["{DOCUMENTS}/Rockstar Games/Red Dead Redemption 2/Profiles"],
    "Red Dead Redemption 2": ["{DOCUMENTS}/Rockstar Games/Red Dead Redemption 2/Profiles"],
    "GTA5": ["{DOCUMENTS}/Rockstar Games/GTA V/Profiles"],
    "GTA V": ["{DOCUMENTS}/Rockstar Games/GTA V/Profiles"],
    "我的世界": ["{APPDATA}/.minecraft"],
    "Minecraft": ["{APPDATA}/.minecraft"],
    "泰拉瑞亚": ["{DOCUMENTS}/My Games/Terraria"],
    "Terraria": ["{DOCUMENTS}/My Games/Terraria"],
    "星露谷物语": ["{APPDATA}/StardewValley"],
    "Stardew Valley": ["{APPDATA}/StardewValley"],
    "空洞骑士": ["{LOCALAPPDATA}/../LocalLow/Team Cherry/Hollow Knight"],
    "Hollow Knight": ["{LOCALAPPDATA}/../LocalLow/Team Cherry/Hollow Knight"],
    "哈迪斯": ["{DOCUMENTS}/Hades"],
    "Hades": ["{DOCUMENTS}/Hades"],
    "怪物猎人：世界": ["{DOCUMENTS}/CAPCOM/MHW"],
    "Monster Hunter: World": ["{DOCUMENTS}/CAPCOM/MHW"],
    "永劫无间": ["{DOCUMENTS}/Naraka_BladePoint"],
    "Naraka: Bladepoint": ["{DOCUMENTS}/Naraka_BladePoint"],
    "鬼谷八荒": ["{LOCALAPPDATA}/guigubahuang"],
    "戴森球计划": ["{LOCALAPPDATA}/Dyson Sphere Program"],
    "Dyson Sphere Program": ["{LOCALAPPDATA}/Dyson Sphere Program"],
}

SAVE_FOLDER_NAMES = [
    'save', 'saves', 'saved', 'savegames', 'savegame', 'savedata',
    'data', 'userdata', 'user', 'profile', 'profiles', 'slot',
    'storage', 'checkpoint', 'checkpoints', 'backup',
    'save_games', 'save-games', 'save_data',
    'playerprofile', 'playerdata', 'gamedata', 'world', 'worlds',
    'Saved', 'SaveGames', 'SavedGames',
]

# ==================== 工具函数 / Utility Functions ====================

def expand_path_vars(path_template):
    path = path_template
    path = path.replace("{APPDATA}", os.environ.get("APPDATA", ""))
    path = path.replace("{LOCALAPPDATA}", os.environ.get("LOCALAPPDATA", ""))
    path = path.replace("{USERPROFILE}", os.environ.get("USERPROFILE", ""))
    path = path.replace("{DOCUMENTS}", os.path.join(os.environ.get("USERPROFILE", ""), "Documents"))
    path = path.replace("{SAVEDGAMES}", os.path.join(os.environ.get("USERPROFILE", ""), "Saved Games"))
    return path


def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        path, _ = winreg.QueryValueEx(key, "InstallPath")
        return path
    except:
        pass
    for p in [r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam", r"D:\Steam"]:
        if Path(p).exists():
            return p
    return None


def get_steam_userdata_path():
    steam_path = get_steam_path()
    if steam_path:
        userdata = Path(steam_path) / "userdata"
        if userdata.exists():
            return userdata
    return None


def scan_game_dir_for_saves(game_dir):
    game_path = Path(game_dir)
    if not game_path.exists():
        return []
    
    found = []
    for name in SAVE_FOLDER_NAMES:
        for match in game_path.rglob(name):
            if match.is_dir():
                depth = len(match.relative_to(game_path).parts)
                if depth <= 4:
                    found.append(str(match))
    
    for p in [game_path / "Saved" / "SaveGames", game_path / "Saved", 
              game_path / "save", game_path / "saves", game_path / "data" / "save"]:
        if p.exists() and p.is_dir():
            found.append(str(p))
    
    unique = list(dict.fromkeys(found))
    unique.sort(key=lambda x: sum(f.stat().st_size for f in Path(x).rglob('*') if f.is_file()), reverse=True)
    return unique


def scan_appdata_for_game(game_name, game_dir=None):
    found = []
    game_name_clean = game_name.lower().replace(" ", "").replace(":", "").replace("-", "").replace("_", "")
    
    name_variants = [game_name_clean]
    if game_dir:
        dir_name = Path(game_dir).name.lower().replace(" ", "").replace(":", "").replace("-", "").replace("_", "")
        if dir_name not in name_variants:
            name_variants.append(dir_name)
    
    search_paths = [
        os.environ.get("APPDATA", ""),
        os.environ.get("LOCALAPPDATA", ""),
        os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "LocalLow"),  # 修复：正确的 LocalLow 路径
        os.path.join(os.environ.get("USERPROFILE", ""), "Saved Games"),
        os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "My Games"),
        os.path.join(os.environ.get("USERPROFILE", ""), "Documents"),
    ]
    
    for base in search_paths:
        if not base or not Path(base).exists():
            continue
        base_path = Path(base)
        
        for folder in base_path.iterdir():
            if not folder.is_dir():
                continue
            folder_clean = folder.name.lower().replace(" ", "").replace(":", "").replace("-", "").replace("_", "")
            
            for variant in name_variants:
                if variant in folder_clean or folder_clean in variant:
                    found.append(str(folder))
                    for sub in folder.iterdir():
                        if sub.is_dir() and sub.name.lower() in [n.lower() for n in SAVE_FOLDER_NAMES]:
                            found.append(str(sub))
            
            try:
                for subfolder in folder.iterdir():
                    if not subfolder.is_dir():
                        continue
                    sub_clean = subfolder.name.lower().replace(" ", "").replace(":", "").replace("-", "").replace("_", "")
                    for variant in name_variants:
                        if variant in sub_clean or sub_clean in variant:
                            found.append(str(subfolder))
                            for sub in subfolder.iterdir():
                                if sub.is_dir() and sub.name.lower() in [n.lower() for n in SAVE_FOLDER_NAMES]:
                                    found.append(str(sub))
            except PermissionError:
                pass
    
    return list(dict.fromkeys(found))


def scan_all_local_appdata():
    found = []
    local_low = Path(os.environ.get("USERPROFILE", "")) / "AppData" / "LocalLow"
    if not local_low.exists():
        return found
    for vendor in local_low.iterdir():
        if vendor.is_dir():
            for game in vendor.iterdir():
                if game.is_dir():
                    found.append(str(game))
    return found


# ==================== 样式配置 / Style Config ====================

class StyleConfig:
    BG_PRIMARY = "#2b2b2b"
    BG_SECONDARY = "#3c3c3c"
    BG_TERTIARY = "#505050"
    FG_PRIMARY = "#ffffff"
    FG_SECONDARY = "#b0b0b0"
    ACCENT = "#4a9eff"
    ACCENT_HOVER = "#6ab0ff"
    FONT_FAMILY = "Microsoft YaHei UI"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 12
    FONT_SIZE_SMALL = 9


# ==================== 主程序 / Main Application ====================

class SaveVault:
    def __init__(self, root):
        self.root = root
        self.root.title("SaveVault")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)
        
        self.app_dir = Path.home() / ".savevault"
        self.app_dir.mkdir(exist_ok=True)
        self.config_file = self.app_dir / "config.json"
        
        # 加载配置 / Load config
        self.config = self.load_config()
        self.current_lang = self.config.get("language", "zh")
        self.games = self.config.get("games", {})
        self.current_game = None
        
        self.setup_styles()
        self.create_ui()
        self.refresh_game_list()
        self.center_window()
    
    def t(self, key):
        """获取翻译 / Get translation"""
        return LANGUAGES.get(self.current_lang, {}).get(key, key)
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        self.config["language"] = self.current_lang
        self.config["games"] = self.games
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
        
        style.configure('TFrame', background=StyleConfig.BG_PRIMARY)
        style.configure('TLabelframe', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.FG_PRIMARY)
        style.configure('TLabelframe.Label', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.ACCENT,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_LARGE, 'bold'))
        style.configure('TLabel', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.FG_PRIMARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL))
        style.configure('Header.TLabel', font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_LARGE, 'bold'),
                       foreground=StyleConfig.ACCENT)
        style.configure('Info.TLabel', foreground=StyleConfig.FG_SECONDARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_SMALL))
        style.configure('TButton', font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL), padding=(12, 6))
        
        style.configure('Treeview', background=StyleConfig.BG_SECONDARY, foreground=StyleConfig.FG_PRIMARY,
                       fieldbackground=StyleConfig.BG_SECONDARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL), rowheight=28)
        style.configure('Treeview.Heading', background=StyleConfig.BG_TERTIARY, foreground=StyleConfig.FG_PRIMARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL, 'bold'))
        style.map('Treeview', background=[('selected', StyleConfig.ACCENT)])
        
        self.root.configure(bg=StyleConfig.BG_PRIMARY)
    
    def find_known_save_path(self, game_name):
        if game_name in GAME_SAVE_PATHS:
            for template in GAME_SAVE_PATHS[game_name]:
                path = expand_path_vars(template)
                if Path(path).exists():
                    return path
        name_lower = game_name.lower()
        for known, paths in GAME_SAVE_PATHS.items():
            if name_lower in known.lower() or known.lower() in name_lower:
                for template in paths:
                    path = expand_path_vars(template)
                    if Path(path).exists():
                        return path
        return None
    
    def create_ui(self):
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 顶部栏 / Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.title_label = ttk.Label(header_frame, text="SaveVault", style='Header.TLabel',
                                     font=(StyleConfig.FONT_FAMILY, 18, 'bold'))
        self.title_label.pack(side=tk.LEFT)
        
        # 语言切换按钮 / Language switch button
        self.lang_btn = ttk.Button(header_frame, text=self.t("language"), width=8, command=self.toggle_language)
        self.lang_btn.pack(side=tk.RIGHT)
        
        # 内容区域 / Content
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板 / Left Panel
        self.left_panel = ttk.LabelFrame(content_frame, text=self.t("game_list"), padding="10")
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        list_container = ttk.Frame(self.left_panel)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.game_listbox = tk.Listbox(
            list_container, background=StyleConfig.BG_SECONDARY, foreground=StyleConfig.FG_PRIMARY,
            selectbackground=StyleConfig.ACCENT, selectforeground='white',
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL),
            borderwidth=0, highlightthickness=0, activestyle='none'
        )
        self.game_listbox.pack(fill=tk.BOTH, expand=True)
        self.game_listbox.bind('<<ListboxSelect>>', self.on_game_select)
        
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.game_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.game_listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame1 = ttk.Frame(self.left_panel)
        btn_frame1.pack(fill=tk.X, pady=(10, 0))
        
        self.add_btn = ttk.Button(btn_frame1, text=self.t("add"), width=12, command=self.add_game)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        self.del_btn = ttk.Button(btn_frame1, text=self.t("delete"), width=8, command=self.delete_game)
        self.del_btn.pack(side=tk.LEFT, padx=2)
        self.edit_btn = ttk.Button(btn_frame1, text=self.t("edit_path"), width=10, command=self.edit_game_path)
        self.edit_btn.pack(side=tk.LEFT, padx=2)
        
        # 右侧面板 / Right Panel
        self.right_panel = ttk.LabelFrame(content_frame, text=self.t("save_backup"), padding="10")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(self.right_panel)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.current_save_label = ttk.Label(info_frame, text=self.t("current_save"), style='Info.TLabel')
        self.current_save_label.pack(side=tk.LEFT)
        self.game_info_label = ttk.Label(info_frame, text=self.t("select_game"), style='Info.TLabel')
        self.game_info_label.pack(side=tk.LEFT, padx=(5, 0))
        
        tree_container = ttk.Frame(self.right_panel)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ('name', 'date', 'size')
        self.backup_tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=12)
        self.backup_tree.heading('name', text=self.t("backup_name"))
        self.backup_tree.heading('date', text=self.t("create_time"))
        self.backup_tree.heading('size', text=self.t("size"))
        self.backup_tree.column('name', width=180, minwidth=120)
        self.backup_tree.column('date', width=140, minwidth=100)
        self.backup_tree.column('size', width=80, minwidth=60, anchor='e')
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar2 = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.backup_tree.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.backup_tree.config(yscrollcommand=scrollbar2.set)
        
        btn_frame2 = ttk.Frame(self.right_panel)
        btn_frame2.pack(fill=tk.X, pady=(10, 0))
        
        # 使用 grid 布局实现按钮自适应
        buttons = [
            (self.t("create_backup"), self.create_backup),
            (self.t("restore"), self.restore_backup),
            (self.t("delete"), self.delete_backup),
            (self.t("rename"), self.rename_backup),
            (self.t("clear_progress"), self.clear_progress),
            (self.t("open_dir"), self.open_backup_dir),
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            btn = ttk.Button(btn_frame2, text=text, command=cmd)
            btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
            btn_frame2.columnconfigure(i, weight=1)
        
        self.create_btn = btn_frame2.winfo_children()[0]
        self.restore_btn = btn_frame2.winfo_children()[1]
        self.del_backup_btn = btn_frame2.winfo_children()[2]
        self.rename_btn = btn_frame2.winfo_children()[3]
        self.clear_btn = btn_frame2.winfo_children()[4]
        self.open_dir_btn = btn_frame2.winfo_children()[5]
        
        # 底部状态栏 / Status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text=self.t("games_count").format(len(self.games), self.app_dir),
                                      style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
    
    def update_ui_text(self):
        """更新所有UI文本 / Update all UI text"""
        self.lang_btn.config(text=self.t("language"))
        self.left_panel.config(text=self.t("game_list"))
        self.right_panel.config(text=self.t("save_backup"))
        self.current_save_label.config(text=self.t("current_save"))
        self.game_info_label.config(text=self.t("select_game"))
        
        self.add_btn.config(text=self.t("add"))
        self.del_btn.config(text=self.t("delete"))
        self.edit_btn.config(text=self.t("edit_path"))
        
        self.create_btn.config(text=self.t("create_backup"))
        self.restore_btn.config(text=self.t("restore"))
        self.del_backup_btn.config(text=self.t("delete"))
        self.rename_btn.config(text=self.t("rename"))
        self.clear_btn.config(text=self.t("clear_progress"))
        self.open_dir_btn.config(text=self.t("open_dir"))
        
        self.backup_tree.heading('name', text=self.t("backup_name"))
        self.backup_tree.heading('date', text=self.t("create_time"))
        self.backup_tree.heading('size', text=self.t("size"))
        
        self.status_label.config(text=self.t("games_count").format(len(self.games), self.app_dir))
    
    def toggle_language(self):
        """切换语言 / Toggle language"""
        self.current_lang = "en" if self.current_lang == "zh" else "zh"
        self.save_config()
        self.update_ui_text()
    
    def refresh_game_list(self):
        self.game_listbox.delete(0, tk.END)
        for name in sorted(self.games.keys()):
            self.game_listbox.insert(tk.END, name)
        self.status_label.config(text=self.t("games_count").format(len(self.games), self.app_dir))
    
    def on_game_select(self, event):
        selection = self.game_listbox.curselection()
        if selection:
            name = self.game_listbox.get(selection[0])
            self.current_game = name
            info = self.games[name]
            save_path = info.get('save_path', '')
            display_path = save_path if len(save_path) <= 60 else "..." + save_path[-57:]
            self.game_info_label.config(text=display_path)
            self.refresh_backup_list()
    
    def refresh_backup_list(self):
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        if not self.current_game:
            return
        
        backup_dir = Path(self.games[self.current_game].get('backup_dir', ''))
        if not backup_dir.exists():
            return
        
        for backup in sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if backup.is_dir():
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
                size_str = self.format_size(size)
                self.backup_tree.insert('', tk.END, 
                                       values=(backup.name, mtime.strftime('%Y-%m-%d %H:%M'), size_str))
    
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def add_game(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("add_game_title"))
        dialog.geometry("680x520")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=StyleConfig.BG_PRIMARY)
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 340
        y = (dialog.winfo_screenheight() // 2) - 260
        dialog.geometry(f'+{x}+{y}')
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=self.t("add_game_title"), style='Header.TLabel',
                 font=(StyleConfig.FONT_FAMILY, 14, 'bold')).grid(row=0, column=0, columnspan=3, 
                                                                   sticky=tk.W, pady=(0, 15))
        
        ttk.Label(main_frame, text=self.t("game_name")).grid(row=1, column=0, sticky=tk.W, pady=8)
        name_var = tk.StringVar()
        name_combo = ttk.Combobox(main_frame, textvariable=name_var, width=55)
        name_combo['values'] = sorted(GAME_SAVE_PATHS.keys())
        name_combo.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=8)
        
        ttk.Label(main_frame, text=self.t("game_dir")).grid(row=2, column=0, sticky=tk.W, pady=8)
        install_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=install_var, width=58).grid(row=2, column=1, sticky=tk.W, pady=8)
        
        def browse_install():
            path = filedialog.askdirectory(title=self.t("game_dir"))
            if path:
                install_var.set(path)
                if not name_var.get():
                    name_var.set(Path(path).name)
        
        ttk.Button(main_frame, text=self.t("browse"), command=browse_install, width=8).grid(row=2, column=2, padx=5, pady=8)
        
        ttk.Label(main_frame, text=self.t("save_path")).grid(row=3, column=0, sticky=tk.W, pady=8)
        save_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=save_var, width=58).grid(row=3, column=1, sticky=tk.W, pady=8)
        
        def browse_save():
            path = filedialog.askdirectory(title=self.t("save_path"))
            if path:
                save_var.set(path)
        
        ttk.Button(main_frame, text=self.t("browse"), command=browse_save, width=8).grid(row=3, column=2, padx=5, pady=8)
        
        status_var = tk.StringVar(value=self.t("scan_hint"))
        ttk.Label(main_frame, textvariable=status_var, style='Info.TLabel'
                 ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text=self.t("scan_result")).grid(row=5, column=0, sticky=tk.NW, pady=5)
        
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=5, column=1, columnspan=2, sticky=tk.NSEW, pady=5)
        
        result_list = tk.Listbox(
            result_frame, height=8, background=StyleConfig.BG_SECONDARY,
            foreground=StyleConfig.FG_PRIMARY, selectbackground=StyleConfig.ACCENT,
            selectforeground='white', font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_SMALL),
            borderwidth=0, highlightthickness=0
        )
        result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_list.config(yscrollcommand=scrollbar.set)
        
        found_paths = []
        
        def on_result_select(event):
            sel = result_list.curselection()
            if sel:
                save_var.set(found_paths[sel[0]])
        
        result_list.bind('<<ListboxSelect>>', on_result_select)
        
        def scan_saves():
            game_name = name_var.get().strip()
            game_dir = install_var.get().strip()
            
            result_list.delete(0, tk.END)
            found_paths.clear()
            status_var.set(self.t("scanning"))
            dialog.update()
            
            all_paths = []
            
            if game_dir:
                all_paths.extend(scan_game_dir_for_saves(game_dir))
            
            if game_name:
                known = self.find_known_save_path(game_name)
                if known and known not in all_paths:
                    all_paths.append(known)
            
            if game_name or game_dir:
                for p in scan_appdata_for_game(game_name or "", game_dir):
                    if p not in all_paths:
                        all_paths.append(p)
            
            steam_userdata = get_steam_userdata_path()
            if steam_userdata:
                for user_dir in steam_userdata.iterdir():
                    if user_dir.is_dir() and user_dir.name.isdigit():
                        for app_dir in user_dir.iterdir():
                            remote = app_dir / "remote"
                            if remote.exists() and str(remote) not in all_paths:
                                all_paths.append(str(remote))
            
            if not game_name and not game_dir:
                all_paths.extend(scan_all_local_appdata())
            
            if all_paths:
                for p in all_paths[:50]:
                    result_list.insert(tk.END, p)
                    found_paths.append(p)
                result_list.selection_set(0)
                save_var.set(all_paths[0])
                status_var.set(self.t("found_paths").format(len(all_paths)))
            else:
                status_var.set(self.t("not_found"))
        
        btn_row = ttk.Frame(main_frame)
        btn_row.grid(row=6, column=0, columnspan=3, pady=15, sticky=tk.W)
        
        ttk.Button(btn_row, text=self.t("db_detect"), command=lambda: (
            save_var.set(self.find_known_save_path(name_var.get()) or ""),
            status_var.set(self.t("db_found") if self.find_known_save_path(name_var.get()) else self.t("db_not_found"))
        ), width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text=self.t("scan"), command=scan_saves, width=10).pack(side=tk.LEFT, padx=3)
        
        btn_bottom = ttk.Frame(main_frame)
        btn_bottom.grid(row=7, column=0, columnspan=3, pady=20)
        
        def confirm():
            name = name_var.get().strip()
            path = save_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", self.t("enter_game_name"))
                return
            if not path:
                messagebox.showerror("Error", self.t("select_save_path"))
                return
            if name in self.games:
                messagebox.showerror("Error", self.t("game_exists"))
                return
            
            self.games[name] = {
                'save_path': path,
                'backup_dir': str(self.app_dir / "backups" / name)
            }
            self.save_config()
            self.refresh_game_list()
            dialog.destroy()
            messagebox.showinfo("Success", f"{self.t('game_added')}: {name}")
        
        ttk.Button(btn_bottom, text=self.t("confirm"), command=confirm, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_bottom, text=self.t("cancel"), command=dialog.destroy, width=12).pack(side=tk.LEFT, padx=5)
        
        main_frame.rowconfigure(5, weight=1)
    
    def delete_game(self):
        selection = self.game_listbox.curselection()
        if not selection:
            messagebox.showwarning("", self.t("select_game_first"))
            return
        
        name = self.game_listbox.get(selection[0])
        if messagebox.askyesno("", self.t("confirm_delete_game").format(name)):
            del self.games[name]
            self.save_config()
            self.refresh_game_list()
            self.current_game = None
            self.game_info_label.config(text=self.t("select_game"))
            self.refresh_backup_list()
    
    def edit_game_path(self):
        selection = self.game_listbox.curselection()
        if not selection:
            messagebox.showwarning("", self.t("select_game_first"))
            return
        
        name = self.game_listbox.get(selection[0])
        current = self.games[name].get('save_path', '')
        new_path = filedialog.askdirectory(title=self.t("save_path"), initialdir=current)
        if new_path:
            self.games[name]['save_path'] = new_path
            self.save_config()
            if self.current_game == name:
                display_path = new_path if len(new_path) <= 60 else "..." + new_path[-57:]
                self.game_info_label.config(text=display_path)
            messagebox.showinfo("", self.t("path_updated"))
    
    def create_backup(self):
        if not self.current_game:
            messagebox.showwarning("", self.t("select_game_first"))
            return
        
        info = self.games[self.current_game]
        save_path = Path(info['save_path'])
        backup_dir = Path(info['backup_dir'])
        
        if not save_path.exists():
            messagebox.showerror("", self.t("save_path_not_exist"))
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = simpledialog.askstring(self.t("create_backup_title"), self.t("enter_backup_name"), 
                                      initialvalue=f"backup_{timestamp}")
        if not name:
            return
        
        backup_path = backup_dir / name
        
        try:
            self.root.config(cursor="watch")
            self.root.update()
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(save_path, backup_path)
            self.refresh_backup_list()
            messagebox.showinfo("", f"{self.t('backup_created')}: {name}")
        except Exception as e:
            messagebox.showerror("", f"{self.t('backup_failed')}: {str(e)}")
        finally:
            self.root.config(cursor="")
    
    def restore_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("", self.t("select_backup_first"))
            return
        
        backup_name = self.backup_tree.item(selection[0])['values'][0]
        info = self.games[self.current_game]
        save_path = Path(info['save_path'])
        backup_path = Path(info['backup_dir']) / backup_name
        
        if not messagebox.askyesno("", self.t("confirm_restore").format(backup_name)):
            return
        
        try:
            self.root.config(cursor="watch")
            self.root.update()
            
            if save_path.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                auto_backup_name = f"_auto_backup_before_restore_{timestamp}"
                auto_backup_path = Path(info['backup_dir']) / auto_backup_name
                
                try:
                    shutil.copytree(save_path, auto_backup_path)
                except Exception as e:
                    self.root.config(cursor="")
                    if not messagebox.askyesno("", self.t("auto_backup_failed").format(str(e))):
                        return
                    self.root.config(cursor="watch")
                
                shutil.rmtree(save_path)
            
            shutil.copytree(backup_path, save_path)
            self.refresh_backup_list()
            messagebox.showinfo("", self.t("restore_success"))
        except Exception as e:
            messagebox.showerror("", f"{self.t('restore_failed')}: {str(e)}")
        finally:
            self.root.config(cursor="")
    
    def delete_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("", self.t("select_backup_first"))
            return
        
        name = self.backup_tree.item(selection[0])['values'][0]
        if messagebox.askyesno("", self.t("confirm_delete_backup").format(name)):
            try:
                shutil.rmtree(Path(self.games[self.current_game]['backup_dir']) / name)
                self.refresh_backup_list()
                messagebox.showinfo("", self.t("delete_success"))
            except Exception as e:
                messagebox.showerror("", f"{self.t('delete_failed')}: {str(e)}")
    
    def rename_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("", self.t("select_backup_first"))
            return
        
        old_name = self.backup_tree.item(selection[0])['values'][0]
        new_name = simpledialog.askstring(self.t("rename_title"), self.t("new_name"), initialvalue=old_name)
        if new_name and new_name != old_name:
            try:
                backup_dir = Path(self.games[self.current_game]['backup_dir'])
                (backup_dir / old_name).rename(backup_dir / new_name)
                self.refresh_backup_list()
                messagebox.showinfo("", self.t("rename_success"))
            except Exception as e:
                messagebox.showerror("", f"{self.t('rename_failed')}: {str(e)}")
    
    def open_backup_dir(self):
        if not self.current_game:
            messagebox.showwarning("", self.t("select_game_first"))
            return
        
        backup_dir = Path(self.games[self.current_game]['backup_dir'])
        backup_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(backup_dir)

    def clear_progress(self):
        """清空当前游戏的存档进度"""
        if not self.current_game:
            messagebox.showwarning("", self.t("select_game_first"))
            return

        info = self.games[self.current_game]
        save_path = Path(info['save_path'])

        # 检查存档目录是否存在且有内容
        if not save_path.exists() or not any(save_path.iterdir()):
            messagebox.showinfo("", self.t("clear_no_save"))
            return

        # 二次确认
        if not messagebox.askyesno("", self.t("confirm_clear_progress").format(self.current_game)):
            return

        try:
            self.root.config(cursor="watch")
            self.root.update()

            # 自动备份当前存档
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            auto_backup_name = f"_auto_backup_before_clear_{timestamp}"
            auto_backup_path = Path(info['backup_dir']) / auto_backup_name
            Path(info['backup_dir']).mkdir(parents=True, exist_ok=True)
            shutil.copytree(save_path, auto_backup_path)

            # 清空存档目录（删除内部所有内容，保留目录本身）
            for item in save_path.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)

            self.refresh_backup_list()
            messagebox.showinfo("", self.t("clear_success"))
        except Exception as e:
            messagebox.showerror("", f"{self.t('clear_failed')}: {str(e)}")
        finally:
            self.root.config(cursor="")


def main():
    root = tk.Tk()
    SaveVault(root)
    root.mainloop()


if __name__ == "__main__":
    main()
