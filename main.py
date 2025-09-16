# local modules
import sorcery_config as config

# PIP modules
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

IMAGE_URL_PREFIX = "https://d27a44hjr9gen3.cloudfront.net/"
ATLAS_DECK_SCALE = 1.0
SPELL_DECK_SCALE = 1.4

TTS_SAVED_OBJ_IMG_SIZE = 256

PATH_TO_ATLAS_JSON = "res/cardNames_Atlas.json"
PATH_TO_AVATARS_JSON = "res/cardNames_Avatars.json"
PATH_TO_SPELLS_JSON = "res/cardNames_Spells.json"

# Generate TTS syntax
def generateGuid():
    return str(os.urandom(3).hex())

def buildDeckObj(cardsInDeck, isAtlas):
    deckObj = {
        "SaveName": "",
        "Date": "",
        "VersionNumber": "",
        "GameMode": "",
        "GameType": "",
        "GameComplexity": "",
        "Tags": [],
        "Gravity": 0.5,
        "PlayArea": 0.5,
        "Table": "",
        "Sky": "",
        "Note": "",
        "TabStates": {},
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
        "ObjectStates": [
            {
                "GUID": "",
                "Name": "Deck",
                "Transform": {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "rotY": 180.0,
                    "rotZ": 0.0,
                    "scaleX": 1.4,
                    "scaleY": 1.0,
                    "scaleZ": 1.4
                },
                "Nickname": "",
                "Description": "",
                "GMNotes": "",
                "AltLookAngle": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "ColorDiffuse": {
                    "r": 0.713235259,
                    "g": 0.713235259,
                    "b": 0.713235259
                },
                "LayoutGroupSortIndex": 0,
                "Value": 0,
                "Locked": False,
                "Grid": True,
                "Snap": True,
                "IgnoreFoW": False,
                "MeasureMovement": False,
                "DragSelectable": True,
                "Autoraise": True,
                "Sticky": True,
                "Tooltip": True,
                "GridProjection": False,
                "HideWhenFaceDown": True,
                "Hands": False,
                "SidewaysCard": False,
                "DeckIDs": [], #all cardIds x 100
                "CustomDeck": {}, # getCustomDeckBlock
                "LuaScript": "",
                "LuaScriptState": "",
                "XmlUI": "",
                "ContainedObjects": [] #getCardCustomBlock
            }
        ]
    }

    cardBackUrl = (config.ATLAS_CARD_BACK_URL if isAtlas else config.SPELL_CARD_BACK_URL)
    deckScale = (ATLAS_DECK_SCALE if isAtlas else SPELL_DECK_SCALE)

    # fill in GUID
    deckObj["ObjectStates"][0]["GUID"] = generateGuid()

    # fill in DeckIDs
    deckIds = []
    for idx, cardInDeck in enumerate(cardsInDeck):
        deckId = (100 * (idx + 1))
        quantity = cardInDeck["quantity"]
        for quantityIdx in range(quantity):
            deckIds.append(deckId)
    deckObj["ObjectStates"][0]["DeckIDs"] = deckIds

    # fill in CustomDeck
    customDeck = {}
    for idx, cardInDeck in enumerate(cardsInDeck):
        cardId = idx + 1
        cardFrontUrl = cardInDeck["imgUrl"]
        customDeck[str(cardId)] = getCustomDeckBlock(cardId, cardFrontUrl, cardBackUrl)
    deckObj["ObjectStates"][0]["CustomDeck"] = customDeck

    # fill in ContainedObjects
    containedObjs = []
    for idx, cardInDeck in enumerate(cardsInDeck):
        cardId = idx + 1
        cardFrontUrl = cardInDeck["imgUrl"]
        quantity = cardInDeck["quantity"]
        for quantityIdx in range(quantity):
            containedObjs.append(getCardCustomBlock(generateGuid(), cardId, cardFrontUrl, cardBackUrl, deckScale))
    deckObj["ObjectStates"][0]["ContainedObjects"] = containedObjs

    # If only one card, replace deck object with card object
    if len(deckIds) <= 1:
        deckObj["ObjectStates"][0] = containedObjs[0]

    return deckObj

def getCustomDeckBlock(cardId, faceUrl, backUrl):
    return {
        "FaceURL": faceUrl,
        "BackURL": backUrl,
        "NumWidth": 1,
        "NumHeight": 1,
        "BackIsHidden": True,
        "UniqueBack": False,
        "Type": 0
    }

def getCardCustomBlock(guid, cardId, faceUrl, backUrl, deckScale):
    return {
        "GUID": guid,
        "Name": "CardCustom",
        "Transform": {
            "posX": 0.0,
            "posY": 0.0,
            "posZ": 0.0,
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 0.0,
            "scaleX": deckScale,
            "scaleY": 1.0,
            "scaleZ": deckScale
        },
        "Nickname": "",
        "Description": "",
        "GMNotes": "",
        "AltLookAngle": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "ColorDiffuse": {
            "r": 0.713235259,
            "g": 0.713235259,
            "b": 0.713235259
        },
        "LayoutGroupSortIndex": 0,
        "Value": 0,
        "Locked": False,
        "Grid": True,
        "Snap": True,
        "IgnoreFoW": False,
        "MeasureMovement": False,
        "DragSelectable": True,
        "Autoraise": True,
        "Sticky": True,
        "Tooltip": True,
        "GridProjection": False,
        "HideWhenFaceDown": True,
        "Hands": True,
        "CardID": cardId*100,
        "SidewaysCard": False,
        "CustomDeck": {
        str(cardId): {
            "FaceURL": faceUrl,
            "BackURL": backUrl,
            "NumWidth": 1,
            "NumHeight": 1,
            "BackIsHidden": True,
            "UniqueBack": False,
            "Type": 0
        }
        },
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": ""
    }

