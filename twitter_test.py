from twitter import *
from Tkinter import *
import json

def showTweets(x, num):
    # display a number of new tweets and usernames
    for i in range(0, num):
        line1 = (x[i]['user']['screen_name'])
        line2 = (x[i]['text'])
        print json.dumps(x[i])
        w = Label(master, text=line1 + "\n" + line2 + "\n\n")
        w.pack()

def getTweets():
    x = t.statuses.home_timeline(screen_name="FYPWOP")
    return x

def tweet():

    global entryWidget

    if entryWidget.get().strip() == "":
        print("Empty")
    else:
        t.statuses.update(status=entryWidget.get().strip())
        entryWidget.delete(0, END)
        print("Working")

# Put in token, token_key, con_secret, con_secret_key
t = Twitter(auth=OAuth('787936570968043520-o1bHGOmR4AEuNoafsWoROAQIQIbwz3i', 's3vsnQAAuyLmhKYirZ0HIKRpreO8VsF84qAMDHfdmmmGG', 'LJ0wq7eWPRSmdJVIoxQtYxyuy', 'CH811T3P1n7ofmPtd0POaML4vfGvKKIz7wLV212wKf3kRdp1i8'))

numberOfTweets = 7

master = Tk()
showTweets(getTweets(), numberOfTweets)

master.title("Tkinter Entry Widget")
master['padx'] = 40
master['pady'] = 20
# Create text frame to hold Label and Entry Widget
textFrame = Frame(master)
# Create label in textFrame
entryLabel = Label(textFrame)
entryLabel['text'] = "Make a new Tweet:"
entryLabel.pack(side=LEFT)
# Create Entry Widget in textFrame
entryWidget = Entry(textFrame)
entryWidget['width'] = 50
entryWidget.pack(side=LEFT)
textFrame.pack()
button = Button(master, text="Submit", command=tweet)
button.pack()

master.mainloop()
