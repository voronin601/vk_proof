from tkinter import PanedWindow, Button, Label, Text, Radiobutton, RIGHT, BOTTOM, X, Y, HORIZONTAL, CENTER, NO, END, VERTICAL, IntVar, Tk, Entry, Menu, Frame, Scrollbar, YES, BOTH, WORD
import vk_api
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import re
import threading
import json
import requests
import socket
import datetime

vse = []
pol = []
gr = []

class Table(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = ttk.Treeview(self, show="headings", selectmode="browse")
        scrolltabley = ttk.Scrollbar(self, command = self.table.yview, orient = VERTICAL)
        scrolltablex = ttk.Scrollbar(self, command = self.table.xview, orient = HORIZONTAL)

        self.table.configure(yscrollcommand = scrolltabley.set)
        self.table.configure(xscrollcommand = scrolltablex.set)

        scrolltabley.pack(side = RIGHT, fill = Y)
        scrolltablex.pack(side = BOTTOM, fill = X)

    def new(self, headings = [], rows = []):
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings
        for head in headings:
            self.table.heading(head, text = head, anchor = CENTER)
            self.table.column(head, width = 40, minwidth = 40, stretch = NO)
  
        for row in rows:
            self.table.insert('', END, values=tuple(row))

        self.table.pack(expand = YES, fill = BOTH)

class Authentication():
    def __init__(self):
        self.root1 = Tk()
        self.vk_session = ''
        l = Label(self.root1, text = 'Код подтверждения:')
        self.en = Entry(self.root1)
        b = Button(self.root1, text = 'Отправить код', command = self.prik)
        l.pack()
        self.en.pack()
        b.pack()
    
    def prik(self):
        self.root1.quit()

    def auth_handler(self):
        self.root1.mainloop()
        return self.en.get(), True

    def main(self, log = str(), pas = str(), l_4 = None):
        self.vk_session = vk_api.VkApi(
            log, pas,
            auth_handler = self.auth_handler
        )
        try:
            self.vk_session.auth()
            self.root1.destroy()
            l_4['text'] = self.vk_session.method('users.get')[0]['first_name'] + '\n' + self.vk_session.method('users.get')[0]['last_name']
            return None
        except vk_api.AuthError as error_msg:
            messagebox.showinfo("Ошибка!", error_msg)

class Grapfics():
    def __init__(self):
        self.aut = ''
        self.root = Tk()
        self.root.state('zoomed')
        self.root.geometry(str(self.root.winfo_screenwidth() - 200) + 'x' + str(self.root.winfo_screenheight() - 200))

        self.pb = ttk.Progressbar(self.root, orient = HORIZONTAL, length = 200, mode = 'determinate') 

        self.menu = Menu(self.root)
        self.menu.add_command(label = "О программе", command = self.prog_menu)

        self.root.config(menu = self.menu)

        self.l_1 = Label(self.root, text = "Авторизация в vk")
        self.l_2 = Label(self.root, text = "Формат списка")
        self.l_3 = Label(self.root, text = "Отчет")
        self.l_4 = Label(self.root, text = "Вы не авторизованы")
        self.l_5 = Label(self.root, text = "")

        self.en_1 = Entry(self.root)
        self.en_2 = Entry(self.root)

        self.pos_1 = IntVar()
        self.pos_1.set(0)
        self.rb_1 = Radiobutton(self.root, text = "1. http://vk.com/groupID http://vk.com/userID", variable = self.pos_1, value = 0)
        self.rb_2 = Radiobutton(self.root, text = "1. http://vk.com/userID http://vk.com/groupID", variable = self.pos_1, value = 1)

        pos_2 = IntVar()
        pos_2.set(0)
        self.rb_3 = Radiobutton(self.root, text = "По участникам", variable = pos_2, value = 0)
        self.rb_4 = Radiobutton(self.root, text = "По группам", variable = pos_2, value = 1)

        self.frame_1 = Frame(self.root)
        self.tex = Text(self.frame_1, width = 60, height = 35, font="Verdana 6",  wrap=WORD)
        self.scr = Scrollbar(self.frame_1, command = self.tex.yview)
        self.tex.configure(yscrollcommand = self.scr.set)
        
        self.splitter = PanedWindow(self.root, orient = HORIZONTAL, height = 500, width = 800)
        self.frame_2 = Frame(self.splitter, width = '20')
        self.table = Table(self.frame_2)
        self.table.pack(expand = YES, fill = BOTH)

        self.splitter.add(self.frame_2)
        
        self.scr.pack(side = 'right', fill = 'y')
        self.frame_1.place(x = '20', y = '205')
        self.tex.pack(fill = 'both')

        if os.path.exists('vk_config.v2.json'):
            with open('vk_config.v2.json', 'r') as t:
                q = json.load(t)
            for i in q.keys():
                log = i
                tok = str(q).split("'access_token': '")[1].split("'")[0]
            self.vk = vk_api.VkApi(login = log, token = tok)
            self.vk.auth(token_only = True)
            self.l_4['text'] = self.vk.method('users.get')[0]['first_name'] + '\n' + self.vk.method('users.get')[0]['last_name']

        self.b_1 = Button(self.root, text = "Войти", command = self.au)
        self.b_2 = Button(self.root, text = "Проверить вступления", width = 20, command = self.k)
        self.b_3 = Button(self.root, text = "Отчет", width = 20, command = lambda: Otch().start())
        self.b_4 = Button(self.root, text = "Выход", command = self.ex)

        self.splitter.place(x = '450', y = '205')
        self.en_1.place(x = '20', y = '55')
        self.en_2.place(x = '20', y = '80')

        self.b_1.place(x = '170', y = '50')
        self.b_2.place(x = '350', y = '140')
        self.b_3.place(x = '350', y = '170')
        self.b_4.place(x = '170', y = '80')

        self.l_1.place(x = '20', y = '30')
        self.l_2.place(x = '20', y = '120')
        #self.l_3.place(x = '550', y = '120')
        self.l_4.place(x = '220', y = '55')

        self.rb_1.place(x = '20', y = '140')
        self.rb_2.place(x = '20', y = '160')

        #self.rb_3.place(x = '550', y = '140')
        #self.rb_4.place(x = '550', y = '160')

        self.pb.place(x = '20', y = '650')
        self.l_5.place(x = '225', y = '650')

        self.root.mainloop()

    def k(self):
        self.l_5['text'] = ""
        self.table.destroy()
        self.table = Table(self.frame_2)
        self.table.pack(expand = YES, fill = BOTH)
        if os.path.exists('vk_config.v2.json'):
            if requests.get('http://3.12.164.15/table/%s' %str(self.vk.method('users.get')[0]['id'])).text == 'True':
                x = threading.Thread(target = st, args = (self.pos_1.get(), self.tex.get('1.0', 'end'), self.vk, self.table, self.l_5, self.pb))
                x.start()
            else: messagebox.showinfo("Ошибка!", "К вашему аккаунту не привязан ключ для работы программы\nОбратитесь по ссылке: https://vk.com/id124569304")
        else:
            if requests.get('http://3.12.164.15/table/%s' %str(self.aut.vk_session.method('users.get')[0]['id'])).text == 'True':
                x = threading.Thread(target = st, args = (self.pos_1.get(), self.tex.get('1.0', 'end'), self.aut.vk_session, self.table, self.l_5, self.pb))
                x.start()
            else: messagebox.showinfo("Ошибка!", "К вашему аккаунту не привязан ключ для работы программы\nОбратитесь по ссылке: https://vk.com/id124569304")

    def ex(self):
        if os.path.exists('vk_config.v2.json'):
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vk_config.v2.json'))
        self.l_4['text'] = "Вы не аторизованы"

    def au(self):
        if not os.path.exists('vk_config.v2.json'):
            self.aut = Authentication()
            self.aut.main(self.en_1.get(), self.en_2.get(), self.l_4)
        else:messagebox.showinfo("Ошибка!", "Для повторной авторизации нужно выйти из нынешнего аккаунта")

    def prog_menu(self):
        self.pr = Tk()
        self.pr.geometry('500x150')

        self.l1_1 = Label(self.pr, text = "Программа сделана для осуществление проверки подписки пользователей\n\n    Разработчик программы:\nvk - https://vk.com/id310539944\nПочта - vovavoronin1999@gmail.com")

        self.l1_1.place(x = '20', y = '20')

        self.pr.mainloop()

class Otch():
    def __init__(self):
        self.ot = Tk()
        self.ot.geometry('520x500')

        self.l_1 = Label(self.ot, text = 'Первый отчет')
        self.l_2 = Label(self.ot, text = 'Второй отчет')

        self.b_1 = Button(self.ot, text = 'Download', command = lambda: self.dow_one())
        self.b_2 = Button(self.ot, text = 'Download', command = lambda: self.dow_two())

        self.Fr1 = Frame(self.ot)
        self.Fr2 = Frame(self.ot)

        self.l_1.place(x = '10', y = '10')
        self.l_2.place(x = '260', y = '10')

        self.b_1.place(x = '100', y = '10')
        self.b_2.place(x = '350', y = '10')

        self.tex_1 = Text(self.Fr1, width = 45, height = 40, font="Verdana 6",  wrap=WORD)
        self.scr_1 = Scrollbar(self.Fr1, command = self.tex_1.yview)
        self.tex_1.configure(yscrollcommand = self.scr_1.set)
        self.scr_1.pack(side = 'right', fill = 'y')
        self.Fr1.place(x = '10', y = '40')
        self.tex_1.pack(fill = 'both')

        self.tex_2 = Text(self.Fr2, width = 45, height = 40, font="Verdana 6",  wrap=WORD)
        self.scr_2 = Scrollbar(self.Fr2, command = self.tex_2.yview)
        self.tex_2.configure(yscrollcommand = self.scr_2.set)
        self.scr_2.pack(side = 'right', fill = 'y')
        self.Fr2.place(x = '260', y = '40')
        self.tex_2.pack(fill = 'both')

        global vse
        global gr
        global pol

        self.vs = vse
        self.group = gr
        self.pols = pol

    def start(self):
        st1 = ''
        st2 = ''

        for idd, i in enumerate(self.pols):
            if "NO" in self.vs[idd]:
                st1 += i + " BLOCKED\n"
            if "-" in self.vs[idd][1:]:
                st1 += "Пользователь " + i + " не вступил в группы:\n"
                for idd_1, j in enumerate(self.vs[idd][1:]):
                    if j == "-":
                        st1 +=  "   " + self.group[idd_1] + "\n"
            st1 += '\n'
        if st1 == '': st1 = "Нет не подписавшихся"

        for idd, i in enumerate(self.group):
            tr = True
            for j in self.vs:
                if j[idd+1] == '-':
                    if tr == True:
                        st2 += "В сообщество " + i + " не вступили люди от этих пабликов:\n"
                        tr = False
                    for q in self.group:
                        if j[0] == q.split(' ')[0]:
                            st2 += "   " + q + "\n"
                            break
            st2 += "\n"

        if st2 == '': st2 = "Нет не подписавшихся"

        self.tex_1.insert(1.0, st1)
        self.tex_2.insert(1.0, st2)
        self.ot.mainloop()

    def dow_one(self):
        name = "1var_" + str(datetime.datetime.now().day) + "_" + str(datetime.datetime.now().month) +  "_" + str(datetime.datetime.now().year) + "__" + str(datetime.datetime.now().hour) + "_" + str(datetime.datetime.now().minute) + ".txt"
        t = open(name, 'w')
        t.write(self.tex_1.get('1.0', 'end'))
        t.close()

    def dow_two(self):
        name = "2var_" + str(datetime.datetime.now().day) + "_" + str(datetime.datetime.now().month) +  "_" + str(datetime.datetime.now().year) + "__" + str(datetime.datetime.now().hour) + "_" + str(datetime.datetime.now().minute) + ".txt"
        t = open(name, 'w')
        t.write(self.tex_2.get('1.0', 'end'))
        t.close()
        

def progress(pb, k):
    pb['value'] = k

def st(typ, tex, vk, table, l_5, pb):
    global gr
    global pol
    for a in tex.split('\n'):
        i = re.sub(r'\s+', ' ', a)
        if i != ' ' and i != '':
            if i[0] == ' ': i = i[1:]
            if i[-1] == ' ': i = i[:-1]
        if i.count('vk.com/') == 1:
            if typ == 0:
                gr.append(i.split(' ')[0] + ' ' + i.split(' ')[1])
            if typ == 1:
                pol.append(i.split(' ')[0] + ' ' + i.split(' ')[1])
        if i.count('vk.com/') == 2:
            if typ == 0:
                gr.append(i.split(' ')[0] + ' ' + i.split(' ')[1])
                pol.append(i.split(' ')[0] + ' ' + i.split(' ')[len(i.split(' '))-1])
            if typ == 1:
                pol.append(i.split(' ')[0] + ' ' + i.split(' ')[1])
                gr.append(i.split(' ')[0] + ' ' + i.split(' ')[len(i.split(' '))-1])
    abc = [i.split(' ')[0] for i in gr]
    abc.insert(0, 'user/group')
    proof(vk, pol, gr, abc, table, l_5, pb)

def id_club(idd, vk):
    return int(vk.method('groups.getById', values = {'group_ids':idd})[0]['id'])

def id_user(idd, vk):
    return int(vk.method('users.get', values = {'user_ids':idd})[0]['id'])

def proof(vk, pols, group, abc, table, l_5, pb):
    global vse
    for idd, i in enumerate(pols):
        vse.append([i.split(' ')[0]])
        l_5['text'] = i
        if 'is_closed' in vk.method('users.get', values = {'user_ids':i.split('/')[len(i.split('/'))-1]})[0]:
            if vk.method('users.get', values = {'user_ids':i.split('/')[len(i.split('/'))-1]})[0]['is_closed'] == False:
                spis = vk.method('groups.get', values = {'user_id':id_user(i.split('/')[len(i.split('/'))-1], vk)})['items']
                for j in group:
                    if id_club(j.split('/')[len(j.split('/'))-1], vk) in spis:
                        vse[idd].append('+')
                    else:
                        vse[idd].append('-')
                    progress(pb, (100/(len(pols))) * (idd+1))
            else:
                for j in group:
                    vse[idd].append('BLOCKED')
                    progress(pb, (100/(len(pols))) * (idd+1))
        else:
            for j in group:
                vse[idd].append('DELETED')
                progress(pb, (100/(len(pols))) * (idd+1))
    table.new(headings = abc, rows = vse)
    l_5['text'] = "Завершено"

if __name__ == "__main__":
    try:
        socket.gethostbyaddr('www.yandex.ru')
        v = '1.0'                                   ###Поменять версию
        if requests.get('http://3.12.164.15/download/%s' %v).text == 'True':
            Grapfics()
        else: 
            messagebox.showinfo("Предупреждение", "Доступна новая версия приложения по ссылке\nhttp://3.12.164.15/download")
            Grapfics()
    except socket.gaierror:
        messagebox.showinfo("Ошибка!", "Нет доступа к интернету")