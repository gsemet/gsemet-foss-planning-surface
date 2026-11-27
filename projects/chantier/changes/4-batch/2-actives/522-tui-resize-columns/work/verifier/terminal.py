"""The Verifier's drive of the real `chantier live` in a classic console window of its own, on the
demo board: it resizes that window, sends it keys, reads the drawn text back from its screen
buffer, and captures that one window (`PrintWindow`), the served path painted over (it lies under
the home folder). Standard library only; it touches no other window and stops only what it started.

usage, from the worktree: uv run --no-sync python <this file> <out folder> <png folder>"""

import ctypes
import os
import struct
import subprocess
import sys
import time
import zlib
from ctypes import wintypes
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKTREE = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-32-CR-522")
SCRATCH = HERE.parent / "scratch"
TITLE = "chantier live (demo)"
HOME_MARKS = (os.environ.get("USERNAME", "").lower(), Path.home().name.lower(), "users")

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
u32 = ctypes.WinDLL("user32", use_last_error=True)
g32 = ctypes.WinDLL("gdi32", use_last_error=True)


def child() -> None:
    """Runs inside the new console: the size, the title, then the head's `chantier live`."""
    os.system("mode con: cols=150 lines=28")
    k32.SetConsoleTitleW(TITLE)
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CODE_SESSION_ID", "CHANTIER_ROOT", "CHANTIER_BATCH", "COPILOT_CLI")}
    env |= {"CHANTIER_CONFIG_HOME": str(SCRATCH / "config"), "PYTHONUTF8": "1",
            "CHANTIER_SKILL_DIR": str(WORKTREE / "skills" / "chantier"),
            "CHANTIER_PLUGIN_ROOT": str(WORKTREE)}
    Path(sys.argv[2]).write_text(str(os.getpid()), encoding="utf-8")
    exe = WORKTREE / ".venv" / "Scripts" / "chantier.exe"
    code = subprocess.call([str(exe), "live"], cwd=SCRATCH / "demo-shop", env=env)
    Path(sys.argv[2] + ".exit").write_text(str(code), encoding="utf-8")


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]


class CSBI(ctypes.Structure):
    _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD), ("wAttributes", wintypes.WORD),
                ("srWindow", SMALL_RECT), ("dwMaximumWindowSize", COORD)]


class FONT(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.ULONG), ("nFont", wintypes.DWORD), ("dwFontSize", COORD),
                ("FontFamily", wintypes.UINT), ("FontWeight", wintypes.UINT),
                ("FaceName", ctypes.c_wchar * 32)]


class KEY(ctypes.Structure):
    _fields_ = [("bKeyDown", wintypes.BOOL), ("wRepeatCount", wintypes.WORD),
                ("wVirtualKeyCode", wintypes.WORD), ("wVirtualScanCode", wintypes.WORD),
                ("UnicodeChar", ctypes.c_wchar), ("dwControlKeyState", wintypes.DWORD)]


class _EV(ctypes.Union):
    _fields_ = [("KeyEvent", KEY), ("pad", ctypes.c_byte * 16)]


class INPUT_RECORD(ctypes.Structure):
    _fields_ = [("EventType", wintypes.WORD), ("Event", _EV)]


k32.CreateFileW.restype = wintypes.HANDLE
k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
k32.ReadConsoleOutputCharacterW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD,
                                            COORD, ctypes.POINTER(wintypes.DWORD)]
k32.GetConsoleScreenBufferInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(CSBI)]
k32.GetCurrentConsoleFontEx.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.POINTER(FONT)]
k32.WriteConsoleInputW.argtypes = [wintypes.HANDLE, ctypes.POINTER(INPUT_RECORD), wintypes.DWORD,
                                   ctypes.POINTER(wintypes.DWORD)]
k32.GetConsoleWindow.restype = wintypes.HWND
u32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
                             ctypes.c_int, ctypes.c_int, wintypes.UINT]
u32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
u32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
u32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
u32.GetDC.restype = wintypes.HDC
u32.GetDC.argtypes = [wintypes.HWND]
u32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
u32.PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
g32.CreateCompatibleDC.restype = wintypes.HDC
g32.CreateCompatibleDC.argtypes = [wintypes.HDC]
g32.CreateCompatibleBitmap.restype = wintypes.HBITMAP
g32.CreateCompatibleBitmap.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]
g32.SelectObject.restype = wintypes.HGDIOBJ
g32.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
g32.GetDIBits.argtypes = [wintypes.HDC, wintypes.HBITMAP, wintypes.UINT, wintypes.UINT,
                          ctypes.c_void_p, ctypes.c_void_p, wintypes.UINT]
g32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
g32.DeleteDC.argtypes = [wintypes.HDC]


