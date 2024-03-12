import json
from collections import defaultdict
from enum import IntEnum

from models import AdviceGroup, Advice, AdviceSection, Character
from utils import pl, get_logger
from flask import g as session_data

logger = get_logger(__name__)


class StorageItemMixin:
    @classmethod
    def is_from_quest(cls, chest):
        return chest in cls.from_quest()

    @classmethod
    def is_dropped(cls, chest):
        return chest in cls.dropped()

    @classmethod
    def is_from_gem_shop(cls, chest):
        return chest in cls.from_gem_shop()

    @classmethod
    def is_from_vendor_shop(cls, chest):
        return chest in cls.from_vendor_shop()

    @classmethod
    def is_crafted(cls, chest):
        return chest in cls.crafted()

    @property
    def type(self):
        if self.__class__.is_from_quest(self):
            return "Quest"
        if self.__class__.is_dropped(self):
            return "Dropped"
        if self.__class__.is_from_vendor_shop(self):
            return "Vendor"
        if self.__class__.is_from_gem_shop(self):
            return "GemShop"
        if self.__class__.is_crafted(self):
            return "Crafted"

        return f"Unknown {self.__class__.__name__} {self.value}"

    @property
    def pretty_name(self):
        return self.name.replace("_", " ").title()

class StorageChest(StorageItemMixin, IntEnum):
    STORAGE_CHEST_1 = 0
    STORAGE_CHEST_2 = 1
    STORAGE_CHEST_3 = 2
    STORAGE_CHEST_4 = 3
    STORAGE_CHEST_5 = 4
    STORAGE_CHEST_6 = 5
    STORAGE_CHEST_7 = 6
    STORAGE_CHEST_8 = 7
    STORAGE_CHEST_9 = 8
    STORAGE_CHEST_10 = 9
    STORAGE_CHEST_11 = 10
    STORAGE_CHEST_12 = 11
    STORAGE_CHEST_13 = 12
    STORAGE_CHEST_14 = 14
    STORAGE_CHEST_15 = 13
    STORAGE_CHEST_16 = 15
    STORAGE_CHEST_17 = 16
    STORAGE_CHEST_18 = 17
    STORAGE_CHEST_19 = 18
    STORAGE_CHEST_20 = 19
    STORAGE_CHEST_21 = 20
    STORAGE_CHEST_22 = 21
    STORAGE_CHEST_23 = 22
    STORAGE_CHEST_24 = 23
    STORAGE_CHEST_25 = 24
    STORAGE_CHEST_26 = 25
    STORAGE_CHEST_27 = 26
    STORAGE_CHEST_28 = 27
    STORAGE_CHEST_90 = 30
    STORAGE_CHEST_91 = 31
    STORAGE_CHEST_92 = 32
    STORAGE_CHEST_93 = 33
    STORAGE_CHEST_94 = 34
    STORAGE_CHEST_95 = 35
    STORAGE_CHEST_96 = 36
    STORAGE_CHEST_97 = 37
    STORAGE_CHEST_98 = 38
    STORAGE_CHEST_99 = 39
    STORAGE_CHEST_99B = 40
    STORAGE_CHEST_99C = 41
    DANK_PAYPAY_CHEST = 100
    GELATINOUS_CHEST = 101
    CHEESY_CHEST = 102
    WOODLIN_CHEST = 103
    NINJA_CHEST = 104

    @classmethod
    def dropped(cls):
        return (
            cls.STORAGE_CHEST_14, cls.STORAGE_CHEST_22, cls.STORAGE_CHEST_23,
            cls.STORAGE_CHEST_24, cls.STORAGE_CHEST_25,
            cls.DANK_PAYPAY_CHEST, cls.GELATINOUS_CHEST, cls.CHEESY_CHEST,
            cls.WOODLIN_CHEST
        )

    @classmethod
    def from_vendor_shop(cls):
        return (
            cls.STORAGE_CHEST_2, cls.STORAGE_CHEST_6, cls.STORAGE_CHEST_7,
            cls.STORAGE_CHEST_8, cls.STORAGE_CHEST_9, cls.STORAGE_CHEST_10,
            cls.STORAGE_CHEST_12, cls.STORAGE_CHEST_13, cls.STORAGE_CHEST_15,
            cls.STORAGE_CHEST_16, cls.STORAGE_CHEST_17, cls.STORAGE_CHEST_18,
            cls.STORAGE_CHEST_19, cls.STORAGE_CHEST_20, cls.STORAGE_CHEST_21,
            cls.STORAGE_CHEST_26, cls.STORAGE_CHEST_27, cls.STORAGE_CHEST_28,
        )

    @classmethod
    def from_gem_shop(cls):
        return (
            cls.STORAGE_CHEST_90, cls.STORAGE_CHEST_91, cls.STORAGE_CHEST_92,
            cls.STORAGE_CHEST_93, cls.STORAGE_CHEST_94, cls.STORAGE_CHEST_95,
            cls.STORAGE_CHEST_96, cls.STORAGE_CHEST_97, cls.STORAGE_CHEST_98,
            cls.STORAGE_CHEST_99, cls.STORAGE_CHEST_99B, cls.STORAGE_CHEST_99C,
        )

    @classmethod
    def from_quest(cls):
        return (
            cls.STORAGE_CHEST_1, cls.STORAGE_CHEST_3, cls.STORAGE_CHEST_4,
            cls.STORAGE_CHEST_5, cls.STORAGE_CHEST_11, cls.NINJA_CHEST
        )

    @classmethod
    def crafted(cls):
        return tuple()


