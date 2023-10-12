from nbt import nbt
import sys
import json


def createBOMFile(data) -> (str, str):
    nbtfile = nbt.NBTFile(fileobj=data)
    recipy = dict()
    chestloot = dict()
    for block in nbtfile["blocks"]:
        item = nbtfile["palette"][block["state"].value]["Name"]
        try:
            for entry in block["nbt"]["Items"]:
                if entry["id"].value in chestloot:
                    chestloot[entry["id"].value] += 1
                else:
                    chestloot[entry["id"].value] = 1
        except KeyError:
            pass
        if item.value in recipy:
            recipy[item.value] += 1
        else:
            recipy[item.value] = 1

    for entity in nbtfile["entities"]:
        if entity["nbt"]["id"].value == "minecraft:armor_stand":
            try:
                for thing in entity["nbt"]["ArmorItems"]:
                    if thing["id"].value in chestloot:
                        chestloot[thing["id"].value] += thing["Count"].value
                    else:
                        chestloot[thing["id"].value] = thing["Count"].value
                for thing in entity["nbt"]["HandItems"]:
                    if thing["id"].value in chestloot:
                        chestloot[thing["id"].value] += thing["Count"].value
                    else:
                        chestloot[thing["id"].value] = thing["Count"].value
            except KeyError:
                pass
            thing = None
        elif entity["nbt"]["id"].value in ["minecraft:item_frame", "minecraft:glow_item_frame"]:
            if entity["nbt"]["Item"]["id"].value in chestloot:
                chestloot[entity["nbt"]["Item"]["id"].value] += 1
            else:
                chestloot[entity["nbt"]["Item"]["id"].value] = 1
        else:
            try:
                for thing in entity["nbt"]["Items"]:
                    if thing["id"].value in chestloot:
                        chestloot[thing["id"].value] += thing["Count"].value
                    else:
                        chestloot[thing["id"].value] = thing["Count"].value
            except KeyError:
                pass
            thing = None

    sortedDict = dict(sorted(recipy.items(), key=lambda item: item[1]))
    blockList = ""
    for name, count in sortedDict.items():
        split = name.split(":")
        blockList += f"{split[1]}: {count}\n"

    itemList = ""
    for x, y in chestloot.items():
        splitX = x.split(":")
        itemList += f"{splitX[1]}: {y},\n"

    entities = ""
    for x, y in chestloot.items():
        splitX = x.split(":")
        entities += f"{splitX[1]}: {y},\n"

    return blockList, itemList


def createBOMFileSchema(data) -> (str, str):
    nbtfile = nbt.NBTFile(fileobj=data)
    blocks = dict()
    entities = dict()
    for item in nbtfile["Palette"]:
        splitName = item.split("[")
        if splitName[0] in blocks:
            blocks[splitName[0]] += nbtfile["Palette"][item].value
        else:
            blocks[splitName[0]] = nbtfile["Palette"][item].value
    sortedDict = dict(sorted(blocks.items(), key=lambda item: item[1]))

    for entity in nbtfile["BlockEntities"]:
        for item in entity["Items"]:
            if item["id"].value in entities:
                entities[item["id"].value] += item["Count"].value
            else:
                entities[item["id"].value] = item["Count"].value

    bomStr = ""
    for x, y in sortedDict.items():
        bomStr += f"{x}:{y},\n"

    itemStr = ""
    for x, y in entities.items():
        itemStr += f"{x}:{y},\n"

    return bomStr, itemStr
