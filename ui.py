# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 03:09:07 2025

@author: xiaoleiwww
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
import glob
import csv
import json

class LanguageManager:
    """语言管理器"""
    def __init__(self, lang_file='lang.json'):
        self.lang_file = lang_file
        self.current_lang = 'en'
        self.languages = {}
        self.callbacks = []
        self.load_languages()
    
    def load_languages(self):
        """加载语言文件"""
        try:
            if os.path.exists(self.lang_file):
                with open(self.lang_file, 'r', encoding='utf-8') as f:
                    self.languages = json.load(f)
            else:
                self.create_default_language_file()
        except Exception as e:
            messagebox.showerror("Error", f"无法加载语言文件: {str(e)}")
            self.create_default_language_file()
    
    def create_default_language_file(self):
        """创建默认语言文件"""
        self.languages = {
            'en': {
                'app_title': 'Bible Reader',
                'select_folder': 'Select Folder',
                'select_image_folder': 'Select Image Folder',
                'base_path': 'Base Path',
                'available_folders': 'Available Folders',
                'ok': 'OK',
                'cancel': 'Cancel',
                'manual_select': 'Manual Select Folder',
                'warning': 'Warning',
                'please_select_folder': 'Please select a folder',
                'image_viewer': 'Image Viewer',
                'current_folder': 'Current Folder',
                'folder_location': 'Folder Location',
                'filename': 'Filename',
                'prev_image': 'Previous',
                'next_image': 'Next',
                'change_folder': 'Change Folder',
                'no_images_found': 'No images found in folder',
                'error': 'Error',
                'folder_not_exist': 'Folder does not exist',
                'version': 'Version',
                'volume': 'Volume',
                'chapter': 'Chapter',
                'verse_range': 'Verse Range',
                'to': 'to',
                'search': 'Search',
                'case_sensitive': 'Case Sensitive',
                'view_images': 'View Images',
                'search_results': 'Search Results',
                'no_results': 'No results found',
                'loading': 'Loading',
                'data_load_error': 'Unable to load data files',
                'searching': 'Searching',
                'root_directory': 'Root Directory',
                'unknown_folder': 'Unknown Folder',
                'no_folder_selected': 'No folder selected',
                'language': 'Language'
            },
            'zh': {
                'app_title': '圣经阅读器',
                'select_folder': '选择文件夹',
                'select_image_folder': '选择图片文件夹',
                'base_path': '基础路径',
                'available_folders': '可用的文件夹',
                'ok': '确定',
                'cancel': '取消',
                'manual_select': '手动选择文件夹',
                'warning': '警告',
                'please_select_folder': '请选择一个文件夹',
                'image_viewer': '图片查看器',
                'current_folder': '当前文件夹',
                'folder_location': '所在文件夹',
                'filename': '文件名',
                'prev_image': '上一张',
                'next_image': '下一张',
                'change_folder': '切换文件夹',
                'no_images_found': '文件夹中未找到图片文件',
                'error': '错误',
                'folder_not_exist': '文件夹不存在',
                'version': '版本',
                'volume': '卷',
                'chapter': '章',
                'verse_range': '节范围',
                'to': '至',
                'search': '搜索',
                'case_sensitive': '区分大小写',
                'view_images': '查看图片',
                'search_results': '搜索结果',
                'no_results': '未找到结果',
                'loading': '加载中',
                'data_load_error': '无法加载数据文件',
                'searching': '正在搜索',
                'root_directory': '根目录',
                'unknown_folder': '未知文件夹',
                'no_folder_selected': '未选择文件夹',
                'language': '语言'
            }
        }
        
        try:
            with open(self.lang_file, 'w', encoding='utf-8') as f:
                json.dump(self.languages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"无法创建语言文件: {str(e)}")
    
    def get_text(self, key):
        """获取当前语言的文本"""
        lang_dict = self.languages.get(self.current_lang, self.languages['en'])
        return lang_dict.get(key, key)
    
    def add_callback(self, callback):
        """添加语言改变回调函数"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """移除语言改变回调函数"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def set_language(self, lang_code):
        """设置当前语言"""
        if lang_code in self.languages:
            self.current_lang = lang_code
            for callback in self.callbacks:
                callback()
            return True
        return False
    
    def get_available_languages(self):
        """获取可用的语言列表"""
        return list(self.languages.keys())
    
    def get_language_display_names(self):
        """获取语言的显示名称"""
        return {
            'en': 'English',
            'zh': '中文'
        }