class Bag(StorageItemMixin, IntEnum):
    INVENTORY_BAG_A = 0
    INVENTORY_BAG_B = 1
    INVENTORY_BAG_C = 2
    INVENTORY_BAG_D = 3
    INVENTORY_BAG_E = 4
    INVENTORY_BAG_F = 5
    INVENTORY_BAG_G = 6
    INVENTORY_BAG_H = 7
    INVENTORY_BAG_U = 20
    INVENTORY_BAG_V = 21
    INVENTORY_BAG_W = 22
    INVENTORY_BAG_X = 23
    INVENTORY_BAG_Y = 24
    INVENTORY_BAG_Z = 25
    SNAKESKINVENTORY_BAG = 100
    TOTALLY_NORMAL_AND_NOT_FAKE_BAG = 101
    BLUNDERBAG = 102
    SANDY_SATCHEL = 103
    BUMMO_BAG = 104
    CAPITALIST_CASE = 105
    WEALTHY_WALLET = 106
    PROSPEROUS_POUCH = 107
    SACK_OF_SUCCESS = 108
    SHIVERING_SACK = 109
    MAMOOTH_HIDE = 110
    PEEPER_POUCH = 111

    @classmethod
    def dropped(cls):
        return (
            cls.SNAKESKINVENTORY_BAG, cls.TOTALLY_NORMAL_AND_NOT_FAKE_BAG,
            cls.INVENTORY_BAG_G, cls.MAMOOTH_HIDE
        )

    @classmethod
    def from_vendor_shop(cls):
        return (
            cls.BUMMO_BAG, cls.CAPITALIST_CASE, cls.WEALTHY_WALLET,
            cls.PROSPEROUS_POUCH, cls.SACK_OF_SUCCESS
        )

    @classmethod
    def from_gem_shop(cls):
        return (
            cls.INVENTORY_BAG_U, cls.INVENTORY_BAG_V, cls.INVENTORY_BAG_W,
            cls.INVENTORY_BAG_X, cls.INVENTORY_BAG_Y, cls.INVENTORY_BAG_Z
        )

    @classmethod
    def from_quest(cls):
        return (
            cls.INVENTORY_BAG_A, cls.INVENTORY_BAG_B, cls.INVENTORY_BAG_C,
            cls.INVENTORY_BAG_D, cls.INVENTORY_BAG_E, cls.INVENTORY_BAG_F,
            cls.INVENTORY_BAG_H
        )

    @classmethod
    def crafted(cls):
        return cls.BLUNDERBAG, cls.SANDY_SATCHEL, cls.SHIVERING_SACK, cls.PEEPER_POUCH


