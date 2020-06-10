from imageai.Detection import VideoObjectDetection
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askdirectory
import threading
import datetime
import cv2 as cv
import os
import shutil

class my_app():

	def __init__(self):

		self.root = Tk()

		self.root.title("CCTV Video Analysis")
		self.root.geometry("450x550")
		self.root.resizable(False, False)

		self.video_path = StringVar()
		self.frame_processing = StringVar()
		self.objects = StringVar()
		self.total_frames = StringVar()
		self.output_name = StringVar()
		self.location = StringVar()
		self.fps = StringVar()
		self.eta = StringVar()

		self.frame = Frame(self.root, padding=(40,40))
		self.frame.grid()
		
		self.video_label = Label(self.frame, text="Video Path")
		self.video_label.grid(row=0, column=0, sticky="EW", padx=10, pady=10)

		self.video_entry = Entry(self.frame, width=40, textvariable=self.video_path)
		self.video_entry.grid(row=0, column=1, sticky="EW", columnspan=2, padx=10, pady=10)
		self.video_entry.insert(0, "Enter path here or click on Upload Video")

		self.upload_button = Button(self.frame, text="Upload Video", command=self.upload_video)
		self.upload_button.grid(row=1, column=0, sticky="EW", padx=10, pady=10)

		self.total_frames_label = Label(self.frame, textvariable=self.total_frames)
		self.total_frames_label.grid(row=1, column=1, sticky="EW", padx=10, pady=10)

		self.fps_label = Label(self.frame, textvariable=self.fps)
		self.fps_label.grid(row=1, column=2, sticky="EW", padx=10, pady=2)

		self.object_label = Label(self.frame, text="Object")
		self.object_label.grid(row=2, column=0, sticky="EW", padx=10, pady=10)

		self.object_entry = Entry(self.frame, width=40, textvariable=self.objects)
		self.object_entry.grid(row=2, column=1, sticky="EW", columnspan=2, padx=10, pady=10)
		self.object_entry.insert(0, "Enter the desired object you want to detect")

		self.object_help_button = Button(self.frame, text="Help", command=self.open_help_window)
		self.object_help_button.grid(row=3, column=0, sticky="EW", padx=10, pady=10)

		self.output_label = Label(self.frame, text="Video Name")
		self.output_label.grid(row=4, column=0, sticky="EW", padx=10, pady=10)

		self.output_entry = Entry(self.frame, width=40, textvariable=self.output_name)
		self.output_entry.grid(row=4, column=1, sticky="EW", columnspan=2, padx=10, pady=10)
		self.output_entry.insert(0, "Enter the desired video name")

		self.location_label = Label(self.frame, text="Video Location")
		self.location_label.grid(row=5, column=0, sticky="EW", padx=10, pady=10)

		self.location_entry = Entry(self.frame, width=40, textvariable=self.location)
		self.location_entry.grid(row=5, column=1, sticky="EW", columnspan=2, padx=10, pady=10)
		self.location_entry.insert(0, "Enter path or click on Browse Location")

		self.browse_button = Button(self.frame, text="Browse Location", command=self.browse_location)
		self.browse_button.grid(row=6, column=0, sticky="EW", padx=10, pady=10)

		# self.

		self.process_button = Button(self.frame, text="Process Video", command=self.runDetection)
		self.process_button.grid(row=7, column=0, sticky="EW", padx=10, pady=20)

		self.progress = Progressbar(self.frame, orient=HORIZONTAL, length=40, mode="indeterminate")

		self.frame_label = Label(self.frame, textvariable=self.frame_processing)
		self.frame_label.grid(row=8, column=1, sticky="EW", columnspan=2, padx=10, pady=10)

		self.time_label = Label(self.frame, textvariable=self.eta)
		self.time_label.grid(row=9, column=1, sticky="EW", padx=10, pady=10)

		self.open_button = Button(self.frame, text="Open Folder", command=self.open_folder)
		self.open_button.grid(row=10, column=0, sticky="EW", padx=10, pady=1)

		self.root.mainloop()

	def upload_video(self):

		file = askopenfile(mode="r", filetypes=[("MP4 Files", "*mp4")])

		if file is not None:

			self.video_path.set(file.name)

			global video_fps, totalFrames

			cap = cv.VideoCapture(file.name)
			totalFrames = int(cap.get(cv.CAP_PROP_FRAME_COUNT)) 
			video_fps = int(cap.get(cv.CAP_PROP_FPS))
			cap.release()

			self.total_frames.set("Total frames: " + str(totalFrames))
			self.fps.set(str(video_fps) + " FPS")
			self.eta.set("ETA: " + str(datetime.timedelta(seconds=(totalFrames//video_fps)*3)))

		else:
			messagebox.showerror("Upload File Error", "Input file path cannot be empty!")

	def open_help_window(self):

		help_window = Toplevel(self.root)

		help_window.title("Objects Help Window")
		help_window.geometry("550x620")
		help_window.resizable(False, False)

		help_frame = Frame(help_window, padding=(40,40))
		help_frame.grid()

		persons = "'person'"
		vehicles1 = "'bicycle', 'car', 'motorcycle', 'airplane'"
		vehicles2 = "'bus', 'train', 'truck', 'boat'"
		road_objects1 = "'traffic light', 'fire hydrant'"
		road_objects2 = "'stop_sign', 'parking meter', 'bench'"
		animals1 = "'bird', 'cat', 'dog', 'bear', 'horse'"
		animals2 = "'sheep', 'cow', 'zebra', 'giraffe', 'elephant'"
		accessories = "'backpack', 'umbrella', 'handbag', 'tie', 'suitcase'"
		games_sports1 = "'frisbee', 'skis', 'snowboard', 'surfboard', 'tennis racket'"
		games_sports2 = "'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard'"
		kitchen_objects1 = "'bottle', 'wine glass', 'cup'"
		kitchen_objects2 = "'fork', 'knife', 'spoon', 'bowl'"
		food1 = "'banana', 'apple', 'sandwich', 'hot dog', 'pizza'"
		food2 = "'orange', 'broccoli', 'carrot', 'donot', 'cake'"
		home_objects1 = "'chair', 'couch', 'potted plant'"
		home_objects2 = "'bed', 'dining table', 'toilet', 'sink'"
		elec_objects1 = "'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'refrigerator'"
		elec_objects2 = "'cell phone', 'microwave', 'oven', 'toaster', 'hair dryer'"
		misc = "'book', 'clock', 'vase', 'scissors', 'teddy bear', 'toothbrush'"

		l0 = Label(help_frame, text="These are the objects which can be identified in video:")
		l0.grid(row=0, column=0, sticky="EW", columnspan=2, padx=10, pady=1)

		l00 = Label(help_frame, text="(Please make sure that you enter the correct spelling as shown here)")
		l00.grid(row=1, column=0, sticky="EW", columnspan=2, padx=10, pady=1)

		lh1 = Label(help_frame, text="Category")
		lh1.grid(row=2, column=0, sticky="EW", padx=10, pady=10)

		lh2 = Label(help_frame, text="Objects")
		lh2.grid(row=2, column=1, sticky="EW", padx=10, pady=10)

		l1 = Label(help_frame, text="People")
		l1.grid(row=3, column=0, sticky="EW", padx=10, pady=3)

		l10 = Label(help_frame, text=persons)
		l10.grid(row=3, column=1, sticky="EW", padx=10, pady=3)

		l2 = Label(help_frame, text="Vehicles")
		l2.grid(row=4, column=0, sticky="EW", padx=10, pady=3)

		l20 = Label(help_frame, text=vehicles1)
		l20.grid(row=4, column=1, sticky="EW", padx=10, pady=3)

		l21 = Label(help_frame, text=vehicles2)
		l21.grid(row=5, column=1, sticky="EW", padx=10, pady=3)

		l3 = Label(help_frame, text="Road Objects")
		l3.grid(row=6, column=0, sticky="EW", padx=10, pady=3)

		l31 = Label(help_frame, text=road_objects1)
		l31.grid(row=6, column=1, sticky="EW", padx=10, pady=3)

		l32 = Label(help_frame, text=road_objects2)
		l32.grid(row=7, column=1, sticky="EW", padx=10, pady=3)

		l4 = Label(help_frame, text="Animals")
		l4.grid(row=8, column=0, sticky="EW", padx=10, pady=3)

		l41 = Label(help_frame, text=animals1)
		l41.grid(row=8, column=1, sticky="EW", padx=10, pady=3)

		l42 = Label(help_frame, text=animals2)
		l42.grid(row=9, column=1, sticky="EW", padx=10, pady=3)

		l5 = Label(help_frame, text="Accessories")
		l5.grid(row=11, column=0, sticky="EW", padx=10, pady=3)

		l51 = Label(help_frame, text=accessories)
		l51.grid(row=11, column=1, sticky="EW", padx=10, pady=3)

		l6 = Label(help_frame, text="Games/Sports Equipments")
		l6.grid(row=12, column=0, sticky="EW", padx=10, pady=3)

		l61 = Label(help_frame, text=games_sports1)
		l61.grid(row=12, column=1, sticky="EW", padx=10, pady=3)

		l62 = Label(help_frame, text=games_sports2)
		l6.grid(row=13, column=1, sticky="EW", padx=10, pady=3)

		l7 = Label(help_frame, text="Kitchen")
		l7.grid(row=14, column=0, sticky="EW", padx=10, pady=3)

		l71 = Label(help_frame, text=kitchen_objects1)
		l71.grid(row=14, column=1, sticky="EW", padx=10, pady=3)

		l72 = Label(help_frame, text=kitchen_objects2)
		l72.grid(row=15, column=1, sticky="EW", padx=10, pady=3)

		l8 = Label(help_frame, text="Home")
		l8.grid(row=16, column=0, sticky="EW", padx=10, pady=3)

		l81 = Label(help_frame, text=home_objects1)
		l81.grid(row=16, column=1, sticky="EW", padx=10, pady=3)

		l82 = Label(help_frame, text=home_objects2)
		l82.grid(row=17, column=1, sticky="EW", padx=10, pady=3)

		l9 = Label(help_frame, text="Electronic/Electrical")
		l9.grid(row=18, column=0, sticky="EW", padx=10, pady=3)

		l91 = Label(help_frame, text=elec_objects1)
		l91.grid(row=18, column=1, sticky="EW", padx=10, pady=3)

		l91 = Label(help_frame, text=elec_objects2)
		l91.grid(row=19, column=1, sticky="EW", padx=10, pady=3)

		l10 = Label(help_frame, text="Miscellaneous")
		l10.grid(row=20, column=0, sticky="EW", padx=10, pady=3)

		l101 = Label(help_frame, text=misc)
		l101.grid(row=20, column=1, sticky="EW", padx=10, pady=3)

		b1 = Button(help_frame, text="OK", command=help_window.destroy)
		b1.grid(row=21, column=0, sticky="EW", padx=10, pady=10)

		help_window.transient(self.root)
		help_window.grab_set()
		self.root.wait_window(help_window)

	def browse_location(self):

		path = askdirectory()

		if path != "":
			self.location.set(path)
			print(self.location.get())

		else:
			messagebox.showerror("Location Error", "Destination location cannot be empty!")

	def runDetection(self):

		def real_runDetection():

			video = self.video_path.get()
			output = self.location.get()
			name = self.output_name.get()
			obj = self.objects.get().lower()

			self.progress.grid(row=7, column=1, columnspan=2, sticky="EW", padx=10, pady=10)
			self.progress.start()

			flag = 0

			obj_list = []

			all_obj_list = [ "person",
			"bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
			"traffic light", "fire hydrant", "stop_sign", "parking meter", "bench",
			"bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
			"backpack", "umbrella", "handbag", "tie", "suitcase",
			"frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
			"bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
			"banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donot", "cake",
			"chair", "couch", "potted plant", "bed", "dining table", "toilet", "sink",
			"tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "hair dryer", "refrigerator",
			"book", "clock", "vase", "scissors", "teddy bear", "toothbrush" ]

			if not os.path.exists(video):
				flag = 1
				messagebox.showerror("Input Video", "Input video path not defined!")
				self.progress.stop()
				self.progress.grid_forget()
				self.process_button['state']='normal'
				return

			if not os.path.exists(output):
				flag = 1
				messagebox.showerror("Output Video", "Output video path not defined!")
				self.progress.stop()
				self.progress.grid_forget()
				self.process_button['state']='normal'
				return

			if name == "" or name == "Enter the desired video name":
				flag = 1
				messagebox.showerror("Output Video", "Output video name not defined!")
				self.progress.stop()
				self.progress.grid_forget()
				self.process_button['state']='normal'
				return

			for x in all_obj_list:
				if x != obj:
					flag = 2
				else:
					flag = 0
					break

			if flag == 2:
				messagebox.showerror("Objects Error", "Object values do not match with any recognised objects!")
				self.progress.stop()
				self.progress.grid_forget()
				self.process_button['state']='normal'
				return

			if flag == 0:

				try:
					execution_path = os.getcwd()

					detector = VideoObjectDetection()
					detector.setModelTypeAsYOLOv3()
					detector.setModelPath("yolo.h5")
					detector.loadModel(detection_speed="flash")

					def saveFrames():

						brackets = []
						index = -1

						for i in range(0, totalFrames):

							if i % video_fps == 0:
								index+=1
								brackets.append([])
								brackets[index].append(i+1)

							else:
								brackets[index].append(i+1)

						index = 0

						cap = cv.VideoCapture(video)

						for i in obj_list:

							if index > len(brackets):
								break

							for j in brackets[index]:

								if i == j:

									cap.set(1, i-1)
									ret, frame = cap.read()
									cv.imwrite(os.path.join(output, str(i)+".jpg"), frame)

									index+=1
									break

						cap.release()

					def forFrames(frame_number, output_array, output_count):

						self.frame_processing.set("Processing frame: " + str(frame_number))

						for key in output_count:
							if key == obj:
								obj_list.append(frame_number)

					ouput = detector.detectObjectsFromVideo(input_file_path=video, output_file_path=os.path.join(output, name),
						frames_per_second=video_fps, log_progress=True, per_frame_function=forFrames, minimum_percentage_probability=30)

					self.frame_processing.set("Processing done, now saving matched frames if any...")

					saveFrames()

					self.progress.stop()
					self.progress.grid_forget()
					self.frame_label.grid_forget()
					messagebox.showinfo("Processing Success", "Video was successfully processed and saved in desired location, to open it click on Open Folder.")
					self.process_button['state']='normal'

				except:
					self.progress.stop()
					self.progress.grid_forget()
					self.frame_label.grid_forget()
					self.process_button['state']='normal'
					messagebox.showerror("Processing Error", "Processing failed!")

		self.process_button['state']='disabled'
		threading.Thread(target=real_runDetection).start()

	def open_folder(self):

		if os.path.exists(self.location.get()):
			os.system("start " + str(self.location.get()))

		else:
			messagebox.showerror("Error", "Path does not exists!")

if __name__ == "__main__":

	app = my_app()
