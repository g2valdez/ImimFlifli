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
image = None
mod1_image = None
mod2_image = None
image_height = 200

while True:
	event, output = window.Read()
	print(event)
	print(output)

	if event is None:
		break

	orig_canvas = window.FindElement('orig_canvas').TKCanvas
	mod1_canvas = window.FindElement('mod1').TKCanvas
	mod2_canvas = window.FindElement('mod2').TKCanvas

	if event == 'OK':
		image = Image.open(output[0])
		ratio = image_height / image.height

		# resize to max height 200
		image = image.resize((int(image.width * ratio), image_height))

		imTk = ImageTk.PhotoImage(image)
		orig_canvas.config(width=imTk.width(), height=imTk.height())
		original_image = orig_canvas.create_image((imTk.width()/2,imTk.height()/2), image=imTk)
		reflect_line = orig_canvas.create_line(imTk.width()/2, 0, imTk.width()/2, imTk.height(), fill='red')


	elif event == 1:
		# change position of line on orig_canvas
		new_x_pos = (imTk.width() * (output[1]/100))
		orig_canvas.coords(reflect_line, new_x_pos, 0, new_x_pos, imTk.height())

		# change width of mod1 and mod2
		reflect_width = int(imTk.width() * (output[1]/100))
		mod1_canvas.config(width=2 * reflect_width, height=imTk.height())
		mod2_canvas.config(width=2 * imTk.width() * ((100 - output[1])/100), height=imTk.height())

		if image != None:
			np_im = numpy.array(image)
			left_reflection = np_im[:, :reflect_width, :]
			left_reversed = numpy.fliplr(numpy.copy(left_reflection))
			left_final = numpy.concatenate((left_reflection, left_reversed), axis=1)
			mod1_image = Image.fromarray(left_final)
			mod1_imTk = ImageTk.PhotoImage(mod1_image)
			mod1_canvas.create_image((reflect_width, mod1_imTk.height()/2), image=mod1_imTk)


			right_reflection = np_im[:, reflect_width:, :]
			right_reversed = numpy.fliplr(numpy.copy(right_reflection))
			right_final = numpy.concatenate((right_reversed, right_reflection), axis=1)
			mod2_image = Image.fromarray(right_final)
			mod2_imTk = ImageTk.PhotoImage(mod2_image)
			mod2_canvas.create_image((imTk.width() * ((100 - output[1])/100), mod2_imTk.height()/2), image=mod2_imTk)


	elif event == "Save ver1" and mod1_image != None:
		fname = format_ofile_name(output[0], '1')
		mod1_image.save(fname)

	elif event == "Save ver2" and mod2_image != None:
		fname = format_ofile_name(output[0], '2')
		mod2_image.save(fname)

