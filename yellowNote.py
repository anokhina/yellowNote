import tkinter as tk
import tkinter.scrolledtext as tkst
import sys, getopt
import os.path
from subprocess import call

cntrl = 1
geometryX = -50
geometryY = -50
file_name = "yellowNote.txt"
fake_message = "File not found: "

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

def int2(s, defval):
    try:
        return int(s)
    except ValueError:
        return defval

def geometry2(i):
     if i > 0 :
        return ("+" + str(i))
     else: 
        return ("" + str(i))
     

def readFile(file_name, data):
    try:
        with open(file_name, 'r') as myfile:
          data = myfile.read()
    except FileNotFoundError:
        print ("FileNotFoundError: " + file_name)
    else:
        print ("File reading error: " + file_name)
    return data
        
def main(argv):
   global geometryX, geometryY, file_name
   usage = '''
   test.py -i <inputFile> -x <geometryX> -y <geometryY>
   '''
   print (usage)
   try:
      opts, args = getopt.getopt(argv,"hi:x:y:",["inputFile=","geometryX=","geometryY="])
   except getopt.GetoptError:
      #print (usage)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (usage)
         sys.exit()
      elif opt in ("-i", "--inputFile"):
         file_name = arg
         
      elif opt in ("-x", "--geometryX"):
         geometryX = int2(arg, geometryX)
      elif opt in ("-y", "--geometryY"):
         geometryY = int2(arg, geometryY)
         
   
   #print ('Input file is "', file_name)
   #print ('x "', geometryX)
   #print ('y "', geometryY)
   
if __name__ == "__main__":
   main(sys.argv[1:])

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        data = readFile(file_name, fake_message + file_name)

        self.button = tk.Button(self)
        self.button["text"] = os.path.basename(file_name)
        self.button["command"] = self.say_hi
        self.button.config(fg="black", bg="yellow")
        self.button.pack(fill='both', side="top")

        frame = tk.Frame(master = self, bg = "yellow")
        frame.pack(fill='both', expand='yes')
        self.editArea = tkst.ScrolledText(
            master = frame,
            bg = "yellow",
            wrap   = tk.WORD,
            width  = 15,
            height = 7
        )
        self.editArea.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
        self.editArea.insert(tk.INSERT, data)
        self.editArea.configure(state='disabled')
        #self.editArea.bind("<Key>", lambda e: "break")
        
    def say_hi(self):
        global cntrl, file_name, fake_message
        if cntrl == 1 :
            cntrl = 0
            root.call("wm", "attributes", ".", "-alpha", "0.9")
            call(["notepad", file_name])
        else:
            cntrl = 1
            root.call("wm", "attributes", ".", "-alpha", "0.5")

        data = readFile(file_name, fake_message + file_name)

        self.editArea.configure(state='normal')
        self.editArea.delete('1.0', tk.END)
        self.editArea.insert(tk.INSERT, data)
        self.editArea.configure(state='disabled')

        root.overrideredirect(cntrl)

root = tk.Tk()
root.overrideredirect(cntrl)
root.wm_attributes("-topmost", 1)
root.geometry(""+geometry2(geometryX)+geometry2(geometryY))
root.call("wm", "attributes", ".", "-alpha", "0.5")
app = Application(master=root)
app.mainloop()

#https://docs.python.org/3/library/tkinter.html