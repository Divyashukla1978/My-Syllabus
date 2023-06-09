from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton,MDRectangleFlatButton,MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard , MDSeparator
from kivy.properties import StringProperty , DictProperty
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem,TwoLineListItem, ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.utils import asynckivy as ak

from kivy.core.audio import SoundLoader
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivy.base import EventLoop


import os 
from os import path
import sys
import time
try:
    from datetime import datetime
except:
    toast('Module import error')
import shutil
import logging
import json
from plyer import sms
from plyer import notification
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


from database import *

def hist(file,text):
    if not os.path.exists('Setting Data/pause_all_search.txt'):
        if os.path.exists('Setting Data/pause_search.txt'):
            type_search = False
        else:
            type_search = True
        ct = time.localtime()
        dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
        tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
        dt = f'Date-{dt} Time-{tt}'
        if file == 'Searched' and type_search == False:
            pass
        else:      
            with open(f'Setting Data/History/{text}.txt','w') as f:
                f.write(f'{file}$$&&$${dt}')
    else:
        pass      
        
MData = {}
def make_data():
    try:
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/data.json"):        
            with open('/storage/emulated/0/Documents/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open('/storage/emulated/0/Documents/My Syllabus/data.json', 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        toast(f'{e}')
        return {}
        
def make_data_note():
    try:
        if os.path.exists("/storage/emulated/0/Documents/My Syllabus/note_data.json"):        
            with open('/storage/emulated/0/Documents/My Syllabus/note_data.json', 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open("/storage/emulated/0/Documents/My Syllabus/note_data.json","w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open('/storage/emulated/0/Documents/My Syllabus/note_data.json', 'r') as openfile:
                MData = json.load(openfile)
        return MData
    except Exception as e:
        toast(f'{e}')
        return {}

def write_data(data):
    try:
        with open("/storage/emulated/0/Documents/My Syllabus/data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')

def write_data_note(data):
    try:
        with open("/storage/emulated/0/Documents/My Syllabus/note_data.json","w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        toast(f'{e}')


class NewChapterBox(BoxLayout):
    pass
class SendReportBox(BoxLayout):
    pass
    
    
class TasksPage(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True
            
    def enter(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        try:
            try:
                self.ids.grid.clear_widgets()
            except:
                pass
            self.task_clk = {}
            if os.path.exists('tasks.json'):
                with open('tasks.json', 'r') as openfile:
                    data = json.load(openfile)
                
                if data == {}:
                    self.ids.grid.add_widget(MDLabel(text='No Task is there add some now',font_style='H3',halign='center',size_hint_y=None,height=300))
                else:
                    for task in data:
                        card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal",on_release=self.task_complete)
                        card2.add_widget(MDLabel(text=f'{task}',halign='center',bold=True))
                        if data[task] == True:
                            card2.add_widget(Image(source='tick.jpg'))
                        else:
                            card2.add_widget(Image(source='wrong.jpg'))
                        self.ids.grid.add_widget(card2)
                        self.task_clk[str(card2)] = f'{task}'
            else:
                self.ids.grid.add_widget(MDLabel(text='No Task Is There Add Some Now',font_style='H3',halign='center',size_hint_y=None,height=300))

        except Exception as e:
            toast(f'{e}')           
            
    def task_complete(self, inst):
        task = self.task_clk[str(inst)]
        self.chap_update_dia = MDDialog(
        title="Task Update",
        text=f'Do you want to update or remove the {task} Task',
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchapup),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.remtask(task,*args)),
            MDRaisedButton(text="UPDATE",on_release= lambda *args: self.task_update(task,*args))])
        self.chap_update_dia.open()
    
    def canchapup(self, obj):
        self.chap_update_dia.dismiss()
        
    def remtask(self, task, obj):
        with open('tasks.json', 'r') as openfile:
            data = json.load(openfile)
        data.pop(task)
        with open('tasks.json', 'w') as f:
             data = json.dumps(data, indent=4)
             f.write(data)
        with open('opened.txt','w') as f:
             f.write('opened')
        self.enter()
        self.chap_update_dia.dismiss()
        hist('Removed a Task',f'Removed a task named {task}')
    
    def task_update(self, task, obj):
        with open('tasks.json', 'r') as openfile:
            data = json.load(openfile)
        if data[task] == True:
            data[task] = False
        else:
            data[task] = True
        with open('tasks.json', 'w') as f:
             data = json.dumps(data, indent=4)
             f.write(data)
        with open('opened.txt','w') as f:
             f.write('opened')
        self.enter()
        self.chap_update_dia.dismiss()
        hist('Updated a Task',f'Updated a task named {task}')
        
    def add_task(self, task):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as openfile:
                data = json.load(openfile)
            if task in data:
                toast('Task is already there')
            else:
                data.update({f'{task}':False})
                with open('tasks.json', 'w') as f:
                    data = json.dumps(data, indent=4)
                    f.write(data)
        else:
            with open('tasks.json', 'w') as f:
                data = {f'{task}':False}
                data = json.dumps(data, indent=4)
                f.write(data)
        with open('opened.txt','w') as f:
            f.write('opened')
        self.enter()
        self.ids.taskt.text = ''
        hist('Added a Task',f'Added a task named {task}')
    
    def home(self):
        self.manager.current = 'mainp'


class SubjectPage(Screen):    
    data = DictProperty()    
    def enter(self):
        global MData
        MData = make_data()        
        self.makepage()
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
            
    def makepage(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        with open('subject_open.txt','r') as f:
            sub = f.read()            
        self.ids.tbar.title = sub
        self.ids.grid.bind(minimum_height=self.ids.grid.setter('height'))
        self.data = {
            'New Chapter': ['book',"on_release" ,lambda x: self.newchap(sub)],
            }
        self.done_chaps = {}
        try:
            self.ids.grid.clear_widgets()
        except:
            pass
        self.subject_clk = {}
        
        card = MDCard(size_hint_y=None,height="600",orientation="vertical",md_bg_color='#f6eeee')       
        try:
            card.padding = (50,50)
        except:
            pass
        try:
            card.spacing = (0,50)
        except:
            pass
        card.add_widget(MDLabel(text=f'{sub}',halign='center',font_style='H3',underline=True))
        tot = MData[sub]["Data"]["total"]
        card.add_widget(MDLabel(text=f"Total Chapters = {tot}"))
        com = MData[sub]["Data"]["completed"]
        card.add_widget(MDLabel(text=f"Total Chapters Completed = {com}"))
        left = tot - com
        card.add_widget(MDLabel(text=f"Total Chapters Left = {left}"))        
        self.ids.grid.add_widget(card)
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='75'))
        self.ids.grid.add_widget(MDSeparator())
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='75'))
        
        for chapter in MData[sub]["Chapters"]:
            card2 = MDCard(size_hint_y=None,height="100",orientation="horizontal",on_release=self.chap_complete)
            card2.add_widget(MDLabel(text=f'{chapter}',halign='center',bold=True))
            if MData[sub]["Chapters"][f'{chapter}'] == True:
                card2.add_widget(Image(source='tick.jpg'))
            else:
                card2.add_widget(Image(source='wrong.jpg'))
            self.ids.grid.add_widget(card2)
            self.subject_clk[str(card2)] = f'{sub}$&${chapter}'
        
        self.ids.grid.add_widget(MDLabel(text='',size_hint_y=None,height='100'))    
        self.ids.grid.add_widget(MDSeparator())
        card = MDCard(size_hint_y=None,height="100",orientation="vertical",md_bg_color='red',on_release=self.go_to_top)
        card.add_widget(MDLabel(text=f'You have reached the end',halign='center',underline=True,italic=True,bold=True))
        self.ids.grid.add_widget(card)

############## Chapter update ###############
    def canchapup(self, obj):
        self.chap_update_dia.dismiss()
    
    def chap_complete(self, inst):
        line = self.subject_clk[str(inst)]
        sub = line.split('$&$')[0]
        chap = line.split('$&$')[-1]
        bottom_sheet_menu = MDListBottomSheet()
        
        bottom_sheet_menu.add_item(f"UPDATE",lambda  *args: self.chapter_update(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Tests",lambda  *args: self.test_show(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Notes",lambda  *args: self.notes_update(sub,chap ,*args))
        bottom_sheet_menu.add_item(f"Remove",lambda *args: self.remchap(sub, chap, *args))
        
        bottom_sheet_menu.open()
    
    def notes_update(self, sub, chapter, inst):
        with open('note_path.txt','w') as f:
            f.write(f'{sub}$$&&$${chapter}')
        self.manager.current = 'notep'
        
    def test_show(self, sub, chapter, inst):
        with open('text_files/test_chapter.txt','w') as f:
            f.write(f"{chapter}")
        with open('text_files/test_subject.txt','w') as f:
            f.write(f"{sub}")
        self.manager.current = 'testmenup'
        
    def chapter_update(self, sub, chapter, inst):
        if MData[sub]["Chapters"][f'{chapter}'] == True:
            MData[sub]["Chapters"][f'{chapter}'] = False
            MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
        else:
            MData[sub]["Chapters"][f'{chapter}'] = True
            MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) + 1
            Snackbar(text=f'Congratulations a chapter completed',md_bg_color='blue').open()
            toast('One step ahead towards your goal')
        write_data(MData)
        self.enter()
        with open('opened.txt','w') as f:
            f.write('opened')
        hiat('Updated a chapter',f'Updated a chapter named {chapter}')
        
    def newchap(self, sub):
        ccls=NewChapterBox()
        self.chap_dia = MDDialog(
        title="New Chapter",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchap),
            MDRaisedButton(text="Create",on_release= lambda *args: self.add_chapter(ccls,sub ,*args))])
        self.chap_dia.open()
    
    def add_chapter(self, content_cls , sub , inst):
        textfield = content_cls.ids.cname
        chapter = textfield._get_text()
        if chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter already exists")
        else:
            MData[f"{sub}"]["Chapters"].update({f"{chapter}":False})
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) + 1
            try:
                write_data(MData)
            except Exception as e:
                toast(f'{e}')        
            Snackbar(text=f"Chapter {chapter} created in {sub}").open()
            self.chap_dia.dismiss()
            with open('opened.txt','w') as f:
                f.write('opened')
            
    def canchap(self, inst):
        self.chap_dia.dismiss()   

    def remchap(self, sub, chap, inst):
        self.rem_chap = MDDialog(
        title="Remove Chapter",
        text=f"Do you want to remove the chapter named {chap}",
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canremchap),
            MDRaisedButton(text="Remove",md_bg_color='red',on_release= lambda *args: self.remove_chapter_final(sub,chap ,*args))
            ])
        self.rem_chap.open()
    
    def remove_chapter_final(self,sub ,chapter, obj):
        if not chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter does not exists")
        else:
            comp = MData[f"{sub}"]["Chapters"][f"{chapter}"]        
            MData[f"{sub}"]["Chapters"].pop(f"{chapter}")
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) - 1
            if comp == True:
                MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
            else:
                pass
            write_data(MData)
            self.rem_chap.dismiss()
            Snackbar(text=f"Chapter named {chapter} Removed",md_bg_color="red").open()
            self.enter()
            with open('opened.txt','w') as f:
                f.write('opened')
        
    def remove_chapter(self, content_cls , sub , inst):
        textfield = content_cls.ids.cname
        chapter = textfield._get_text()
        if not chapter in MData[f"{sub}"]["Chapters"]:
            toast("Chapter does not exists")
        else:
            comp = MData[f"{sub}"]["Chapters"][f"{chapter}"]        
            MData[f"{sub}"]["Chapters"].pop(f"{chapter}")
            MData[sub]["Data"]["total"] = int(MData[sub]["Data"]["total"]) - 1
            if comp == True:
                MData[sub]["Data"]["completed"] = int(MData[sub]["Data"]["completed"]) - 1
            else:
                pass
            write_data(MData)
            Snackbar(text=f"Chapter {chapter} Removed in {sub}").open()
            self.rem_chap.dismiss()
            with open('opened.txt','w') as f:
                f.write('opened')
            
    def canremchap(self, inst):
        self.rem_chap.dismiss()
     
    def go_to_top(self, inst):
        self.ids.scroll.scroll_y = 1
           
    def home(self):
        self.manager.current = 'mainp'
        