class FolderSelector:
    """文件夹选择器"""
    def __init__(self, parent, lang_manager, base_folder="pics"):
        self.parent = parent
        self.lang_manager = lang_manager
        self.base_folder = base_folder
        self.selected_folder = None
        self.folders = []
        
        # 注册语言回调
        self.lang_manager.add_callback(self.on_language_changed)
        
        # 扫描文件夹
        self.scan_folders()
        
        # 创建选择界面
        self.create_selector_window()
    
    def on_language_changed(self):
        """语言改变时的回调"""
        if hasattr(self, 'selector_window') and self.selector_window.winfo_exists():
            self.update_ui_text()
    
    def update_ui_text(self):
        """更新UI文本"""
        self.selector_window.title(self.lang_manager.get_text('select_image_folder'))
        
        # 更新标题
        self.title_label.config(text=self.lang_manager.get_text('select_image_folder'))
        
        # 更新路径标签
        self.path_label.config(text=f"{self.lang_manager.get_text('base_path')}: {os.path.abspath(self.base_folder)}")
        
        # 更新列表标签
        self.list_label.config(text=f"{self.lang_manager.get_text('available_folders')}:")
        
        # 更新按钮文本
        self.ok_button.config(text=self.lang_manager.get_text('ok'))
        self.cancel_button.config(text=self.lang_manager.get_text('cancel'))
        self.manual_button.config(text=self.lang_manager.get_text('manual_select'))
        
        # 更新根目录选项
        if self.folders and self.folders[0] in ['Root Directory', '根目录']:
            self.folder_listbox.delete(0)
            self.folder_listbox.insert(0, self.lang_manager.get_text('root_directory'))
            self.folders[0] = self.lang_manager.get_text('root_directory')
    
    def scan_folders(self):
        """扫描pics文件夹中的所有子文件夹"""
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder, exist_ok=True)
            self.folders = []
            return
        
        try:
            for item in os.listdir(self.base_folder):
                item_path = os.path.join(self.base_folder, item)
                if os.path.isdir(item_path):
                    self.folders.append(item)
            
            self.folders.sort()
            self.folders.insert(0, self.lang_manager.get_text('root_directory'))
            
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_text('error'), 
                               f"扫描文件夹时出错: {str(e)}")
            self.folders = [self.lang_manager.get_text('root_directory')]
    
    def create_selector_window(self):
        """创建文件夹选择窗口"""
        self.selector_window = tk.Toplevel(self.parent)
        self.selector_window.title(self.lang_manager.get_text('select_image_folder'))
        self.selector_window.geometry("400x300")
        self.selector_window.transient(self.parent)
        self.selector_window.grab_set()
        
        # 主框架
        main_frame = tk.Frame(self.selector_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        self.title_label = tk.Label(main_frame, text=self.lang_manager.get_text('select_image_folder'), 
                                   font=('Arial', 12, 'bold'))
        self.title_label.pack(pady=10)
        
        # 路径显示
        self.path_label = tk.Label(main_frame, 
                                  text=f"{self.lang_manager.get_text('base_path')}: {os.path.abspath(self.base_folder)}",
                                  font=('Arial', 9), fg='#777777')
        self.path_label.pack(pady=5)
        
        # 文件夹列表框架
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 列表标签
        self.list_label = tk.Label(list_frame, text=f"{self.lang_manager.get_text('available_folders')}:", 
                                  font=('Arial', 10))
        self.list_label.pack(anchor=tk.W)
        
        # 文件夹列表框
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.folder_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                        font=('Arial', 10))
        self.folder_listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.folder_listbox.yview)
        
        # 添加文件夹到列表
        for folder in self.folders:
            self.folder_listbox.insert(tk.END, folder)
        
        # 默认选择第一个
        if self.folders:
            self.folder_listbox.selection_set(0)
        
        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 确定按钮
        self.ok_button = tk.Button(button_frame, text=self.lang_manager.get_text('ok'), 
                                  command=self.on_ok, bg='#28a745', fg='white', font=('Arial', 10))
        self.ok_button.pack(side=tk.LEFT, padx=5)
        
        # 取消按钮
        self.cancel_button = tk.Button(button_frame, text=self.lang_manager.get_text('cancel'), 
                                      command=self.on_cancel, bg='#6c757d', fg='white', font=('Arial', 10))
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # 手动选择按钮
        self.manual_button = tk.Button(button_frame, text=self.lang_manager.get_text('manual_select'), 
                                      command=self.on_manual, bg='#4a7abc', fg='white', font=('Arial', 10))
        self.manual_button.pack(side=tk.RIGHT, padx=5)
        
        # 绑定双击事件
        self.folder_listbox.bind('<Double-Button-1>', lambda e: self.on_ok())
    
    def on_ok(self):
        """确定选择"""
        selection = self.folder_listbox.curselection()
        if selection:
            folder_name = self.folders[selection[0]]
            if folder_name == self.lang_manager.get_text('root_directory'):
                self.selected_folder = self.base_folder
            else:
                self.selected_folder = os.path.join(self.base_folder, folder_name)
            self.selector_window.destroy()
        else:
            messagebox.showwarning(self.lang_manager.get_text('warning'), 
                                 self.lang_manager.get_text('please_select_folder'))
    
    def on_cancel(self):
        """取消选择"""
        self.selected_folder = None
        self.selector_window.destroy()
    
    def on_manual(self):
        """手动选择文件夹"""
        folder = filedialog.askdirectory(
            title=self.lang_manager.get_text('select_folder'),
            initialdir=self.base_folder
        )
        if folder:
            self.selected_folder = folder
            self.selector_window.destroy()
    
    def get_selected_folder(self):
        """获取选择的文件夹"""
        return self.selected_folder

