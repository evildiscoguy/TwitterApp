import tkinter as tk
from tkinter import ttk
import tweepy
import tkinter.scrolledtext as scrolledtext

from credentials import keys

API_KEY = keys["API_KEY"]
API_SECRET_KEY = keys["API_SECRET_KEY"]
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def check_msg_len(_):
    text_var.set(str(len(txt_tweet.get("1.0", 'end-1c'))))
    if (len(txt_tweet.get("1.0", 'end-1c'))) > 280:
        lbl_char_count.configure(fg="red")
    else:
        lbl_char_count.configure(fg="green")


def tweet_too_long():
    win_tweet_too_long = tk.Toplevel()
    win_tweet_too_long.title("Whoops")
    win_tweet_too_long.geometry("250x50")
    frm_tweet_too_long = ttk.Frame(win_tweet_too_long)
    lbl_tweet_too_long = ttk.Label(
        text="Tweet too long!",
        master=frm_tweet_too_long)
    btn_tweet_too_long = ttk.Button(
        text="OK",
        command=win_tweet_too_long.destroy,
        master=frm_tweet_too_long)
    frm_tweet_too_long.pack(fill="both")
    lbl_tweet_too_long.pack()
    btn_tweet_too_long.pack(side="bottom")


# Create a popup for if no tweet has been entered
def tweet_empty():
    win_tweet_empty = tk.Toplevel()
    win_tweet_empty.title("Whoops")
    frm_tweet_empty = ttk.Frame(win_tweet_empty)
    win_tweet_empty.geometry("250x50")
    lbl_tweet_empty = ttk.Label(
        text="No Tweet Entered!",
        master=frm_tweet_empty)
    btn_tweet_empty = ttk.Button(
        text="OK",
        command=win_tweet_empty.destroy,
        master=frm_tweet_empty)
    frm_tweet_empty.pack(fill="both")
    lbl_tweet_empty.pack()
    btn_tweet_empty.pack(side="bottom")


# Check to see if tweet has been entered and send on success
def send_tweet():
    tweet = txt_tweet.get(1.0, "end-1c")
    if tweet == "":
        tweet_empty()
    else:
        if (len(txt_tweet.get("1.0", 'end-1c'))) > 280:
            tweet_too_long()
        else:
            api.update_status(status=tweet)
            tweet_sent()


# Popup to say tweet has been sent
def tweet_sent():

    # Reset the text box after closing pop up
    def reset_on_success():
        # txt_tweet.delete(1.0, "end")
        win_tweet_sent.destroy()

    win_tweet_sent = tk.Toplevel()
    win_tweet_sent.title("Success")
    win_tweet_sent.geometry("250x50")
    frm_tweet_sent = ttk.Frame(win_tweet_sent)
    lbl_tweet_sent = ttk.Label(
        text="Tweet Sent!",
        master=frm_tweet_sent)
    btn_close_popup = ttk.Button(
        text="OK",
        command=reset_on_success,
        master=frm_tweet_sent)
    frm_tweet_sent.pack(fill="both")
    lbl_tweet_sent.pack()
    btn_close_popup.pack(side="bottom")


window = tk.Tk()
window_style = ttk.Style()
window_style.theme_use("clam")
window.title("TweetBot")
frm_window = ttk.Frame()
lbl_instructions = ttk.Label(
    text="Enter your tweet below in the text field:",
    master=frm_window)
txt_tweet = scrolledtext.ScrolledText(
    font="Arial",
    bg="white",
    fg="black",
    insertbackground="black",
    height=5,
    width=45,
    wrap="word",
    undo=True,
    padx=2,
    pady=2,
    master=frm_window)

# Configure line height padding in the text box to stop cut off
txt_tweet.config(spacing1=2)
txt_tweet.config(spacing2=2)
txt_tweet.config(spacing3=2)

btn_send_tweet = ttk.Button(
    text="Send Tweet",
    command=send_tweet,
    master=frm_window)

text_var = tk.StringVar()
lbl_char_count = tk.Label(
    bg="black",
    borderwidth=2,
    relief="raised",
    textvariable=text_var,
    master=frm_window)
txt_tweet.bind("<KeyRelease>", check_msg_len)

frm_window.pack(fill="both")
lbl_instructions.pack(side=tk.TOP)
btn_send_tweet.pack(side=tk.BOTTOM)
lbl_char_count.pack(side=tk.BOTTOM)
txt_tweet.pack(side=tk.LEFT, expand=True, fill="both")

window.resizable(False, False)
window.mainloop()