# File IO operations
def getOutputPath():
    outputPath = ""
    if config.SAVE_TO_TTS_PATH:
        ttsSavedObjsPath = ""
        if len(config.CUSTOM_TTS_PATH) > 0:
            if config.CUSTOM_TTS_PATH.endsWith("Saved Objects"):
                ttsSavedObjsPath = config.CUSTOM_TTS_PATH
            else:
                raise("Invalid Tabletop Simulator Path. (Normally located in C:/Users/x/Documents/My Games/Tabletop Simulator/Saves/Saved Objects)")
        else:
            ttsSavedObjsPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/Saved Objects")
        
        if len(config.TTS_SUBPATH) > 0:
            outputPath = ttsSavedObjsPath + config.TTS_SUBPATH
            if os.path.exists(ttsSavedObjsPath) and not os.path.exists(outputPath):
                os.makedirs(outputPath)
        else:
            outputPath = ttsSavedObjsPath
       
    else:
        outputPath = config.CUSTOM_OUTPUT_PATH
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

    return outputPath

def createTtsImage(caption, jsonFileName):
    # create blank image
    img = Image.new("RGB", (TTS_SAVED_OBJ_IMG_SIZE, TTS_SAVED_OBJ_IMG_SIZE), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # draw centered caption
    font = ImageFont.truetype("arial.ttf", 16)
    draw.text(((TTS_SAVED_OBJ_IMG_SIZE/2), (TTS_SAVED_OBJ_IMG_SIZE/2)), caption, fill=(255,255,255), font=font, anchor="mm")

    # save image
    pngFileName = os.path.splitext(jsonFileName)[0] + ".png"
    if os.path.exists(pngFileName):
        raise Exception("PNG file already exists")
    else:
        img.save(pngFileName, "PNG")

def readDeckList(filePath):
    # read user deck list
    deckListTxt = ""
    with open(filePath, 'r') as file:
        deckListTxt = file.read()
    deckName = os.path.splitext(os.path.basename(filePath))[0]

    # read config files
    atlasCards = []
    avatarCards = []
    spellCards = []
    with open(PATH_TO_ATLAS_JSON, 'r') as file:
        atlasTxt = file.read()
        atlasCards = json.loads(atlasTxt)

    with open(PATH_TO_AVATARS_JSON, 'r') as file:
        avatarTxt = file.read()
        avatarCards = json.loads(avatarTxt)

    with open(PATH_TO_SPELLS_JSON, 'r') as file:
        spellTxt = file.read()
        spellCards = json.loads(spellTxt)

    # declare deck object to return
    deckObj = {
        "deckName": deckName,
        "atlasCards": [],
        "spellCards": [],
        "avatarCards": []
    }

    # for each line in deckListTxt, add cards to deckObj
    lineRegex = re.compile("(\d+)\s+(.+)")
    for line in deckListTxt.splitlines():
        if len(line.strip()) > 0:
            try:
                parsedLine = lineRegex.findall(line)
                if len(parsedLine) != 1:
                    raise Exception("regex invalid: incorrect number of matches")
                quantity = int(parsedLine[0][0])
                cardName = parsedLine[0][1]

                if cardName in avatarCards:
                    deckObj["avatarCards"].append(
                        {
                            "imgUrl": IMAGE_URL_PREFIX + avatarCards[cardName][0],
                            "quantity": quantity
                        }
                    )
                elif cardName in atlasCards:
                    deckObj["atlasCards"].append(
                        {
                            "imgUrl": IMAGE_URL_PREFIX + atlasCards[cardName][0],
                            "quantity": quantity
                        }
                    )
                elif cardName in spellCards:
                     deckObj["spellCards"].append(
                        {
                            "imgUrl": IMAGE_URL_PREFIX + spellCards[cardName][0],
                            "quantity": quantity
                        }
                    )
                else:
                    raise Exception(f"Invalid card name: {cardName}")
                
            except Exception as e:
                print(f"Could not parse line: {line}")
                print(repr(e))
                raise e
    return deckObj
    
def saveDeckToFile(deckName, atlasDeckObj, spellDeckObj, avatarDeckObj):
    # write contents to file
    outputPath = getOutputPath()
    atlasFileName = f"{outputPath}/ATLAS_{deckName}.json"
    spellFileName = f"{outputPath}/SPELL_{deckName}.json"
    avatarFileName = f"{outputPath}/AVATAR_{deckName}.json"
    if os.path.exists(atlasFileName) or os.path.exists(spellFileName) or os.path.exists(avatarFileName):
        raise Exception("JSON file already exists")
    else:
        with open(atlasFileName, "w") as f:
            f.write(json.dumps(atlasDeckObj, indent=2))

        with open(spellFileName, "w") as f:
            f.write(json.dumps(spellDeckObj, indent=2))

        with open(avatarFileName, "w") as f:
            f.write(json.dumps(avatarDeckObj, indent=2))

        # create images
        atlasImgCaption =f"{deckName} (ATLAS)"
        spellsImgCaption =f"{deckName} (SPELLS)"
        avatarImgCaption =f"{deckName} (AVATAR)"
        createTtsImage(atlasImgCaption, atlasFileName)
        createTtsImage(spellsImgCaption, spellFileName)
        createTtsImage(avatarImgCaption, avatarFileName)


deckList = readDeckList(config.PATH_TO_DECK_LIST)
atlasObj = buildDeckObj(deckList["atlasCards"], isAtlas=True)
spellObj = buildDeckObj(deckList["spellCards"], isAtlas=False)
avatarObj = buildDeckObj(deckList["avatarCards"], isAtlas=False)

saveDeckToFile(deckList["deckName"], atlasObj, spellObj, avatarObj)