class ImageViewer:
    """图片查看器"""
    def __init__(self, parent, lang_manager, image_folder=None):
        self.parent = parent
        self.lang_manager = lang_manager
        self.image_folder = image_folder
        self.images = []
        self.current_index = 0
        
        # 注册语言回调
        self.lang_manager.add_callback(self.on_language_changed)
        
        if not self.image_folder:
            self.select_folder()
        else:
            self.load_images()
            self.create_image_window()
    
    def on_language_changed(self):
        """语言改变时的回调"""
        if hasattr(self, 'image_window') and self.image_window.winfo_exists():
            self.update_ui_text()
    
    def update_ui_text(self):
        """更新UI文本"""
        self.image_window.title(f"{self.lang_manager.get_text('image_viewer')} - {os.path.basename(self.image_folder)}")
        
        # 更新文件夹标题
        self.folder_title_label.config(text=f"{self.lang_manager.get_text('current_folder')}: {self.image_folder}")
        
        # 更新按钮文本
        self.prev_btn.config(text=self.lang_manager.get_text('prev_image'))
        self.next_btn.config(text=self.lang_manager.get_text('next_image'))
        self.change_folder_btn.config(text=self.lang_manager.get_text('change_folder'))
        
        # 更新当前图片信息
        if self.images:
            self.show_current_image()
    
    def select_folder(self):
        """选择图片文件夹"""
        selector = FolderSelector(self.parent, self.lang_manager)
        self.parent.wait_window(selector.selector_window)
        
        selected_folder = selector.get_selected_folder()
        if selected_folder:
            self.image_folder = selected_folder
            self.load_images()
            self.create_image_window()
        else:
            messagebox.showinfo("Info", self.lang_manager.get_text('no_folder_selected'))
    
    def load_images(self):
        """加载图片文件列表"""
        if not self.image_folder or not os.path.exists(self.image_folder):
            messagebox.showerror(self.lang_manager.get_text('error'), 
                               f"{self.lang_manager.get_text('folder_not_exist')}: {self.image_folder}")
            return
        
        self.images.clear()
        self.current_index = 0
        
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
        for ext in image_extensions:
            pattern = os.path.join(self.image_folder, "**", ext)
            found_images = glob.glob(pattern, recursive=True)
            self.images.extend(found_images)
        
        self.images = list(set(self.images))
        self.images.sort()
    
    def get_folder_info(self, image_path):
        """获取图片的文件夹信息"""
        if not self.image_folder:
            return self.lang_manager.get_text('unknown_folder')
        
        try:
            rel_path = os.path.relpath(image_path, self.image_folder)
            folder_path = os.path.dirname(rel_path)
            
            if folder_path == '.':
                return self.lang_manager.get_text('root_directory')
            else:
                return folder_path
        except:
            return os.path.dirname(image_path)
    
    def create_image_window(self):
        """创建图片查看窗口"""
        if not self.images:
            messagebox.showinfo("Info", 
                              f"{self.lang_manager.get_text('no_images_found')}: '{self.image_folder}'")
            return
        
        self.image_window = tk.Toplevel(self.parent)
        self.image_window.title(f"{self.lang_manager.get_text('image_viewer')} - {os.path.basename(self.image_folder)}")
        self.image_window.geometry("900x700")
        self.image_window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # 顶部信息栏
        top_info_frame = tk.Frame(self.image_window, bg='#e8f4fd')
        top_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.folder_title_label = tk.Label(top_info_frame, 
                                          text=f"{self.lang_manager.get_text('current_folder')}: {self.image_folder}", 
                                          font=('Arial', 9), bg='#e8f4fd', fg='#2c3e50')
        self.folder_title_label.pack(anchor=tk.W)
        
        # 图片显示区域
        self.image_frame = tk.Frame(self.image_window)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 信息显示区域
        info_frame = tk.Frame(self.image_window)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 文件夹信息
        self.folder_label = tk.Label(info_frame, text="", font=('Arial', 10), 
                                    bg='#f0f0f0', padx=10, pady=5, wraplength=800)
        self.folder_label.pack(fill=tk.X)
        
        # 文件名信息
        self.filename_label = tk.Label(info_frame, text="", font=('Arial', 9), 
                                      fg='#777777', padx=10, pady=2)
        self.filename_label.pack(fill=tk.X)
        
        # 控制按钮
        control_frame = tk.Frame(self.image_window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.prev_btn = tk.Button(control_frame, text=self.lang_manager.get_text('prev_image'), 
                                 command=self.prev_image, bg='#4a7abc', fg='white', font=('Arial', 10))
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(control_frame, text=self.lang_manager.get_text('next_image'), 
                                 command=self.next_image, bg='#4a7abc', fg='white', font=('Arial', 10))
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # 切换文件夹按钮
        self.change_folder_btn = tk.Button(control_frame, text=self.lang_manager.get_text('change_folder'), 
                                          command=self.change_folder, bg='#28a745', fg='white', font=('Arial', 10))
        self.change_folder_btn.pack(side=tk.LEFT, padx=20)
        
        # 图片计数
        self.counter_label = tk.Label(control_frame, text="", font=('Arial', 10))
        self.counter_label.pack(side=tk.LEFT, padx=20)
        
        # 显示第一张图片
        self.show_current_image()
    
    def on_window_close(self):
        """窗口关闭时的清理工作"""
        self.cleanup()
        self.image_window.destroy()
    
    def cleanup(self):
        """清理资源"""
        self.images.clear()
        self.current_index = 0
        if hasattr(self, 'image_label') and hasattr(self.image_label, 'image'):
            self.image_label.image = None
    
    def change_folder(self):
        """切换文件夹"""
        self.cleanup()
        self.image_window.destroy()
        self.select_folder()
    
    def show_current_image(self):
        """显示当前图片"""
        if not self.images:
            return
        
        try:
            image_path = self.images[self.current_index]
            image = Image.open(image_path)
            
            # 调整图片大小以适应窗口
            window_width = 850
            window_height = 500
            image.thumbnail((window_width, window_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            # 显示文件夹信息
            folder_info = self.get_folder_info(image_path)
            self.folder_label.configure(text=f"{self.lang_manager.get_text('folder_location')}: {folder_info}")
            
            # 显示文件名
            filename = os.path.basename(image_path)
            self.filename_label.configure(text=f"{self.lang_manager.get_text('filename')}: {filename}")
            
            # 显示计数
            self.counter_label.configure(text=f"{self.current_index + 1} / {len(self.images)}")
            
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_text('error'), f"无法加载图片: {str(e)}")
    
    def next_image(self):
        """下一张图片"""
        if self.images and self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.show_current_image()
    
    def prev_image(self):
        """上一张图片"""
        if self.images and self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()

class BibleReader:
    def __init__(self, root):
        self.root = root
        self.lang_manager = LanguageManager()
        
        self.lang_manager.add_callback(self.on_language_changed)
        
        self.root.title(self.lang_manager.get_text('app_title'))
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # 加载数据
        self.load_data()
        
        # 创建界面
        self.create_widgets()
        
        # 初始化显示
        self.update_content()
    
    def on_language_changed(self):
        """语言改变时的回调函数"""
        # 更新窗口标题
        self.root.title(self.lang_manager.get_text('app_title'))
        
        # 更新所有UI文本
        self.update_ui_text()
    
    def update_ui_text(self):
        """更新所有UI组件的文本"""
        # 更新语言选择标签
        self.lang_label.config(text=f"{self.lang_manager.get_text('language')}:")
        
        # 更新版本选择标签
        self.version_label.config(text=f"{self.lang_manager.get_text('version')}:")
        
        # 更新卷选择标签
        self.volume_label.config(text=f"{self.lang_manager.get_text('volume')}:")
        
        # 更新章选择标签
        self.chapter_label.config(text=f"{self.lang_manager.get_text('chapter')}:")
        
        # 更新节范围标签
        self.verse_label.config(text=f"{self.lang_manager.get_text('verse_range')}:")
        self.verse_to_label.config(text=self.lang_manager.get_text('to'))
        
        # 更新搜索相关控件
        self.search_label.config(text=f"{self.lang_manager.get_text('search')}:")
        self.search_button.config(text=self.lang_manager.get_text('search'))
        self.case_check.config(text=self.lang_manager.get_text('case_sensitive'))
        
        # 更新图片查看按钮
        self.image_btn.config(text=self.lang_manager.get_text('view_images'))
        
        # 更新语言选择框的值
        lang_display_names = self.lang_manager.get_language_display_names()
        display_values = [f"{code} - {name}" for code, name in lang_display_names.items()]
        self.lang_combo['values'] = display_values
        
        # 设置当前语言显示
        current_display = f"{self.lang_manager.current_lang} - {lang_display_names.get(self.lang_manager.current_lang, self.lang_manager.current_lang)}"
        self.lang_var.set(current_display)
        
        # 更新内容显示
        self.update_content()
    
    def load_data(self):
        """加载圣经数据和卷名数据"""
        try:
            # 加载圣经文本数据
            self.df = []
            with open('data.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.df.append(row)
            
            # 加载卷名数据
            self.bibleid_df = []
            with open('bibleid.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.bibleid_df.append(row)
            
            # 创建卷名映射字典
            self.volume_names = {}
            for row in self.bibleid_df:
                sn = int(row['SN'])
                self.volume_names[sn] = {
                    'short': row['ShortName'],
                    'full': row['FullName'],
                    'chapters': int(row['ChapterNumber'])
                }
            
            # 获取可用的版本列表
            if self.df:
                sample_row = self.df[0]
                self.versions = [col for col in sample_row.keys() if col in ['strjw', 'NCB', 'LCC', 'TCB', 'NIV']]
            else:
                self.versions = ['strjw', 'NCB', 'LCC', 'TCB', 'NIV']
                
            self.current_version = self.versions[0] if self.versions else 'strjw'
            
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_text('error'), 
                               f"{self.lang_manager.get_text('data_load_error')}: {str(e)}")
            self.df = []
            self.bibleid_df = []
            self.volume_names = {}
    
    def get_volume_name(self, volume_sn, name_type='full'):
        """根据卷SN获取卷名"""
        volume_sn = int(volume_sn)
        if volume_sn in self.volume_names:
            return self.volume_names[volume_sn].get(name_type, f'Volume {volume_sn}')
        return f'Volume {volume_sn}'
    
    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制面板
        control_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行控制项
        control_row1 = tk.Frame(control_frame, bg='#ffffff')
        control_row1.pack(fill=tk.X, padx=5, pady=5)
        
        # 语言选择
        self.lang_label = tk.Label(control_row1, text=f"{self.lang_manager.get_text('language')}:", 
                                  bg='#ffffff', font=('Arial', 10))
        self.lang_label.pack(side=tk.LEFT, padx=5)
        
        self.lang_var = tk.StringVar()
        lang_display_names = self.lang_manager.get_language_display_names()
        display_values = [f"{code} - {name}" for code, name in lang_display_names.items()]
        
        self.lang_combo = ttk.Combobox(control_row1, textvariable=self.lang_var, 
                                      values=display_values, state="readonly", width=12)
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 设置当前语言显示
        current_display = f"{self.lang_manager.current_lang} - {lang_display_names.get(self.lang_manager.current_lang, self.lang_manager.current_lang)}"
        self.lang_var.set(current_display)
        
        # 版本选择
        self.version_label = tk.Label(control_row1, text=f"{self.lang_manager.get_text('version')}:", 
                                     bg='#ffffff', font=('Arial', 10))
        self.version_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.version_var = tk.StringVar(value=self.current_version)
        version_combo = ttk.Combobox(control_row1, textvariable=self.version_var, 
                                    values=self.versions, state="readonly")
        version_combo.pack(side=tk.LEFT, padx=5)
        version_combo.bind('<<ComboboxSelected>>', self.on_version_change)
        
        # 卷选择
        self.volume_label = tk.Label(control_row1, text=f"{self.lang_manager.get_text('volume')}:", 
                                    bg='#ffffff', font=('Arial', 10))
        self.volume_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.volumes = sorted(set(int(row['VolumeSN']) for row in self.df)) if self.df else []
        volume_display_values = []
        for vol in self.volumes:
            vol_name = self.get_volume_name(vol, 'full')
            volume_display_values.append(f"{vol}. {vol_name}")
        
        self.volume_var = tk.StringVar()
        self.volume_combo = ttk.Combobox(control_row1, textvariable=self.volume_var, 
                                        values=volume_display_values, state="readonly", width=15)
        self.volume_combo.pack(side=tk.LEFT, padx=5)
        self.volume_combo.bind('<<ComboboxSelected>>', self.on_volume_change)
        
        # 章选择
        self.chapter_label = tk.Label(control_row1, text=f"{self.lang_manager.get_text('chapter')}:", 
                                     bg='#ffffff', font=('Arial', 10))
        self.chapter_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.chapters = []
        self.chapter_var = tk.StringVar()
        self.chapter_combo = ttk.Combobox(control_row1, textvariable=self.chapter_var, 
                                         values=self.chapters, state="readonly", width=5)
        self.chapter_combo.pack(side=tk.LEFT, padx=5)
        self.chapter_combo.bind('<<ComboboxSelected>>', self.on_chapter_change)
        
        # 图片查看按钮
        self.image_btn = tk.Button(control_row1, text=self.lang_manager.get_text('view_images'), 
                                  command=self.open_image_viewer, bg='#28a745', fg='white', font=('Arial', 10))
        self.image_btn.pack(side=tk.RIGHT, padx=5)
        
        # 第二行控制项
        control_row2 = tk.Frame(control_frame, bg='#ffffff')
        control_row2.pack(fill=tk.X, padx=5, pady=5)
        
        # 节范围选择
        self.verse_label = tk.Label(control_row2, text=f"{self.lang_manager.get_text('verse_range')}:", 
                                   bg='#ffffff', font=('Arial', 10))
        self.verse_label.pack(side=tk.LEFT, padx=5)
        
        self.verse_start_var = tk.StringVar()
        self.verse_start_combo = ttk.Combobox(control_row2, textvariable=self.verse_start_var, 
                                             width=5, state="readonly")
        self.verse_start_combo.pack(side=tk.LEFT, padx=5)
        self.verse_start_combo.bind('<<ComboboxSelected>>', self.on_verse_change)
        
        self.verse_to_label = tk.Label(control_row2, text=self.lang_manager.get_text('to'), 
                                      bg='#ffffff', font=('Arial', 10))
        self.verse_to_label.pack(side=tk.LEFT, padx=5)
        
        self.verse_end_var = tk.StringVar()
        self.verse_end_combo = ttk.Combobox(control_row2, textvariable=self.verse_end_var, 
                                           width=5, state="readonly")
        self.verse_end_combo.pack(side=tk.LEFT, padx=5)
        self.verse_end_combo.bind('<<ComboboxSelected>>', self.on_verse_change)
        
        # 搜索框
        self.search_label = tk.Label(control_row2, text=f"{self.lang_manager.get_text('search')}:", 
                                    bg='#ffffff', font=('Arial', 10))
        self.search_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(control_row2, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', self.on_search)
        
        self.search_button = tk.Button(control_row2, text=self.lang_manager.get_text('search'), 
                                      command=self.on_search, bg='#4a7abc', fg='white', font=('Arial', 10))
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # 搜索选项
        self.case_sensitive = tk.BooleanVar()
        self.case_check = tk.Checkbutton(control_row2, text=self.lang_manager.get_text('case_sensitive'), 
                                        variable=self.case_sensitive, bg='#ffffff', font=('Arial', 9))
        self.case_check.pack(side=tk.LEFT, padx=10)
        
        # 内容显示区域
        content_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.SUNKEN, bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 文本显示区域
        self.text_display = tk.Text(content_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                                   font=('Arial', 12), bg='#ffffff', fg='#333333',
                                   padx=10, pady=10, spacing1=5, spacing2=2, spacing3=5)
        self.text_display.pack(fill=tk.BOTH, expand=True)
        self.text_display.config(state=tk.DISABLED)
        
        scrollbar.config(command=self.text_display.yview)
        
        # 初始化卷选择
        if volume_display_values:
            self.volume_combo.set(volume_display_values[0])
            self.on_volume_change()
    
    def on_language_change(self, event=None):
        """语言切换"""
        selected = self.lang_var.get()
        if selected:
            lang_code = selected.split(' - ')[0]
            self.lang_manager.set_language(lang_code)
    
    def get_volume_sn_from_display(self, display_value):
        """从显示文本中提取卷SN"""
        if '.' in display_value:
            return int(display_value.split('.')[0])
        return int(display_value)
    
    def open_image_viewer(self):
        """打开图片查看器"""
        ImageViewer(self.root, self.lang_manager)
    
    def on_version_change(self, event=None):
        self.current_version = self.version_var.get()
        self.update_content()
    
    def on_volume_change(self, event=None):
        volume_display = self.volume_var.get()
        if volume_display:
            volume_sn = self.get_volume_sn_from_display(volume_display)
            self.chapters = sorted(set(int(row['ChapterSN']) for row in self.df 
                                    if int(row['VolumeSN']) == volume_sn))
            self.chapter_combo['values'] = self.chapters
            if self.chapters:
                self.chapter_combo.set(self.chapters[0])
                self.on_chapter_change()
    
    def on_chapter_change(self, event=None):
        volume_display = self.volume_var.get()
        chapter = self.chapter_var.get()
        if volume_display and chapter:
            volume_sn = self.get_volume_sn_from_display(volume_display)
            verses = sorted(set(int(row['VerseSN']) for row in self.df 
                              if int(row['VolumeSN']) == volume_sn and int(row['ChapterSN']) == int(chapter)))
            self.verse_start_combo['values'] = verses
            self.verse_end_combo['values'] = verses
            if verses:
                self.verse_start_combo.set(verses[0])
                self.verse_end_combo.set(verses[-1])
                self.on_verse_change()
    
    def on_verse_change(self, event=None):
        self.update_content()
    
    def simple_search(self, text, pattern, case_sensitive=False):
        """简单的字符串搜索"""
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        positions = []
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return positions
    
    def on_search(self, event=None):
        query = self.search_var.get().strip()
        if not query:
            return
        
        # 显示搜索进度
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, f"{self.lang_manager.get_text('searching')} '{query}'...\n\n", "info")
        self.text_display.config(state=tk.DISABLED)
        self.root.update()
        
        # 使用简单搜索算法
        results = []
        
        for row in self.df:
            for version in self.versions:
                text = row.get(version, '')
                if text:
                    matches = self.simple_search(text, query, self.case_sensitive.get())
                    if matches:
                        results.append({
                            'version': version,
                            'text': text,
                            'volume': int(row['VolumeSN']),
                            'chapter': int(row['ChapterSN']),
                            'verse': int(row['VerseSN']),
                            'match_count': len(matches)
                        })
        
        if results:
            # 显示搜索结果
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            
            self.text_display.insert(tk.END, f"{self.lang_manager.get_text('search_results')} '{query}' ({len(results)}):\n\n", "title")
            
            for i, result in enumerate(results[:100]):
                vol_name = self.get_volume_name(result['volume'], 'short')
                self.text_display.insert(tk.END, f"【{vol_name}{result['chapter']}:{result['verse']}】", "verse_ref")
                self.text_display.insert(tk.END, f" ({result['version']}) ", "version_tag")
                self.text_display.insert(tk.END, f" {result['text']}\n\n")
            
            if len(results) > 100:
                self.text_display.insert(tk.END, f"... {len(results) - 100} more results not shown", "info")
            
            self.text_display.config(state=tk.DISABLED)
        else:
            messagebox.showinfo(self.lang_manager.get_text('search_results'), 
                              f"{self.lang_manager.get_text('no_results')} '{query}'")
    
    def update_content(self):
        if not self.df:
            return
        
        volume_display = self.volume_var.get()
        chapter = self.chapter_var.get()
        verse_start = self.verse_start_var.get()
        verse_end = self.verse_end_var.get()
        
        if not all([volume_display, chapter, verse_start, verse_end]):
            return
        
        try:
            volume_sn = self.get_volume_sn_from_display(volume_display)
            chapter_num = int(chapter)
            verse_start_num = int(verse_start)
            verse_end_num = int(verse_end)
            
            # 获取指定范围的经文
            verses = [row for row in self.df 
                     if int(row['VolumeSN']) == volume_sn 
                     and int(row['ChapterSN']) == chapter_num 
                     and int(row['VerseSN']) >= verse_start_num 
                     and int(row['VerseSN']) <= verse_end_num]
            
            if not verses:
                self.text_display.config(state=tk.NORMAL)
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, self.lang_manager.get_text('no_results'))
                self.text_display.config(state=tk.DISABLED)
                return
            
            # 显示经文内容
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            
            # 添加标题
            vol_full_name = self.get_volume_name(volume_sn, 'full')
            self.text_display.insert(tk.END, f"{vol_full_name} {chapter_num}:{verse_start_num}-{verse_end_num}\n\n", "title")
            
            # 添加经文内容
            for verse in verses:
                verse_text = verse.get(self.current_version, '')
                if verse_text:
                    self.text_display.insert(tk.END, f"{verse['VerseSN']}. ", "verse_num")
                    self.text_display.insert(tk.END, f"{verse_text}\n\n")
            
            self.text_display.config(state=tk.DISABLED)
            
        except ValueError as e:
            print(f"Update content error: {e}")

def configure_styles(text_widget):
    text_widget.tag_configure("title", font=('Arial', 14, 'bold'), foreground='#2c3e50')
    text_widget.tag_configure("verse_num", font=('Arial', 12, 'bold'), foreground='#e74c3c')
    text_widget.tag_configure("verse_ref", font=('Arial', 10, 'italic'), foreground='#7f8c8d')
    text_widget.tag_configure("version_tag", font=('Arial', 9), foreground='#3498db')
    text_widget.tag_configure("info", font=('Arial', 10), foreground='#7f8c8d')
    text_widget.tag_configure("highlight", background='#fff3cd')

if __name__ == "__main__":
    root = tk.Tk()
    app = BibleReader(root)
    configure_styles(app.text_display)
    root.mainloop()