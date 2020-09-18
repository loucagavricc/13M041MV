import tkinter as tk
import _thread
from time import sleep
import _queue as Queue

request_queue = Queue.queue()
result_queue = Queue.queue()

def submit_to_tkinter(callable, *args, **kwargs):
    request_queue.put((callable, args, kwargs))
    return result_queue.get()

t = None
def threadmain():
    global t

    def timertick():
        try:
            callable, args, kwargs = request_queue.get_nowait()
        except Queue.Empty:
            pass
        else:
            print("something in queue")
            retval = callable(*args, **kwargs)
            result_queue.put(retval)

        t.after(500, timertick)

    t = tk.Tk()
    t.configure(width=640, height=480)
    b = tk.Button(text='test', name='button', command=exit)
    b.place(x=0, y=0)
    timertick()
    t.mainloop()

def foo():
    t.title("Hello world")

def bar(button_text):
    t.children["button"].configure(text=button_text)

def get_button_text():
    return t.children["button"]["text"]
