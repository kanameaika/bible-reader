'\nCreated on Fri Oct  3 03:09:07 2025\n\n@author: xiaoleiwww\n'
_A4='verse_num'
_A3='version_tag'
_A2='verse_ref'
_A1='Root Directory'
_A0='title'
_z='info'
_y='#28a745'
_x='bold'
_w=False
_v='no_folder_selected'
_u='unknown_folder'
_t='searching'
_s='data_load_error'
_r='folder_not_exist'
_q='no_images_found'
_p='filename'
_o='folder_location'
_n='please_select_folder'
_m='warning'
_l='select_folder'
_k='ChapterSN'
_j='full'
_i='values'
_h='#4a7abc'
_g='language'
_f='no_results'
_e='search_results'
_d='view_images'
_c='case_sensitive'
_b='verse_range'
_a='change_folder'
_Z='next_image'
_Y='prev_image'
_X='current_folder'
_W='image_viewer'
_V='manual_select'
_U='cancel'
_T='ok'
_S='available_folders'
_R='base_path'
_Q='app_title'
_P='utf-8'
_O='en'
_N='VerseSN'
_M='VolumeSN'
_L='to'
_K='search'
_J='chapter'
_I='volume'
_H='version'
_G='error'
_F='select_image_folder'
_E='white'
_D='root_directory'
_C=None
_B=True
_A='Arial'
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import os
from PIL import Image,ImageTk
import glob,csv,json
class LanguageManager:
	'语言管理器'
	def __init__(A,lang_file='lang.json'):A.lang_file=lang_file;A.current_lang=_O;A.languages={};A.callbacks=[];A.load_languages()
	def load_languages(A):
		'加载语言文件'
		try:
			if os.path.exists(A.lang_file):
				with open(A.lang_file,'r',encoding=_P)as B:A.languages=json.load(B)
			else:A.create_default_language_file()
		except Exception as C:messagebox.showerror('Error',f"无法加载语言文件: {str(C)}");A.create_default_language_file()
	def create_default_language_file(A):
		'创建默认语言文件';B='loading';A.languages={_O:{_Q:'Bible Reader',_l:'Select Folder',_F:'Select Image Folder',_R:'Base Path',_S:'Available Folders',_T:'OK',_U:'Cancel',_V:'Manual Select Folder',_m:'Warning',_n:'Please select a folder',_W:'Image Viewer',_X:'Current Folder',_o:'Folder Location',_p:'Filename',_Y:'Previous',_Z:'Next',_a:'Change Folder',_q:'No images found in folder',_G:'Error',_r:'Folder does not exist',_H:'Version',_I:'Volume',_J:'Chapter',_b:'Verse Range',_L:_L,_K:'Search',_c:'Case Sensitive',_d:'View Images',_e:'Search Results',_f:'No results found',B:'Loading',_s:'Unable to load data files',_t:'Searching',_D:_A1,_u:'Unknown Folder',_v:'No folder selected',_g:'Language'},'zh':{_Q:'圣经阅读器',_l:'选择文件夹',_F:'选择图片文件夹',_R:'基础路径',_S:'可用的文件夹',_T:'确定',_U:'取消',_V:'手动选择文件夹',_m:'警告',_n:'请选择一个文件夹',_W:'图片查看器',_X:'当前文件夹',_o:'所在文件夹',_p:'文件名',_Y:'上一张',_Z:'下一张',_a:'切换文件夹',_q:'文件夹中未找到图片文件',_G:'错误',_r:'文件夹不存在',_H:'版本',_I:'卷',_J:'章',_b:'节范围',_L:'至',_K:'搜索',_c:'区分大小写',_d:'查看图片',_e:'搜索结果',_f:'未找到结果',B:'加载中',_s:'无法加载数据文件',_t:'正在搜索',_D:'根目录',_u:'未知文件夹',_v:'未选择文件夹',_g:'语言'}}
		try:
			with open(A.lang_file,'w',encoding=_P)as C:json.dump(A.languages,C,ensure_ascii=_w,indent=2)
		except Exception as D:print(f"无法创建语言文件: {str(D)}")
	def get_text(A,key):'获取当前语言的文本';B=A.languages.get(A.current_lang,A.languages[_O]);return B.get(key,key)
	def add_callback(A,callback):'添加语言改变回调函数';A.callbacks.append(callback)
	def remove_callback(A,callback):
		'移除语言改变回调函数';B=callback
		if B in A.callbacks:A.callbacks.remove(B)
	def set_language(A,lang_code):
		'设置当前语言';B=lang_code
		if B in A.languages:
			A.current_lang=B
			for C in A.callbacks:C()
			return _B
		return _w
	def get_available_languages(A):'获取可用的语言列表';return list(A.languages.keys())
	def get_language_display_names(A):'获取语言的显示名称';return{_O:'English','zh':'中文'}
