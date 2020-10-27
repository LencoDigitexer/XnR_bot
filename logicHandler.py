from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class LogicHandler():
    def __init__(self):
        self.xui = "xui"

    def mainMenuKeyboard(self):
        kb = VkKeyboard(one_time=False)
        kb.add_button("На сегодня", color=VkKeyboardColor.POSITIVE)
        kb.add_button("На завтра", color=VkKeyboardColor.NEGATIVE)
        #kb.add_button("На всю неделю", color=VkKeyboardColor.POSITIVE)
        return kb.get_keyboard()
    
    def emptyKeyboard(self):
        kb = VkKeyboard()
        return kb.get_empty_keyboard()

