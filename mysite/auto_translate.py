
from babel.messages.pofile import read_po, write_po
from translate import Translator

translator = Translator(to_lang='Chinese')
input_po = 'translations/zh_CN/LC_MESSAGES/messages.po'  # 输入的.po文件路径
output_po = 'translations/zh_CN/LC_MESSAGES/messages_translated.po'  # 输出的.po文件路径

with open(input_po, 'r', encoding='utf-8') as po_file:
    catalog = read_po(po_file)
    for message in catalog:
        if not message.string:  # 未翻译的字符串
            print("开始翻译: " + message.id)
            result = translator.translate(message.id)
            message.string = result
            print("翻译完毕: " + result)

with open(output_po, 'wb') as po_file:
    write_po(po_file, catalog, omit_header=True)