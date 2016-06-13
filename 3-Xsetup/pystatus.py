from i3pystatus import Status
from i3pystatus.updates import pacman, cower

status = Status()

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM KW31
#                          ^-- calendar week
status.register("clock",
    format="%a %-d %b %X KW%V",)

# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces
status.register("network",
    format_up="{v4cidr}",)

# Shows disk usage of /
# Format:
# 42/128G [86G]
# status.register("disk",
#     path="/",
#     format="{used}+{avail}G]",)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
status.register("pulseaudio",
    format="{volume}%",)

status.register("updates",
    format = "Updates: {count}",
    format_no_updates = "No updates",
    backends = [pacman.Pacman(), cower.Cower()])

status.run()
