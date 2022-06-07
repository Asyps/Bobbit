def vt_seq_win(enable: bool = True):
        from ctypes import byref, windll
        from ctypes.wintypes import DWORD
        kernel = windll.kernel32
        handle = kernel.GetStdHandle(-11)
        mode = DWORD(-1)

        if kernel.GetConsoleMode(handle, byref(mode)) == 0:
            raise WindowsError("GetConsoleMode returned 0")
        if mode.value == 0xFFFFFFFF:
            raise WindowsError("Invalid mode value received")

        if enable:
            kernel.SetConsoleMode(handle, mode.value | 0b111)
        else:
            kernel.SetConsoleMode(handle, mode.value & ~0b111)

vt_seq_win()