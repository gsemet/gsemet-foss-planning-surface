"""Does rich drop a hex colour under NO_COLOR with the test's Console, and with no_color=False?"""

import io
import os

from rich.console import Console
from rich.text import Text

os.environ["NO_COLOR"] = "1"
for extra in ({}, {"no_color": False}):
    out = io.StringIO()
    Console(
        file=out, force_terminal=True, color_system="truecolor", legacy_windows=False, **extra
    ).print(Text("ready", style="#2f9e6b"))
    print(extra, "colour code present:", "38;2;47;158;107" in out.getvalue())
