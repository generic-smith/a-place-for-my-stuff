import tkinter as tk
from tkinter import *
import pandas as pd
import os
from tkscrolledframe import ScrolledFrame
import atexit

testpath = "F:\Media\Tom and Jerry Cartoons Complete Collection (1940-2007) [DVDRip] M8\\066   Smitten Kitten [1952].avi"
testpath2 = "F:/Media/Tom and Jerry Cartoons Complete Collection (1940-2007) [DVDRip] M8/066   Smitten Kitten [1952].avi"

test_name = "066   Smitten Kitten [1952].avi"
test_root = "F:/Media/Tom and Jerry Cartoons Complete Collection (1940-2007) [DVDRip] M8/"


def save_ml(media_list):
    media_list.to_csv("media_list.csv", index=False)
    return True


def update_ml():
    try:
        return pd.read_csv("media_list.csv")
    except:
        return pd.DataFrame(columns=["Name", "Root", "Watched"])


def convert_path(path):
    return path.replace("\\", "/")


def add_media_files():
    global media_list
    file_types = ["mp4", "avi", "mkv", "mov"]
    folder_path = "F:/Media/Tom and Jerry Cartoons Complete Collection (1940-2007) [DVDRip] M8"

    for root, dirs, files in os.walk(folder_path, topdown=False):
        print(files)
        media_list = media_list.append(
            pd.DataFrame.from_dict({"Name": files, "Root": [root] * len(files), "Watched": [False] * len(files)}),
            ignore_index=True)
    print(media_list)
    save_ml(media_list)


def mark_as_seen(index, button):
    media_list.loc[index] = [media_list.loc[index]["Name"], media_list.loc[index]["Root"],
                             not media_list.loc[index]["Watched"]]
    set_button_state(button, media_list.loc[index]["Watched"])


def set_button_state(button, watched):
    if watched:
        button.config(relief=SUNKEN, text="o.o")
    else:
        button.config(relief=RAISED, text="-.-")


def open_media(path, index, button):
    os.startfile(path)
    mark_as_seen(index, button)


def populate_ml():
    print("Loading...")
    for m in range(len(media_list["Name"])):
        name_text = tk.Label(inner_frame, text=media_list.loc[m]["Name"])
        name_text.grid(row=m + 1, column=0, sticky=E)
        root_text = tk.Label(inner_frame, text=media_list.loc[m]["Root"])
        root_text.grid(row=m + 1, column=1, sticky=E)
        watched_text = tk.Button(inner_frame, justify=CENTER)
        set_button_state(watched_text, media_list.loc[m]["Watched"])
        watched_text.config(command=lambda i=m, arg=watched_text: mark_as_seen(i, arg))
        watched_text.grid(row=m + 1, column=2, sticky="WE")
        play_button = tk.Button(inner_frame, text="►", justify=CENTER,
                                command=lambda i=m, b=watched_text, r=media_list.loc[m]["Root"],
                                               n=media_list.loc[m]["Name"]:
                                open_media("{}/{}".format(r, n), i, b))
        play_button.grid(row=m + 1, column=3, sticky="WE")


def exit_handler():
    save_ml(media_list)
    print('Saving before exit!')


atexit.register(exit_handler)

media_list = update_ml()

root = tk.Tk()
root.title("Nate's Media Manager")
mainframe = tk.Frame(root, height=800, width=600)
mainframe.pack(fill=BOTH, expand=True, padx=10, pady=10)

command_frame = tk.Frame(mainframe, borderwidth=2)
command_frame.pack(side=TOP, expand=False, fill=X)
add_media_button = tk.Button(command_frame, text="Add Media Files", command=add_media_files)
add_media_button.pack(side=LEFT)
refresh_button = tk.Button(command_frame, text="Refresh", command=populate_ml)
refresh_button.pack(side=RIGHT)
media_list_frame = ScrolledFrame(mainframe, scrollbars='both')
media_list_frame.pack(side=TOP, expand=True, fill=BOTH)
inner_frame = media_list_frame.display_widget(Frame)

name_header = tk.Label(inner_frame, text="Name", borderwidth=2, justify=CENTER, relief=GROOVE)
name_header.grid(row=0, column=0, sticky=N, columnspan=True)

root_header = tk.Label(inner_frame, text="Root", borderwidth=2, justify=CENTER, relief=GROOVE)
root_header.grid(row=0, column=1, sticky=N, columnspan=True)

watched_header = tk.Label(inner_frame, text="Watched", borderwidth=2, justify=CENTER, relief=GROOVE)
watched_header.grid(row=0, column=2, sticky=N, columnspan=True)
play_header = tk.Label(inner_frame, text="Play", borderwidth=2, justify=CENTER, relief=GROOVE)
play_header.grid(row=0, column=3, sticky=N, columnspan=True)

populate_ml()

root.mainloop()
