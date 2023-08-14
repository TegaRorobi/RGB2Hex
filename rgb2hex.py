'''
Developer : Tega Andrew Rorobi
email   : rorobitega@gmail.com
twitter : @Tega_Rorobi
github  : https://github.com/TegaRorobi
last_modidified: 
'''

# imports
import sys, math, argparse
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox

'''
TODO:   ADD A KIND OF DISPLAY THAT SHOWS THE COLORS AS THE 
        PERSON CONVERTS THE COLOR CODES IN REALTIME. e.g a label 
        that changes color according to the input colors
'''

# use a cli to allow setting the color scheme
parser = argparse.ArgumentParser()
parser.add_argument('--colors', nargs=2)
args = parser.parse_args()
mode =  args.colors[0] if args.colors else None
color = args.colors[1] if args.colors else None


class Converter(ctk.CTk):

    def __init__(self):
        super().__init__()

        # set color scheme
        ctk.set_appearance_mode(mode or "dark")
        ctk.set_default_color_theme(color or "green")



        # configure some window properties
        self.title('Custom Tkinter Converter by Tega Rorobi')
        self.geometry('700x400')
        # self.resizable(0,0)
        self.grid_columnconfigure (1, weight=1)
        self.grid_rowconfigure    (0, weight=1)



        # the dicts that do the conversion
        self.hex_dict = {
            key:value for key, value in zip(range(16), [str(i) for i in range(10)]+list("ABCDEF"))
            }
        self.rgb_dict = {
            value:key for key, value in self.hex_dict.items()
            }



        # the sidebar
        self.sidebar = ctk.CTkFrame(master=self, width=140)
        self.sidebar.grid(row=0, column=0, padx=(0, 0), pady=0, sticky='ns')
        self.sidebar.grid_rowconfigure(2, weight=1)


        # create some widgets that go into the sidebar
        self.logo_img= ctk.CTkImage(Image.open('assets/ctk_logo.png'), size=(20, 20))
        self.logo_label = ctk.CTkLabel(master=self.sidebar, text='  Deciphrexx', font=('', 15), image=self.logo_img, compound='left')
        self.logo_label.grid(row=0, column=0, sticky='nsew')

        self.scaling_label=ctk.CTkLabel(master=self.sidebar,text='Widget Scaling:', font=('', 15))
        self.scaling_label.grid(row=3, pady=12)
        self.scaling_optionmenu = ctk.CTkOptionMenu(master=self.sidebar, values=['80%', '90%', '100%', '110%', '120%'], command=self.set_scaling)
        self.scaling_optionmenu.grid(row=4, padx=15, pady=(0, 10))

        self.appearance_mode_label = ctk.CTkLabel(master=self.sidebar, text='Appearance Mode:', font=('', 15))
        self.appearance_mode_label.grid(row=5, pady=12)
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(master=self.sidebar, values=['Light', 'Dark', 'System'], command=self.set_appearance_mode)
        self.appearance_mode_optionmenu.grid(row=6, padx=15, pady=(0, 20))






        # the mainframe
        self.mainframe = ctk.CTkFrame(master=self)
        self.mainframe.grid(row=0, column=1, sticky='nsew')
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)


        # create some frames that go into the mainframe
        self.frame1 = ctk.CTkFrame(master=self.mainframe)
        self.frame1.grid(row=0, column=0, pady=(1, 6), padx=(0, 12), sticky='nsew')
        # self.frame1.pack(pady=(1, 6), padx=(0, 12), fill='both', expand=True)

        self.frame2 = ctk.CTkFrame(master=self.mainframe)
        self.frame2.grid(row=1, column=0, pady=(6, 10), padx=12, sticky='s')
        # self.frame2.pack(pady=(6, 10), padx=12, anchor='s')



        #### FRAME 1 ####


        # configuring the rows and columns for the frames in the mainframe
        self.frame1.grid_rowconfigure((0, 5), weight=1)
        self.frame1.grid_columnconfigure((0, 3), weight=1)
        self.frame2.grid_columnconfigure((0, 1), weight=1)


        # create the widgets in frame1 of the mainframe
        #bug resolved: using self.title instead of self.main_title result in an error with CTkMessageBox
        self.main_title = ctk.CTkLabel(master=self.frame1, text="🔁Rgb <-> Hex Converter", font=('Fira Code', 25))
        self.rgb_convert_button = ctk.CTkButton(master=self.frame1, text='Convert -> Hex', font=('Fira Code', 16), command=self.get_hex)
        self.rgb_entry = ctk.CTkEntry(master=self.frame1, width=180, placeholder_text="RGB ex. 25 125 225", font=('Fira Code', 15))
        self.solution_textbox = ctk.CTkTextbox(master=self.frame1, height=25, font=('Fira Code', 16))
        self.hex_convert_button = ctk.CTkButton(master=self.frame1, text='Convert -> RGB', font=('Fira Code', 16), command=self.get_rgb)
        self.hex_entry = ctk.CTkEntry(master=self.frame1, width=180, placeholder_text='Hex ex. #D6FF29', font=('Fira Code', 15))


        # grid the widgets onto the screen

        self.main_title.grid         (row=1, column=1, pady=(15, 25),    sticky='nsew', columnspan=2)
        self.rgb_entry.grid          (row=2, column=1, padx=40, pady=30, sticky='nsew')
        self.rgb_convert_button.grid (row=2, column=2, padx=40, pady=30, sticky='nsew')
        self.solution_textbox.grid   (row=3, column=1, padx=40, pady=20, sticky='nsew', columnspan=2)
        self.hex_entry.grid          (row=4, column=1, padx=40, pady=30, sticky='nsew')
        self.hex_convert_button.grid (row=4, column=2, padx=40, pady=30, sticky='nsew')







        ##### FRAME 2 ####

        # add a little footer in frame2
        self.footer = ctk.CTkLabel(master=self.frame2, text="Made with 🐍🐍", font=('', 18))
        self.footer.pack(anchor='center')

        self.scaling_optionmenu.set('100%')
        self.appearance_mode_optionmenu.set(ctk.get_appearance_mode())

    def get_hex(self):
        hex_str = ''
        rgb_vals = (self.rgb_entry.get()).split()
        try:
            for value in rgb_vals[:3]:
                hex_str += (self.hex_dict[math.floor(int(value)/16)] + self.hex_dict[int(value)%16])
            self.solution_textbox.delete(0.0, 'end')
            self.solution_textbox.insert('0.0', '  '+f"R({rgb_vals[0]}) G({rgb_vals[1]}) B({rgb_vals[2]}) -> #{hex_str}(hex)")
        except:
            # messagebox.showerror("Computation Error", "Please enter a RGB value in the specified format: `xxx xxx xxx` where xxx <= 255.")
            CTkMessagebox(
                title="Computation Error : Invalid RGB code", 
                message="Please enter an RGB value in the specified format: `xxx xxx xxx` where xxx <= 255.", 
                font=('Fira Code', 13), 
                icon="cancel")


    def get_rgb(self):
        rgb_lst = []
        hex_val = self.hex_entry.get().upper().replace('#', '')
        try:
            # could've used numpy for this splitting, but that would just make the app slower and more dependent 
            for value in [hex_val[x:x+2] for x in range(0, 6, 2)]:
                rgb_lst.append((16*self.rgb_dict[value[0]]) + (self.rgb_dict[value[1]]))
            self.solution_textbox.delete(0.0, 'end')
            self.solution_textbox.insert('0.0', '  '+f"#{hex_val[:6]}(hex) -> R({rgb_lst[0]}) G({rgb_lst[1]}) B({rgb_lst[2]})")
        except:
            # messagebox.showerror("Computation Error", "Please enter a six(6) character hex value in the specified format: `xxxxxx` or `#xxxxxx` where `x` is a value including 0-9, a-f, A-F.")
            CTkMessagebox(
                title="Computation Error : Invalid Hex code", 
                message="Please enter a six(6) character hex value in the specified format: `xxxxxx` or `#xxxxxx` where `x` is a value including 0-9, a-f, A-F.",
                font=('Fira Code', 13), 
                icon="cancel")

    def set_appearance_mode(self, mode:str):
        ctk.set_appearance_mode(mode)

    def set_scaling(self, scale):
        float_scale = int(scale.replace('%', '')) / 100
        ctk.set_widget_scaling(float_scale)
  

if __name__ == '__main__':
    app = Converter()
    app.mainloop()