class FolderSelector:
	'文件夹选择器'
	def __init__(A,parent,lang_manager,base_folder='pics'):A.parent=parent;A.lang_manager=lang_manager;A.base_folder=base_folder;A.selected_folder=_C;A.folders=[];A.lang_manager.add_callback(A.on_language_changed);A.scan_folders();A.create_selector_window()
	def on_language_changed(A):
		'语言改变时的回调'
		if hasattr(A,'selector_window')and A.selector_window.winfo_exists():A.update_ui_text()
	def update_ui_text(A):
		'更新UI文本';A.selector_window.title(A.lang_manager.get_text(_F));A.title_label.config(text=A.lang_manager.get_text(_F));A.path_label.config(text=f"{A.lang_manager.get_text(_R)}: {os.path.abspath(A.base_folder)}");A.list_label.config(text=f"{A.lang_manager.get_text(_S)}:");A.ok_button.config(text=A.lang_manager.get_text(_T));A.cancel_button.config(text=A.lang_manager.get_text(_U));A.manual_button.config(text=A.lang_manager.get_text(_V))
		if A.folders and A.folders[0]in[_A1,'根目录']:A.folder_listbox.delete(0);A.folder_listbox.insert(0,A.lang_manager.get_text(_D));A.folders[0]=A.lang_manager.get_text(_D)
	def scan_folders(A):
		'扫描pics文件夹中的所有子文件夹'
		if not os.path.exists(A.base_folder):os.makedirs(A.base_folder,exist_ok=_B);A.folders=[];return
		try:
			for B in os.listdir(A.base_folder):
				C=os.path.join(A.base_folder,B)
				if os.path.isdir(C):A.folders.append(B)
			A.folders.sort();A.folders.insert(0,A.lang_manager.get_text(_D))
		except Exception as D:messagebox.showerror(A.lang_manager.get_text(_G),f"扫描文件夹时出错: {str(D)}");A.folders=[A.lang_manager.get_text(_D)]
	def create_selector_window(A):
		'创建文件夹选择窗口';A.selector_window=tk.Toplevel(A.parent);A.selector_window.title(A.lang_manager.get_text(_F));A.selector_window.geometry('400x300');A.selector_window.transient(A.parent);A.selector_window.grab_set();B=tk.Frame(A.selector_window,padx=20,pady=20);B.pack(fill=tk.BOTH,expand=_B);A.title_label=tk.Label(B,text=A.lang_manager.get_text(_F),font=(_A,12,_x));A.title_label.pack(pady=10);A.path_label=tk.Label(B,text=f"{A.lang_manager.get_text(_R)}: {os.path.abspath(A.base_folder)}",font=(_A,9),fg='#777777');A.path_label.pack(pady=5);D=tk.Frame(B);D.pack(fill=tk.BOTH,expand=_B,pady=10);A.list_label=tk.Label(D,text=f"{A.lang_manager.get_text(_S)}:",font=(_A,10));A.list_label.pack(anchor=tk.W);E=tk.Frame(D);E.pack(fill=tk.BOTH,expand=_B,pady=5);F=tk.Scrollbar(E);F.pack(side=tk.RIGHT,fill=tk.Y);A.folder_listbox=tk.Listbox(E,yscrollcommand=F.set,font=(_A,10));A.folder_listbox.pack(fill=tk.BOTH,expand=_B);F.config(command=A.folder_listbox.yview)
		for G in A.folders:A.folder_listbox.insert(tk.END,G)
		if A.folders:A.folder_listbox.selection_set(0)
		C=tk.Frame(B);C.pack(fill=tk.X,pady=10);A.ok_button=tk.Button(C,text=A.lang_manager.get_text(_T),command=A.on_ok,bg=_y,fg=_E,font=(_A,10));A.ok_button.pack(side=tk.LEFT,padx=5);A.cancel_button=tk.Button(C,text=A.lang_manager.get_text(_U),command=A.on_cancel,bg='#6c757d',fg=_E,font=(_A,10));A.cancel_button.pack(side=tk.LEFT,padx=5);A.manual_button=tk.Button(C,text=A.lang_manager.get_text(_V),command=A.on_manual,bg=_h,fg=_E,font=(_A,10));A.manual_button.pack(side=tk.RIGHT,padx=5);A.folder_listbox.bind('<Double-Button-1>',lambda e:A.on_ok())
	def on_ok(A):
		'确定选择';B=A.folder_listbox.curselection()
		if B:
			C=A.folders[B[0]]
			if C==A.lang_manager.get_text(_D):A.selected_folder=A.base_folder
			else:A.selected_folder=os.path.join(A.base_folder,C)
			A.selector_window.destroy()
		else:messagebox.showwarning(A.lang_manager.get_text(_m),A.lang_manager.get_text(_n))
	def on_cancel(A):'取消选择';A.selected_folder=_C;A.selector_window.destroy()
	def on_manual(A):
		'手动选择文件夹';B=filedialog.askdirectory(title=A.lang_manager.get_text(_l),initialdir=A.base_folder)
		if B:A.selected_folder=B;A.selector_window.destroy()
	def get_selected_folder(A):'获取选择的文件夹';return A.selected_folder
