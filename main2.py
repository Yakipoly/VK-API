from time import sleep, time
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN

# Это не трогать
LIST_FACS = ['информатики и вычислительной техники', 'машиностроительный', 'медицинский', 'иностранных языков', 'историко-географический', 'фпмфиит', 'ричфиж',
    'радиоэлектроники и автоматики', 'управления и социальных технологий', 'химико-фармацевтический', 'энергетики и электротехники', 'строительный', 'экономический', 'искусств', 'юридический']
# Это не трогать
ANSWERS = ['чепуха', 'факт']

# Это можно трогать
QUESTIONS = [
        """Источник землетрясений находится в земном ядре?""",

    """Чепуха!

        Места в недрах Земли, где непосредственно происходят подвижки горных пород, называются гипоцентрами землетрясений.
        Они находятся на глубинах до нескольких сотен километров.Причем большая часть землетрясений локализована в пределах земной коры, которая не превышает по толщине нескольких десятков километров""",

    """Международная космическая станция движется в атмосфере Земли?""",
    """Факт!

        Высота полета МКС — около 400 км. Между тем, следы земной атмосферы прослеживаются до расстояний около 100 тыс. км. Слой атмосферы, лежащий в диапазоне высот от 80-90 км до 800 км, называется термосферой.
        Верхние разреженные слои атмосферы, вместе с тем, принято считать космическим пространством. Их не следует путать с так называемыми плотными слоями атмосферы, в которых из-за высокого сопротивления воздуха невозможно орбитальное движение.""",

    """Протоны и нейтроны состоят из более мелких частиц?""",

    """Факт!
        Протоны и нейтроны, из которых состоят атомные ядра, по современным представлениям, не являются фундаментальными частицами материи. Они, в свою очередь, состоят из кварков, которые наряду с электронами, нейтрино и фотонами, являются подлинно элементарными частицами. В состав каждого протона и каждого нейтрона входит по три кварка.
    """,

    """Гомеопатия не имеет убедительных научных обоснований?""",

    """Факт!
        Медики многократно проводили слепые проверки эффективности гомеопатических методов лечения. Выяснилось, что ни для одного заболевания гомеопатия не дает большего эффекта, чем плацебо (пустышка).""",

    """Питаться ГМО опасно, потому что в них содержатся гены?""",

    """Чепуха!
        Гены есть у всех животных и растений, а не только у генетически модифицированных организмов. Соответственно, молекулы ДНК, в которых содержатся гены, есть в любой пище, кроме продуктов глубокой переработки, таких как масло или сахар. Молекулы ДНК неустойчивы и легко разрушаются пищеварительными ферментами. Поэтому содержащийся в них генетический код никаким образом не может влиять на организм человека. Если бы это было иначе, мы постоянно попадали бы под влияние генов растений и животных, которыми питаемся.""",

  	"""В работе современных процессоров используются сверхпроводники?""",

    """Чепуха!

        В процессорах современных компьютеров используются не сверхпроводники, а полупроводники. Это вещества, проводимость которых сильно зависит от приложенного электрического напряжения. Такое свойство очень удобно для создания систем управления. Сверхпроводники же — это совсем другой класс веществ, которые полностью утрачивают электрическое сопротивление при низких температурах. Их используют для создания сильных электромагнитов, а также для передачи электроэнергии без тепловых потерь."""
]