def handle(name: str) -> int:
    h = k32.CreateFileW(name, 0xC0000000, 3, None, 3, 0, None)
    assert h not in (None, wintypes.HANDLE(-1).value), (name, ctypes.get_last_error())
    return h


def info() -> CSBI:
    h = handle("CONOUT$")
    out = CSBI()
    assert k32.GetConsoleScreenBufferInfo(h, ctypes.byref(out)), ctypes.get_last_error()
    k32.CloseHandle(wintypes.HANDLE(h))
    return out


def size() -> tuple[int, int]:
    w = info().srWindow
    return w.Right - w.Left + 1, w.Bottom - w.Top + 1


def screen() -> list[str]:
    cols, rows = size()
    top = info().srWindow.Top
    h = handle("CONOUT$")
    lines = []
    for y in range(rows):
        buf, n = ctypes.create_unicode_buffer(cols + 1), wintypes.DWORD()
        k32.ReadConsoleOutputCharacterW(h, buf, cols, COORD(0, top + y), ctypes.byref(n))
        lines.append(buf[: n.value].rstrip())
    k32.CloseHandle(wintypes.HANDLE(h))
    return lines


def send(text: str) -> None:
    h = handle("CONIN$")
    for ch in text:
        vk = {"\t": 9}.get(ch, ord(ch.upper()))
        for down in (True, False):
            r = INPUT_RECORD(1, _EV(KeyEvent=KEY(down, 1, vk, 0, ch, 0)))
            n = wintypes.DWORD()
            assert k32.WriteConsoleInputW(h, ctypes.byref(r), 1, ctypes.byref(n))
        time.sleep(0.3)
    k32.CloseHandle(wintypes.HANDLE(h))


def resize(cols: int, rows: int = 28) -> None:
    """The window resized as a user's drag does: by its width in pixels, 8 px per cell."""
    hwnd = k32.GetConsoleWindow()
    for _ in range(8):
        now_c, now_r = size()
        if (now_c, now_r) == (cols, rows):
            break
        cr, wr = wintypes.RECT(), wintypes.RECT()
        u32.GetClientRect(hwnd, ctypes.byref(cr))
        u32.GetWindowRect(hwnd, ctypes.byref(wr))
        w = wr.right - wr.left + (cols - now_c) * round(cr.right / now_c)
        h = wr.bottom - wr.top + (rows - now_r) * round(cr.bottom / now_r)
        assert u32.SetWindowPos(hwnd, None, 0, 0, w, h, 0x16), ctypes.get_last_error()
        time.sleep(1.5)
    time.sleep(2.0)
    assert size()[0] == cols, size()  # the height may differ by a row or two