class ImageViewer:
	'图片查看器'
	def __init__(A,parent,lang_manager,image_folder=_C):
		A.parent=parent;A.lang_manager=lang_manager;A.image_folder=image_folder;A.images=[];A.current_index=0;A.lang_manager.add_callback(A.on_language_changed)
		if not A.image_folder:A.select_folder()
		else:A.load_images();A.create_image_window()
	def on_language_changed(A):
		'语言改变时的回调'
		if hasattr(A,'image_window')and A.image_window.winfo_exists():A.update_ui_text()
	def update_ui_text(A):
		'更新UI文本';A.image_window.title(f"{A.lang_manager.get_text(_W)} - {os.path.basename(A.image_folder)}");A.folder_title_label.config(text=f"{A.lang_manager.get_text(_X)}: {A.image_folder}");A.prev_btn.config(text=A.lang_manager.get_text(_Y));A.next_btn.config(text=A.lang_manager.get_text(_Z));A.change_folder_btn.config(text=A.lang_manager.get_text(_a))
		if A.images:A.show_current_image()
	def select_folder(A):
		'选择图片文件夹';B=FolderSelector(A.parent,A.lang_manager);A.parent.wait_window(B.selector_window);C=B.get_selected_folder()
		if C:A.image_folder=C;A.load_images();A.create_image_window()
		else:messagebox.showinfo('Info',A.lang_manager.get_text(_v))
	def load_images(A):
		'加载图片文件列表'
		if not A.image_folder or not os.path.exists(A.image_folder):messagebox.showerror(A.lang_manager.get_text(_G),f"{A.lang_manager.get_text(_r)}: {A.image_folder}");return
		A.images.clear();A.current_index=0;B=['*.jpg','*.jpeg','*.png','*.gif','*.bmp','*.tiff']
		for C in B:D=os.path.join(A.image_folder,'**',C);E=glob.glob(D,recursive=_B);A.images.extend(E)
		A.images=list(set(A.images));A.images.sort()
	def get_folder_info(A,image_path):
		'获取图片的文件夹信息';B=image_path
		if not A.image_folder:return A.lang_manager.get_text(_u)
		try:
			D=os.path.relpath(B,A.image_folder);C=os.path.dirname(D)
			if C=='.':return A.lang_manager.get_text(_D)
			else:return C
		except:return os.path.dirname(B)
	def create_image_window(A):
		'创建图片查看窗口';E='#e8f4fd'
		if not A.images:messagebox.showinfo('Info',f"{A.lang_manager.get_text(_q)}: '{A.image_folder}'");return
		A.image_window=tk.Toplevel(A.parent);A.image_window.title(f"{A.lang_manager.get_text(_W)} - {os.path.basename(A.image_folder)}");A.image_window.geometry('900x700');A.image_window.protocol('WM_DELETE_WINDOW',A.on_window_close);D=tk.Frame(A.image_window,bg=E);D.pack(fill=tk.X,padx=10,pady=5);A.folder_title_label=tk.Label(D,text=f"{A.lang_manager.get_text(_X)}: {A.image_folder}",font=(_A,9),bg=E,fg='#2c3e50');A.folder_title_label.pack(anchor=tk.W);A.image_frame=tk.Frame(A.image_window);A.image_frame.pack(fill=tk.BOTH,expand=_B,padx=10,pady=10);A.image_label=tk.Label(A.image_frame);A.image_label.pack(fill=tk.BOTH,expand=_B);C=tk.Frame(A.image_window);C.pack(fill=tk.X,padx=10,pady=5);A.folder_label=tk.Label(C,text='',font=(_A,10),bg='#f0f0f0',padx=10,pady=5,wraplength=800);A.folder_label.pack(fill=tk.X);A.filename_label=tk.Label(C,text='',font=(_A,9),fg='#777777',padx=10,pady=2);A.filename_label.pack(fill=tk.X);B=tk.Frame(A.image_window);B.pack(fill=tk.X,padx=10,pady=5);A.prev_btn=tk.Button(B,text=A.lang_manager.get_text(_Y),command=A.prev_image,bg=_h,fg=_E,font=(_A,10));A.prev_btn.pack(side=tk.LEFT,padx=5);A.next_btn=tk.Button(B,text=A.lang_manager.get_text(_Z),command=A.next_image,bg=_h,fg=_E,font=(_A,10));A.next_btn.pack(side=tk.LEFT,padx=5);A.change_folder_btn=tk.Button(B,text=A.lang_manager.get_text(_a),command=A.change_folder,bg=_y,fg=_E,font=(_A,10));A.change_folder_btn.pack(side=tk.LEFT,padx=20);A.counter_label=tk.Label(B,text='',font=(_A,10));A.counter_label.pack(side=tk.LEFT,padx=20);A.show_current_image()
	def on_window_close(A):'窗口关闭时的清理工作';A.cleanup();A.image_window.destroy()
	def cleanup(A):
		'清理资源';A.images.clear();A.current_index=0
		if hasattr(A,'image_label')and hasattr(A.image_label,'image'):A.image_label.image=_C
	def change_folder(A):'切换文件夹';A.cleanup();A.image_window.destroy();A.select_folder()
	def show_current_image(A):
		'显示当前图片'
		if not A.images:return
		try:B=A.images[A.current_index];C=Image.open(B);E=850;F=500;C.thumbnail((E,F),Image.Resampling.LANCZOS);D=ImageTk.PhotoImage(C);A.image_label.configure(image=D);A.image_label.image=D;G=A.get_folder_info(B);A.folder_label.configure(text=f"{A.lang_manager.get_text(_o)}: {G}");H=os.path.basename(B);A.filename_label.configure(text=f"{A.lang_manager.get_text(_p)}: {H}");A.counter_label.configure(text=f"{A.current_index+1} / {len(A.images)}")
		except Exception as I:messagebox.showerror(A.lang_manager.get_text(_G),f"无法加载图片: {str(I)}")
	def next_image(A):
		'下一张图片'
		if A.images and A.current_index<len(A.images)-1:A.current_index+=1;A.show_current_image()
	def prev_image(A):
		'上一张图片'
		if A.images and A.current_index>0:A.current_index-=1;A.show_current_image()
