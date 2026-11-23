//go:build windows

package main

import (
	"runtime"
	"syscall"
	"time"
	"unsafe"

	"golang.org/x/sys/windows"
)

func trayAvailable() bool { return true }

// windowClass names the main window so we can find its HWND.
const windowClass = "sheetsDeskMainWindow"

var (
	ole32                = windows.NewLazySystemDLL("ole32.dll")
	procCoCreateInstance = ole32.NewProc("CoCreateInstance")
	user32               = windows.NewLazySystemDLL("user32.dll")
	procFindWindowW      = user32.NewProc("FindWindowW")

	clsidTaskbarList = windows.GUID{Data1: 0x56FDF344, Data2: 0xFD6D, Data3: 0x11d0, Data4: [8]byte{0x95, 0x8A, 0x00, 0x60, 0x97, 0xC9, 0xA0, 0x90}}
	iidITaskbarList  = windows.GUID{Data1: 0x56FDF342, Data2: 0xFD6D, Data3: 0x11d0, Data4: [8]byte{0x95, 0x8A, 0x00, 0x60, 0x97, 0xC9, 0xA0, 0x90}}
)

// ITaskbarList vtable slots.
const (
	tbRelease   = 2
	tbHrInit    = 3
	tbDeleteTab = 5
)

// hideTaskbarButton removes the main window's taskbar button (the app lives in
// the tray). The shell adds a button whenever the window is shown, so this
// runs after every show; it retries briefly because Wails shows the window
// asynchronously on its UI thread.
func hideTaskbarButton() {
	go func() {
		for _, d := range []time.Duration{50, 250, 750} {
			time.Sleep(d * time.Millisecond)
			deleteTab()
		}
	}()
}

func deleteTab() {
	runtime.LockOSThread()
	defer runtime.UnlockOSThread()
	cls, _ := windows.UTF16PtrFromString(windowClass)
	hwnd, _, _ := procFindWindowW.Call(uintptr(unsafe.Pointer(cls)), 0)
	if hwnd == 0 {
		return
	}
	var pid uint32
	if _, err := windows.GetWindowThreadProcessId(windows.HWND(hwnd), &pid); err != nil || pid != windows.GetCurrentProcessId() {
		return
	}
	if err := windows.CoInitializeEx(0, windows.COINIT_APARTMENTTHREADED); err == nil {
		defer windows.CoUninitialize()
	}
	// tb points at the COM object, whose first word points at its vtable.
	var tb *struct{ vtbl *[8]uintptr }
	if hr, _, _ := procCoCreateInstance.Call(uintptr(unsafe.Pointer(&clsidTaskbarList)), 0,
		1 /* CLSCTX_INPROC_SERVER */, uintptr(unsafe.Pointer(&iidITaskbarList)), uintptr(unsafe.Pointer(&tb))); hr != 0 || tb == nil {
		return
	}
	this := uintptr(unsafe.Pointer(tb))
	defer syscallN(tb.vtbl[tbRelease], this)
	if hr := syscallN(tb.vtbl[tbHrInit], this); hr != 0 {
		return
	}
	syscallN(tb.vtbl[tbDeleteTab], this, hwnd)
}

// syscallN calls a COM method; it returns the HRESULT.
func syscallN(fn uintptr, args ...uintptr) uintptr {
	r, _, _ := syscall.SyscallN(fn, args...)
	return r
}