class VKAPI:

    def __init__(self) -> None:
        pass
    
    def whiler(self):
        vk_session = vk.VkApi(token=TOKEN)
        self.vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                try:
                    text = event.text 
                    text = text.lower()
                except Exception as e:
                    print(e)
                user_id = event.user_id
                try:
                    payload = int(event.payload)
                except:
                    payload = None
                
                try:
                    if text == 'старт':
                        print(f"User ID: {user_id}")
                        self.handle_start(user_id)
                    elif text == 'начать':
                        print(f"User ID: {user_id}")
                        self.handle_start(user_id)
                    elif text in LIST_FACS:
                        self.handle_solution_fac(user_id, payload)
                    elif text in ANSWERS:
                        self.getQuestion(user_id, payload)
                    else:
                        self.i_dont_know(user_id)
                except Exception as e:
                    print(e)

    def msg_send(self, user_id, message, keyboard = None):
        try:
            if not keyboard:
                keyboard = VkKeyboard(one_time=True)
                self.vk_api.messages.send(
                    user_id=user_id,
                    message=message,
                    random_id=int(round(time() * 1000)),
                    keyboard=keyboard.get_empty_keyboard()
                )
            else:
                self.vk_api.messages.send(
                    user_id=user_id,
                    message=message,
                    random_id=int(round(time() * 1000)),
                    keyboard=keyboard.get_keyboard()
                )
        except Exception as e:
            print(e)


    def handle_start(self, user_id):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Информатики и вычислительной техники',
                            color=VkKeyboardColor.PRIMARY, payload=1)
        keyboard.add_line()
        keyboard.add_button('Машиностроительный',
                            color=VkKeyboardColor.PRIMARY, payload=2)
        keyboard.add_button(
            'Медицинский', color=VkKeyboardColor.PRIMARY, payload=3)
        keyboard.add_line()
        keyboard.add_button('Иностранных языков',
                            color=VkKeyboardColor.PRIMARY, payload=4)
        keyboard.add_button('Историко-географический',
                            color=VkKeyboardColor.PRIMARY, payload=5)
        keyboard.add_line()
        keyboard.add_button('ФПМФиИТ', color=VkKeyboardColor.PRIMARY, payload=6)
        keyboard.add_button('РиЧФиЖ', color=VkKeyboardColor.PRIMARY, payload=7)
        keyboard.add_line()
        keyboard.add_button('Радиоэлектроники и автоматики',
                            color=VkKeyboardColor.PRIMARY, payload=8)
        keyboard.add_line()
        keyboard.add_button('Управления и социальных технологий',
                            color=VkKeyboardColor.PRIMARY, payload=9)
        keyboard.add_line()
        keyboard.add_button('Химико-фармацевтический',
                            color=VkKeyboardColor.PRIMARY, payload=10)
        keyboard.add_button('Энергетики и электротехники',
                            color=VkKeyboardColor.PRIMARY, payload=11)
        keyboard.add_line()
        keyboard.add_button(
            'Строительный', color=VkKeyboardColor.PRIMARY, payload=12)
        keyboard.add_button(
            'Экономический', color=VkKeyboardColor.PRIMARY, payload=13)
        keyboard.add_line()
        keyboard.add_button('Искусств', color=VkKeyboardColor.PRIMARY, payload=14)
        keyboard.add_button(
            'Юридический', color=VkKeyboardColor.PRIMARY, payload=15)

        self.msg_send(user_id, 'Здравствуйте, Вас приветствует команда Студенческого Научного Общества. Мы подготовили небольшой квиз, по прохождению которого вы сможете поучаствовать в розыгрыше нашего мерча! \n\n Для начала выберите свой факультет', keyboard)



    def handle_solution_fac(self, user_id, payload):
        try:
            fac_id = payload
            print(f"User id {user_id} fac id {fac_id}")
            with open('students.txt', 'a') as fd:
                fd.write(f'\nID:{user_id};FD:{fac_id};')
        except:
            pass
        
        message = QUESTIONS[0]
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Чепуха', color=VkKeyboardColor.PRIMARY, payload=1)
        keyboard.add_button('Факт', color=VkKeyboardColor.PRIMARY, payload=1)
        self.msg_send(user_id, message, keyboard)

    def getQuestion(self, user_id, payload):
        try:
            question_now_id = int(payload)
        except:
            message = """Что-то пошло не так, попробуйте начать заново, написав слово Начать"""
            self.msg_send(user_id, message)
            return
        message = QUESTIONS[question_now_id]

        self.msg_send(user_id, message)

        question_next_id = question_now_id + 1
        try:
            message = QUESTIONS[question_next_id]
        except:
            # вышли за предел
            message = """Подписывайтесь в группу председателя @sno_ivt(факультета Информатики и вычислительной техники | Алексеева Екатерина), там вы найдете много полезных советов по научной деятельности) Инсайдики из первых уст"""
            # message = """Тест сделан председателем факультета Информатики и вычислительной техники @sno_ivt(Алексеевой Екатериной). Подписывайтесь, там вы найдете много полезных советов по научной деятельности) Инсайдики из первых уст"""
            self.msg_send(user_id, message)
            sleep(1)
            message = """Обрабатываем результаты теста..."""
            self.msg_send(user_id, message)
            
            message = """Вы прошли тест!\nПоследним этапом будет подписаться на группу @snochuvsu (Студенческое научное общество | СНО ЧувГУ). \nЖдите результатов в течение суток"""
            self.msg_send(user_id, message)
            return
        # sleep(0.5)
        question_next_id = question_next_id + 1
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Чепуха', color=VkKeyboardColor.PRIMARY, payload=question_next_id)
        keyboard.add_button('Факт', color=VkKeyboardColor.PRIMARY, payload=question_next_id)

        self.msg_send(user_id, message, keyboard)
        
    def i_dont_know(self, user_id):
        self.msg_send(user_id, 'Хм, кажется я Вас не понял...')

while True:
    v = VKAPI()
    try:
        v.whiler()
    except Exception as e:
        print(e)
        continue

    