class BibleReader:
	def __init__(A,root):A.root=root;A.lang_manager=LanguageManager();A.lang_manager.add_callback(A.on_language_changed);A.root.title(A.lang_manager.get_text(_Q));A.root.geometry('1200x800');A.root.configure(bg='#f5f5f5');A.load_data();A.create_widgets();A.update_content()
	def on_language_changed(A):'语言改变时的回调函数';A.root.title(A.lang_manager.get_text(_Q));A.update_ui_text()
	def update_ui_text(A):'更新所有UI组件的文本';A.lang_label.config(text=f"{A.lang_manager.get_text(_g)}:");A.version_label.config(text=f"{A.lang_manager.get_text(_H)}:");A.volume_label.config(text=f"{A.lang_manager.get_text(_I)}:");A.chapter_label.config(text=f"{A.lang_manager.get_text(_J)}:");A.verse_label.config(text=f"{A.lang_manager.get_text(_b)}:");A.verse_to_label.config(text=A.lang_manager.get_text(_L));A.search_label.config(text=f"{A.lang_manager.get_text(_K)}:");A.search_button.config(text=A.lang_manager.get_text(_K));A.case_check.config(text=A.lang_manager.get_text(_c));A.image_btn.config(text=A.lang_manager.get_text(_d));B=A.lang_manager.get_language_display_names();C=[f"{A} - {B}"for(A,B)in B.items()];A.lang_combo[_i]=C;D=f"{A.lang_manager.current_lang} - {B.get(A.lang_manager.current_lang,A.lang_manager.current_lang)}";A.lang_var.set(D);A.update_content()
	def load_data(A):
		'加载圣经数据和卷名数据';I='NIV';H='TCB';G='LCC';F='NCB';E='strjw'
		try:
			A.df=[]
			with open('csv/data.csv','r',encoding=_P)as C:
				D=csv.DictReader(C)
				for B in D:A.df.append(B)
			A.bibleid_df=[]
			with open('csv/bibleid.csv','r',encoding=_P)as C:
				D=csv.DictReader(C)
				for B in D:A.bibleid_df.append(B)
			A.volume_names={}
			for B in A.bibleid_df:J=int(B['SN']);A.volume_names[J]={'short':B['ShortName'],_j:B['FullName'],'chapters':int(B['ChapterNumber'])}
			if A.df:K=A.df[0];A.versions=[A for A in K.keys()if A in[E,F,G,H,I]]
			else:A.versions=[E,F,G,H,I]
			A.current_version=A.versions[0]if A.versions else E
		except Exception as L:messagebox.showerror(A.lang_manager.get_text(_G),f"{A.lang_manager.get_text(_s)}: {str(L)}");A.df=[];A.bibleid_df=[];A.volume_names={}
	def get_volume_name(B,volume_sn,name_type=_j):
		'根据卷SN获取卷名';A=volume_sn;A=int(A)
		if A in B.volume_names:return B.volume_names[A].get(name_type,f"Volume {A}")
		return f"Volume {A}"
	def create_widgets(A):
		F='<<ComboboxSelected>>';E='readonly';B='#ffffff';H=tk.Frame(A.root,bg='#f5f5f5');H.pack(fill=tk.BOTH,expand=_B,padx=10,pady=10);I=tk.Frame(H,bg=B,relief=tk.RAISED,bd=1);I.pack(fill=tk.X,pady=(0,10));C=tk.Frame(I,bg=B);C.pack(fill=tk.X,padx=5,pady=5);A.lang_label=tk.Label(C,text=f"{A.lang_manager.get_text(_g)}:",bg=B,font=(_A,10));A.lang_label.pack(side=tk.LEFT,padx=5);A.lang_var=tk.StringVar();L=A.lang_manager.get_language_display_names();P=[f"{A} - {B}"for(A,B)in L.items()];A.lang_combo=ttk.Combobox(C,textvariable=A.lang_var,values=P,state=E,width=12);A.lang_combo.pack(side=tk.LEFT,padx=5);A.lang_combo.bind(F,A.on_language_change);Q=f"{A.lang_manager.current_lang} - {L.get(A.lang_manager.current_lang,A.lang_manager.current_lang)}";A.lang_var.set(Q);A.version_label=tk.Label(C,text=f"{A.lang_manager.get_text(_H)}:",bg=B,font=(_A,10));A.version_label.pack(side=tk.LEFT,padx=(20,5));A.version_var=tk.StringVar(value=A.current_version);M=ttk.Combobox(C,textvariable=A.version_var,values=A.versions,state=E);M.pack(side=tk.LEFT,padx=5);M.bind(F,A.on_version_change);A.volume_label=tk.Label(C,text=f"{A.lang_manager.get_text(_I)}:",bg=B,font=(_A,10));A.volume_label.pack(side=tk.LEFT,padx=(20,5));A.volumes=sorted(set(int(A[_M])for A in A.df))if A.df else[];G=[]
		for N in A.volumes:R=A.get_volume_name(N,_j);G.append(f"{N}. {R}")
		A.volume_var=tk.StringVar();A.volume_combo=ttk.Combobox(C,textvariable=A.volume_var,values=G,state=E,width=15);A.volume_combo.pack(side=tk.LEFT,padx=5);A.volume_combo.bind(F,A.on_volume_change);A.chapter_label=tk.Label(C,text=f"{A.lang_manager.get_text(_J)}:",bg=B,font=(_A,10));A.chapter_label.pack(side=tk.LEFT,padx=(20,5));A.chapters=[];A.chapter_var=tk.StringVar();A.chapter_combo=ttk.Combobox(C,textvariable=A.chapter_var,values=A.chapters,state=E,width=5);A.chapter_combo.pack(side=tk.LEFT,padx=5);A.chapter_combo.bind(F,A.on_chapter_change);A.image_btn=tk.Button(C,text=A.lang_manager.get_text(_d),command=A.open_image_viewer,bg=_y,fg=_E,font=(_A,10));A.image_btn.pack(side=tk.RIGHT,padx=5);D=tk.Frame(I,bg=B);D.pack(fill=tk.X,padx=5,pady=5);A.verse_label=tk.Label(D,text=f"{A.lang_manager.get_text(_b)}:",bg=B,font=(_A,10));A.verse_label.pack(side=tk.LEFT,padx=5);A.verse_start_var=tk.StringVar();A.verse_start_combo=ttk.Combobox(D,textvariable=A.verse_start_var,width=5,state=E);A.verse_start_combo.pack(side=tk.LEFT,padx=5);A.verse_start_combo.bind(F,A.on_verse_change);A.verse_to_label=tk.Label(D,text=A.lang_manager.get_text(_L),bg=B,font=(_A,10));A.verse_to_label.pack(side=tk.LEFT,padx=5);A.verse_end_var=tk.StringVar();A.verse_end_combo=ttk.Combobox(D,textvariable=A.verse_end_var,width=5,state=E);A.verse_end_combo.pack(side=tk.LEFT,padx=5);A.verse_end_combo.bind(F,A.on_verse_change);A.search_label=tk.Label(D,text=f"{A.lang_manager.get_text(_K)}:",bg=B,font=(_A,10));A.search_label.pack(side=tk.LEFT,padx=(20,5));A.search_var=tk.StringVar();O=tk.Entry(D,textvariable=A.search_var,width=20);O.pack(side=tk.LEFT,padx=5);O.bind('<Return>',A.on_search);A.search_button=tk.Button(D,text=A.lang_manager.get_text(_K),command=A.on_search,bg=_h,fg=_E,font=(_A,10));A.search_button.pack(side=tk.LEFT,padx=5);A.case_sensitive=tk.BooleanVar();A.case_check=tk.Checkbutton(D,text=A.lang_manager.get_text(_c),variable=A.case_sensitive,bg=B,font=(_A,9));A.case_check.pack(side=tk.LEFT,padx=10);J=tk.Frame(H,bg=B,relief=tk.SUNKEN,bd=1);J.pack(fill=tk.BOTH,expand=_B);K=tk.Scrollbar(J);K.pack(side=tk.RIGHT,fill=tk.Y);A.text_display=tk.Text(J,wrap=tk.WORD,yscrollcommand=K.set,font=(_A,12),bg=B,fg='#333333',padx=10,pady=10,spacing1=5,spacing2=2,spacing3=5);A.text_display.pack(fill=tk.BOTH,expand=_B);A.text_display.config(state=tk.DISABLED);K.config(command=A.text_display.yview)
		if G:A.volume_combo.set(G[0]);A.on_volume_change()
	def on_language_change(A,event=_C):
		'语言切换';B=A.lang_var.get()
		if B:C=B.split(' - ')[0];A.lang_manager.set_language(C)
	def get_volume_sn_from_display(B,display_value):
		'从显示文本中提取卷SN';A=display_value
		if'.'in A:return int(A.split('.')[0])
		return int(A)
	def open_image_viewer(A):'打开图片查看器';ImageViewer(A.root,A.lang_manager)
	def on_version_change(A,event=_C):A.current_version=A.version_var.get();A.update_content()
	def on_volume_change(A,event=_C):
		B=A.volume_var.get()
		if B:
			C=A.get_volume_sn_from_display(B);A.chapters=sorted(set(int(A[_k])for A in A.df if int(A[_M])==C));A.chapter_combo[_i]=A.chapters
			if A.chapters:A.chapter_combo.set(A.chapters[0]);A.on_chapter_change()
	def on_chapter_change(A,event=_C):
		C=A.volume_var.get();D=A.chapter_var.get()
		if C and D:
			E=A.get_volume_sn_from_display(C);B=sorted(set(int(A[_N])for A in A.df if int(A[_M])==E and int(A[_k])==int(D)));A.verse_start_combo[_i]=B;A.verse_end_combo[_i]=B
			if B:A.verse_start_combo.set(B[0]);A.verse_end_combo.set(B[-1]);A.on_verse_change()
	def on_verse_change(A,event=_C):A.update_content()
	def simple_search(F,text,pattern,case_sensitive=_w):
		'简单的字符串搜索';B=pattern;A=text
		if not case_sensitive:A=A.lower();B=B.lower()
		D=[];E=0
		while _B:
			C=A.find(B,E)
			if C==-1:break
			D.append(C);E=C+1
		return D
	def on_search(A,event=_C):
		J='verse';I='text';C=A.search_var.get().strip()
		if not C:return
		A.text_display.config(state=tk.NORMAL);A.text_display.delete(1.,tk.END);A.text_display.insert(tk.END,f"{A.lang_manager.get_text(_t)} '{C}'...\n\n",_z);A.text_display.config(state=tk.DISABLED);A.root.update();B=[]
		for E in A.df:
			for G in A.versions:
				F=E.get(G,'')
				if F:
					H=A.simple_search(F,C,A.case_sensitive.get())
					if H:B.append({_H:G,I:F,_I:int(E[_M]),_J:int(E[_k]),J:int(E[_N]),'match_count':len(H)})
		if B:
			A.text_display.config(state=tk.NORMAL);A.text_display.delete(1.,tk.END);A.text_display.insert(tk.END,f"{A.lang_manager.get_text(_e)} '{C}' ({len(B)}):\n\n",_A0)
			for(L,D)in enumerate(B[:100]):K=A.get_volume_name(D[_I],'short');A.text_display.insert(tk.END,f"【{K}{D[_J]}:{D[J]}】",_A2);A.text_display.insert(tk.END,f" ({D[_H]}) ",_A3);A.text_display.insert(tk.END,f" {D[I]}\n\n")
			if len(B)>100:A.text_display.insert(tk.END,f"... {len(B)-100} more results not shown",_z)
			A.text_display.config(state=tk.DISABLED)
		else:messagebox.showinfo(A.lang_manager.get_text(_e),f"{A.lang_manager.get_text(_f)} '{C}'")
	def update_content(A):
		if not A.df:return
		B=A.volume_var.get();C=A.chapter_var.get();D=A.verse_start_var.get();E=A.verse_end_var.get()
		if not all([B,C,D,E]):return
		try:
			F=A.get_volume_sn_from_display(B);G=int(C);H=int(D);I=int(E);J=[A for A in A.df if int(A[_M])==F and int(A[_k])==G and int(A[_N])>=H and int(A[_N])<=I]
			if not J:A.text_display.config(state=tk.NORMAL);A.text_display.delete(1.,tk.END);A.text_display.insert(tk.END,A.lang_manager.get_text(_f));A.text_display.config(state=tk.DISABLED);return
			A.text_display.config(state=tk.NORMAL);A.text_display.delete(1.,tk.END);M=A.get_volume_name(F,_j);A.text_display.insert(tk.END,f"{M} {G}:{H}-{I}\n\n",_A0)
			for K in J:
				L=K.get(A.current_version,'')
				if L:A.text_display.insert(tk.END,f"{K[_N]}. ",_A4);A.text_display.insert(tk.END,f"{L}\n\n")
			A.text_display.config(state=tk.DISABLED)
		except ValueError as N:print(f"Update content error: {N}")
def configure_styles(text_widget):B='#7f8c8d';A=text_widget;A.tag_configure(_A0,font=(_A,14,_x),foreground='#2c3e50');A.tag_configure(_A4,font=(_A,12,_x),foreground='#e74c3c');A.tag_configure(_A2,font=(_A,10,'italic'),foreground=B);A.tag_configure(_A3,font=(_A,9),foreground='#3498db');A.tag_configure(_z,font=(_A,10),foreground=B);A.tag_configure('highlight',background='#fff3cd')
if __name__=='__main__':root=tk.Tk();app=BibleReader(root);configure_styles(app.text_display);root.mainloop()
