from slope_generator_GUI_files.template_NML import NML_string
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sys, os
import shutil


def change_gamma(channel, gamma):
	return 255 * (channel / 255) ** gamma


class SlopeGeneratorGUI(tk.Tk):
	def __init__(self, ask_to_exit=True):
		super().__init__()
		self.title("Slope Generator")
		self.iconphoto(False, tk.PhotoImage(file=os.path.join("slope_generator_GUI_files", "openttd_favicon.png")))
		self.GUI_width  = 500
		self.GUI_height = 560
		self.geometry(f"{self.GUI_width}x{self.GUI_height}+50+50")
		self.resizable(False, False)

		# Initialize variables
		self.list_of_coordinates_for_templates = [(32, 0), (64, 16), (32, 0), (64, 16), (0,  16), (32, 32), (0,  16), (32, 40), (32, 24), (32, 24), (32, 8), (0,  16), (32, 24), (32, 0), (64, 16), (32, 0), (0,  24), (32, 24), (32, 24)]
		self.colors = [(16, 16, 16), (32, 32, 32), (48, 48, 48), (64, 64, 64), (80, 80, 80), (100, 100, 100), (116, 116, 116), (132, 132, 132), (148, 148, 148), (168, 168, 168), (184, 184, 184), (200, 200, 200), (216, 216, 216), (232, 232, 232), (252, 252, 252)]
		self.range_shadow    = [1.00, 2.50]
		self.range_light     = [1.00, 0.00]
		self.range_gridlines = [1.00, 1.80]
		self.default_shadow    = 1.60
		self.default_light     = 0.50
		self.default_gridlines = 1.00
		self.list_of_templates = []
		self.list_of_templates_gridlines = []
		self.list_of_cutouts = []
		self.selected_file   = None
		self.export_filename = None

		# Build GUI
		self.bind('<Escape>', lambda event: self.exit_GUI(event, ask_to_exit))
		self.create_widgets()

		self.mainloop()

	def exit_GUI(self, event, ask):
		if ask:
			response = messagebox.askokcancel(title=f"Close?", message=f"Are you sure you want to exit?")
			if response:
				self.destroy()
		else:
			self.destroy()

	def create_widgets(self):
		font_buttons = ('Helvetica', 8, 'bold')
		font_entry   = ('Tahoma', 10, 'normal')
		padding_N    = 10
		padding_W    = 10
		background_color  = "#646488"
		orange_color_font = "#fcb030"
		white_color_font  = "#fcfcfc"
		black_color_font  = "#101010"
		black_color_bckg  = "#272820"
		yellow_color_bckg = "#e8b810"

		self.configure(bg=background_color)

		self.frame_open = tk.Frame(self, bg=background_color)
		self.frame_adjust = tk.Frame(self, bg=background_color)
		self.frame_preview = tk.Frame(self, bg=background_color)
		self.frame_open.place(x=0+padding_W, y=padding_N, width=self.GUI_width-2*padding_W, height=40)
		self.update_idletasks()
		self.frame_adjust.place(x=0+padding_W, y=self.frame_open.winfo_y()+self.frame_open.winfo_height()+5, width=self.GUI_width-2*padding_W, height=180)
		self.update_idletasks()
		self.frame_preview.place(x=0+padding_W, y=self.frame_open.winfo_y()+self.frame_open.winfo_height()+self.frame_adjust.winfo_height()+15,
								width=self.GUI_width-2*padding_W, height=320)
		self.update_idletasks()

		self.button_open_file = tk.Button(self.frame_open, text="Open file...", command=self.open_file, font=font_buttons, fg=black_color_font, bg=yellow_color_bckg)
		self.button_open_file.place(x=0, y=0, width=120, height=40)
		self.update_idletasks()

		style = ttk.Style()
		style.theme_use('alt')
		style.configure("Custom.TEntry", padding=[14, 0, 0, 0], fieldbackground=black_color_bckg, foreground=white_color_font)
		self.entry_open_file = ttk.Entry(self.frame_open, font=font_entry, style="Custom.TEntry")
		self.entry_open_file.place(x=self.button_open_file.winfo_width()+10,
								   y=self.button_open_file.winfo_y(),
								   width=350, height=self.button_open_file.winfo_height())

		#############################################################################################
		self.button_reset = tk.Button(self.frame_adjust, text="Reset", command=self.reset_gamma, font=font_buttons, fg=black_color_font, bg=yellow_color_bckg)
		self.button_reset.place(x=self.GUI_width-3*padding_W-48, y=0, width=58, height=20)
		image = Image.open(os.path.join("slope_generator_GUI_files", "adjust_shadows.png"))
		photo = ImageTk.PhotoImage(image)
		self.label_shadow = tk.Label(self.frame_adjust, image=photo)
		self.label_shadow.place(x=0, y=10, width=91, height=11)
		self.update_idletasks()
		self.label_shadow.image = photo

		self.entry_shadow_var = tk.StringVar()
		style.configure("TScale", background=background_color)
		self.slider_shadow = ttk.Scale(self.frame_adjust, from_=self.range_shadow[0], to=self.range_shadow[1], orient="horizontal", length=400,
									   command=self.update_entry_shadow, style="TScale")
		self.slider_shadow.place(x=0, y=self.label_shadow.winfo_y()+20)
		self.update_idletasks()
		self.slider_shadow.set(self.default_shadow)
		
		self.entry_shadow = ttk.Entry(self.frame_adjust, font=font_entry, textvariable=self.entry_shadow_var, style="Custom.TEntry")
		self.entry_shadow.place(x=self.GUI_width-2*padding_W-59, y=self.label_shadow.winfo_y()+13, width=59, height=35)
		self.entry_shadow.bind("<Return>", self.update_slider_shadow)
		self.slider_shadow.bind("<ButtonRelease-1>", self.update_preview)

		#############################################################################################
		light_position = self.label_shadow.winfo_y()+50
		image = Image.open(os.path.join("slope_generator_GUI_files", "adjust_light.png"))
		photo = ImageTk.PhotoImage(image)
		self.label_light = tk.Label(self.frame_adjust, image=photo)
		self.label_light.place(x=0, y=self.label_shadow.winfo_y()+light_position, width=91, height=11)
		self.update_idletasks()
		self.label_light.image = photo

		self.entry_light_var = tk.StringVar()
		self.slider_light = ttk.Scale(self.frame_adjust, from_=self.range_light[0], to=self.range_light[1], orient="horizontal", length=400,
									  command=self.update_entry_light, style="TScale")
		self.slider_light.place(x=0, y=self.label_light.winfo_y()+20)
		self.update_idletasks()
		self.slider_light.set(self.default_light)
		
		self.entry_light = ttk.Entry(self.frame_adjust, font=font_entry, textvariable=self.entry_light_var, style="Custom.TEntry")
		self.entry_light.place(x=self.GUI_width-2*padding_W-59, y=self.label_light.winfo_y()+13, width=59, height=35)
		self.entry_light.bind("<Return>", self.update_slider_light)
		self.slider_light.bind("<ButtonRelease-1>", self.update_preview)

		#############################################################################################
		gridlines_position = self.label_light.winfo_y()+50
		image = Image.open(os.path.join("slope_generator_GUI_files", "adjust_gridlines.png"))
		photo = ImageTk.PhotoImage(image)
		self.label_gridlines = tk.Label(self.frame_adjust, image=photo)
		self.label_gridlines.place(x=0, y=self.label_shadow.winfo_y()+gridlines_position, width=91, height=11)
		self.update_idletasks()
		self.label_gridlines.image = photo

		self.entry_gridlines_var = tk.StringVar()
		self.slider_gridlines = ttk.Scale(self.frame_adjust, from_=self.range_gridlines[0], to=self.range_gridlines[1], orient="horizontal", length=400,
									  command=self.update_entry_gridlines, style="TScale")
		self.slider_gridlines.place(x=0, y=self.label_gridlines.winfo_y()+20)
		self.update_idletasks()
		self.slider_gridlines.set(self.default_gridlines)

		self.entry_gridlines = ttk.Entry(self.frame_adjust, font=font_entry, textvariable=self.entry_gridlines_var, style="Custom.TEntry")
		self.entry_gridlines.place(x=self.GUI_width-2*padding_W-59, y=self.label_gridlines.winfo_y()+13, width=59, height=35)
		self.entry_gridlines.bind("<Return>", self.update_slider_gridlines)
		self.slider_gridlines.bind("<ButtonRelease-1>", self.update_preview)

		#############################################################################################
		image = Image.open(os.path.join("slope_generator_GUI_files", "preview.png"))
		photo = ImageTk.PhotoImage(image)

		self.canvas_preview = tk.Canvas(self.frame_preview, width=self.GUI_width-2*padding_W, height=240, highlightthickness=0, bd=0)
		self.canvas_preview.place(x=0, y=0, width=self.GUI_width-2*padding_W, height=240)
		self.update_idletasks()
		self.canvas_preview.create_image(0, 0, anchor="nw", image=photo)
		self.canvas_preview.images = []
		self.canvas_preview.images.append(photo)

		buttons_space = 10
		button_export_width = self.frame_preview.winfo_width()//2 - buttons_space//2
		self.button_export = tk.Button(self.frame_preview, text="Export sprites...", command=self.save_PNG, font=font_buttons, fg=black_color_font, bg=yellow_color_bckg)
		self.button_export.place(x=0, y=self.canvas_preview.winfo_height()+8, width=button_export_width*1, height=60)
		self.update_idletasks()
		self.button_NML = tk.Button(self.frame_preview, text="Save NML template...", command=self.save_NML, font=font_buttons, fg=black_color_font, bg=yellow_color_bckg)
		self.button_NML.place(x=self.button_export.winfo_width()+buttons_space, y=self.canvas_preview.winfo_height()+8, width=button_export_width*1, height=60)

		

	def update_entry_shadow(self, val):
		self.entry_shadow_var.set(f"{float(val):.2f}")

	def update_entry_light(self, val):
		self.entry_light_var.set(f"{float(val):.2f}")

	def update_entry_gridlines(self, val):
		self.entry_gridlines_var.set(f"{float(val):.2f}")

	def update_slider_shadow(self, *args):
		val = float(self.entry_shadow_var.get())
		if val < self.range_shadow[0]:
			self.slider_shadow.set(self.range_shadow[0])
		elif val > self.range_shadow[1]:
			self.slider_shadow.set(self.range_shadow[1])
		else:
			self.slider_shadow.set(val)
		self.update_preview()

	def update_slider_light(self, *args):
		val = float(self.entry_light_var.get())
		if val < self.range_light[0]:
			self.slider_light.set(self.range_light[0])
		elif val > self.range_light[1]:
			self.slider_light.set(self.range_light[1])
		else:
			self.slider_light.set(val)
		self.update_preview()

	def update_slider_gridlines(self, *args):
		val = float(self.entry_gridlines_var.get())
		if val < self.range_gridlines[0]:
			self.slider_gridlines.set(self.range_gridlines[0])
		elif val > self.range_gridlines[1]:
			self.slider_gridlines.set(self.range_gridlines[1])
		else:
			self.slider_gridlines.set(val)
		self.update_preview()

	def map_gamma_to_colors(self, *args):
		start = float(self.entry_shadow.get())
		end = float(self.entry_light.get())
		gamma = [1] * len(self.colors)
		# Shadows gamma values
		step = (1 - start) / (len(self.colors)//2)
		for i in range(0, 7):
			gamma[i] = round(start + i * step, 2)
		# Light gamma values
		step = (1 - end) / (len(self.colors)//2)
		for i in range(1, 8):
			gamma[i+7] = round(1 - i * step, 2)
		# Pair colors from template with gamma values
		self.dict_of_gamma = {self.colors[i]: gamma[i] for i in range(len(self.colors))}

	def open_file(self, *args):
		self.selected_file = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("PNG files", "*.png")])
		if not self.selected_file:
			return
		
		self.export_filename = None

		path = self.selected_file.split("/")
		if len(path) > 3:
			text = f".../{path[-3]}/{path[-2]}/{path[-1]}"
		else:
			text = self.selected_file

		self.entry_open_file.delete(0, tk.END)
		self.entry_open_file.insert(0, text)
		
		self.multiply_input_ground()

		self.update_preview()

	def multiply_input_ground(self):
		# Creates 2x2 grid from the input ground tile.
		img = Image.open(self.selected_file).convert("RGBA")
		img = self.clean_up_tile(img, remove_bckg=True, crop_bckg=True)

		# Multiply the ground
		new_img = Image.new("RGBA", (128, 63), (0, 0, 0, 0))
		new_img.paste(img, (32, 0),  mask=img)
		new_img.paste(img, (0, 16),  mask=img)
		new_img.paste(img, (64, 16), mask=img)
		new_img.paste(img, (32, 32), mask=img)

		self.input_ground = new_img

	def process_ground(self):
		self.list_of_cutouts = []
		self.map_gamma_to_colors()
		if not self.list_of_templates:
			self.list_of_templates = self.prepare_templates(os.path.join("slope_generator_GUI_files", "template.png"))
		self.create_cutouts()

		if not self.list_of_templates_gridlines:
			self.list_of_templates_gridlines = self.prepare_templates(os.path.join("slope_generator_GUI_files", "template_gridlines.png"))
		self.add_gridlines()

	def prepare_templates(self, template_file):
		img = Image.open(template_file).convert("RGBA")
		width, height = img.size

		results = []
		# Loop to extract each template
		for start_x in range(0, width, 80):
			end_x = start_x + 64
			if end_x > width: break
			cropped_image = img.crop((start_x, 0, end_x, height))
			cropped_image = self.clean_up_tile(cropped_image, remove_bckg=False, crop_bckg=True)
			
			results.append(cropped_image)

		return results

	def clean_up_tile(self, img, remove_bckg=False, crop_bckg=False):
		w, h = img.size
		img_data = img.load()

		if remove_bckg:
			# Make background transparent if blue or white
			for y in range(h):
					for x in range(w):
						if img_data[x, y] in [(0, 0, 255, 255), (255, 255, 255, 255)]: img_data[x, y] = (0, 0, 0, 0)
		if crop_bckg:
			# Crop background if needed
			alpha = img.split()[-1]
			bbox = alpha.getbbox()
			if bbox:
				img = img.crop(bbox)

		return img

	def create_cutouts(self):
		for template, coord in zip(self.list_of_templates, self.list_of_coordinates_for_templates):
			mask = Image.new("RGBA", self.input_ground.size, (0, 0, 0, 0))
			mask.paste(template, coord, mask=template)
			cutout = Image.composite(self.input_ground, mask, mask)
			cutout = self.clean_up_tile(cutout, remove_bckg=False, crop_bckg=True)

			# Edit gamma of pixels according to template
			w, h = cutout.size
			template_data = template.load()
			cutout_data = cutout.load()

			for y in range(h):
				for x in range(w):
					template_color = template_data[x, y][:3]
					cutout_color = cutout_data[x, y][:3]
					if template_color in self.dict_of_gamma:
						gamma = self.dict_of_gamma[template_color]
						r = change_gamma(cutout_color[0], gamma)
						g = change_gamma(cutout_color[1], gamma)
						b = change_gamma(cutout_color[2], gamma)
						cutout_data[x, y] = (int(r), int(g), int(b), 255)

			self.list_of_cutouts.append(cutout)

	def add_gridlines(self):
		for i, (template, cutout) in enumerate(zip(self.list_of_templates_gridlines, self.list_of_cutouts)):
			# Lower gamma to create gridlines
			w, h = cutout.size
			template_data = template.load()
			cutout_data = cutout.load()

			gamma_gridlines = float(self.entry_gridlines.get())

			for y in range(h):
				for x in range(w):
					template_color = template_data[x, y][:3]
					cutout_color = cutout_data[x, y][:3]
					if template_color == (255, 0, 0):
						r = change_gamma(cutout_color[0], gamma_gridlines)
						g = change_gamma(cutout_color[1], gamma_gridlines)
						b = change_gamma(cutout_color[2], gamma_gridlines)
						cutout_data[x, y] = (int(r), int(g), int(b), 255)

			self.list_of_cutouts[i] = cutout

	def update_preview(self, *args):
		if not self.selected_file:
			return
		self.process_ground()
		self.insert_tiles_into_preview()

	def insert_tiles_into_preview(self):
		coords = [
			[(1, 102), (33, 118), (65, 134), (97, 150), (129, 70), (129, 166), (161, 86), (161, 182), (193, 198), (225, 214), (1, 38), (33, 22), (65, 6), (97, -10), (161, -10), (289, 214), (321, 198), (353, 182), (193, 6), (225, 22), (257, 38), (289, 54), (321, 70), (353, 86), (129, -26), (257, 230), (449, 134), (-31, 86), (-31, 54)],
			[(289, 86), (289, 182), (417, 118), (417, 150)],
			[(129, 6), (321, 102), (385, 102)],
			[(97, 86), (129, 102), (161, 22), (193, 38), (225, 54), (257, 70)],
			[(1,70)],
			[(289, 118), (289, 150)],
			[(33, 54), (65, 38), (97, 22), (193, 102)],
			[(161, 118), (225, 150)],
			[(257, 190), (321, 158), (385, 158)],
			[(97, 46)],
			[(257, 126)],
			[(65, 62), (257, 94), (257, 158), (193, 126)],
			[(33, 78), (65, 94), (97, 110), (129, 126), (161, 142), (193, 158), (225, 174), (161, 46), (193, 62)],
			[(129,30), (225, 110)],
			[(225, 78)],
			[(353, 134)],
			[(353, 118)],
			[(385, 126)],
			[(321, 126)]
		]

		for i, tile in enumerate(coords):
			for coord in tile:
				img = self.list_of_cutouts[i]
				overlay_img = ImageTk.PhotoImage(img)
				self.canvas_preview.create_image(coord, anchor="nw", image=overlay_img)
				self.canvas_preview.images.append(overlay_img)

	def save_PNG(self):
		if not self.selected_file:
			return
		root, ext = os.path.splitext(os.path.basename(self.selected_file))
		output_name = root + "_auto-slope" + ext
		file_path = filedialog.asksaveasfilename(filetypes = [('PNG files', '*.png')], defaultextension = '*.png',
												 initialfile=output_name)

		if file_path:
			output_image = self.create_output_image()
			output_image.save(file_path)
			self.export_filename = os.path.splitext(os.path.basename(file_path))[0]
			source = os.path.join("slope_generator_GUI_files", "water.png")
			destination = os.path.join(os.path.dirname(file_path), f"{self.export_filename}_water.png")
			shutil.copy(source, destination)

	def save_NML(self, *args):
		if not self.selected_file:
			return
		root, ext = os.path.splitext(os.path.basename(self.selected_file))
		if self.export_filename:
			NML_string_edited = NML_string.replace("INPUTFILE", root).replace("SPRITESFILE", self.export_filename)
		else:
			NML_string_edited = NML_string.replace("INPUTFILE", root).replace("SPRITESFILE", root)

		file_path = filedialog.asksaveasfilename(filetypes = [('NML files', '*.nml')], defaultextension = '*.nml', initialfile=root+".nml")
		if file_path:
			with open(file_path, mode='w') as output_file:
			    output_file.write(NML_string_edited)

	def create_output_image(self):
		output_image = Image.new("RGBA", (1504, 50), (0, 0, 0, 0))
		for image, x in zip(self.list_of_cutouts, range(len(self.list_of_cutouts))):
			output_image.paste(image, (x*80, 0), mask=image)

		result_image = Image.new("RGBA", (1504, 100), (0, 0, 0, 0))
		result_image.paste(output_image, (0, 0), mask=output_image)

		template_coast = Image.open(os.path.join("slope_generator_GUI_files", "template_coast.png")).convert("RGBA")
		alpha = template_coast.split()[-1]
		output_image_coast = Image.composite(output_image, Image.new("RGBA", output_image.size, (0, 0, 0, 0)), alpha)

		result_image.paste(output_image_coast, (0, 50), mask=output_image_coast)

		return result_image

	def reset_gamma(self, *args):
		self.slider_shadow.set(self.default_shadow)
		self.slider_light.set(self.default_light)
		self.slider_gridlines.set(self.default_gridlines)
		self.update_preview()

if __name__ == '__main__':
	SlopeGeneratorGUI(ask_to_exit=True)