def png(path: Path, width: int, height: int, bgra: bytearray) -> None:
    raw = bytearray()
    for y in range(height):
        row = bgra[y * width * 4 : (y + 1) * width * 4]
        rgb = bytearray(width * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = row[2::4], row[1::4], row[0::4]
        raw += b"\0" + rgb

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    head = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head)
                     + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def capture(hwnd: int, path: Path, log) -> None:
    """This one window; the header row after `chantier live  ` (the served path) painted over."""
    lines = screen()
    assert lines[0].startswith("chantier live  "), lines[0][:20]
    for i, line in enumerate(lines[1:], 1):
        assert not any(m and m in line.lower() for m in HOME_MARKS), f"row {i} names the user"
    wr, cr, origin = wintypes.RECT(), wintypes.RECT(), wintypes.POINT(0, 0)
    u32.GetWindowRect(hwnd, ctypes.byref(wr))
    u32.GetClientRect(hwnd, ctypes.byref(cr))
    u32.ClientToScreen(hwnd, ctypes.byref(origin))
    w, h = wr.right - wr.left, wr.bottom - wr.top
    screen_dc = u32.GetDC(None)
    dc = g32.CreateCompatibleDC(screen_dc)
    bmp = g32.CreateCompatibleBitmap(screen_dc, w, h)
    old = g32.SelectObject(dc, bmp)
    assert u32.PrintWindow(hwnd, dc, 2), "PrintWindow failed"
    g32.SelectObject(dc, old)
    header = struct.pack("<IiiHHIIiiII", 40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    bits = ctypes.create_string_buffer(w * h * 4)
    assert g32.GetDIBits(dc, bmp, 0, h, bits, ctypes.create_string_buffer(header, 1064), 0) == h
    g32.DeleteObject(bmp)
    g32.DeleteDC(dc)
    u32.ReleaseDC(None, screen_dc)
    pixels = bytearray(bits.raw)
    font = FONT()
    font.cbSize = ctypes.sizeof(FONT)
    out = handle("CONOUT$")
    k32.GetCurrentConsoleFontEx(out, False, ctypes.byref(font))
    k32.CloseHandle(wintypes.HANDLE(out))
    cols, rows = size()
    cell_w, cell_h = cr.right / cols, cr.bottom / rows
    dx, dy = origin.x - wr.left, origin.y - wr.top
    x0, x1 = dx + int(15 * cell_w) - 2, dx + cr.right
    y0, y1 = dy, dy + int(cell_h + 0.999) + 1
    for y in range(y0, min(y1, h)):
        pixels[(y * w + x0) * 4 : (y * w + min(x1, w)) * 4] = bytes((96, 96, 96, 255)) * (min(x1, w) - x0)
    png(path, w, h, pixels)
    log(f"captured {path.name}: window {w}x{h} px, client {cr.right}x{cr.bottom}, "
        f"{cols}x{rows} cells ({cell_w:.2f}x{cell_h:.2f} px, font {font.dwFontSize.X}x{font.dwFontSize.Y}); "
        f"painted over x {x0}..{x1}, y {y0}..{y1} (header row from column 15)")


def masked(lines: list[str]) -> list[str]:
    """The text read back, with the served path of the header rewritten to a made-up one."""
    first = lines[0]
    if first.startswith("chantier live  C:/Users/"):
        rest = first.split("changes", 1)
        tail = first[first.index("  v0.") :] if "  v0." in first else "…"
        first = "chantier live  /work/demo-shop (real path rewritten)" + (tail if len(rest) else "")
    return [first, *lines[1:]]


def main() -> None:
    out_dir, png_dir = Path(sys.argv[1]), Path(sys.argv[2])
    ctypes.WinDLL("shcore").SetProcessDpiAwareness(2)
    pidfile = SCRATCH / "live-child.pid"
    for f in (pidfile, Path(str(pidfile) + ".exit")):
        f.unlink(missing_ok=True)
    host = subprocess.Popen(["conhost.exe", sys.executable, str(Path(__file__).resolve()),
                             "--child", str(pidfile)])
    report = (out_dir / "terminal-drawn.txt").open("w", encoding="utf-8", newline="\n")

    def log(text: str) -> None:
        report.write(text + "\n")
        report.flush()

    try:
        deadline = time.monotonic() + 60
        while not pidfile.exists() or not pidfile.read_text():
            assert time.monotonic() < deadline, "the console did not start"
            time.sleep(0.2)
        pid = int(pidfile.read_text())
        log(f"started conhost PID {host.pid}, its python PID {pid}; `chantier live` at 3412cd9")
        k32.FreeConsole()
        assert k32.AttachConsole(pid), ctypes.get_last_error()
        hwnd = k32.GetConsoleWindow()
        while "working 1" not in "\n".join(screen()):
            assert time.monotonic() < deadline, screen()
            time.sleep(0.5)
        time.sleep(2)

        def show(step: str) -> None:
            lines = screen()
            log(f"\n== {step}: terminal {size()[0]}x{size()[1]}")
            log("\n".join(masked(lines)))

        show("start")
        capture(hwnd, png_dir / "live-terminal-150.png", log)
        for width in (141, 140, 122, 121):
            resize(width)
            show(f"resized to {width}")
        resize(122)
        capture(hwnd, png_dir / "live-terminal-122.png", log)
        send("t")
        time.sleep(1.5)
        show("key t at 122 (Ago)")
        resize(121)
        show("resized to 121 with Ago")
        send("t")
        resize(150)
        send("\t\t\t\t")
        time.sleep(1.5)
        show("Tab x4 at 150 (the active panel moves into the left column)")
        resize(121)
        show("resized to 121: the left column goes")
        send("m")
        resize(90)
        show("m (maximized) at 90")
        send("m")
        time.sleep(1.5)
        show("m again at 90 (normal layout)")
        resize(150)
        send("q")
        deadline = time.monotonic() + 20
        while not Path(str(pidfile) + ".exit").exists():
            assert time.monotonic() < deadline, "live did not quit on q"
            time.sleep(0.2)
        log(f"\nq: `chantier live` exit {Path(str(pidfile) + '.exit').read_text()}")
        k32.FreeConsole()
        host.wait(20)
        log(f"conhost PID {host.pid} ended")
    except BaseException as e:
        log(f"FAILED: {e!r}")
        raise
    finally:
        if host.poll() is None:  # only the process tree this script started
            subprocess.run(["taskkill", "/PID", str(host.pid), "/T", "/F"], check=False,
                           stdin=subprocess.DEVNULL, capture_output=True)
            log(f"stopped my own process tree, PID {host.pid}")
        report.close()


if __name__ == "__main__":
    child() if sys.argv[1] == "--child" else main()
