import maya.cmds as cmds


#https://docs.google.com/spreadsheets/d/1zNmHCuumKLYpFHkW06hhpEibx4VkQHNohyxzpdGhObA/edit#gid=0
nh = {
"nh00":"NOCTIS",
"nh01":"GLADIOLUS",
"nh02":"PROMPTO",
"nh03":"IGNIS",
"nh04":"LUNAFREYA",
"nh05":"ARDEN",
"nh06":"UMBRA",
"nh07":"PRYNA",
"nh08":"RAVUS",
"nh09":"GENTIANA",
"nh10":"ARANEA",
"nh11":"CID",
"nh12":"IRIS",
"nh13":"COR",
"nh14":"IEDOLAS",
"nh16":"NOCTIS_YOUNGER",
"nh17":"LUNAFREYA_YOUNGER",
"nh18":"VERSTAEL",
"nh19":"CINDY",
"nh22":"DINO",
"nh23":"WESKHAM",
"nh24":"CAMELIA",
"nh25":"LOQI",
"nh26":"CALIGO",
"nh27":"JARED",
"nh28":"TALCOTT",
"nh29":"TALCOTT_OLDER",
"nh34":"REGIS"
}


um = {
"um02_001":"DAVE",
"um04_001":"VYV",
"um04_201":"DUSTIN",
"um13_110":"WEDGE",
"um13_410":"BIGGS"
}


uw = {
"uw02_001":"SANIA",
"uw04_200":"COCTURA",
"uw04_201":"MONICA",
"uw04_405":"HOLLY"
}


uy = {
"uy01_001":"EZMA",
"uy02_002":"KIMYA"
}


me = {
"me00_000":"Garula",
"me00_010":"Dualhorn",
"me00_018":"Infected_Dualhorn",
"me00_019":"Albino Dualhorn",
"me00_020":"Aspidochelon",
"me01_000":"Coeurl",
"me01_000":"Albino Coeurl",
"me01_010":"Sabertusk_Toutetsu",
"me01_010":"Albino Sabertusk",
"me01_011":"Toukotsu",
"me01_012":"Kyuki",
"me01_012":"Kyuki_Ep_Gladio",
"me01_013":"Konton",
"me01_020":"Mushufushu",
"me01_500":"Garm",
"me02_000":"Mesmenir",
"me02_001":"Bicorn",
"me02_001":"Albino Bicorn",
"me02_010":"Anak Stag",
"me02_010":"Albino Anak",
"me02_011":"Bushfire",
"me03_000":"Sahagin",
"me03_001":"Seadevil",
"me03_010":"Gigantoad",
"me03_500":"Alligator",
"me04_000":"Catoblepas",
"me04_010":"Kujata",
"me05_010":"Cockatrice",
"me05_020":"Basilisk",
"me05_030":"Chickatrice",
"me06_000":"Killer_Bee",
"me06_010":"Snatcher",
"me07_000":"Behemoth",
"me07_000":"Albino_Behemoth",
"me07_010":"Griffon",
"me07_020":"Bulette",
"me07_020":"Bulette_Ep_Gladio",
"me07_030":"Cerberus",
"me07_100":"King Behemoth",
"me07_110":"Quetzalcoatl",
"me07_900":"Deadeye",
"me08_000":"Malboro",
"me09_000":"Bandersnatch",
"me09_000":"Bandersnatch_Ep_Gladio",
"me09_100":"Jabberwock",
"me10_000":"Midgardsormr",
"me10_009":"Albino Midgardsormr",
"me10_010":"Hundlegs",
"me10_100":"Jormungand",
"me11_000":"Karlabos",
"me11_010":"Rockceasar",
"me11_020":"Powerceasar",
"me11_030":"Scorpion",
"me12_000":"Treant",
"me12_001":"Mandrake",
"me13_000":"Petite Dragon_Wyvern",
"me13_000":"Petite Dragon_Wyvern_Ep_Gladio",
"me14_000":"Daggerquil_Swordtail",
"me14_011":"Unused_eagle",
"me14_001":"Raijintyo",
"me15_000":"Cactuar_Sabotender"
}


