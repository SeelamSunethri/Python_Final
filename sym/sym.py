import shutil
import psutil
from datetime import datetime
import time
import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta




class System_Monitor():

	def disk_usage(self, path):
		stat = shutil.disk_usage(path)
		return stat._asdict()

	def cpu_ram_usage(self):
		cpu = psutil.cpu_percent()
		ram = psutil.virtual_memory()._asdict()
		return cpu, ram

	def __init__(self):

		self.main_window = tk.Tk()
		self.main_window.geometry("500x400")
		self.running = True
		self.cpu = []
		self.disk_total = []
		self.disk_used = []
		self.disk_free = []
		self.graph_color = "black"

		self.ram_percent = []
		self.ram_total = []
		self.ram_used = []
		self.ram_free = []

	def update_metrics(self):

		path = "C:"
		disk_stat = self.disk_usage(path)
		cpu, ram = self.cpu_ram_usage()

		self.cpu.append(cpu)
		self.disk_total.append(round(disk_stat['total'] / (1024 ** 3), 3))

		self.disk_used.append((round(disk_stat['used'] / (1024 ** 3), 3)))
		self.disk_free.append((disk_stat['free'] / (1024 * 3), 3))

		self.ram_percent.append((ram['percent']))
		self.ram_total.append((round(ram['total'] / (1024 ** 3), 3)))
		self.ram_used.append((round(ram['used'] / (1024 ** 3), 3)))
		self.ram_free.append((round(ram['free'] / (1024 ** 3), 3)))


	def cpu(self):
		pass

	def disk(self):
		pass

	def ram(self):
		pass

	def network(self):
		pass

	def main(self):


		header_frame = tk.Frame(self.main_window)
		header_frame.pack(padx=10, pady=10)
		header = tk.Label(header_frame, text = "System Monitor")

		header.pack()

		values_frame = tk.Frame(self.main_window)
		values_frame.pack()

		network_value = tk.Label(values_frame, text="Network:     ")
		ram_value = tk.Label(values_frame, text = "RAM:     ")
		cpu_value = tk.Label(values_frame, text = "CPU:     ")
		disk_value = tk.Label(values_frame, text = "DISK:     ")



		network_value.pack(side=tk.LEFT)
		ram_value.pack(side=tk.LEFT)
		cpu_value.pack(side=tk.LEFT)
		disk_value.pack(side=tk.LEFT)


		Frame_1 = tk.Frame(self.main_window)
		Frame_1.pack(padx=10, pady=10)

		cpu_button = tk.Button(Frame_1, text="             CPU             ", command=None)
		disk_button = tk.Button(Frame_1,text="             DISK            ", command=None)
		ram_button = tk.Button(Frame_1, text="             RAM             ", command=None)
		network_button = tk.Button(Frame_1, text="              NETWORK            ", command=None)

		cpu_button.pack(side = tk.RIGHT)
		disk_button.pack(side = tk.RIGHT)
		ram_button.pack(side = tk.RIGHT)
		network_button.pack(side = tk.RIGHT)
		myCanvas = tk.Canvas(self.main_window, bg="white", height=300, width=400)

		myCanvas.pack(fill=tk.BOTH)
		l1 = myCanvas.create_line(0,0,0,300, width=6, fill = self.graph_color)
		l2 = myCanvas.create_line(0,0,600,0, width=6, fill = self.graph_color)
		l3 = myCanvas.create_line(0,300,600,300, fill = self.graph_color)
		l4 = myCanvas.create_line(497,0,497,300, fill = self.graph_color)
		graph_lines = [l1, l2, l3, l4]

		for y in range(0, 600, 30):
			for x in range(0,600, 25):
				myCanvas.create_line(x, y, x, 300, fill="grey")

		for x in range(0, 600, 30):
			for y in range(0,600, 25):
				myCanvas.create_line(x, y, 600, y, fill = "grey")



		start = datetime.now()

		x_start = 2
		while True:

			refresh_timer =  datetime.now() - start
			if str(refresh_timer).split(":")[2].split(".")[0] == '02':
				start = datetime.now()
				self.graph_color="red"
				for line in graph_lines:
					myCanvas.itemconfig(line, fill = self.graph_color)
				self.update_metrics()


				print(self.disk_total)
				print(self.disk_used)
				print(self.disk_free)
				print(int(self.cpu[-1]*3))
				print(self.ram_percent)
				print(self.ram_total)
				print(self.ram_used)
				print(self.ram_free)
				print(refresh_timer)


				ram_value.config(text = f"RAM:     {self.ram_percent[-1]}")
				cpu_value.config(text = f"CPU:     {self.cpu[-1]}")
				myCanvas.create_oval(x_start, self.cpu[-1]*3, x_start, self.cpu[-1]*3, width=2, fill='red')
				myCanvas.create_oval(x_start, self.ram_percent[-1]*3, x_start, self.ram_percent[-1]*3, width=2, fill='red')

				if len(self.cpu) > 2:
					myCanvas.create_line(x_start-25,self.cpu[-2]*3,  x_start, self.cpu[-1]*3, fill = "green")
					myCanvas.create_line(x_start - 25, self.ram_percent[-2] * 3, x_start, self.ram_percent[-1] * 3, fill="red")

				x_start += 25




				print(str(refresh_timer).split(":")[2].split(".")[0])

			#self.main_window.after(1000, self.update_metrics())
			self.main_window.update()



monitor = System_Monitor()
monitor.main()