from tkinter import *
import main as DataExport
import string
import json
import time
import datetime
import threading


valid_chars = "!£$^&()_+{}@~¬`-=[];'#,. %s%s" % (string.ascii_letters, string.digits)

root = Tk()


BtnColor = "#009ACD"
BtnColor_active = "#00688B"
WndColor = "#1E1E1E"


settings = DataExport.settings()

#MainFrame = Frame(root, width=60, height=20, bg="black")

#TxtFieldsFrame = Frame(root, width=1000, height=100)
#TxtFieldsFrame.grid(row=0)



UsernameLbl = Label(root, text="Username", font=12, fg="white", bg=WndColor)
UsernameLbl.grid(row=0, sticky=E, pady=10, padx=10)
UsernameEnt = Entry(root, width=50, bd=0, font=12)
UsernameEnt.grid(row=0, column=1, pady=10, padx=10)
UsernameEnt.insert(0, settings['username'])
FilenameLbl = Label(root, text="Filename", font=12, fg="white", bg=WndColor)
FilenameLbl.grid(row=1, sticky=E, pady=10, padx=10)
FilenameEnt = Entry(root, width=50, bd=0, font=12)
FilenameEnt.grid(row=1, column=1, pady=10, padx=10)
FilenameEnt.insert(0, settings['filename'])


#BtnFrame = Frame(root, width=1000, height=100)
#BtnFrame.grid(row=1)


def conv_filename(filename, username):
    
    if filename != '':
        if filename[-5:] == '.json':
            pass
        else:
            filename += '.json'
        #
        filename = ''.join(c for c in filename if c in valid_chars)
    elif filename == '':
        usernameEdit = ''.join(c for c in username if c in valid_chars)
        filename = usernameEdit + ' scrobbles.json'
    
    return filename
#

def playcountLbl():
    
    username = UsernameEnt.get()
    filename = conv_filename(FilenameEnt.get(), username)
    
    listensFile = json.loads(open(filename, 'r').read())
    
    totalPlaycount = listensFile['total playcount']
    
    print(totalPlaycount)
    
    
    return totalPlaycount
#

def start_over():
    
    settings_filename = 'lastfm data settings.json'
    
    username = UsernameEnt.get()
    filename = conv_filename(FilenameEnt.get(), username)
    
    
    if username == '':
        label_txt = 'Username is a required field'
        txt.set(label_txt)
        settings['username'] = username
        settings['filename'] = filename
        json.dump(settings, open(settings_filename, 'w'))
    else:
        txt.set('')
        settings['username'] = username
        settings['filename'] = filename
        json.dump(settings, open(settings_filename, 'w'))
        DataExport.get_tracks(username, 0, 200, filename)
        txt_TotalPlaycount.set(playcountLbl())
#
def update():
    
    settings_filename = 'lastfm data settings.json'
    
    username = UsernameEnt.get()
    filename = FilenameEnt.get()
    
    if filename != '':
        if filename[-5:] == '.json':
            pass
        else:
            filename += '.json'
        #
        filename = ''.join(c for c in filename if c in valid_chars)
    elif filename == '':
        usernameEdit = ''.join(c for c in username if c in valid_chars)
        filename = usernameEdit + ' scrobbles.json'
    
    
    if username == '':
        label_txt = 'Username is a required'
        txt.set(label_txt)
        settings['username'] = username
        settings['filename'] = filename
        json.dump(settings, open(settings_filename, 'w'))
    else:
        txt.set('')
        settings['username'] = username
        settings['filename'] = filename
        json.dump(settings, open(settings_filename, 'w'))
        before = playcountLbl()
        DataExport.update(filename)
        after = playcountLbl()
        tracksAdded = after - before
        txt_TracksAdded.set(tracksAdded)
        txt_TotalPlaycount.set(after)
#
def sec_to_min(second):
    sec = datetime.timedelta(seconds=int(second))
    d = datetime.datetime(1,1,1) + sec
    time = "{minutes}:{seconds}".format(minutes=d.minute, seconds=d.second)
    if len(time[time.index(":")+1:]) == 1:
        if d.second == 0:
            time += '0'
        elif d.second >> 0:
            time = time[:-1] + "0" + time[-1:]
    #
    
    return time
#
def idle():
    print(IdleVar.get())
    
    t = 10 * 60
    
    while IdleVar.get() == True:
        for i in range(t,0,-1):
            txt_idle.set(sec_to_min(i))
            #print(i)
            time.sleep(1)
            if IdleVar.get() == False:
                break
                #idleThread.join()
        update()
#
def idleThread():
    
    Thread = threading.Thread(target=idle)
    
    if IdleVar.get() == True:
        Thread.start()
    elif IdleVar.get() == False:
        txt_idle.set('')
        #Thread.join()
        
    '''
    try:
        idleThread.join()
    except RuntimeError as e:
        if e == "cannot join current thread":
            pass
        
    
    '''
#

txt = StringVar()
UsernameLbl_2 = Label(root, textvariable=txt, font=12, bg=WndColor, fg="red").grid(row=2, columnspan=2)

txt_idle = StringVar()
IdleLbl = Label(root, textvariable=txt_idle, font=("Helvetica", "50"), bg=WndColor, fg="red").grid(row=3, column=2, rowspan=2, columnspan=2)

TotalPlaycountTxtLbl = Label(root, text="Playcount", font=12, bg=WndColor, fg="white").grid(row=0, column=2, sticky=E)

txt_TotalPlaycount = StringVar()
TotalPlaycountNumLbl = Label(root, textvariable=txt_TotalPlaycount, font=12, bg=WndColor, fg="red", width=10).grid(row=0, column=3, sticky=E)

TracksAddedLbl = Label(root, text="Tracks Added", font=12, bg=WndColor, fg="white").grid(row=1, column=2, sticky=E)

txt_TracksAdded = StringVar()
TracksAddedNumLbl = Label(root, textvariable=txt_TracksAdded, font=12, bg=WndColor, fg="red", width=10).grid(row=1, column=3, sticky=E)

IdleVar = BooleanVar()
IdleBtn = Checkbutton(root, text="Idle", font=12, activebackground=WndColor, bg=WndColor, fg="white", variable=IdleVar, command=idleThread)
IdleBtn.grid(row=2, column=2, columnspan=2)

StartOverBtn = Button(root, text="Start over", width=50, height=2, font=12, activebackground=BtnColor_active, bg=BtnColor, bd=0, command=start_over)
StartOverBtn.grid(columnspan=2, row=3 , pady=5)


UpdateBtn = Button(root, text="Update", width=50, height=2, font=12, activebackground=BtnColor_active, bg=BtnColor, bd=0, command=update)
UpdateBtn.grid(columnspan=2, row=4, pady=10)


#MainFrame.grid()
root.configure(bg=WndColor)
root.mainloop()