def getCandyHourSections(inputJSON):
    bank = dict(zip(inputJSON["ChestOrder"], inputJSON["ChestQuantity"]))

    # Standard Time Candies: 1hr - 72hr
    normal_candy = (bank.get(f"Timecandy{i}", 0) for i in range(1, 7))
    normal_candy_times = 1, 2, 4, 12, 24, 72
    guaranteedCandyHours = sum(
        qty * hr
        for qty, hr in zip(normal_candy, normal_candy_times)
    )

    tier_regular = "no guaranteed candy"
    guaranteedCandyString = f"You have {tier_regular} in your bank. Wow."

    if guaranteedCandyHours > 0:
        tier_regular = str(guaranteedCandyHours)
        guaranteedCandyString = f"You have {guaranteedCandyHours} hours ({guaranteedCandyHours / 24:.2f} days) of guaranteed candy in your bank."

    if guaranteedCandyHours >= 1000:
        guaranteedCandyString += "<br>Don't forget about them!"

    # Variable Time Candies: Steamy, Spooky, Cosmic
    variable_candy = (bank.get(f"Timecandy{i}", 0) for i in range(7, 10))
    variable_candy_times = (1/6, 24), (1/3, 12), (1/12, 500)
    variableCandyHoursMin = 0
    variableCandyHoursMax = 0

    section_regular = AdviceSection(
        name="Regular Candy",
        tier=tier_regular,
        header=guaranteedCandyString,
        picture="Candy_1hr.png"
    )

    for qty, (hrs_min, hrs_max) in zip(variable_candy, variable_candy_times):
        variableCandyHoursMin += qty * hrs_min
        variableCandyHoursMax += qty * hrs_max

    tier_variable = "no variable candy"
    variableCandyString = f"You have {tier_variable} in your bank."

    if variableCandyHoursMin > 0:
        hours_range = f"{variableCandyHoursMin:.2f} - {variableCandyHoursMax:.2f}"
        days_range = f"{variableCandyHoursMin / 24:.2f} - {variableCandyHoursMax / 24:.2f}"
        tier_variable = hours_range
        variableCandyString = f"You have somewhere between {hours_range} hours ({days_range} days) of variable candy in your bank."

    # TODO: Maybe Black / Divinity Pearls?

    section_variable = AdviceSection(
        name="Variable Candy",
        tier=tier_variable,
        header=variableCandyString,
        picture="Candy_Cosmic.png"
    )

    return section_regular, section_variable


def getBagType(inputBagNumber):
    return getStorageItemType(inputBagNumber, Bag)


def getChestType(inputChestNumber):
    return getStorageItemType(inputChestNumber, StorageChest)


def getStorageItemType(storageItemIndex, cls):
    try:
        bag = cls(int(storageItemIndex))
    except ValueError as e:
        logger.exception(f"failed to parse {cls.__name__} '{storageItemIndex = }'", exc_info=e)
        return f"Unknown Bag '{storageItemIndex}'"

    return bag.type


def parseInventoryBagsCount(inputJSON, _, playerNames):
    currentMaxQuestBags = 7  # As of v2.00
    currentMaxDroppedBags = 4  # As of v2.00
    currentMaxCraftedBags = 4  # As of v2.00
    currentMaxVendorBags = 5  # As of v2.00
    currentMaxGemShopBags = 6  # As of v2.00
    currentMaxBagsSum = currentMaxQuestBags + currentMaxDroppedBags + currentMaxCraftedBags + currentMaxVendorBags + currentMaxGemShopBags
    playerBagDict = {}
    playerBagsByTypeDict = {}
    playersMissingBags = []

    for counter, name in enumerate(playerNames):
        try:
            playerBagDict[name] = json.loads(inputJSON[f'InvBagsUsed_{counter}']) #yet another string pretending to be a list of lists..
        except Exception as reason:
            logger.exception("Unable to retrieve Inventory Bags Used for %s: ", name, exc_info=reason)

    #print(playerBagDict)
    for player, bagList in playerBagDict.items():
        #print(type(player), player)
        #print(type(bagList), bagList)
        bagTypeCounts = defaultdict(int)

        for bag in bagList:
            thisBag = getBagType(bag)
            #print(bag, thisBag)
            bagTypeCounts[thisBag] += 1

        playerBagsByTypeDict[player] = bagTypeCounts
        total = sum(bagTypeCounts.values())

        if total < currentMaxBagsSum:
            playersMissingBags.append((player, total))

    #print(playerBagsByTypeDict)

    # tier = f"{len(playersMissingBags)}/{len(playerNames)}"
    # header = f"You collected bags on {tier} players. Collect more!"

    advices_MissingBags = [
        Advice(label=name, picture_class="", progression=bagsCount, goal=currentMaxBagsSum) for name, bagsCount in playersMissingBags
    ]

    # if not advice_MissingBags:
    #     tier = f"{len(playerNames)}/{len(playerNames)}"
    #     header = f"You collected bags on all {tier} players. Enjoy your vastness of space! ❤️"

    group_bags = AdviceGroup(
        tier="",
        pre_string="Collect inventory bags on the following players",
        advice=advices_MissingBags
    )

    logger.debug('%s', str(group_bags))
    return group_bags

