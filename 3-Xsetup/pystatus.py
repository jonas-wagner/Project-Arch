from i3pystatus import Status
from i3pystatus.updates import pacman, cower

status = Status()

globInterval = 5

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM KW31
#                          ^-- calendar week
status.register("clock",
    format="%a %-d %b %X KW%V",)

status.register("battery",
    interval=globInterval,
    format="{status} {percentage:02.0f}% {remaining:%E%hh:%Mm}",
    alert=True,
    alert_percentage=10,
    status={
        "DIS":  "DIS",
        "CHR":  "CHR",
        "FULL": "FULL",
    },)

status.register("backlight",
    interval=globInterval,
    format="☀{percentage}%",
    base_path="/sys/class/backlight/intel_backlight/",)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
status.register("pulseaudio",
    format="♪{volume}%",)


# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces
status.register("network",
    interface="wlp4s0",
    format_up="{v4cidr}",)

for vpn in ["scc"]:
        status.register("openvpn",
        vpn_name=vpn,
        interval=globInterval,
        status_command="bash -c 'nmcli connection show --active | grep %(vpn_name)s'",)


# Shows disk usage of /
# Format:
# 42/128G [86G]
# status.register("disk",
#     path="/",
#     format="{used}+{avail}G]",)


status.register("updates",
    format = "Pacman updates: {count}",
    format_no_updates = "",
    backends = [pacman.Pacman()])

status.register("updates",
    format = "Cower updates: {count}",
    format_no_updates = "",
    backends = [cower.Cower()])
status.run()
