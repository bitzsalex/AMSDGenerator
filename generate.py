from trdg.generators import GeneratorFromStrings
from itertools import product
import os
import json


# reading the text file, and converting it to list
with open("./trdg/texts/main.txt", "r", encoding="utf-8") as file:
    content = file.read()
    content = content.split("\n")

images_count = len(content)

fonts_list = ["./trdg/fonts/am/PGUNICODE1.TTF", "./trdg/fonts/am/PGUNICODE2.TTF", "./trdg/fonts/am/nyala.ttf", "./trdg/fonts/am/AbyssinicaSIL-Regular.ttf", "./trdg/fonts/am/CODE2000.TTF", "./trdg/fonts/am/NotoSerifEthiopic-Regular.ttf", "./trdg/fonts/am/VGUnicode.TTF", "./trdg/fonts/am/jiretsl.ttf"]


def generate_from_font_list():
    save_dir = "./from_font_list/"

    for font in fonts_list:
        folder_name = "_".join(comb) + "/"
        generator = GeneratorFromStrings(
            count=images_count,
            strings=content,
            language="am",
            fonts=[font],
            size=26,
            fit=True,
        )
        
        folder_path = os.path.join(save_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            
        images_path = os.path.join(folder_path, "images/")
        os.makedirs(images_path, exist_ok=True)

        counter = 0
        labels = {}
        for image, label in generator:
            image_name = f"{counter:07}.jpg"
            labels[image_name] = label
            image.save(os.path.join(images_path, image_name))
            counter += 1
        
        labels_name = os.path.join(folder_path, "labels.json")
        with open(labels_name, "w", encoding="utf-8") as file:
            json.dump(labels, file, ensure_ascii=False, indent=4)


def generate_different_combinations():
    # this function generates a dataset with different background, skew angle, color, and blur level
    # if you wish to learn more about it, read: https://textrecognitiondatagenerator.readthedocs.io/en/latest/overview.html
    check_list = [['bl0', 'bl1', 'bl2'], ['ds0', 'ds3'], ['bg0', 'bg1'], ['sk0', 'sk2'], ['cl2', 'cl38']]
    combinations = list(product(*check_list))
    save_dir = "./gen_out/"

    for comb in combinations[24:35] + combinations[-3:]:
        folder_name = "_".join(comb) + "/"
        comb_dict = {
            "blur": int(comb[0][2:]),
            "distorsion_type": int(comb[1][2:]),
            "background_type": int(comb[2][2:]),
            "skewing_angle": int(comb[3][2:]),
            "text_color": "#222222" if int(comb[4][2:]) == 2 else "#333333,#888888",
        }

        generator = GeneratorFromStrings(
            count=images_count,
            strings=content,
            language="am",
            fonts=fonts_list,
            random_blur=True,
            random_skew=True,
            distorsion_orientation=2,
            size=26,
            alignment=0,
            fit=True,
            **comb_dict
        )
        
        folder_path = os.path.join(save_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            
        images_path = os.path.join(folder_path, "images/")
        os.makedirs(images_path, exist_ok=True)

        counter = 0
        labels = {}
        for image, label in generator:
            image_name = f"{counter:07}.jpg"
            labels[image_name] = label
            image.save(os.path.join(images_path, image_name))
            counter += 1
        
        labels_name = os.path.join(folder_path, "labels.json")
        with open(labels_name, "w", encoding="utf-8") as file:
            json.dump(labels, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_from_font_list()
    # generate_different_combinations()