def parseInventoryBagSlots(inputJSON, characterDict) -> AdviceGroup:
    inventorySlots_AdviceList = []
    currentMaxInventorySlots = 83  #As of v2.02
    currentMaxUsableInventorySlots = 80  #As of v2.02
    currentMaxWithoutAutoloot = 78
    defaultInventorySlots = 16  # Characters have 16 inventory slots by default
    playerBagDict = {}
    playerBagSlotsDict = {}
    playersWithMaxBagSlots = []
    playersMissingBagSlots = []

    for chararacterIndex in characterDict:
        try:
            playerBagDict[chararacterIndex] = json.loads(inputJSON['InvBagsUsed_'+str(chararacterIndex)])  #yet another string pretending to be a list of lists
        except:
            logger.exception(f"Unable to retrieve InvBagsUsed for {chararacterIndex} ({characterDict[chararacterIndex].character_name})")

    inventorySlots_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Collect more inventory space",
        advices=[],
    )
    if session_data.account.autoloot:
        autoLootSlots = 5
        inventorySlots_AdviceGroup.post_string = "+5 slots from AutoLoot included."
    else:
        autoLootSlots = 0
        inventorySlots_AdviceGroup.post_string = "AutoLoot is set to Unpurchased. This bundle gives 5 inventory slots."

    for chararacterIndex, bagList in playerBagDict.items():
        sumSlots = defaultInventorySlots + autoLootSlots
        for bag in bagList:
            try:
                sumSlots += int(bagList[bag])
            except:
                logger.exception(f"Could not increase character {chararacterIndex}'s bagslots by {type(bagList[bag])} {bagList[bag]}")
        playerBagSlotsDict[chararacterIndex] = {"Total":sumSlots}
        if sumSlots >= currentMaxUsableInventorySlots:
            playersWithMaxBagSlots.append(chararacterIndex)
        elif sumSlots == currentMaxWithoutAutoloot and session_data.account.autoloot == False:
            playersWithMaxBagSlots.append(chararacterIndex)
        else:
            playersMissingBagSlots.append(chararacterIndex)
    logger.info(f"playerBagDict: {playerBagDict}")
    logger.info(f"playersMissingBagSlots: {playersMissingBagSlots}")
    for playerIndex in playersMissingBagSlots:
        inventorySlots_AdviceList.append(Advice(
            label=session_data.account.all_characters[playerIndex].character_name,
            picture_class=session_data.account.all_characters[playerIndex].class_name_icon,
            progression=playerBagSlotsDict[playerIndex]["Total"],
            goal=currentMaxUsableInventorySlots
        ))

    inventorySlots_AdviceGroup.advices = inventorySlots_AdviceList
    return inventorySlots_AdviceGroup

def parseStorageChests(inputJSON):
    currentMaxChestsSum = 45  # As of v2.0
    usedStorageChests = json.loads(inputJSON['InvStorageUsed'])
    missing_chests = [chest for chest in StorageChest if str(chest.value) not in usedStorageChests.keys()]

    advices = [
        Advice(label=chest.pretty_name, picture_class=chest.pretty_name) for chest in missing_chests
    ]

    group = AdviceGroup(
        tier="",
        pre_string=f"Collect {len(missing_chests)} more storage chest{pl(['']*len(missing_chests))} for your bank",
        advices=advices
    )
    if len(advices) == 0:
        group.pre_string = "You've collected all current Storage Chests! You best ❤️"

    return group


def parseConsumables(inputJSON, characterDict):
    sections_candy = getCandyHourSections(inputJSON)
    group_bags = parseInventoryBagSlots(inputJSON, characterDict)
    group_chests = parseStorageChests(inputJSON)

    groups = [group_bags, group_chests]

    section_storage = AdviceSection(
        name="Storage",
        tier="",
        header="Collect more space for your bank and inventories:",
        picture="Cosmic_Storage_Chest.png",
        groups=groups
    )
    if section_storage.collapse:
        section_storage.header = "You've collected all current Storage Chests and Inventory Bags! You best ❤️"

    return *sections_candy, section_storage
