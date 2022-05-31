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
level_index = 0
for level in level_collection:
    level_dict = {
        "player": [],
        "walls": [],
        "boxes": [],
        "goals": [],
        "size": 0
    }
    if int(level.attrib["Width"]) == 7 and int(level.attrib["Height"]) == 7:
        level_dict["size"] = int(level.attrib["Width"])
        for line_index, line in enumerate(level):
            for index, char in enumerate(line.text):
                match char:
                    case '@':
                        level_dict["player"] = [index, line_index]
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
        level_index += 1
