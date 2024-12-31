import pyautogui
from tkinter import *
from tkinter import colorchooser, filedialog, ttk
from PIL import Image, ImageTk, ImageGrab

class main:
	def __init__(self, master):
		self.master = master
		self.color = 'Black'
		self.color_bg = 'White'
		self.old_x = None
		self.old_y = None
		self.pen_width = 5
		self.drawn_lines = []
		self.drawWidgets()
		self.c.bind('<B1-Motion>', self.paint)
		self.c.bind('<ButtonRelease-1>', self.reset)
		self.eraser = False

	def paint(self, e):
		if self.old_x and self.old_y:
			color_to_use = self.color_bg if self.eraser else self.color
			created_line = self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.pen_width, fill=color_to_use, capstyle=ROUND, smooth=True)
			
			self.drawn_lines.append({
				'line_id': created_line,
				'erased': self.eraser
			})

		self.old_x = e.x
		self.old_y = e.y

	def reset(self, e):
		self.old_x = None
		self.old_y = None

	def change_width(self, e):
		self.pen_width = e

	def clear(self):
		self.drawn_lines = []
		self.c.delete(ALL)

	def change_color(self):
		self.color = colorchooser.askcolor(color=self.color)[1]

	def change_bg(self):
		self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
		self.c['bg'] = self.color_bg
		
		if self.drawn_lines:
			for line in self.drawn_lines:
				if line['erased']:
					self.c.itemconfig(line['line_id'], fill=self.color_bg)

				self.c.itemconfig(line, fill=self.color_bg)

	def eraser(self):
		self.eraser = not self.eraser
		self.eraser_button.config(relief=SUNKEN if self.eraser else RAISED)

	def load_image(self):
		filepath = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp;*.gif')])
		if filepath:
			self.clear()
			self.loaded_image_path = filepath
			img = Image.open(filepath)
			
			canvas_width = self.c.winfo_width()
			canvas_height = self.c.winfo_height()
			img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
			
			self.tk_img = ImageTk.PhotoImage(img)
			self.c.create_image(0, 0, anchor='nw', image=self.tk_img)

	def save_as_png(self):
		filename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
		if filename:
			x = self.c.winfo_rootx()
			y = self.c.winfo_rooty()
			width = self.c.winfo_width()
			height = self.c.winfo_height()

			screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
			screenshot.save(filename)

	def on_crosshair_change(self, *args):
		selected_option = self.crosshair_list.get()
		self.c.config(cursor=selected_option)

	def drawWidgets(self):
		self.controls = Frame(self.master, pady=5)
		self.controls.pack(fill=X)

		Label(self.controls, text='Pen Width:', font=('arial 18')).pack(side=LEFT, padx=5)
		
		self.slider = ttk.Scale(self.controls, from_=5, to=100, command=self.change_width, orient=HORIZONTAL)
		self.slider.set(self.pen_width)
		self.slider.pack(side=LEFT, padx=5)

		Button(self.controls, text='Clear', command=self.clear).pack(side=LEFT, padx=5)

		self.eraser_button = Button(self.controls, text='Eraser', command=self.eraser, relief=RAISED)
		self.eraser_button.pack(side=LEFT, padx=5)

		Button(self.controls, text='Change Pen Color', command=self.change_color).pack(side=LEFT, padx=5)
		Button(self.controls, text='Change Background Color', command=self.change_bg).pack(side=LEFT, padx=5)

		self.crosshair_list = StringVar(self.controls)
		self.crosshair_list.set('arrow')

		list = [
			'arrow',
			'circle',
			'cross',
			'dotbox',
			'plus',
			'target',
			'tcross',
		]
		
		om = OptionMenu(self.controls, self.crosshair_list, *list)
		om.config(width=10)
		om.pack(side=LEFT, padx=5)
		self.crosshair_list.trace_add('write', self.on_crosshair_change)
		
		self.c = Canvas(self.master, bg=self.color_bg, width=800, height=600, cursor='arrow')
		self.c.pack(fill=BOTH, expand=True)

		self.menu = Menu(self.master)
		self.master.config(menu=self.menu)
		file = Menu(self.menu)
		file.add_command(label='Clear', command=self.clear)
		file.add_command(label='Load Image', command=self.load_image)
		file.add_command(label='Save', command=self.save_as_png)
		file.add_command(label='Exit', command=lambda: exit())
		self.menu.add_cascade(label='Options', menu=file)

window = Tk()
window.title('Painter')

main(window)

window.mainloop()