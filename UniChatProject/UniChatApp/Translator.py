from googletrans import Translator

def funmode(org_message, src_lg, dest_lg):
    translator = Translator()
    # languages for serial translation
    lg1 = "mi"
    lg2 = "kk"
    lg3 = "jw"

    # translating the message from one language into another.
    first_result = translator.translate(org_message, src=src_lg, dest=lg1)
    second_result = translator.translate(first_result.text, src=lg1, dest=lg2)
    thrdresult = translator.translate(second_result.text, src=lg2, dest=lg3)
    finalresult = translator.translate(thrdresult.text, src=lg3, dest=dest_lg)

    return finalresult.text


text = funmode("Das ist der Test", "de", "en")
