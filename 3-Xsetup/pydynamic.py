import i3ipc
import json

AVAILABLE = [1 ,2, 3, 4, 5, 6, 7, 8, 9, 0]
DATABASE = "/home/elcerdo/.config/i3/dynamic.json"
# Create on next empty workspace

database = None
with open(DATABASE, 'r') as f:
    database = json.load(f)

class MissingEntriesException(Exception):
    pass

i3 = i3ipc.Connection()

def match_container(container, match_dict):
    ignore = ["ws_tag"]
    for identifier, value in match_dict.items():
        if identifier in ignore:
            continue
        
        try:
            container_value = getattr(container, identifier)
        except AttributeError:
            return False
        else:
            if container_value != value:
                return False
    # print("DEBUG: container matched: "+str(match_dict))
    return True

def on_window_new(i3, event):
    required = "ws_tag"
    for entry in database:
        if required not in entry.keys():
            continue
        if not match_container(event.container, entry):
            continue

            
        workspaces = i3.get_workspaces()
        ws_numbers = [x["num"] for x in workspaces]
        # Determine next free ws.
        try:
            next_free = [x for x in AVAILABLE if x not in ws_numbers][0]
        except IndexError:
            next_free = -1
        old_name = str(next_free)
        # Add to ws that already contains the correct ws_tag instead.
        for ws in workspaces:
            if entry["ws_tag"] in ws["name"]:
                next_free = ws["num"]
                old_name = ws["name"]
        
        new_name = "%s: %s" % (str(next_free), entry["ws_tag"])
        if next_free == -1:
            return

        i3.command('[con_id=%s] move --no-auto-back-and-forth workspace number %s' % (event.container.id, next_free))

        if old_name != new_name:
            i3.command('rename workspace %s to %s' % (old_name, new_name))
        break
    return
            
i3.on('window::new', on_window_new)

i3.main()
