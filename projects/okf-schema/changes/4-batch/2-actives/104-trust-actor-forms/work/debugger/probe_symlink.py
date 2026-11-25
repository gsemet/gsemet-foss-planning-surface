"""Read-only host probe: why does symlink creation fail? Creates links only in a new temp folder.

Changes no host setting. Removes its temp folder at the end.
"""

import ctypes
import datetime
import os
import sys
import tempfile
import winreg
from ctypes import wintypes

KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)
ADVAPI32 = ctypes.WinDLL("advapi32", use_last_error=True)
SHELL32 = ctypes.WinDLL("shell32", use_last_error=True)


def raw_create_symlink(link: str, target: str, flags: int) -> str:
    """Call CreateSymbolicLinkW directly and report the Win32 error."""
    function = KERNEL32.CreateSymbolicLinkW
    function.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD]
    function.restype = ctypes.c_ubyte
    ctypes.set_last_error(0)
    ok = function(link, target, flags)
    error = ctypes.get_last_error()
    return "created" if ok else f"refused, GetLastError={error}"


def token_facts() -> None:
    """Print facts about this process token that can block unprivileged links."""
    token = wintypes.HANDLE()
    KERNEL32.GetCurrentProcess.restype = wintypes.HANDLE
    ADVAPI32.OpenProcessToken.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.HANDLE),
    ]
    if not ADVAPI32.OpenProcessToken(KERNEL32.GetCurrentProcess(), 0x0008, ctypes.byref(token)):
        print("OpenProcessToken failed", ctypes.get_last_error())
        return
    ADVAPI32.IsTokenRestricted.argtypes = [wintypes.HANDLE]
    print("token restricted:", bool(ADVAPI32.IsTokenRestricted(token)))
    ADVAPI32.GetTokenInformation.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    for label, info_class in (("elevation type", 18), ("is AppContainer", 29)):
        value = wintypes.DWORD()
        size = wintypes.DWORD()
        ADVAPI32.GetTokenInformation(
            token, info_class, ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(size)
        )
        print(f"token {label}:", value.value)
    buffer = ctypes.create_string_buffer(256)
    size = wintypes.DWORD()
    if ADVAPI32.GetTokenInformation(token, 25, buffer, 256, ctypes.byref(size)):
        sid = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]
        ADVAPI32.GetSidSubAuthorityCount.argtypes = [ctypes.c_void_p]
        ADVAPI32.GetSidSubAuthorityCount.restype = ctypes.POINTER(ctypes.c_ubyte)
        ADVAPI32.GetSidSubAuthority.argtypes = [ctypes.c_void_p, wintypes.DWORD]
        ADVAPI32.GetSidSubAuthority.restype = ctypes.POINTER(wintypes.DWORD)
        count = ADVAPI32.GetSidSubAuthorityCount(sid)[0]
        level = ADVAPI32.GetSidSubAuthority(sid, count - 1)[0]
        print(f"integrity level: 0x{level:04x} (0x2000 = medium)")
    length = wintypes.UINT(0)
    KERNEL32.GetCurrentPackageFullName.argtypes = [ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
    code = KERNEL32.GetCurrentPackageFullName(ctypes.byref(length), None)
    print("packaged (MSIX) process:", code != 15700, f"(code {code})")


def registry_facts() -> None:
    """Print the Developer Mode values and when their key last changed."""
    for path in (
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock",
        r"SOFTWARE\Policies\Microsoft\Windows\Appx",
    ):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
        except OSError as error:
            print(f"HKLM\\{path}: absent or unreadable ({error.winerror})")
            continue
        with key:
            _, values, modified = winreg.QueryInfoKey(key)
            when = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
            when += datetime.timedelta(microseconds=modified // 10)
            print(f"HKLM\\{path}: last written {when.astimezone().isoformat(timespec='seconds')}")
            for index in range(values):
                name, value, _kind = winreg.EnumValue(key, index)
                print(f"    {name} = {value!r}")


def link_facts() -> None:
    """Try each way to create a link inside a new temp folder."""
    with tempfile.TemporaryDirectory(prefix="cr104-symlink-probe-") as root:
        target_file = os.path.join(root, "target.txt")
        with open(target_file, "w", encoding="utf-8") as handle:
            handle.write("x")
        target_dir = os.path.join(root, "target-dir")
        os.mkdir(target_dir)
        for label, link, target, is_dir in (
            ("os.symlink file", "f-link", target_file, False),
            ("os.symlink directory", "d-link", target_dir, True),
        ):
            try:
                os.symlink(target, os.path.join(root, link), target_is_directory=is_dir)
                print(label, "-> created")
            except OSError as error:
                print(label, f"-> refused, winerror={error.winerror}")
        for flags in (0x0, 0x2):
            print(
                f"CreateSymbolicLinkW file flags=0x{flags:x} ->",
                raw_create_symlink(os.path.join(root, f"raw{flags}"), target_file, flags),
            )


def main() -> None:
    """Run every probe."""
    print("python", sys.version.split()[0], "windows build", sys.getwindowsversion().build)
    print("shell user is admin:", bool(SHELL32.IsUserAnAdmin()))
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    print("probe time:", now)
    token_facts()
    registry_facts()
    link_facts()


if __name__ == "__main__":
    main()
