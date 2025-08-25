# by AI
# adapter for keyboard libary -> pyinput
# used because keyboard library does not really support mac

from pynput import keyboard as _kb

__all__ = ["wait", "add_hotkey"]

def _to_pattern(hotkey: str) -> str:
    """Convert 'ctrl+shift+a' into a pynput GlobalHotKeys pattern."""
    specials = {
        "ctrl": "<ctrl>", "control": "<ctrl>",
        "alt": "<alt>", "option": "<alt>",
        "shift": "<shift>",
        "cmd": "<cmd>", "command": "<cmd>", "win": "<cmd>", "super": "<cmd>",
        "enter": "<enter>", "return": "<enter>",
        "esc": "<esc>", "escape": "<esc>",
        "space": "<space>", "tab": "<tab>",
        "up": "<up>", "down": "<down>", "left": "<left>", "right": "<right>",
    }
    parts = [p.strip().lower() for p in hotkey.replace("-", "+").split("+") if p.strip()]

    def tok(p: str) -> str:
        if p in specials: return specials[p]
        if p.startswith("f") and p[1:].isdigit(): return f"<{p}>"
        if len(p) == 1: return p
        return f"<{p}>"

    return "+".join(tok(p) for p in parts)


def add_hotkey(hotkey, callback, args=()):
    """
    Register a hotkey that triggers callback(*args). Returns the listener.
    Stop it later with: handle.stop()  (and optionally handle.join()).
    """
    pattern = _to_pattern(hotkey)

    def on_activate():
        try:
            callback(*args)
        except Exception:
            # Keep it simple: swallow callback errors so the listener survives.
            pass

    handle = _kb.GlobalHotKeys({pattern: on_activate})
    handle.start()  # runs its own thread internally; no threading module needed here
    return handle


def wait(hotkey):
    """
    Block until the specified hotkey is pressed once.
    """
    pattern = _to_pattern(hotkey)
    handle = None

    def on_activate():
        # stop the listener; join() below will return
        handle.stop()

    handle = _kb.GlobalHotKeys({pattern: on_activate})
    handle.start()
    handle.join()