class ReportPage(Screen):
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.home()
            return True 
            
    def enter(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
        menu_items = [
            {"viewclass": "OneLineListItem","text": f"Home","height": dp(56),"on_release": lambda x=f"home": self.menu_callback(x)},
            {"viewclass": "OneLineListItem","text": f"Screen Shot","height": dp(56),"on_release": lambda x=f"getimg": self.menu_callback(x)},
            {"viewclass": "OneLineListItem","text": f"Copy To Clipboard","height": dp(56),"on_release": lambda x=f"copy": self.menu_callback(x)},
        ]
         
        self.menu = MDDropdownMenu(items=menu_items,width_mult=4,border_margin=dp(36),background_color='#33adff')
        with open('label.txt','r') as f:
            report_text = f.read()
            
        report_text = report_text.replace('&&$$&&','')
        self.ids.cont.text = report_text
    
    def menu_callback(self, item):
        self.menu.dismiss()
        item = str(item)
        if item == 'home':
            self.manager.current = 'mainp'
        elif item =='getimg':
            try:
                file_path='/storage/emulated/0/Documents/My Syllabus/report.png'
                self.ids.board.export_to_png(file_path)                
                toast('Image Captured and stored in My Syllabus folder')
            except Exception as e:
                toast(f'{e}')
        elif item == 'copy':
            from kivy.core.clipboard import Clipboard
            with open('report.txt','r') as f:
                text = f.read()
            Clipboard.copy(text)
            toast('Copyied to clipboard')        
        else:
            pass 
     
    def menu_open(self, button):
        async def open(self):
            self.menu.caller = button
            self.menu.open()
        ak.start(open(self))
        
    def home(self):
        self.manager.current = 'mainp'
        
class NotePage(Screen):
    def enter(self):
        Data = make_data_note()
        with open('note_path.txt','r') as f:
            path = f.read()
        sub = path.split('$$&&$$')[0]
        chap = path.split('$$&&$$')[-1]
        self.ids.tbar.title = chap       
        if sub in Data:
            if chap in Data[sub]:
                self.ids.main_text.text = Data[sub][chap]['note']
            else:
                self.ids.main_text.text = 'No Note Is There'
                Data[sub][chap] = {'note':'No Note Is There'}
                write_data_note(Data)
        else:
            Data[sub] = {}
            Data[sub][chap] = {'note':'No Note Is There'}
            self.ids.main_text.text = 'No Note Is There'
            write_data_note(Data)            
    
    def save(self):
        Data = make_data_note()
        with open('note_path.txt','r') as f:
            path = f.read()
        sub = path.split('$$&&$$')[0]
        chap = path.split('$$&&$$')[-1]
        Data[sub][chap] = {'note':str(self.ids.main_text.text)}
        write_data_note(Data)
    
    def share(self):
        text = self.ids.main_text.text
        try:
            from kvdroid.tools import share_text
            share_text(text, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
        
    def home(self):
        self.manager.current = 'subp'


class Setting(Screen):
    wh = Window.height
    ww = Window.width
    def home(self):
        self.manager.current = 'mainp'
    
    def dlset(self):
        if os.path.exists('Setting Data/dark_mode.txt'):
            return True
        else:
            return False
            
    def asset(self):
        if os.path.exists('Setting Data/app_style.txt'):
            return True
        else:
            return False
            
    def nrset(self):
        if os.path.exists('Setting Data/name_radius.txt'):
            return True
        else:
            return False
    
    def pausesearchset(self):
        if os.path.exists('Setting Data/pause_search.txt'):
            return True
        else:
            return False
            
    def pause_search(self, instance_switch, active_value: bool):
        if active_value == True:
            with open('Setting Data/pause_search.txt','w') as f:
                f.write('Pause search')
        else:
            os.remove('Setting Data/pause_search.txt')
            
    def pauseset(self):
        if os.path.exists('Setting Data/pause_all_search.txt'):
            return True
        else:
            return False
            
    def pause_all_search(self, instance_switch, active_value: bool):
        if active_value == True:
            with open('Setting Data/pause_all_search.txt','w') as f:
                f.write('Pause search')
        else:
            os.remove('Setting Data/pause_all_search.txt')

class HistoryPage(Screen):
    def enter(self):
        print('Entered History Page')
        lst = os.listdir('Setting Data/History/')
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
            
        if len(lst) > 100:
            toast('List too long wait a minute')
            for i in lst:
                if os.path.exists('Setting Data/name_radius.txt'):
                    rl = [25, 25, 25, 25]
                else:
                    rl = [0, 0, 0, 0]
                with open(f'Setting Data/History/{i}','r') as f:
                    sec = f.read()
                i = i.replace('.txt','')
                lst2 = i.split('$$&&$$')
                mt = lst2[0]
                dt = lst2[-1]
                self.ids.flist.add_widget(ThreeLineListItem(text=f"{mt}",secondary_text=f'{i}',tertiary_text=f'{dt}',bg_color='#d9d9d9',radius=rl,on_release=self.hopen))
        elif lst == []:
            if os.path.exists('Setting Data/name_radius.txt'):
                rl = [25, 25, 25, 25]
            else:
                rl = [0, 0, 0, 0]
            self.ids.flist.add_widget(TwoLineListItem(text=f"No History Is There",secondary_text=f'No History',bg_color='#d9d9d9',radius=rl))
        
        else:
            for i in lst:
                if os.path.exists('Setting Data/name_radius.txt'):
                    rl = [25, 25, 25, 25]
                else:
                    rl = [0, 0, 0, 0]
                with open(f'Setting Data/History/{i}','r') as f:
                    sec = f.read()
                i = i.replace('.txt','')
                lst2 = sec.split('$$&&$$')
                mt = lst2[0]
                dt = lst2[-1]
                self.ids.flist.add_widget(ThreeLineListItem(text=f"{mt}",secondary_text=f'{i}',tertiary_text=f'{dt}',bg_color='#d9d9d9',radius=rl,on_release=self.hopen))
    
        if os.path.exists('Setting Data/pause_all_search.txt'):
            try:
                self.ids.flist.clear_widgets()
            except:
                pass
            self.ids.flist.add_widget(OneLineListItem(text=f"Search History Is Paused",bg_color='#ff4d4d'))
        else:
            pass        
    
    def trash(self):
        self.trash_dia = MDDialog(
            title="Delete History",
            text='Do you want to delete all the history',
            width=Window.width-100,
            buttons=[
                MDFlatButton(text="Cancel",on_release= self.cancel),
                MDRaisedButton(text="Delete",on_release=self.deleteall)]
            )
        self.trash_dia.open()
        
    def cancel(self,obj):
        self.trash_dia.dismiss()
        
    def deleteall(self,obj):
        shutil.rmtree('Setting Data/History/')
        toast('History Deleted')
        os.mkdir('Setting Data/History/')
        self.enter()
        self.trash_dia.dismiss()
        Snackbar(text='All your history has been deleted',md_bg_color='red').open()
    
    def hopen(self, inst):
        query = inst.secondary_text
        bottom_sheet_menu = MDListBottomSheet()
        bottom_sheet_menu.add_item(f"Delete",lambda x, y=query: self.delhis(f"{y}"))
        bottom_sheet_menu.open()     
    
    def delhis(self, query):
        os.remove(f'Setting Data/History/{query}.txt')
        self.enter()
                
    def home(self):
        self.manager.current = 'mainp'