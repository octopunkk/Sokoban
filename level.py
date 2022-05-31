import xml.etree.ElementTree as ET
import json

tree = ET.parse('microban.slc')
level_collection = tree.getroot()[-1]

'''
@ player
# wall
$ box
. goal
* box + goal
'''
for level_index, level in enumerate(level_collection):
    level_dict = {
        "player": [],
        "walls": [],
        "boxes": [],
        "goals": [],
        "width": 0,
        "height": 0
    }
    level_dict["width"] = int(level.attrib["Width"])
    level_dict["height"] = int(level.attrib["Height"])
    for line_index, line in enumerate(level):
        for index, char in enumerate(line.text):
            match char:
                case '@':
                    level_dict["player"].append([index, line_index])
                case '#':
                    level_dict["walls"].append([index, line_index])
                case '$':
                    level_dict["boxes"].append([index, line_index])
                case '.':
                    level_dict["goals"].append([index, line_index])
                case '*':
                    level_dict["boxes"].append([index, line_index])
                    level_dict["goals"].append([index, line_index])
    with open(f'levels/microban_{level_index}.json', 'w') as outfile:
        json.dump(level_dict, outfile)
