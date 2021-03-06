from typing import List

from libqtile import bar, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen

mod = "mod4"

keys = [
    # MonadTall key bindings
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "equal", lazy.layout.normalize()),

    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod, "shift"], "f", lazy.window.bring_to_front()),
    Key([mod], "grave", lazy.window.toggle_fullscreen()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [Group(i) for i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]

for group in groups:
    # Each group is identified by the first letter of its name
    group_key = group.name[0]
    keys.extend(
        [
            Key([mod], group_key, lazy.group[group.name].toscreen(toggle=False)),  # Switch to group
            Key([mod, "shift"], group_key, lazy.window.togroup(group.name)),  # Move to group
        ]
    )

layouts = [
    layout.MonadTall(ratio=0.6),
    layout.Max(),
    layout.Floating(),
]

widget_defaults = dict(font="sans", fontsize=12, padding=3)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                widget.Battery(
                    full_char="🔌",
                    charge_char="🔌",
                    discharge_char="🔋",
                    show_short_text=False,
                    # Currently hour is broken, ideally this would be what i'd use.
                    # Until that's fixed, i'll just use percentage.
                    # format="{char} {percent:2.0%} ({hour:d}:{min:02d})"
                    format="{char} {percent:2.0%}"
                ),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                # TODO add weather
            ],
            24,
        )
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                widget.Battery(
                    full_char="🔌",
                    charge_char="🔌",
                    discharge_char="🔋",
                    show_short_text=False,
                    # Currently hour is broken, ideally this would be what i'd use.
                    # Until that's fixed, i'll just use percentage.
                    # format="{char} {percent:2.0%} ({hour:d}:{min:02d})"
                    format="{char} {percent:2.0%}"
                ),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                # TODO add weather
            ],
            24,
        )
    )
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules: List = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        {"wmclass": "confirm"},
        {"wmclass": "dialog"},
        {"wmclass": "download"},
        {"wmclass": "error"},
        {"wmclass": "file_progress"},
        {"wmclass": "notification"},
        {"wmclass": "splash"},
        {"wmclass": "toolbar"},
        {"wmclass": "ssh-askpass"},
        {"wname": "pinentry"},
        {"wname": "floatme"},
        {"wname": "pulsemixer (floatme)"},
        {"wname": "alsamixer (floatme)"},
        {"wname": "bmenu (floatme)"},
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "LG3D"  # Setting this makes java apps happier (see docs)
