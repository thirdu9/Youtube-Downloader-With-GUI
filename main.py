import os
from tkinter import *
from tkinter import filedialog
from tkinter.font import BOLD, ITALIC
from tkinter.ttk import Style
from moviepy import *
from moviepy.editor import VideoFileClip
from pytube import YouTube
import moviepy.editor as me
import shutil


class video_downloader:
    
    ##################**********functions**********##################
    def select_path():
        global path
        #select path from explorer
        path = filedialog.askdirectory()
        path_label.config(text=f"Destination Folder: {path}",font=(BOLD))

    def download_video():
        global link,video
        #get url path
        url_link = url.get()
        link = url_link

        video = YouTube(link)
        print(f'''Video Details
------------------------------------------------------------------------------------------------------------------------------------
        |Video link - {url_link}
        |Video Name - {video.title}
        |Channel Name - {video.author}
        |Video duration - {video.length} secs
        |Video Description - {video.description[0:100]}...
        ''')
        
        #get selected path
        user_path = path_label.cget("text")
        #path = path


        #destroying
        url.after(2,url.destroy) #destroy entry
        select_btn.after(1,select_btn.destroy)#Destroy select button
        download_btn.after(1,url_label.destroy)#Destroy url_label('Paste url here')
        download_btn.after(1,download_btn.destroy) #Destroy Dwonload button
        
        #title Label
        title0 = Label(screen,text="TITLE: ")
        title0.config(font=('georgia',18,BOLD))
        canvas.create_window(375,220,window=title0)

        #Video Title
        title1 = Label(screen,text=f"{video.title}",wraplength=screen.winfo_width()) #.config(text=f'Title: {yt.title}',font=('times',15,ITALIC,BOLD))
        title1.config( font=('times',16,ITALIC,BOLD))
        canvas.create_window(375,275,window=title1)

        
################**BUTTONS**############
        

        #create Home Button in 'Select' Position    
        home_btn  = Button(screen,text="HOME",command=video_downloader.Home,background='#345',foreground='white',activebackground='#000',activeforeground='#fff')
        canvas.create_window(375,420,window=home_btn)

        #High Res Video Button
        High_Res = Button(screen,text='Highest Quality',command=video_downloader.high_res)
        canvas.create_window(175,500,window=High_Res)

        #Audio_only Button
        aud_only_btn = Button(screen,text='Audio Only\n(Highest quality)',command=video_downloader.audio_only)
        canvas.create_window(375,500,window=aud_only_btn)

        #Low_Res Video Button
        Low_Res = Button(screen,text="Lowest Quality",command=video_downloader.low_res,bg='Red',activebackground='#345',activeforeground='white', padx=5, pady=5,relief=GROOVE)
        canvas.create_window(575,500,window=Low_Res)


#####################################

    def Home():
        screen.destroy()
        print('New window created!')
        main()

############Downloading Functions###########

    #Highest Res video download
    def high_res():
        #update Window title
        screen.title("Downloading...")

        #downloading video
        #dwnld_vid = video.streams.get_by_itag().download()
        
        print(f'''Downloading video in Highest Quality available
        |Video Resolution - {video.streams.filter(progressive=True,mime_type='video/mp4').order_by("resolution")}''')#.last().__getattribute__('itag')

        print('\n\n')
        ff = video.streams.all()#.filter(progressive=True,mime_type='video/mp4').order_by("resolution")
        for i in ff:
            print(i,'\n')
        video.streams.get_by_itag(401).download()
        #moving file to selected dir
        #shutil.move(video.streams.get_highest_resolution().download(),path)

        #update title
        screen.title('Download complete!')
        print(f'File path path - {path}')
        print('Download Complete!')

    #Lowest Res Mp4 Video Download
    def low_res():
        #update Window title
        screen.title("Downloading...")
        print(f'''Downloading video in Lowest Quality available
        |Video Resolution - {video.streams.get_lowest_resolution().resolution}''')

        #downloading video
        video.streams.get_lowest_resolution().download()

        #moving file from downloaded Directory to user selected path
        shutil.move(video.streams.get_lowest_resolution().download(),path)
        
        #update title
        screen.title('Download complete!')
        print('Download complete!')

    #Only Audio Mp4 file download
    def audio_only():
        #update title
        outputaudio = video.title + '.mp3'
        outputaudio= outputaudio.replace(' | ','-')
        screen.title('Downloading...')
        print('Downloading in Highest Audio Quality available')
        print(outputaudio)

        print(f'''
        |Output format - mp3
        |File folder - {path}''')

        mp4audio = video.streams.get_audio_only().download()
        audioclip = me.AudioFileClip(mp4audio)
        audioclip.write_audiofile(outputaudio)
        os.remove(mp4audio)
        
        #moving file to selected dir
        shutil.move(outputaudio,path)
        
        #delete the dowloaded mp4 file
        #shutil.
        
        screen.title('Download Complete!')
        print('Done!')

#####################################
        
#Main
def main():
    global screen, canvas,url,select_btn,download_btn,path_label,url_label
    screen = Tk()
    title = screen.title("YouTube Downloader")
    screen.geometry('750x650+250+50')
    screen.resizable(False,False)

    canvas = Canvas(screen, width=750,height=650)
    canvas.pack()


    #logo image
    logo = PhotoImage(file='yt.png')

    #resize
    logo = logo.subsample(2,2)

    #adding logo to canvas
    canvas.create_image(375,80,image = logo)

    #link field
    url = Entry(screen,width=50)
    url.focus_set()
    canvas.create_window(375, 270,window=url)

    url_label = Label(screen,text='Paste URL here ↓👇',font=('Helvetica',15,BOLD))
    canvas.create_window(375, 220,window=url_label)



    #select Path
    path_label= Label(screen,text="Choose Folder",font=('arial',13))
    select_btn = Button(screen,text="Select",command=video_downloader.select_path)


    canvas.create_window(375,350,window = path_label)
    canvas.create_window(375,400,window = select_btn)

    #download button
    download_btn = Button(screen,text="Downlod",command=video_downloader.download_video,bg='Red',foreground='white',activebackground='#345',activeforeground='white', padx=40, pady=5 )
    canvas.create_window(375,500,window=download_btn)





    #start
    screen.mainloop()

if __name__ == '__main__':
    main()
else:
    pass