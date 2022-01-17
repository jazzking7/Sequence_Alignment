# Author: Jasper Wang
# Goal: Parameters to the sequence alignment
# Date: 20 Dec 2021

from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class Control_Panel:
    def __init__(self, aligner):
        self.aligner = aligner
        self.window = Tk()
        # File selector
        self.file_frame = LabelFrame(master=self.window, text="File Selection")
        self.file_frame.pack(expand=True, fill=BOTH, padx=5, pady=5)
        file = Label(master=self.file_frame, text="File: ").grid(row=0, column=0)
        filename = Label(master=self.file_frame, text="---").grid(row=0, column=1)
        select = Button(master=self.file_frame, text="Select File", command=self.selectfile)
        select.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # Parameters
        self.parameters = LabelFrame(master=self.window, text="Parameters")
        self.parameters.pack(expand=True, fill=BOTH, padx=5)
        lbl = Label(master=self.parameters, text="*All scores must be integers").grid(row=0, column=0)
        lbl1 = Label(master=self.parameters, text="Match Score: ").grid(row=1, column=0)
        lbl2 = Label(master=self.parameters, text="Mismatch Score: ").grid(row=2, column=0)
        lbl3 = Label(master=self.parameters, text="Gap penalty: ").grid(row=3, column=0)
        e1 = Entry(master=self.parameters).grid(row=1, column=1, padx=5, pady=4)
        e2 = Entry(master=self.parameters).grid(row=2, column=1, padx=5)
        e3 = Entry(master=self.parameters).grid(row=3, column=1, padx=5, pady=4)
        # Computation
        compute = Button(master=self.window, text="Compute Optimal Alignments", command=self.compute_result)
        compute.pack(expand=True, fill=BOTH, padx=5, pady=5)

    def selectfile(self):
        self.window.filename = filedialog.askopenfilename(
            initialdir="/Desktop", title="Select A File", filetypes=(
                ("all files", "*.*"), ("FASTA files", "*.fasta"), ("Text files", "*.txt")))
        for label in self.file_frame.grid_slaves():
            if int(label.grid_info()["row"]) == 0 and int(label.grid_info()["column"]) == 1:
                label.grid_forget()
        lbl = Label(master=self.file_frame, text=self.window.filename).grid(row=0, column=1)

    def compute_result(self):
        para = [i for i in self.parameters.grid_slaves(column=1)]
        self.aligner.set_parameters(int(para[2].get()), int(para[1].get()), int(para[0].get()))
        S1, S2 = self.aligner.analyze(self.window.filename)
        top = Toplevel()
        top.title("Display Result")
        lbl1 = Label(master=top, text="Sequence 1:").pack()
        lbl2 = Label(master=top, text=S1).pack(fill=BOTH, expand=1)
        lbl3 = Label(master=top, text="Sequence 2:").pack(fill=BOTH, expand=1)
        lbl4 = Label(master=top, text=S2).pack()
        lbl5 = Label(master=top, text="""Notice: the results have been saved into the text file \"Result.txt\",
        in the same directory where the source codes are located.""").pack()
        result = open("Result.txt", "w")
        result.write("Sequence 1:\n")
        result.write(f"{S1}\n")
        result.write("Sequence 2:\n")
        result.write(f"{S2}\n")
        result.close()

    def Start(self):
        self.window.title("Control Panel")
        self.window.eval("tk::PlaceWindow . center")
        self.window.mainloop()
