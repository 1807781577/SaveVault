#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Save Manager - 游戏存档备份工具
支持多游戏、多存档管理，自动识别存档位置
"""

import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
from pathlib import Path
import winreg

# ==================== 游戏数据库 ====================

GAME_SAVE_PATHS = {
    # FromSoftware
    "艾尔登法环": ["{APPDATA}/EldenRing"],
    "只狼": ["{APPDATA}/Sekiro"],
    "黑暗之魂3": ["{APPDATA}/DarkSoulsIII"],
    "黑暗之魂2": ["{APPDATA}/DarkSoulsII"],
    "装甲核心6": ["{APPDATA}/ArmoredCore6"],
    # CD Projekt Red
    "赛博朋克2077": ["{SAVEDGAMES}/CD Projekt Red/Cyberpunk 2077"],
    "巫师3": ["{SAVEDGAMES}/CD Projekt Red/The Witcher 3"],
    # Bethesda
    "上古卷轴5": ["{DOCUMENTS}/My Games/Skyrim Special Edition"],
    "辐射4": ["{DOCUMENTS}/My Games/Fallout4"],
    "星空": ["{DOCUMENTS}/My Games/Starfield"],
    # Larian
    "博德之门3": ["{LOCALAPPDATA}/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/Savegames"],
    "神界原罪2": ["{LOCALAPPDATA}/Larian Studios/Divinity Original Sin 2/PlayerProfiles/Public/SaveGames"],
    # Capcom
    "怪物猎人：世界": ["{DOCUMENTS}/CAPCOM/MHW"],
    "怪物猎人：崛起": ["{DOCUMENTS}/CAPCOM/MHRise"],
    "生化危机4重制版": ["{LOCALAPPDATA}/CAPCOM/Resident Evil 4"],
    "鬼泣5": ["{LOCALAPPDATA}/CAPCOM/DevilMayCry5"],
    # 其他热门
    "霍格沃茨之遗": ["{LOCALAPPDATA}/Hogwarts Legacy/Saved/SaveGames"],
    "黑神话：悟空": ["{LOCALAPPDATA}/b1/Saved/SaveGames"],
    "荒野大镖客2": ["{DOCUMENTS}/Rockstar Games/Red Dead Redemption 2/Profiles"],
    "GTA5": ["{DOCUMENTS}/Rockstar Games/GTA V/Profiles"],
    "我的世界": ["{APPDATA}/.minecraft"],
    "泰拉瑞亚": ["{DOCUMENTS}/My Games/Terraria"],
    "星露谷物语": ["{APPDATA}/StardewValley"],
    "空洞骑士": ["{LOCALAPPDATA}/../LocalLow/Team Cherry/Hollow Knight"],
    "哈迪斯": ["{DOCUMENTS}/Hades"],
    "死亡搁浅": ["{LOCALAPPDATA}/KojimaProductions/DeathStranding"],
    "永劫无间": ["{DOCUMENTS}/Naraka_BladePoint"],
    "鬼谷八荒": ["{LOCALAPPDATA}/guigubahuang"],
    "戴森球计划": ["{LOCALAPPDATA}/Dyson Sphere Program"],
}

SAVE_FOLDER_NAMES = [
    'save', 'saves', 'saved', 'savegames', 'savegame', 'savedata',
    'data', 'userdata', 'user', 'profile', 'profiles', 'slot',
    'storage', 'checkpoint', 'checkpoints', 'backup',
    'save_games', 'save-games', 'save_data',
    'playerprofile', 'playerdata', 'gamedata', 'world', 'worlds',
    'Saved', 'SaveGames', 'SavedGames',
]

# ==================== 工具函数 ====================

def expand_path_vars(path_template):
    """展开路径变量"""
    path = path_template
    path = path.replace("{APPDATA}", os.environ.get("APPDATA", ""))
    path = path.replace("{LOCALAPPDATA}", os.environ.get("LOCALAPPDATA", ""))
    path = path.replace("{USERPROFILE}", os.environ.get("USERPROFILE", ""))
    path = path.replace("{DOCUMENTS}", os.path.join(os.environ.get("USERPROFILE", ""), "Documents"))
    path = path.replace("{SAVEDGAMES}", os.path.join(os.environ.get("USERPROFILE", ""), "Saved Games"))
    return path


def get_steam_path():
    """获取Steam安装路径"""
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
    """获取Steam userdata路径"""
    steam_path = get_steam_path()
    if steam_path:
        userdata = Path(steam_path) / "userdata"
        if userdata.exists():
            return userdata
    return None


def scan_game_dir_for_saves(game_dir):
    """扫描游戏安装目录寻找存档文件夹"""
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
    """扫描AppData目录寻找游戏存档"""
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
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Low"),
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
    """扫描 LocalLow 目录下所有游戏"""
    found = []
    local_low = Path(os.environ.get("LOCALAPPDATA", "")) / "Low"
    if not local_low.exists():
        return found
    for vendor in local_low.iterdir():
        if vendor.is_dir():
            for game in vendor.iterdir():
                if game.is_dir():
                    found.append(str(game))
    return found


# ==================== 样式配置 ====================

class StyleConfig:
    """UI样式配置"""
    # 颜色方案
    BG_PRIMARY = "#2b2b2b"
    BG_SECONDARY = "#3c3c3c"
    BG_TERTIARY = "#505050"
    FG_PRIMARY = "#ffffff"
    FG_SECONDARY = "#b0b0b0"
    ACCENT = "#4a9eff"
    ACCENT_HOVER = "#6ab0ff"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    DANGER = "#f44336"
    
    # 字体
    FONT_FAMILY = "Microsoft YaHei UI"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 12
    FONT_SIZE_SMALL = 9


# ==================== 主程序 ====================

class GameSaveManager:
    """游戏存档管理器"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Game Save Manager")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)
        
        # 配置路径
        self.app_dir = Path.home() / ".game_save_manager"
        self.app_dir.mkdir(exist_ok=True)
        self.config_file = self.app_dir / "games.json"
        
        # 数据
        self.games = self.load_config()
        self.current_game = None
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_ui()
        self.refresh_game_list()
        
        # 居中窗口
        self.center_window()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        
        # 尝试使用clam主题作为基础
        try:
            style.theme_use('clam')
        except:
            pass
        
        # 配置框架样式
        style.configure('TFrame', background=StyleConfig.BG_PRIMARY)
        style.configure('TLabelframe', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.FG_PRIMARY)
        style.configure('TLabelframe.Label', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.ACCENT,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_LARGE, 'bold'))
        
        # 配置标签样式
        style.configure('TLabel', background=StyleConfig.BG_PRIMARY, foreground=StyleConfig.FG_PRIMARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL))
        style.configure('Header.TLabel', font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_LARGE, 'bold'),
                       foreground=StyleConfig.ACCENT)
        style.configure('Info.TLabel', foreground=StyleConfig.FG_SECONDARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_SMALL))
        
        # 配置按钮样式
        style.configure('TButton', font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL),
                       padding=(12, 6))
        style.configure('Accent.TButton', foreground='white')
        style.map('Accent.TButton',
                 background=[('active', StyleConfig.ACCENT_HOVER), ('!active', StyleConfig.ACCENT)])
        
        # 配置输入框样式
        style.configure('TEntry', fieldbackground=StyleConfig.BG_TERTIARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL))
        style.configure('TCombobox', fieldbackground=StyleConfig.BG_TERTIARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL))
        
        # 配置Treeview样式
        style.configure('Treeview', 
                       background=StyleConfig.BG_SECONDARY,
                       foreground=StyleConfig.FG_PRIMARY,
                       fieldbackground=StyleConfig.BG_SECONDARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL),
                       rowheight=28)
        style.configure('Treeview.Heading',
                       background=StyleConfig.BG_TERTIARY,
                       foreground=StyleConfig.FG_PRIMARY,
                       font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL, 'bold'))
        style.map('Treeview', background=[('selected', StyleConfig.ACCENT)])
        
        # 设置根窗口背景
        self.root.configure(bg=StyleConfig.BG_PRIMARY)
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.games, f, ensure_ascii=False, indent=2)
    
    def find_known_save_path(self, game_name):
        """从已知数据库查找存档路径"""
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
        """创建主界面"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 顶部标题栏
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="Game Save Manager", style='Header.TLabel',
                               font=(StyleConfig.FONT_FAMILY, 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(header_frame, text="游戏存档备份管理工具", style='Info.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 0))
        
        # 内容区域
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板 - 游戏列表
        left_panel = ttk.LabelFrame(content_frame, text="游戏列表", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 游戏列表容器
        list_container = ttk.Frame(left_panel)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 游戏列表
        self.game_listbox = tk.Listbox(
            list_container,
            background=StyleConfig.BG_SECONDARY,
            foreground=StyleConfig.FG_PRIMARY,
            selectbackground=StyleConfig.ACCENT,
            selectforeground='white',
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_NORMAL),
            borderwidth=0,
            highlightthickness=0,
            activestyle='none'
        )
        self.game_listbox.pack(fill=tk.BOTH, expand=True)
        self.game_listbox.bind('<<ListboxSelect>>', self.on_game_select)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.game_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.game_listbox.config(yscrollcommand=scrollbar.set)
        
        # 游戏操作按钮
        btn_frame1 = ttk.Frame(left_panel)
        btn_frame1.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame1, text="添加游戏", command=self.add_game, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame1, text="删除", command=self.delete_game, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame1, text="编辑路径", command=self.edit_game_path, width=10).pack(side=tk.LEFT, padx=2)
        
        # 右侧面板 - 存档备份
        right_panel = ttk.LabelFrame(content_frame, text="存档备份", padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 当前游戏信息
        info_frame = ttk.Frame(right_panel)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="当前存档:", style='Info.TLabel').pack(side=tk.LEFT)
        self.game_info_label = ttk.Label(info_frame, text="请选择游戏", style='Info.TLabel')
        self.game_info_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 备份列表
        tree_container = ttk.Frame(right_panel)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ('name', 'date', 'size')
        self.backup_tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=12)
        self.backup_tree.heading('name', text='备份名称')
        self.backup_tree.heading('date', text='创建时间')
        self.backup_tree.heading('size', text='大小')
        self.backup_tree.column('name', width=180, minwidth=120)
        self.backup_tree.column('date', width=140, minwidth=100)
        self.backup_tree.column('size', width=80, minwidth=60, anchor='e')
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar2 = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.backup_tree.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.backup_tree.config(yscrollcommand=scrollbar2.set)
        
        # 备份操作按钮
        btn_frame2 = ttk.Frame(right_panel)
        btn_frame2.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame2, text="创建备份", command=self.create_backup, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="恢复", command=self.restore_backup, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="删除", command=self.delete_backup, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="重命名", command=self.rename_backup, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="打开目录", command=self.open_backup_dir, width=10).pack(side=tk.LEFT, padx=2)
        
        # 底部状态栏
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                      text=f"已添加 {len(self.games)} 款游戏 | 数据目录: {self.app_dir}",
                                      style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT)
    
    def refresh_game_list(self):
        self.game_listbox.delete(0, tk.END)
        for name in sorted(self.games.keys()):
            self.game_listbox.insert(tk.END, name)
        self.status_label.config(text=f"已添加 {len(self.games)} 款游戏 | 数据目录: {self.app_dir}")
    
    def on_game_select(self, event):
        selection = self.game_listbox.curselection()
        if selection:
            name = self.game_listbox.get(selection[0])
            self.current_game = name
            info = self.games[name]
            save_path = info.get('save_path', '')
            # 截断过长的路径
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
        """添加游戏对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加游戏")
        dialog.geometry("680x520")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=StyleConfig.BG_PRIMARY)
        
        # 居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 340
        y = (dialog.winfo_screenheight() // 2) - 260
        dialog.geometry(f'+{x}+{y}')
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(main_frame, text="添加新游戏", style='Header.TLabel',
                 font=(StyleConfig.FONT_FAMILY, 14, 'bold')).grid(row=0, column=0, columnspan=3, 
                                                                   sticky=tk.W, pady=(0, 15))
        
        # 游戏名称
        ttk.Label(main_frame, text="游戏名称:").grid(row=1, column=0, sticky=tk.W, pady=8)
        name_var = tk.StringVar()
        name_combo = ttk.Combobox(main_frame, textvariable=name_var, width=55)
        name_combo['values'] = sorted(GAME_SAVE_PATHS.keys())
        name_combo.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=8)
        
        # 游戏安装目录
        ttk.Label(main_frame, text="游戏目录:").grid(row=2, column=0, sticky=tk.W, pady=8)
        install_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=install_var, width=58).grid(row=2, column=1, sticky=tk.W, pady=8)
        
        def browse_install():
            path = filedialog.askdirectory(title="选择游戏安装目录")
            if path:
                install_var.set(path)
                if not name_var.get():
                    name_var.set(Path(path).name)
        
        ttk.Button(main_frame, text="浏览", command=browse_install, width=8).grid(row=2, column=2, padx=5, pady=8)
        
        # 存档路径
        ttk.Label(main_frame, text="存档路径:").grid(row=3, column=0, sticky=tk.W, pady=8)
        save_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=save_var, width=58).grid(row=3, column=1, sticky=tk.W, pady=8)
        
        def browse_save():
            path = filedialog.askdirectory(title="选择存档目录")
            if path:
                save_var.set(path)
        
        ttk.Button(main_frame, text="浏览", command=browse_save, width=8).grid(row=3, column=2, padx=5, pady=8)
        
        # 状态
        status_var = tk.StringVar(value="选择游戏目录或输入名称后点击扫描")
        ttk.Label(main_frame, textvariable=status_var, style='Info.TLabel'
                 ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # 扫描结果
        ttk.Label(main_frame, text="扫描结果:").grid(row=5, column=0, sticky=tk.NW, pady=5)
        
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=5, column=1, columnspan=2, sticky=tk.NSEW, pady=5)
        
        result_list = tk.Listbox(
            result_frame, height=8,
            background=StyleConfig.BG_SECONDARY,
            foreground=StyleConfig.FG_PRIMARY,
            selectbackground=StyleConfig.ACCENT,
            selectforeground='white',
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZE_SMALL),
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
            status_var.set("正在扫描...")
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
                status_var.set(f"找到 {len(all_paths)} 个可能的存档目录")
            else:
                status_var.set("未找到存档，请手动选择")
        
        # 操作按钮
        btn_row = ttk.Frame(main_frame)
        btn_row.grid(row=6, column=0, columnspan=3, pady=15, sticky=tk.W)
        
        ttk.Button(btn_row, text="数据库检测", command=lambda: (
            save_var.set(self.find_known_save_path(name_var.get()) or ""),
            status_var.set("已从数据库检测" if self.find_known_save_path(name_var.get()) else "数据库中未找到")
        ), width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text="扫描存档", command=scan_saves, width=10).pack(side=tk.LEFT, padx=3)
        
        # 底部按钮
        btn_bottom = ttk.Frame(main_frame)
        btn_bottom.grid(row=7, column=0, columnspan=3, pady=20)
        
        def confirm():
            name = name_var.get().strip()
            path = save_var.get().strip()
            
            if not name:
                messagebox.showerror("错误", "请输入游戏名称")
                return
            if not path:
                messagebox.showerror("错误", "请选择存档路径")
                return
            if name in self.games:
                messagebox.showerror("错误", "游戏已存在")
                return
            
            self.games[name] = {
                'save_path': path,
                'backup_dir': str(self.app_dir / "backups" / name)
            }
            self.save_config()
            self.refresh_game_list()
            dialog.destroy()
            messagebox.showinfo("成功", f"已添加游戏: {name}")
        
        ttk.Button(btn_bottom, text="确定", command=confirm, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_bottom, text="取消", command=dialog.destroy, width=12).pack(side=tk.LEFT, padx=5)
        
        main_frame.rowconfigure(5, weight=1)
    
    def delete_game(self):
        selection = self.game_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个游戏")
            return
        
        name = self.game_listbox.get(selection[0])
        if messagebox.askyesno("确认删除", f"确定要删除游戏 '{name}' 吗？\n\n备份文件不会被删除"):
            del self.games[name]
            self.save_config()
            self.refresh_game_list()
            self.current_game = None
            self.game_info_label.config(text="请选择游戏")
            self.refresh_backup_list()
    
    def edit_game_path(self):
        selection = self.game_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个游戏")
            return
        
        name = self.game_listbox.get(selection[0])
        current = self.games[name].get('save_path', '')
        new_path = filedialog.askdirectory(title="选择存档目录", initialdir=current)
        if new_path:
            self.games[name]['save_path'] = new_path
            self.save_config()
            if self.current_game == name:
                display_path = new_path if len(new_path) <= 60 else "..." + new_path[-57:]
                self.game_info_label.config(text=display_path)
            messagebox.showinfo("成功", "路径已更新")
    
    def create_backup(self):
        if not self.current_game:
            messagebox.showwarning("提示", "请先选择一个游戏")
            return
        
        info = self.games[self.current_game]
        save_path = Path(info['save_path'])
        backup_dir = Path(info['backup_dir'])
        
        if not save_path.exists():
            messagebox.showerror("错误", "存档路径不存在")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = simpledialog.askstring("创建备份", "请输入备份名称:", initialvalue=f"backup_{timestamp}")
        if not name:
            return
        
        backup_path = backup_dir / name
        
        try:
            self.root.config(cursor="watch")
            self.root.update()
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(save_path, backup_path)
            self.refresh_backup_list()
            messagebox.showinfo("成功", f"备份创建成功: {name}")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {str(e)}")
        finally:
            self.root.config(cursor="")
    
    def restore_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个备份")
            return
        
        backup_name = self.backup_tree.item(selection[0])['values'][0]
        info = self.games[self.current_game]
        save_path = Path(info['save_path'])
        backup_path = Path(info['backup_dir']) / backup_name
        
        if not messagebox.askyesno("确认恢复", 
                                   f"确定恢复到 '{backup_name}' 吗？\n\n当前存档将被覆盖！"):
            return
        
        try:
            self.root.config(cursor="watch")
            self.root.update()
            if save_path.exists():
                shutil.rmtree(save_path)
            shutil.copytree(backup_path, save_path)
            messagebox.showinfo("成功", "存档恢复成功！")
        except Exception as e:
            messagebox.showerror("错误", f"恢复失败: {str(e)}")
        finally:
            self.root.config(cursor="")
    
    def delete_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个备份")
            return
        
        name = self.backup_tree.item(selection[0])['values'][0]
        if messagebox.askyesno("确认删除", f"确定删除备份 '{name}' 吗？"):
            try:
                shutil.rmtree(Path(self.games[self.current_game]['backup_dir']) / name)
                self.refresh_backup_list()
                messagebox.showinfo("成功", "备份已删除")
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")
    
    def rename_backup(self):
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个备份")
            return
        
        old_name = self.backup_tree.item(selection[0])['values'][0]
        new_name = simpledialog.askstring("重命名", "新名称:", initialvalue=old_name)
        if new_name and new_name != old_name:
            try:
                backup_dir = Path(self.games[self.current_game]['backup_dir'])
                (backup_dir / old_name).rename(backup_dir / new_name)
                self.refresh_backup_list()
                messagebox.showinfo("成功", "重命名成功")
            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {str(e)}")
    
    def open_backup_dir(self):
        if not self.current_game:
            messagebox.showwarning("提示", "请先选择一个游戏")
            return
        
        backup_dir = Path(self.games[self.current_game]['backup_dir'])
        backup_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(backup_dir)


def main():
    root = tk.Tk()
    GameSaveManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
