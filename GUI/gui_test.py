import tkinter as tk


class ExampleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.some_frame = None

        tk.Button(self.master, text="About", command = self.create_stuff).pack()

        # self.master.title("FYP")
        # #Window size
        # self.master.geometry('800x300')      #Window size

        # #Title 
        # Title = tk.Label(self.master, text="Welcome!", font=("Arial Bold", 30))
        # Title.place(x=300, y=0)
        # #Panadol concentration estimation button
        # Panadol_btn = tk.Button(self.master, text="Panadol concentration estimation")
        # Panadol_btn.place(x=10, y=150)

        # #Dengue detection button
        # Dengue_btn = tk.Button(self.master, text="Dengue detection")
        # Dengue_btn.place(x=310, y=150)

        # #Multiple disease detection button
        # Multiple_disease_btn = tk.Button(self.master, text="Multiple disease detection")
        # Multiple_disease_btn.place(x=510, y=150)

        # #About button
        # About_btn = tk.Button(self.master, text="About")
        # About_btn.place(x=710, y=260)

    def create_stuff(self):
        if self.some_frame == None:
            self.some_frame = tk.Frame(self.master)
            self.some_frame.pack()

            for i in range(5):
                tk.Label(self.some_frame, text = "This is label {}!".format(i+1)).pack()

            tk.Button(self.some_frame, text="Destroy all widgets in this frame!",
                      command= self.destroy_some_frame).pack()

    def destroy_some_frame(self):
        self.some_frame.destroy()
        self.some_frame = None

root = tk.Tk()
my_example = ExampleApp(root)
root.mainloop()