from googletrans import Translator
from time import sleep
from tqdm import tqdm
import json
import os

dict_file = open("language_zh.json","rt",encoding='utf-8')
lang_dict = json.load(dict_file)
sleep_time = 2

def single_translator(file_path, lang_in, lang_out):
    """Translate a single file from lang_in to lang_out

    :param file_path: string, file path
    :param lang_in: string, language code
    :param lang_out: string, language code
    :return: string, translated text or file exists message
    """
    file_name = os.path.basename(file_path)[0]
    # Build output file name  生成输出文件名

    f_tail = "".join(["", lang_in, lang_dict[lang_in], "to", lang_out, lang_dict[lang_out]])
    fname_out = file_path.replace(".srt",  f_tail + ".srt").replace("data", "output")
    # Checkout if the file exists return the file
    if os.path.exists(fname_out):
        print(f"{fname_out} exists!")
        return fname_out
    translator = Translator(service_urls=['translate.google.com'])
    lines = open(file_path, 'r').readlines()
    text = ""
    result = ""
    limit_len = 4000
    line_num = len(lines)
    # Get translate by lines
    for i in tqdm(range(line_num)):
        line = lines[i]
        text += line
        if len(text) > limit_len or i == line_num - 1:
            trans = translator.translate(text, src=lang_in, dest=lang_out)
            result += trans.text
            text = ""
            sleep(sleep_time)
    # Write to file
    with open(fname_out, "w") as f:
        f.write(result)
    return result

def multiple_translator(file_path, lang_in, lang_out_list):
    """Translate a single file from lang_in to lang_out_list

    :param file_path:string, file path
    :param lang_in:string, language code
    :param lang_out_list:list, language code list
    :return:
    """
    lang_out_len = len(lang_out_list)
    for i in range(lang_out_len):
        try:
            lang = lang_out_list[i]
            # print(f"Start to {lang_in}|{lang_dict[lang_in]} to {lang}|{lang_dict[lang]}: {i+1}/{lang_out_len}")
            single_translator(file_path, lang_in, lang)
        except Exception as e:
            # print(f"Retry to {lang_in} to {lang}")
            single_translator(file_path, lang_in, lang)

# 要翻译的源文件的路径和文件名
file_path = "../data/open_ai_whisper.srt"
# Please change the language code to your own language code源文件的语言
lang_in = 'en'
# Please change the language code list to your own language code list要翻译成的语言列表
#lang_out = ['en', 'zh-tw', 'ar', 'tl',
#            'ko', 'ms', 'pt', 'ja',
#            'th', 'es', 'hi', 'id', 'vi']
lang_out = ['zh-cn']
# Start to translate
multiple_translator(file_path, lang_in, lang_out)
