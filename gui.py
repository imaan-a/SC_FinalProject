
from tkinter import *
import requests
from PIL import ImageTk, Image
from final_IA import MovieInfo
from io import BytesIO
import webbrowser
from functools import partial


def set_movie_instance(movie):
    '''
    Creates instance of MovieInfo object.

    **Parameters**
        movie: **str**
            Movie title or title fragment.

    **Returns**
        None
    '''
    mov1 = MovieInfo(movie)
    return mov1


def add_pic(instance, frame):
    '''
    Adds movie poster to the given gui frame.

    **Parameters**
        instance: **MovieInfo**
            MovieInfo object containing movie data.
        frame: **tkinter.Frame**
            Frame that the picture will be place inside.

    **Returns**
        None
    '''
    pic_url = instance.get_pic_details()
    picrespon = requests.get(pic_url)
    img = Image.open(BytesIO(picrespon.content))
    img = img.resize((178, 264), Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    pic_lab = Label(frame, image=img_tk)
    pic_lab.image = img_tk
    pic_lab.grid(row=8, column=8, rowspan=20)


def urlopen(links, i):
    '''
    Opens a url in the default web browser.

    **Parameters**
        links: **list, str**
            List of urls from different services for the same title as strings.
        i: **int**
            Passes information on which link to open.

    **Returns**
        None
    '''
    webbrowser.open_new(links[i])


def click_watch(instance, clicked):
    '''
    Puts list of where to watch the selected title on the interface for users
    to select.

    **Parameters**
        instance: **MovieInfo**
            MovieInfo object that has data on the initialized title.
        clicked: **tkinter variable**
            Variable of the drop down menu to select country.

    **Returns**
        None
    '''
    country = clicked.get()
    out_frame.grid_forget()
    where_frame = LabelFrame(root, padx=115, pady=20)
    where_frame.grid(row=8, column=10, rowspan=20)
    add_pic(instance, where_frame)
    servs, links = instance.wheretowatch(country)
    for i, value in enumerate(servs):
        Button(where_frame, text=value,
               command=partial(urlopen, links, i)).grid(row=13+i, column=9)


def click_info():
    '''
    Puts information about the user-entered title onto the interface window.
    Information consists of movie title, year, runtime, director and principal
    cast members.

    **Parameters**
        None

    **Returns**
        None
    '''
    mov1 = set_movie_instance(e.get())
    add_pic(mov1, out_frame)
    txt1, txt2 = mov1.get_info()
    info2 = Label(out_frame, text=txt1).grid(row=8, column=9, sticky=W)
    for i, value in enumerate(txt2):
        Label(out_frame, text=value).grid(row=11 + i, column=9, sticky=W)
    clicked = StringVar()
    clicked.set('United States')
    pick_c = OptionMenu(out_frame, clicked, 'United States', 'Canada',
                        'United Kingdom', 'Spain', 'France', 'Brazil',
                        'Hong Kong', 'Japan')
    pick_c.grid(row=15, column=9)
    wat_but = Button(out_frame, text='Watch Now',
                     command=partial(click_watch, mov1, clicked))
    wat_but.grid(row=17, column=9)


def click_rec_info(recs, j):
    '''
    Puts information about the recommended title that was selected onto the
    interface window. Information consists of movie title, year, runtime,
    director and principal cast members.

    **Parameters**
        None

    **Returns**
        None
    '''
    mov2 = set_movie_instance(recs[j+1])
    out_frame.grid_forget()
    top_frame = LabelFrame(root, padx=115, pady=20)
    top_frame.grid(row=8, column=10, rowspan=20)
    add_pic(mov2, top_frame)
    txt1, txt2 = mov2.get_info()
    info2 = Label(top_frame, text=txt1).grid(row=9, column=9, sticky=W)
    for i, value in enumerate(txt2):
        Label(top_frame, text=value).grid(row=12 + i, column=9, sticky=W)
    clicked = StringVar()
    clicked.set('United States')
    pick_c = OptionMenu(top_frame, clicked, 'United States', 'Canada',
                        'United Kingdom', 'Spain', 'France', 'Brazil',
                        'Hong Kong', 'Japan')
    pick_c.grid(row=16, column=9)
    wat_but = Button(top_frame, text='Watch Now',
                     command=partial(click_watch, mov2, clicked))
    wat_but.grid(row=18, column=9)


def click_rec():
    '''
    Puts a list of movies that are similar to the user-entered title onto the
    interface window.  Options for more information on each title given.

    **Parameters**
        None

    **Returns**
        None
    '''
    mov1 = set_movie_instance(e.get())
    recs = mov1.recommendations()
    for i, value in enumerate(recs):
        Label(out_frame, text=value).grid(row=11 + i, column=9, sticky=W)
    for j in range(len(recs) - 1):
        Button(out_frame, text='Get Info',
               command=partial(click_rec_info,
                               recs, j)).grid(row=12 + j, column=10, sticky=W)

root = Tk()
root.title('Movie Database')

in_frame = LabelFrame(root, padx=30, pady=50)
in_frame.grid(row=4, column=10, columnspan=4)
out_frame = LabelFrame(root, padx=115, pady=20)
out_frame.grid(row=8, column=10, columnspan=4, rowspan=20)

myLabel = Label(in_frame, text='Enter a Movie Title:')
myLabel.grid(row=2, column=10)

e = Entry(in_frame, width=30, fg='blue')
e.grid(row=3, column=9, columnspan=3)

info_but = Button(in_frame, text='Get Info', padx=5, command=click_info,
                  fg='blue')
info_but.grid(row=7, column=9)

rec_but = Button(in_frame, text='Find Similar', command=click_rec, fg='blue')
rec_but.grid(row=7, column=11)

root.mainloop()
