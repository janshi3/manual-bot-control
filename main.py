from config import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import requests

URL = "https://binance-burger-bot.herokuapp.com/webhook"

PING_URL = "https://binance-burger-bot.herokuapp.com/ping"


def get_asset():
    try:
        f = open("asset.txt", "r")
        old_asset = f.read()
        f.close()
    except FileNotFoundError:
        old_asset = "None"
    return old_asset


def set_asset():
    new_asset = simpledialog.askstring("New Asset", "Input New Asset Name:").upper()
    f = open("asset.txt", "w")
    f.write(new_asset)
    f.close()
    global asset
    asset = new_asset
    b_change.configure(text="Change Asset \n (" + asset + ")")


def send_request(asset, action, comment):
    message = '{"passphrase": "' + PASSPHRASE + '","time": "None","ticker": "' + asset + \
              'USDT","base_currency": "USDT","strategy": {"order_action": "' + action + \
              '","order_comment": "' + comment + '"}}'
    response = requests.post(URL, data=message)
    if response:
        messagebox.showinfo("Success!", response.content)
    else:
        messagebox.showinfo("Failure!", "No Response!")


def ping():
    response = requests.post(PING_URL, data='{"ping": "Yes"}')


asset = get_asset()

display = Tk()
display.resizable(width=False, height=False)
display.geometry("160x258-0+0")

b_long = Button(display, text="Long", width=10, height=5, bg="green3",
                command=lambda: send_request(asset, "BUY", "BUY"))

b_short = Button(display, text="Short", width=10, height=5, bg="red3",
                 command=lambda: send_request(asset, "SELL", "SELL"))

b_clong = Button(display, text="Cancel Long", width=10, height=5, bg="SpringGreen2",
                 command=lambda: send_request(get_asset(), "SELL", "NONE"))

b_cshort = Button(display, text="Cancel Short", width=10, height=5, bg="coral2",
                  command=lambda: send_request(get_asset(), "BUY", "NONE"))

b_change = Button(display, text="Change Asset \n (" + asset + ")", width=10, height=5, bg="yellow2",
                  command=lambda: set_asset())

b_ping = Button(display, text="Ping", width=10, height=5, bg="yellow3", command=lambda: ping())

b_long.grid(row=0, column=0)

b_short.grid(row=1, column=0)

b_clong.grid(row=0, column=1)

b_cshort.grid(row=1, column=1)

b_change.grid(row=2, column=0)

b_ping.grid(row=2, column=1)

display.mainloop()
