from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from tkinter import ttk as ttk
root=Tk()
root.title('Lallu MP3 Player')
p=PhotoImage(file='icon.png')
root.iconphoto(False,p)
root.geometry("500x450")
pygame.mixer.init()
def play_time():
	if stopped:
		return 
	cur_time=pygame.mixer.music.get_pos()/1000
	#sliderl.config(text=f'Slider: {int(myslider.get())} of Song Length : {int(cur_time)}')
	ccur_time=time.strftime('%M:%S',time.gmtime(cur_time))
	nextone=song_list.curselection()
	song=song_list.get(ACTIVE)
	song=f'E:/Python/MP3/audio/{song}.mp3'
	song_mut=MP3(song)
	global song_l
	song_l=song_mut.info.length
	csong_l=time.strftime('%M:%S',time.gmtime(song_l))
	cur_time+=1
	if(int(myslider.get())==int(song_l)):
		sb.config(text=f'Time Elapsed : {csong_l}')
		nextsong()
	elif paused:
		pass
	elif(int(cur_time)==int(myslider.get())):
		slider_p=int(song_l)
		myslider.config(to=slider_p,value=int(cur_time))
		sb.config(text=f'Time Elapsed : {ccur_time} of {csong_l}')
	else:
		slider_p=int(song_l)
		myslider.config(to=slider_p,value=int(myslider.get()))
		ccur_time=time.strftime('%M:%S',time.gmtime(myslider.get()))
		sb.config(text=f'Time Elapsed : {ccur_time} of {csong_l}')
		nt=myslider.get()+1
		myslider.config(value=nt)

	sb.after(1000,play_time)
def add_song():
	song= filedialog.askopenfilename(initialdir='audio/',title="Choose a Song", filetypes=(("mp3 types","*.mp3"),))
	print(song)
	song=song.replace("E:/Python/MP3/audio/","")
	print(song)
	song=song.replace(".mp3","")
	song_list.insert(END,song)
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/',title="Choose a Song", filetypes=(("mp3 types","*.mp3"),))
	for song in songs:
		song=song.replace("E:/Python/MP3/audio/","")
		song=song.replace(".mp3","")
		song_list.insert(END,song)

def playsong():
	global stopped
	stopped= False
	song=song_list.get(ACTIVE)
	print(song)
	song=f'E:/Python/MP3/audio/{song}.mp3'
	print(song)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	play_time()
global stopped
stopped=False	
def stopsong():
	sb.config(text='')
	myslider.config(value=0)
	pygame.mixer.music.stop()
	song_list.selection_clear(ACTIVE)
	global stopped
	stopped= True
global paused
paused= False
def pausesong(is_paused):
	global paused
	paused=is_paused
	if(paused):
		pygame.mixer.music.unpause()
		paused=False
	else:
		pygame.mixer.music.pause()
		paused=True
def nextsong():
	sb.config(text='')
	myslider.config(value=0)
	nextone=song_list.curselection()
	nextone=nextone[0]+1
	song=song_list.get(nextone)
	song=f'E:/Python/MP3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	song_list.selection_clear(0,END)
	song_list.activate(nextone)
	song_list.selection_set(nextone,last=None)
def previoussong():
	sb.config(text='')
	myslider.config(value=0)
	previousone=song_list.curselection()
	previousone=previousone[0]-1
	song=song_list.get(previousone)
	song=f'E:/Python/MP3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	song_list.selection_clear(0,END)
	song_list.activate(previousone)
	song_list.selection_set(previousone,last=None)
def delete_song():
	stopsong()
	song_list.delete(ANCHOR)
	pygame.mixer.music.stop()
def delete_many_songs():
	stopsong()
	song_list.delete(0,END)
	pygame.mixer.music.stop()
def slide(x):
	#sliderl.config(text=f'{int(myslider.get())} of {int(song_l)}') 
	song=song_list.get(ACTIVE)
	song=f'E:/Python/MP3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0,start=myslider.get())
def vol(x):
	pygame.mixer.music.set_volume(v_slider.get())


mas_frame= Frame(root)
mas_frame.pack(pady=20)
song_list=Listbox(mas_frame, bg="black", fg="white", width=60, selectbackground="white",selectforeground="black")
song_list.grid(row=0,column=0)
play=PhotoImage(file='play.png')
pause=PhotoImage(file='pause.png')
back=PhotoImage(file='back.png')
forward=PhotoImage(file='next.png')
stop=PhotoImage(file='stop.png')
controlframe=Frame(mas_frame)
controlframe.grid(row=1,column=0)
vol_frame=LabelFrame(mas_frame,text="Volume")
vol_frame.grid(row=0,column=1,padx=10)
bb= Button(controlframe,image=back,borderwidth=0,command=previoussong)
fb=Button(controlframe,image=forward,borderwidth=0,command=nextsong)
playb=Button(controlframe,image=play,borderwidth=0,command=playsong)
pb=Button(controlframe,image=pause,borderwidth=0,command=lambda: pausesong(paused))
sb=Button(controlframe,image=stop,borderwidth=0,command=stopsong)
bb.grid(row=0,column=0)
fb.grid(row=0,column=1)
sb.grid(row=0,column=4)
playb.grid(row=0,column=2)
pb.grid(row=0,column=3)
m=Menu(root)
root.config(menu=m)
ads=Menu(m)
m.add_cascade(label="Add Songs",menu=ads)
ads.add_command(label="Add One Song to List",command=add_song)
ads.add_command(label="Add Many Songs to List",command=add_many_songs)
rsm=Menu(m)
m.add_cascade(label="Delete Songs",menu=rsm)
rsm.add_command(label="Delete a Song",command=delete_song)
rsm.add_command(label="Delete All Songs",command=delete_many_songs)
sb=Label(root,text='',relief=GROOVE,bd=1,anchor=E)
sb.pack(fill=X,side=BOTTOM,ipady=2)
v_slider=ttk.Scale(vol_frame,from_=0,to=1,orient=VERTICAL,value=1,command=vol,length=125)
v_slider.pack(pady=10)
myslider=ttk.Scale(mas_frame, from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
myslider.grid(row=2,column=0,pady=30)
#sliderl=Label(root,text="0")
#sliderl.pack(pady=5)



root.mainloop()

