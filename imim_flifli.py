from PIL import ImageTk, Image
import PySimpleGUI as sg
import numpy
import os

def format_ofile_name(fname, ver):
	fname = os.path.basename(fname)
	fname = fname.split('.')[0]
	fname += ver
	fname += '.png' 
	return fname

def make_left_image(image, reflect_width):
	np_im = numpy.array(image)
	left_reflection = np_im[:, :reflect_width, :]
	left_reversed = numpy.fliplr(numpy.copy(left_reflection))
	left_final = numpy.concatenate((left_reflection, left_reversed), axis=1)
	return Image.fromarray(left_final)

def make_right_image(image, reflect_width):
	np_im = numpy.array(image)
	right_reflection = np_im[:, reflect_width:, :]
	right_reversed = numpy.fliplr(numpy.copy(right_reflection))
	right_final = numpy.concatenate((right_reversed, right_reflection), axis=1)
	return Image.fromarray(right_final)

window = sg.Window('ImIm FliFli'). Layout(
	[
		[sg.Text('Filename')], [sg.InputText('B:/image0.jpg'), sg.FileBrowse()], 
		[sg.OK()],
		[sg.Slider(range=(0, 100), default_value=50, orientation='horizontal', enable_events=True)],
		[sg.Canvas(size=(50,50), background_color='black', key='orig_canvas')],
		[sg.Canvas(size=(50,50), background_color='black', key='mod1'), sg.Button(button_text="Save ver1")], 
		[sg.Canvas(size=(50,50), background_color='black', key='mod2'), sg.Button(button_text="Save ver2")]
	])

reflect_line = None
orig_image = None
image = None
mod1_imTk = None
mod2_imTk = None
image_height = 200

while True:
	event, output = window.Read()

	if event is None:
		break

	orig_canvas = window.FindElement('orig_canvas').TKCanvas
	mod1_canvas = window.FindElement('mod1').TKCanvas
	mod2_canvas = window.FindElement('mod2').TKCanvas

	if event == 'OK':
		orig_image = Image.open(output[0])
		ratio = image_height / orig_image.height

		# resize to max height 200
		image = orig_image.resize((int(orig_image.width * ratio), image_height))

		imTk = ImageTk.PhotoImage(image)
		orig_canvas.config(width=imTk.width(), height=imTk.height())
		original_image = orig_canvas.create_image((imTk.width()/2,imTk.height()/2), image=imTk)
		reflect_line = orig_canvas.create_line(imTk.width()/2, 0, imTk.width()/2, imTk.height(), fill='red')


	elif event == 1 and image != None:
		# change position of line on orig_canvas
		new_x_pos = (imTk.width() * (output[1]/100))
		orig_canvas.coords(reflect_line, new_x_pos, 0, new_x_pos, imTk.height())

		# change width of mod1 and mod2
		reflect_width = int(imTk.width() * (output[1]/100))
		mod1_canvas.config(width=2 * reflect_width, height=imTk.height())
		mod2_canvas.config(width=2 * imTk.width() * ((100 - output[1])/100), height=imTk.height())

		if image != None:
			mod1_imTk = ImageTk.PhotoImage(make_left_image(image, reflect_width))
			mod1_canvas.create_image((reflect_width, mod1_imTk.height()/2), image=mod1_imTk)

			mod2_imTk = ImageTk.PhotoImage(make_right_image(image, reflect_width))
			mod2_canvas.create_image((imTk.width() * ((100 - output[1])/100), mod2_imTk.height()/2), image=mod2_imTk)


	elif event == "Save ver1" and mod1_imTk != None:
		fname = format_ofile_name(output[0], '1')
		make_left_image(orig_image, int(orig_image.width * (output[1]/100))).save(fname)

	elif event == "Save ver2" and mod2_imTk != None:
		fname = format_ofile_name(output[0], '2')
		make_right_image(orig_image, int(orig_image.width * (output[1]/100))).save(fname)