mf = {
"mf00_000":"Goblin",
"mf00_001":"Hobgoblin",
"mf00_010":"Garchimacera_Garkimasra",
"mf00_011":"Imp",
"mf00_020":"Skeleton",
"mf00_020":"Skeleton_Ep_Gladio",
"mf00_500":"Dark_Goblin",
"mf00_502":"Corpse",
"mf01_000":"Naga",
"mf01_001":"Nagarani_Nagarasa",
"mf02_000":"Suronin",
"mf02_001":"Yojimbo",
"mf02_010":"Reaper",
"mf02_010":"Reaper_Ep_Gladio",
"mf03_000":"Arachne",
"mf03_001":"Tarantula",
"mf03_501":"Black_Widow",
"mf04_000":"Iron_Giant",
"mf04_001":"Wolfmeister",
"mf04_500":"Majin",
"mf05_000":"Chardarnook",
"mf06_000":"Daemonwall",
"mf07_000":"Deathclaw",
"mf08_000":"Unknown",
"mf09_000":"Lich",
"mf09_001":"Necromancer",
"mf09_010":"Mindflayer",
"mf09_502":"Wraith",
"mf10_500":"Shadow",
"mf11_000":"Tonberry",
"mf11_001":"Master Tonberry",
"mf12_000":"Ahriman",
"mf12_001":"Ahriman_2",
"mf13_000":"Bomb",
"mf13_001":"Bomb_2",
"mf13_001":"Ice_Bomb",
"mf13_002":"Ice_Bomb_2",
"mf13_002":"Thunder_Bomb",
"mf13_002":"Thunder_Bomb_Ep_Gladio",
"mf13_003":"Thumber_Bomb_2",
"mf14_000":"Flan",
"mf14_001":"Black_Flan",
"mf14_010":"Hecteyes",
"mf16_000":"Melusine",
"mf100":"Gargoyle"
}


es = {
"es00_000":"Magitek_Soldier_no_Weapon",
"es00_000":"Flag",
"es00_010":"Longsword",
"es00_010":"Flag_2",
"es00_020":"Soldier",
"es00_020":"Dualwielding_Soldier",
"es00_020":"Flag_3",
"es00_500":"Soldier_2",
"es00_500":"Longsword_2",
"es00_500":"Dualwielding_Soldier_2",
"es00_600":"Bomber",
"es00_600":"Explosive",
"es00_600":"Suicider",
"es00_700":"Soldier_3",
"es00_710":"Soldier_4",
"es02_000":"Rifle",
"es02_010":"Rifle_10_Years_Later",
"es02_020":"Rifle_Shield",
"es02_030":"Sniper_Rifle",
"es02_040":"Rifle_2",
"es02_050":"Rifle_Shield_2",
"es02_060":"Sniper_Rifle_2",
"es02_100":"Rocket",
"es02_100":"Rocket_10_Years_Later",
"es03_000":"Spear"
}


we = {
"we01_001":"Blood_Sword",
"we01_100":"Broad_Sword",
"we01_200":"Engine_Blade",
"we02_400":"Two_Handed_Sword",
"we03_100":"Javelin",
"we03_200":"Drain_Lance",
"we04_100":"Assassin_Daggers",
"we05_200":"Valiant",
"we05_400":"Rebellion",
"we20_000":"Sword_of_the_Wise",
"we21_000":"Axe_of_the_Conqueror",
"we22_000":"Bow_of_the_Clever",
"we23_000":"Swords_of_the_Wanderer",
"we24_000":"Blade_of_the_Mystic",
"we25_000":"Star_of_the_Rogue",
"we26_000":"Sword_of_the_Tall",
"we27_000":"Shield_of_the_Just",
"we28_000":"Mace_of_the_Fierce",
"we29_000":"Scepter_of_the_Pious",
"we30_000":"Trident_of_the_Oracle",
"we31_000":"Katana_of_the_Warrior",
"we32_000":"Sword_of_the_Father",
"we40_000":"Kotetsu",
"we40_010":"Kotetsu_sheathed",
"we40_020":"Kikuichimonji",
"we41_000":"Stoss_Spear"
}


pf = {
"pf-model_000":"plate",
"pf-model_001":"bowl",
"pf-model_340":"carrots_lettuce_brusselSprouts_potatoes",
"pf-model_621":"Taelpar_Harvest_Galette",
"pf-model_633":"Plump_n_Pungent_Tofu"
}


pr = {
"pr-model_004":"Veggie_Medley_Stew"
}




doze_names = {"nh":nh, "um":um, "uw":uw, "uy":uy, "me":me, "mf":mf, "es":es, "we":we, "pf":pf, "pr":pr}




def create_topLevel_group_name(ID, file_name):
	id_simple = ID[:2]
	groupName = "NONE"
	if id_simple in doze_names:
		if ID in nh:
			groupName = doze_names[id_simple][ID]
		elif file_name in doze_names[id_simple]:
			groupName = doze_names[id_simple][file_name]
		else:
			groupName = file_name
	else:
		groupName = file_name
	return groupName
	
	
	
	
	groupName = model_baseID + "__GROUP"
	if cmds.objExists(groupName):
		pass
	else:
		cmds.group(em=True, name=groupName)