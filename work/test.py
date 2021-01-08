import time
from googletrans import Translator
import quicktranslate
#实例化


service_urls=[
      'translate.google.cn',
    ]
translator = Translator(service_urls)
print(translator.translate('星期日').text)
# res=quicktranslate.get_translate_google('星期日')
# print(res)
