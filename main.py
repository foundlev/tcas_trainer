import sys
# Графический интерфейс.
import tkinter
from tkinter.ttk import Label
from typing import Any
from PIL import Image, ImageTk, ImageFont, ImageDraw
# Для воспроизведения аудио.
import winsound
# Для создания отдельных потоков.
import threading
# Для копирования объектов.
import copy
import time

# Подключаем конфиг.
import config
# Различные расчеты.
import calculations
import myresourcepath
import myobjects


#########################

# ЯП: Python 3.10.1
# Дата начала разработки: 07.04.2022
# Дата окончания разработки: xxx

#########################


class SalimStepaApp:
    def __init__(self) -> None:
        # Создаем экземпляр для работы с GUI.
        self.root = tkinter.Tk()
        self.info_frame = None
        self.info_frame_page = 1
        # Определяем разрешение экрана (default: 1920x1080).
        self.display = {
            "width": self.root.winfo_screenwidth(),
            "height": self.root.winfo_screenheight()
        }
        self.settings = {}
        # Изображения.
        self.imgs = {
            "tagNeedle": {
                "red": Image.open(self.resource_path("imgs\\tags\\needle_red.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
                "yellow": Image.open(self.resource_path("imgs\\tags\\needle_yellow.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
                "blue": Image.open(self.resource_path("imgs\\tags\\needle_blue.png")).convert("RGBA").resize(self.correct_scale((14, 14)))
            },
            "tags": {
                "red": Image.open(self.resource_path("imgs\\tags\\tag_red.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
                "yellow": Image.open(self.resource_path("imgs\\tags\\tag_yellow.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
                "blue": Image.open(self.resource_path("imgs\\tags\\tag_blue.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
                "bluefull": Image.open(self.resource_path("imgs\\tags\\tag_bluefull.png")).convert("RGBA").resize(self.correct_scale((14, 14))),
            },
            "markers": {
                "vertical": {
                    "ta": Image.open(self.resource_path("imgs\\markers\\vertical_ta.png")).convert("RGBA").resize(self.correct_scale((75, 42))),
                    "tara": Image.open(self.resource_path("imgs\\markers\\vertical_tara.png")).convert("RGBA").resize(self.correct_scale((75, 42)))
                },
                "horizontal": {
                    "ta": {
                        40: Image.open(self.resource_path("imgs\\markers\\horizontal_ra_40.png")).convert("RGBA").resize(self.correct_scale((75, 42))),
                        45: Image.open(self.resource_path("imgs\\markers\\horizontal_ra_45.png")).convert("RGBA").resize(self.correct_scale((75, 42))),
                        48: Image.open(self.resource_path("imgs\\markers\\horizontal_ra_48.png")).convert("RGBA").resize(self.correct_scale((75, 42)))
                    },
                    "tara": {
                        25: Image.open(self.resource_path("imgs\\markers\\horizontal_tara_25.png")).convert("RGBA").resize(self.correct_scale((75, 42))),
                        30: Image.open(self.resource_path("imgs\\markers\\horizontal_tara_30.png")).convert("RGBA").resize(self.correct_scale((75, 42))),
                        35: Image.open(self.resource_path("imgs\\markers\\horizontal_tara_35.png")).convert("RGBA").resize(self.correct_scale((75, 42)))
                    }
                }
            },
            "fl": {
                50: Image.open(self.resource_path("imgs\\fl_050.png")).convert("RGBA").resize(self.correct_scale((70, 30))),
                100: Image.open(self.resource_path("imgs\\fl_100.png")).convert("RGBA").resize(self.correct_scale((70, 30))),
                200: Image.open(self.resource_path("imgs\\fl_200.png")).convert("RGBA").resize(self.correct_scale((70, 30)))
            },
            "background": Image.open(self.resource_path("imgs\\background.png")).convert("RGBA").resize(self.correct_scale((1536 - 4, 864 - 4))),
            "control": {
                "mute": Image.open(self.resource_path("imgs\\mute.png")).convert("RGBA").resize(self.correct_scale((52, 52))),
                "play": Image.open(self.resource_path("imgs\\play.png")).convert("RGBA").resize(self.correct_scale((50, 50))),
                "reload": Image.open(self.resource_path("imgs\\reload.png")).convert("RGBA").resize(self.correct_scale((50, 50)))
            },
            "boundaries": {
                "main": Image.open(self.resource_path("imgs\\boundaries.png")).convert("RGBA").resize(self.correct_scale((85, 48))),
                "intruder": Image.open(self.resource_path("imgs\\boundaries.png")).convert("RGBA").resize(self.correct_scale((84, 48)))
            },
            "collision": {
                "ok": Image.open(self.resource_path("imgs\\ok.png")).convert("RGBA").resize(self.correct_scale((50, 50))),
                "attention": Image.open(self.resource_path("imgs\\attention.png")).convert("RGBA").resize(self.correct_scale((50, 50))),
                "up": Image.open(self.resource_path("imgs\\arrow_up.png")).convert("RGBA").resize(self.correct_scale((40, 40))),
                "down": Image.open(self.resource_path("imgs\\arrow_down.png")).convert("RGBA").resize(self.correct_scale((40, 40)))
            },
            "info": {
                "close": Image.open(self.resource_path("imgs\\info_close.png")).convert("RGBA").resize(self.correct_scale((50, 50))),
                "arrows": {
                    "previous": Image.open(self.resource_path("imgs\\info_arrow_previous.png")).convert("RGBA").resize(self.correct_scale((50, 50))),
                    "next": Image.open(self.resource_path("imgs\\info_arrow_next.png")).convert("RGBA").resize(self.correct_scale((50, 50)))
                },
                "pages": [
                    Image.open(self.resource_path("imgs\\info_page1.png")).convert("RGBA").resize(self.correct_scale((1536, 864))),
                    Image.open(self.resource_path("imgs\\info_page2.png")).convert("RGBA").resize(self.correct_scale((1536, 864))),
                    Image.open(self.resource_path("imgs\\info_page3.png")).convert("RGBA").resize(self.correct_scale((1536, 864))),
                    Image.open(self.resource_path("imgs\\info_page4.png")).convert("RGBA").resize(self.correct_scale((1536, 864)))
                ]
            },
            "switcher": [
                Image.open(self.resource_path("imgs\\switcher_1.png")).convert("RGBA").resize(self.correct_scale((42, 42))),
                Image.open(self.resource_path("imgs\\switcher_2.png")).convert("RGBA").resize(self.correct_scale((80, 80))),
                Image.open(self.resource_path("imgs\\switcher_3.png")).convert("RGBA").resize(self.correct_scale((68, 68)))
            ],
            "limitations": {
                "empty": Image.open(self.resource_path("imgs\\sector_empty.png")).convert("RGBA").resize(self.correct_scale((235, 235))),
                "up": Image.open(self.resource_path("imgs\\sector_up.png")).convert("RGBA").resize(self.correct_scale((235, 235))),
                "down": Image.open(self.resource_path("imgs\\sector_down.png")).convert("RGBA").resize(self.correct_scale((235, 235)))
            },
            "aircraft": {
                "main": {
                    "horizonIndicator": {
                        10: Image.open(self.resource_path("imgs\\320\\320_climb10.png")).convert("RGBA").resize(self.correct_scale((238, 240))),
                        5: Image.open(self.resource_path("imgs\\320\\320_climb5.png")).convert("RGBA").resize(self.correct_scale((238, 240))),
                        0: Image.open(self.resource_path("imgs\\320\\320_fl.png")).convert("RGBA").resize(self.correct_scale((238, 240))),
                        -5: Image.open(self.resource_path("imgs\\320\\320_descent5.png")).convert("RGBA").resize(self.correct_scale((238, 240))),
                        -10: Image.open(self.resource_path("imgs\\320\\320_descent10.png")).convert("RGBA").resize(self.correct_scale((238, 240)))
                    },
                    "vertical": Image.open(self.resource_path("imgs\\mainplane_vertical.png")).convert("RGBA").resize(self.correct_scale((80, 80)))
                },
                "intruder": {
                    "horizonIndicator": {
                        10: Image.open(self.resource_path("imgs\\737\\737_climb10.png")).convert("RGBA").resize(self.correct_scale((253, 232))),
                        5: Image.open(self.resource_path("imgs\\737\\737_climb5.png")).convert("RGBA").resize(self.correct_scale((253, 232))),
                        0: Image.open(self.resource_path("imgs\\737\\737_fl.png")).convert("RGBA").resize(self.correct_scale((253, 232))),
                        -5: Image.open(self.resource_path("imgs\\737\\737_descent5.png")).convert("RGBA").resize(self.correct_scale((253, 232))),
                        -10: Image.open(self.resource_path("imgs\\737\\737_descent10.png")).convert("RGBA").resize(self.correct_scale((253, 232)))
                    },
                    "vertical": {
                        "current": Image.open(self.resource_path("imgs\\intruder_vertical.png")).convert("RGBA").resize(self.correct_scale((80, 80))),
                        "possible": Image.open(self.resource_path("imgs\\intruder_vertical_possible.png")).convert("RGBA").resize(self.correct_scale((80, 80)))
                    },
                    "horizontal": Image.open(self.resource_path("imgs\\intruder_horizontal.png")).convert("RGBA").resize(self.correct_scale((64, 64)))
                }
            },
            "needle": Image.open(self.resource_path("imgs\\needle.png")).convert("RGBA").resize(self.correct_scale((171, 171))),
            "point": [
                Image.open(self.resource_path("imgs\\point0.png")).convert("RGBA").resize(self.correct_scale((6, 6))),
                Image.open(self.resource_path("imgs\\point1.png")).convert("RGBA").resize(self.correct_scale((6, 6)))
            ]
        }
        # Шрифты.
        self.fonts = {
            "digital": [
                ImageFont.truetype(self.resource_path("fonts\\DigitalNumbers-Regular.ttf"), size=self.correct_scale(30))
            ],
            "default": [
                ImageFont.truetype(self.resource_path("fonts\\arial_pbg.ttf"), size=self.correct_scale(16))
            ]
        }
        # Аудио.
        self.audio = {
            "traffic": self.resource_path("sounds\\traffic.wav"),
            "clear": self.resource_path("sounds\\clear_of_conflict.wav"),
            "climb": self.resource_path("sounds\\climb.wav"),
            "increaseClimb": self.resource_path("sounds\\increase_climb.wav"),
            "descent": self.resource_path("sounds\\descent.wav"),
            "increaseDescent": self.resource_path("sounds\\increase_descent.wav")
        }
        # Самолеты.
        self.aircraft_main = myobjects.Aircraft()
        self.aircraft_intruder = myobjects.AircraftMovable()
        self.aircraft_intruder.set_xpndr(new_value='1500')
        # Указатели вертикальной скорости - вариометры.
        self.variometer_main = myobjects.Variometer()
        self.variometer_intruder = myobjects.Variometer()
        # Отображение приборов.
        self.panel_background = None

    @staticmethod
    def make_safely_movable(value):
        if isinstance(value, list) or isinstance(value, dict):
            value = copy.deepcopy(value)
        return value

    def get_attribute(self, key, default_value=None) -> Any:
        value = self.settings.get(key, default_value)
        return self.make_safely_movable(value)

    def set_attribute(self, key, value) -> None:
        if value is None and self.get_attribute(key):
            del self.settings[key]
        else:
            self.settings[key] = self.make_safely_movable(value)

    def value(self, key, value=None, default_value=None) -> Any:
        if value is None:
            return self.get_attribute(key, default_value)
        else:
            self.set_attribute(key, value)

    def correct_scale(self, value, rounding=True, multiplier=1, native_failure_multiplier=1):
        """Изменяет размер(ы) в соответствии с текущим разрешением экрана."""
        # Получаем текущую ширину и высоту экрана.
        width, height = self.display['width'], self.display['height']
        # Получаем родное разрешение, на котором создавалась программа.
        native_width, native_height = config.NATIVE_RESOLUTION

        # Вычисляем отношения к родному разрешению.
        relative_width = width / (native_width * native_failure_multiplier)
        relative_height = height / (native_height * native_failure_multiplier)

        if isinstance(value, list) or isinstance(value, tuple):
            new_value = [value[0] * relative_width * multiplier, value[1] * relative_height * multiplier]
            # Округляем если нужно.
            new_value = [int(round(new_value[0])), int(round(new_value[1]))] if rounding else new_value
            # Определяет тип возвращаемого объекта.
            return tuple(new_value) if isinstance(value, tuple) else new_value
        else:
            # Вычисляем общую относительную величину.
            relative_common = (relative_width + relative_height) / 2
            new_value = value * relative_common * multiplier
            return int(round(new_value)) if rounding else new_value

    @staticmethod
    def resource_path(relative_path):
        return myresourcepath.resource_path(relative_path)

    @staticmethod
    def exit():
        sys.exit()

    @staticmethod
    def _audio(path_wav: str):
        winsound.PlaySound(path_wav, winsound.SND_FILENAME)

    def play_audio(self, name: str, only_once=True):
        if self.value("soundMode", default_value=True):
            if not only_once or not self.value(f"soundPlayed_{name}"):
                self.value(f"soundPlayed_{name}", True)
                path_wav = self.audio[name]

                th = threading.Thread(target=self._audio, args=(path_wav,), daemon=True)
                th.start()

    def load(self):
        # Добавляем название.
        self.root.title(config.APP_TITLE)
        # Развернем программу на весь экран.
        self.root.wm_attributes('-fullscreen', True)

        ###########################################################

        # Формируем рамку для контента.
        frame_main = tkinter.Frame(self.root)
        frame_main.pack(side=tkinter.TOP, fill='x')

        # Копируем фон.
        background = copy.deepcopy(self.imgs["background"])

        # Отображаем общее изображение.
        background_photo = ImageTk.PhotoImage(background)
        self.panel_background = Label(frame_main, image=background_photo)
        self.panel_background.pack(side=tkinter.BOTTOM)

        ###########################################################

        # Реакция на ЛКМ.
        self.root.bind("<1>", self._click)
        # Реакция на вращение колесика мыши.
        self.root.bind("<MouseWheel>", self._mouse_rotating)

        # Создаем отдельный поток для обновления изображения.
        screen_updater = threading.Thread(target=self._update_screen, daemon=True)
        screen_updater.start()

        # Создаем отдельный поток для проведения полета самолета.
        flight_updater = threading.Thread(target=self._update_flight, daemon=True)
        flight_updater.start()

        # Запускаем программу.
        self.root.mainloop()

    def load_info(self):
        if self.info_frame:
            self.info_frame.destroy()
            self.info_frame_page = 1

        info_background = copy.deepcopy(self.imgs["info"]["pages"][self.info_frame_page - 1])

        # Кнопка закрытия информации.
        info_close = self.imgs["info"]["close"]
        info_background.alpha_composite(info_close, self.correct_scale((1470, 10)))

        if self.info_frame_page > 1:
            # Кнопка возврата на предыдущую страницу.
            info_arrow_previous = self.imgs["info"]["arrows"]["previous"]
            info_background.alpha_composite(info_arrow_previous, self.correct_scale((1400, 800)))

        if self.info_frame_page < len(self.imgs["info"]["pages"]):
            # Кнопка перехода на следующую страницу.
            info_arrow_next = self.imgs["info"]["arrows"]["next"]
            info_background.alpha_composite(info_arrow_next, self.correct_scale((1470, 800)))

        background_photo = ImageTk.PhotoImage(info_background)
        self.panel_background.configure(image=background_photo)
        self.panel_background.image = background_photo

    def _click(self, event):
        self._catch_event(event)

    def _mouse_rotating(self, event):
        self._catch_event(event)

    def _catch_event(self, event):
        print(f"Event: {event}")
        # Нажатие ЛКМ.
        if event.num == 1:

            # Если сейчас отображается информация.
            if self.value('showingInfo'):

                # Кнопка закрытия информации.
                if calculations.in_zone(event, (1470, 10), (1520, 60), self.correct_scale):
                    self.value('showingInfo', False)

                # Кнопка возврата на предыдущую страницу.
                elif self.info_frame_page > 1 and calculations.in_zone(event, (1400, 800), (1450, 850), self.correct_scale):
                    self.info_frame_page -= 1
                    self.load_info()

                # Кнопка перехода на следующую страницу.
                elif self.info_frame_page < len(self.imgs["info"]["pages"]) and calculations.in_zone(event, (1470, 800), (1520, 850), self.correct_scale):
                    self.info_frame_page += 1
                    self.load_info()

                return

            # Кнопка выхода из программы.
            if calculations.in_zone(event, (1470, 10), (1520, 60), self.correct_scale):
                self.exit()

            # Кнопка управления звуком.
            elif calculations.in_zone(event, (1470, 140), (1520, 190), self.correct_scale):
                self.value('soundMode', not self.value('soundMode', default_value=True))

            # Кнопка запуска полета.
            if self.aircraft_intruder.can_launch() and calculations.in_zone(event, (420, 510), (465, 560), self.correct_scale):
                self.aircraft_intruder.fly_mode = True

            # Кнопка перезапуска полета.
            elif self.aircraft_intruder.can_reload() and calculations.in_zone(event, (420, 510), (465, 560), self.correct_scale):
                self.aircraft_intruder.reload()

                # Сбрасываем проигрывание аудио.
                self.value("playChangeDirectionSound", False)
                for key in self.settings.keys():
                    if "soundPlayed_" in key:
                        self.value(key, False)

                # Сбрасываем маркеры.
                markers = ['showMarkerHorizontalTA', 'showMarkerHorizontalTARA',
                           'showMarkerVerticalUpTA', 'showMarkerVerticalDownTA',
                           'showMarkerVerticalUpTARA', 'showMarkerVerticalDownTARA']
                for key in markers:
                    self.value(key, False)

            # Кнопка показа информации.
            if calculations.in_zone(event, (1470, 70), (1520, 120), self.correct_scale):

                if not self.aircraft_intruder.fly_mode or self.aircraft_intruder.flight_finished:
                    self.info_frame_page = 1
                    self.value('needLoadInfo', True)

            else:
                # Если выполняется полет.
                if self.aircraft_intruder.fly_mode:
                    return

                coords_by_position = {
                    myobjects.Positions.up: ((520, 364), (600, 444)),
                    myobjects.Positions.middle: ((520, 414), (600, 494)),
                    myobjects.Positions.down: ((520, 464), (600, 544))
                }

                # Если самолет в режиме выбора позиции.
                if self.aircraft_intruder.selecting_mode:
                    # Выбираем позицию самолета.
                    for new_position, coords in coords_by_position.items():
                        if calculations.in_zone(event, *coords, self.correct_scale):
                            self.aircraft_intruder.set_position(new_position)
                            return

                # Нажимаем на самолет, чтобы изменить его позицию.
                if calculations.in_zone(event, *coords_by_position[self.aircraft_intruder.position], self.correct_scale):
                    # Включаем режим выбора позиции для самолета.
                    self.aircraft_intruder.selecting_mode = True

                # Вводим код ответчика.

                elif calculations.in_zone(event, (930, 650), (965, 680), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=1)

                elif calculations.in_zone(event, (930, 710), (965, 740), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=4)

                elif calculations.in_zone(event, (930, 770), (965, 800), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=7)

                elif calculations.in_zone(event, (990, 650), (1020, 680), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=2)

                elif calculations.in_zone(event, (990, 710), (1020, 740), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=5)

                elif calculations.in_zone(event, (990, 770), (1020, 800), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=0)

                elif calculations.in_zone(event, (1050, 650), (1080, 680), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=3)

                elif calculations.in_zone(event, (1050, 710), (1080, 740), self.correct_scale):
                    self.aircraft_main.update_xpndr(new_numb=6)

                elif calculations.in_zone(event, (1050, 770), (1080, 800), self.correct_scale):
                    self.aircraft_main.clear_xpndr()

                # Переключение эшелона полета.

                # Переключение по кругу.
                elif calculations.in_zone(event, (450, 20), (520, 500), self.correct_scale):
                    fls = {
                        50: myobjects.FlightLevels.level_100,
                        100: myobjects.FlightLevels.level_200,
                        200: myobjects.FlightLevels.level_50
                    }
                    self.aircraft_intruder.fl = fls[self.aircraft_intruder.fl['numb']]

                # Переключение вверх.
                elif calculations.in_zone(event, (530, 15), (580, 30), self.correct_scale):
                    fls = {
                        50: myobjects.FlightLevels.level_100,
                        100: myobjects.FlightLevels.level_200,
                        200: myobjects.FlightLevels.level_200
                    }
                    self.aircraft_intruder.fl = fls[self.aircraft_intruder.fl['numb']]

                # Переключение вниз.
                elif calculations.in_zone(event, (530, 35), (580, 50), self.correct_scale):
                    fls = {
                        50: myobjects.FlightLevels.level_50,
                        100: myobjects.FlightLevels.level_50,
                        200: myobjects.FlightLevels.level_100
                    }
                    self.aircraft_intruder.fl = fls[self.aircraft_intruder.fl['numb']]

                # Кнопки управления набором высоты Boeing.

                # Кнопка: UP FAST
                elif calculations.in_zone(event, (110, 610), (180, 650), self.correct_scale):
                    self.aircraft_intruder.direction = myobjects.Directions.up_fast

                # Кнопка: UP
                elif calculations.in_zone(event, (110, 660), (180, 700), self.correct_scale):
                    self.aircraft_intruder.direction = myobjects.Directions.up

                # Кнопка: STRAIGHT
                elif calculations.in_zone(event, (110, 710), (180, 750), self.correct_scale):
                    self.aircraft_intruder.direction = myobjects.Directions.straight

                # Кнопка: DOWN
                elif calculations.in_zone(event, (110, 755), (180, 790), self.correct_scale):
                    self.aircraft_intruder.direction = myobjects.Directions.down

                # Кнопка: DOWN FAST
                elif calculations.in_zone(event, (110, 800), (180, 840), self.correct_scale):
                    self.aircraft_intruder.direction = myobjects.Directions.down_fast

                # Переключатель Boeing ALT RPTG.
                elif calculations.in_zone(event, (250, 760), (300, 800), self.correct_scale):
                    self.value('switcherBoeing1', not self.value('switcherBoeing1'))

                # Переключатель Boeing XPNDR.
                elif calculations.in_zone(event, (660, 760), (710, 800), self.correct_scale):
                    self.value('switcherBoeing2', not self.value('switcherBoeing2'))

                # Кнопки управления набором высоты Airbus.

                # Кнопка: UP FAST
                elif calculations.in_zone(event, (1370, 610), (1440, 650), self.correct_scale):
                    self.aircraft_main.direction = myobjects.Directions.up_fast

                # Кнопка: UP
                elif calculations.in_zone(event, (1370, 660), (1440, 700), self.correct_scale):
                    self.aircraft_main.direction = myobjects.Directions.up

                # Кнопка: STRAIGHT
                elif calculations.in_zone(event, (1370, 710), (1440, 750), self.correct_scale):
                    self.aircraft_main.direction = myobjects.Directions.straight

                # Кнопка: DOWN
                elif calculations.in_zone(event, (1370, 755), (1440, 790), self.correct_scale):
                    self.aircraft_main.direction = myobjects.Directions.down

                # Кнопка: DOWN FAST
                elif calculations.in_zone(event, (1370, 800), (1440, 840), self.correct_scale):
                    self.aircraft_main.direction = myobjects.Directions.down_fast

                # Переключатель Boeing TCAS.
                elif calculations.in_zone(event, (630, 660), (700, 730), self.correct_scale):
                    now_value = self.value('switcherBoeing3', default_value='stby')
                    if now_value == 'stby':
                        self.value('switcherBoeing3', 'xpndr')
                        self.aircraft_intruder.update_tcas()
                    elif now_value == 'xpndr':
                        self.value('switcherBoeing3', 'ta')
                        self.aircraft_intruder.update_tcas(ta=True)
                    elif now_value == 'ta':
                        self.value('switcherBoeing3', 'tara')
                        self.aircraft_intruder.update_tcas(tara=True)
                    elif now_value == 'tara':
                        self.value('switcherBoeing3', 'stby')
                        self.aircraft_intruder.update_tcas()

                # Переключатель Airbus UP.
                elif calculations.in_zone(event, (850, 640), (900, 690), self.correct_scale):
                    self.value('switcherAribus1', not self.value('switcherAribus1'))

                # Переключатель Airbus MID.
                elif calculations.in_zone(event, (850, 700), (900, 750), self.correct_scale):
                    self.value('switcherAribus2', not self.value('switcherAribus2'))

                # Переключатель Airbus LOW.
                elif calculations.in_zone(event, (850, 760), (900, 810), self.correct_scale):
                    now_value = self.value('switcherAribus3', default_value='abv')
                    if now_value == 'abv':
                        self.value('switcherAribus3', 'n')
                    elif now_value == 'n':
                        self.value('switcherAribus3', 'blw')
                    elif now_value == 'blw':
                        self.value('switcherAribus3', 'abv')

                # Переключатель Airbus TCAS.
                elif calculations.in_zone(event, (1160, 740), (1240, 820), self.correct_scale):
                    now_value = self.value('switcherAirbus4', default_value='stby')
                    if now_value == 'stby':
                        self.value('switcherAirbus4', 'alt')
                        self.aircraft_main.update_tcas()
                    elif now_value == 'alt':
                        self.value('switcherAirbus4', 'xpndr')
                        self.aircraft_main.update_tcas()
                    elif now_value == 'xpndr':
                        self.value('switcherAirbus4', 'ta')
                        self.aircraft_main.update_tcas(ta=True)
                    elif now_value == 'ta':
                        self.value('switcherAirbus4', 'tara')
                        self.aircraft_main.update_tcas(tara=True)
                    elif now_value == 'tara':
                        self.value('switcherAirbus4', 'stby')
                        self.aircraft_main.update_tcas()

        # Вращение колесика мыши.
        elif event.delta:
            # Определяем направление движения.
            # rotation_direction = 1 if event.delta >= 0 else -1
            pass

    def _change_direction(self, stored_direction: myobjects.Directions, new_direction: myobjects.Directions):
        if not self.value("playChangeDirectionSound"):
            # Самолет летел вниз.
            if stored_direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                # Теперь летит вверх.
                if new_direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                    self.play_audio("climb")
                    self.value("playChangeDirectionSound", True)

                # Теперь летит также вниз.
                elif new_direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                    self.play_audio("increaseDescent")
                    self.value("playChangeDirectionSound", True)

            # Самолет летел вверх.
            elif stored_direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                # Теперь летит также вверх.
                if new_direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                    self.play_audio("increaseClimb")
                    self.value("playChangeDirectionSound", True)

                # Теперь летит вниз.
                elif new_direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                    self.play_audio("descent")
                    self.value("playChangeDirectionSound", True)

            # Самолет летел прямо.
            elif stored_direction == myobjects.Directions.straight:
                # Теперь летит вверх.
                if new_direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                    self.play_audio("climb")
                    self.value("playChangeDirectionSound", True)

                # Теперь летит вниз.
                elif new_direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                    self.play_audio("descent")
                    self.value("playChangeDirectionSound", True)

    def _update_flight(self):
        while True:
            time.sleep(0.05)

            if not self.aircraft_intruder.fly_mode or self.aircraft_intruder.flight_finished:
                continue

            # Двигаем самолет.
            self.aircraft_intruder.move(self.aircraft_main.direction, self.aircraft_main.vert_speed)
            # Проверяем их столкновение.
            self.aircraft_intruder.check_collision(correction_function=self.correct_scale)

            if self.aircraft_intruder.in_red and (self.aircraft_intruder.tara or self.aircraft_main.tara):
                self.aircraft_intruder.alt_correction = True

            # Отмечаем вход / выход (TA / TARA).
            if self.aircraft_main.ta or self.aircraft_main.tara:
                if self.aircraft_intruder.in_yellow and not self.value('showMarkerHorizontalTA'):
                    self.value('showMarkerHorizontalTA', True)

                    self.play_audio("traffic")

                if not self.aircraft_intruder.in_yellow and self.value('showMarkerHorizontalTA') and not (self.value('showMarkerVerticalUpTA') or self.value('showMarkerVerticalDownTA')):
                    if self.aircraft_intruder.altitude >= 0:
                        self.value('showMarkerVerticalUpTA', True)
                    else:
                        self.value('showMarkerVerticalDownTA', True)

            if self.aircraft_main.tara:
                if self.aircraft_intruder.in_red and not self.value('showMarkerHorizontalTARA'):
                    self.value('showMarkerHorizontalTARA', True)

                if not self.aircraft_intruder.in_red and self.value('showMarkerHorizontalTARA') and not (self.value('showMarkerVerticalUpTARA') or self.value('showMarkerVerticalDownTARA')):
                    if self.aircraft_intruder.altitude >= 0:
                        self.value('showMarkerVerticalUpTARA', True)
                    else:
                        self.value('showMarkerVerticalDownTARA', True)

            # Если включен режим исправления траектории.
            if self.aircraft_intruder.alt_correction:
                altitude = self.aircraft_intruder.altitude
                required_altitude = self.correct_scale(100)

                if abs(altitude) < required_altitude:
                    # Вычисляем оставшееся расстояние и относительную вертикальную скорость.
                    distance_left = self.aircraft_intruder.calc_distance_left()
                    speed = self.aircraft_intruder.speed

                    time_left = distance_left / speed
                    if time_left:
                        required_vert_speed = (required_altitude - abs(altitude)) / time_left

                        stored_direction = self.aircraft_main.direction

                        if self.aircraft_intruder.tara and self.aircraft_main.tara:
                            required_vert_speed /= 2

                            self.aircraft_intruder.direction = myobjects.Directions.up_fast if altitude > 0 else myobjects.Directions.down_fast
                            self.aircraft_intruder.vert_speed = (1 if altitude > 0 else -1) * required_vert_speed

                            self.aircraft_main.direction = myobjects.Directions.down_fast if altitude > 0 else myobjects.Directions.up_fast
                            self.aircraft_main.vert_speed = (-1 if altitude > 0 else 1) * required_vert_speed

                            self._change_direction(stored_direction, self.aircraft_main.direction)

                        elif self.aircraft_intruder.tara:
                            self.aircraft_intruder.direction = myobjects.Directions.up_fast if altitude >= 0 else myobjects.Directions.down_fast
                            self.aircraft_intruder.vert_speed = (1 if altitude >= 0 else -1) * required_vert_speed

                        elif self.aircraft_main.tara:
                            self.aircraft_main.direction = myobjects.Directions.up_fast if altitude <= 0 else myobjects.Directions.down_fast
                            self.aircraft_main.vert_speed = (1 if altitude <= 0 else -1) * required_vert_speed

                            self._change_direction(stored_direction, self.aircraft_main.direction)

                    else:
                        if self.aircraft_intruder.tara:
                            self.aircraft_intruder.direction = myobjects.Directions.straight
                            self.aircraft_intruder.vert_speed = 0
                        self.aircraft_intruder.alt_correction = False

                        if self.aircraft_main.tara:
                            self.play_audio("clear")
                            self.aircraft_main.direction = myobjects.Directions.straight
                            self.aircraft_main.vert_speed = 0

                else:
                    if self.aircraft_intruder.tara:
                        self.aircraft_intruder.direction = myobjects.Directions.straight
                        self.aircraft_intruder.vert_speed = 0
                    self.aircraft_intruder.alt_correction = False

                    if self.aircraft_main.tara:
                        self.play_audio("clear")
                        self.aircraft_main.direction = myobjects.Directions.straight
                        self.aircraft_main.vert_speed = 0

    def _update_screen(self):
        while True:
            if self.value('showingInfo'):
                time.sleep(0.1)
                continue

            background = copy.deepcopy(self.imgs["background"])

            # Отображаем точки хитбоксов.
            if config.SHOW_HITBOXES:
                poing0_img = self.imgs["point"][0]
                for point_coords in self.aircraft_intruder.int_hitbox_points:
                    background.alpha_composite(poing0_img, self.correct_scale(point_coords))
                for point_coords in self.aircraft_intruder.main_hitbox_points:
                    background.alpha_composite(poing0_img, self.correct_scale(point_coords))

                poing1_img = self.imgs["point"][1]
                for point_coords in self.aircraft_intruder.yellow_points:
                    background.alpha_composite(poing1_img, self.correct_scale(point_coords))
                for point_coords in self.aircraft_intruder.red_points_1:
                    background.alpha_composite(poing1_img, self.correct_scale(point_coords))
                for point_coords in self.aircraft_intruder.red_points_2:
                    background.alpha_composite(poing1_img, self.correct_scale(point_coords))

            # Режим звукового сопровождения.
            if not self.value('soundMode', default_value=True):
                mute_img = self.imgs['control']['mute']
                background.alpha_composite(mute_img, self.correct_scale((1468, 136)))

            # Кнопка PLAY / STOP.
            if self.aircraft_intruder.can_launch():
                play_img = self.imgs['control']['play']
                background.alpha_composite(play_img, self.correct_scale((417, 510)))

            elif self.aircraft_intruder.can_reload():
                reload_img = self.imgs['control']['reload']
                background.alpha_composite(reload_img, self.correct_scale((417, 510)))

            # Отображение кодов ответчика.

            airbus_xpndr = ImageDraw.Draw(background)
            airbus_xpndr_text = self.aircraft_main.get_xpndr_text()
            airbus_xpndr.text(self.correct_scale((1146, 670)), airbus_xpndr_text, font=self.fonts["digital"][0])

            boeing_xpndr = ImageDraw.Draw(background)
            boeing_xpndr_text = self.aircraft_intruder.get_xpndr_text()
            boeing_xpndr.text(self.correct_scale((430, 684)), boeing_xpndr_text, font=self.fonts["digital"][0])

            # Ограничения вертикальной скорости.

            # Для Boeing.
            vert_limitation_img = self.imgs['limitations']['empty']
            if self.aircraft_intruder.alt_correction:
                if self.aircraft_intruder.tara:
                    if self.aircraft_intruder.direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                        vert_limitation_img = self.imgs['limitations']['up']

                    elif self.aircraft_intruder.direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                        vert_limitation_img = self.imgs['limitations']['down']

            background.alpha_composite(vert_limitation_img, self.correct_scale((113, 351)))

            # Для Airbus.
            vert_limitation_img = self.imgs['limitations']['empty']
            if self.aircraft_intruder.alt_correction:
                if self.aircraft_main.tara:
                    if self.aircraft_main.direction in [myobjects.Directions.up, myobjects.Directions.up_fast]:
                        vert_limitation_img = self.imgs['limitations']['up']

                    elif self.aircraft_main.direction in [myobjects.Directions.down, myobjects.Directions.down_fast]:
                        vert_limitation_img = self.imgs['limitations']['down']

            background.alpha_composite(vert_limitation_img, self.correct_scale((1193, 351)))

            # Указатели вертикальной скорости.
            needle_img = self.imgs['needle']

            # Boeing.
            self.variometer_intruder.update(self.aircraft_intruder.direction, self.aircraft_intruder.vert_speed)
            self.variometer_intruder.rotate()
            variometer_rotation = self.variometer_intruder.get_rotation()
            background.alpha_composite(needle_img.rotate(variometer_rotation), self.correct_scale((145, 388)))

            # Airbus.
            self.variometer_main.update(self.aircraft_main.direction, self.aircraft_main.vert_speed)
            self.variometer_main.rotate()
            variometer_rotation = self.variometer_main.get_rotation()
            background.alpha_composite(needle_img.rotate(variometer_rotation), self.correct_scale((1226, 388)))

            # Эшелон полета.
            fl_img = self.imgs['fl'][self.aircraft_intruder.fl['numb']]
            background.alpha_composite(fl_img, self.correct_scale((450, 17)))

            if self.value('showMarkerHorizontalTA'):
                # Отметка входа в TA.
                ta_horizontal_img = self.imgs['markers']['horizontal']['ta'][self.aircraft_intruder.fl['ta']]
                background.alpha_composite(ta_horizontal_img, self.correct_scale((591, 340)))

            if self.value('showMarkerHorizontalTARA'):
                # Отметка входа в TARA.
                tara_horizontal_img = self.imgs['markers']['horizontal']['tara'][self.aircraft_intruder.fl['tara']]
                background.alpha_composite(tara_horizontal_img, self.correct_scale((750, 340)))

            if self.value('showMarkerVerticalUpTA') or self.value('showMarkerVerticalDownTA'):
                coords = (1067, 360) if self.value('showMarkerVerticalUpTA') else (1067, 512)
                # Отметка выхода из TA.
                ta_vertical_img = self.imgs['markers']['vertical']['ta']
                background.alpha_composite(ta_vertical_img, self.correct_scale(coords))

            if self.value('showMarkerVerticalUpTARA') or self.value('showMarkerVerticalDownTARA'):
                coords = (1067, 397) if self.value('showMarkerVerticalUpTARA') else (1067, 480)
                # Отметка выхода из TARA.
                tara_vertical_img = self.imgs['markers']['vertical']['tara']
                background.alpha_composite(tara_vertical_img, self.correct_scale(coords))

            # Переключатель Boeing ALT RPTG.
            rotation_angle = 26 if self.value('switcherBoeing1') else -4
            switcher_boeing_1 = self.imgs["switcher"][0].rotate(-rotation_angle)
            background.alpha_composite(switcher_boeing_1, self.correct_scale((249, 762)))

            # Переключатель Boeing XPNDR.
            rotation_angle = 4 if self.value('switcherBoeing2') else -26
            switcher_boeing_2 = self.imgs["switcher"][0].rotate(-rotation_angle)
            background.alpha_composite(switcher_boeing_2, self.correct_scale((668, 764)))

            # Переключатель Boeing STBY-XPNDR-TCAS.
            now_value = self.value('switcherBoeing3', default_value='stby')
            if now_value == 'stby':
                rotation_angle = -62
            elif now_value == 'xpndr':
                rotation_angle = -24
            elif now_value == 'ta':
                rotation_angle = 0
            elif now_value == 'tara':
                rotation_angle = 30
            else:
                rotation_angle = -30
            switcher_boeing_3 = self.imgs["switcher"][1].rotate(-rotation_angle)
            background.alpha_composite(switcher_boeing_3, self.correct_scale((619, 656)))

            # Переключатель Airbus UP.
            rotation_angle = 23 if self.value('switcherAribus1') else -10
            switcher_airbus_1 = self.imgs["switcher"][0].rotate(-rotation_angle)
            background.alpha_composite(switcher_airbus_1, self.correct_scale((854, 646)))

            # Переключатель Airbus MID.
            rotation_angle = 18 if self.value('switcherAribus2') else -10
            switcher_airbus_2 = self.imgs["switcher"][0].rotate(-rotation_angle)
            background.alpha_composite(switcher_airbus_2, self.correct_scale((855, 704)))

            # Переключатель Airbus LOW.
            now_value = self.value('switcherAribus3', default_value='abv')
            if now_value == 'abv':
                rotation_angle = 60
            elif now_value == 'n':
                rotation_angle = 90
            elif now_value == 'blw':
                rotation_angle = 120
            else:
                rotation_angle = 60
            switcher_airbus_3 = self.imgs["switcher"][0].rotate(-rotation_angle)
            background.alpha_composite(switcher_airbus_3, self.correct_scale((854, 761)))

            # Переключатель Airbus TCAS.
            now_value = self.value('switcherAirbus4', default_value='stby')
            if now_value == 'stby':
                rotation_angle = 30
            elif now_value == 'alt':
                rotation_angle = 60
            elif now_value == 'xpndr':
                rotation_angle = 90
            elif now_value == 'ta':
                rotation_angle = 120
            elif now_value == 'tara':
                rotation_angle = 150
            else:
                rotation_angle = 30
            switcher_airbus_4 = self.imgs["switcher"][2].rotate(-rotation_angle)
            background.alpha_composite(switcher_airbus_4, self.correct_scale((1161, 748)))

            # Отрисовываем выделение кнопок управления набором высоты.
            boundaries_img_main = self.imgs['boundaries']['main']
            boundaries_img_intruder = self.imgs['boundaries']['intruder']

            boundaries_coords = {
                "main": {
                    myobjects.Directions.up_fast: (1361, 606),
                    myobjects.Directions.up: (1361, 654),
                    myobjects.Directions.straight: (1361, 703),
                    myobjects.Directions.down: (1361, 749),
                    myobjects.Directions.down_fast: (1361, 796)
                },
                "intruder": {
                    myobjects.Directions.up_fast: (103, 606),
                    myobjects.Directions.up: (103, 654),
                    myobjects.Directions.straight: (103, 703),
                    myobjects.Directions.down: (103, 749),
                    myobjects.Directions.down_fast: (103, 796)
                }
            }

            # Главный самолет.
            current_coords = boundaries_coords["main"][self.aircraft_main.direction]
            background.alpha_composite(boundaries_img_main, self.correct_scale(current_coords))

            # Самолет нарушитель.
            current_coords = boundaries_coords["intruder"][self.aircraft_intruder.direction]
            background.alpha_composite(boundaries_img_intruder, self.correct_scale(current_coords))

            # Отрисовываем оба самолета.

            # Главный самолет - вид сбоку.
            main_aircraft_vert_img = self.imgs["aircraft"]["main"]["vertical"].rotate(-self.aircraft_main.get_pitch())
            background.alpha_composite(main_aircraft_vert_img, self.correct_scale((966, 414)))

            # Указатели исправления для Главного самолета.
            if self.aircraft_intruder.alt_correction and self.aircraft_main.tara:
                if self.aircraft_main.direction in [myobjects.Directions.up_fast, myobjects.Directions.up]:
                    arrow_up = self.imgs["collision"]["up"]
                    background.alpha_composite(arrow_up, self.correct_scale((988, 408)))
                elif self.aircraft_main.direction in [myobjects.Directions.down_fast, myobjects.Directions.down]:
                    arrow_down = self.imgs["collision"]["down"]
                    background.alpha_composite(arrow_down, self.correct_scale((988, 470)))

            # Самолет нарушитель.
            coords_by_position = {
                myobjects.Positions.up: (520, 364),
                myobjects.Positions.middle: (520, 414),
                myobjects.Positions.down: (520, 464)
            }
            # Вид сбоку
            calculated_position = self.aircraft_intruder.calc_position()
            intuder_aircraft_vert_img = self.imgs["aircraft"]["intruder"]["vertical"]["current"].rotate(self.aircraft_intruder.get_pitch())
            background.alpha_composite(intuder_aircraft_vert_img, self.correct_scale(calculated_position))

            # Указатели исправления для Самолета нарушителя.
            if self.aircraft_intruder.alt_correction and self.aircraft_intruder.tara:
                if self.aircraft_intruder.direction in [myobjects.Directions.up_fast, myobjects.Directions.up]:
                    arrow_up = self.imgs["collision"]["up"]
                    background.alpha_composite(arrow_up, self.correct_scale((calculated_position[0] + 22, calculated_position[1] - 6)))
                elif self.aircraft_intruder.direction in [myobjects.Directions.down_fast, myobjects.Directions.down]:
                    arrow_down = self.imgs["collision"]["down"]
                    background.alpha_composite(arrow_down, self.correct_scale((calculated_position[0] + 22, calculated_position[1] + 54)))

            # Вид сверху.
            intuder_aircraft_horiz_img = self.imgs["aircraft"]["intruder"]["horizontal"]
            background.alpha_composite(intuder_aircraft_horiz_img, self.correct_scale((calculated_position[0] + 16, 162)))

            # Отрисовывем возможные позиции самолета, если включен режим selectingMode.
            if self.aircraft_intruder.selecting_mode:
                for position, coords in coords_by_position.items():
                    if self.aircraft_intruder.position != position:
                        intuder_aircraft_vert_possible_img = self.imgs["aircraft"]["intruder"]["vertical"]["possible"].rotate(self.aircraft_intruder.get_pitch())
                        background.alpha_composite(intuder_aircraft_vert_possible_img, self.correct_scale(coords))

            # Отображение на радаре.  TODO:

            # Радар самолета нарушителя.
            vert_speed_intruder = self.aircraft_intruder.calc_vert_speed(self.aircraft_main.direction, self.aircraft_main.vert_speed)
            vert_speed_main = -vert_speed_intruder
            if vert_speed_main > 0:
                tag_rotation = 0
            elif vert_speed_main < 0:
                tag_rotation = 180
            else:
                tag_rotation = None

            if self.value('switcherAirbus4', default_value='stby') != 'stby' and (self.aircraft_intruder.ta or self.aircraft_intruder.tara):
                if self.aircraft_intruder.in_red and self.aircraft_intruder.tara:
                    tag_img = self.imgs['tags']['red']
                    tag_needle_img = self.imgs['tagNeedle']['red']
                elif self.aircraft_intruder.in_yellow:
                    tag_img = self.imgs['tags']['yellow']
                    tag_needle_img = self.imgs['tagNeedle']['yellow']
                elif self.aircraft_intruder.distance >= 430:
                    tag_img = self.imgs['tags']['blue']
                    tag_needle_img = self.imgs['tagNeedle']['blue']
                else:
                    tag_img = self.imgs['tags']['bluefull']
                    tag_needle_img = self.imgs['tagNeedle']['blue']

                tag_y = (self.aircraft_intruder.distance / 540) * (553 - 440) + 415
                background.alpha_composite(tag_img, self.correct_scale((224, tag_y)))
                if not (tag_rotation is None):
                    background.alpha_composite(tag_needle_img.rotate(tag_rotation), self.correct_scale((240, tag_y)))

                elevation = ImageDraw.Draw(background)
                elevation_int = -self.aircraft_intruder.calc_elevation()
                if elevation_int > 0:
                    elevetion_y = tag_y - 18
                    elevation_x = 222
                    elevation_text = '0' + str(abs(elevation_int))
                elif elevation_int < 0:
                    elevetion_y = tag_y + 18
                    elevation_x = 218
                    elevation_text = '-0' + str(abs(elevation_int))
                else:
                    elevetion_y = tag_y - 18
                    elevation_x = 222
                    elevation_text = '00'

                elevation.text(self.correct_scale((elevation_x, elevetion_y)), elevation_text, font=self.fonts["default"][0])

            # Радар самолета главного.
            if vert_speed_intruder > 0:
                tag_rotation = 0
            elif vert_speed_intruder < 0:
                tag_rotation = 180
            else:
                tag_rotation = None

            if self.value('switcherBoeing3', default_value='stby') != 'stby' and (self.aircraft_main.ta or self.aircraft_main.tara):
                if self.aircraft_intruder.in_red and self.aircraft_main.tara:
                    tag_img = self.imgs['tags']['red']
                    tag_needle_img = self.imgs['tagNeedle']['red']
                elif self.aircraft_intruder.in_yellow:
                    tag_img = self.imgs['tags']['yellow']
                    tag_needle_img = self.imgs['tagNeedle']['yellow']
                elif self.aircraft_intruder.distance >= 430:
                    tag_img = self.imgs['tags']['blue']
                    tag_needle_img = self.imgs['tagNeedle']['blue']
                else:
                    tag_img = self.imgs['tags']['bluefull']
                    tag_needle_img = self.imgs['tagNeedle']['blue']

                tag_y = (self.aircraft_intruder.distance / 540) * (553 - 440) + 415
                background.alpha_composite(tag_img, self.correct_scale((1304, tag_y)))
                if not (tag_rotation is None):
                    background.alpha_composite(tag_needle_img.rotate(tag_rotation), self.correct_scale((1320, tag_y)))

                elevation = ImageDraw.Draw(background)
                elevation_int = self.aircraft_intruder.calc_elevation()
                if elevation_int > 0:
                    elevetion_y = tag_y - 18
                    elevation_x = 1302
                    elevation_text = '0' + str(abs(elevation_int))
                elif elevation_int < 0:
                    elevetion_y = tag_y + 18
                    elevation_x = 1298
                    elevation_text = '-0' + str(abs(elevation_int))
                else:
                    elevetion_y = tag_y + 18
                    elevation_x = 1302
                    elevation_text = '00'

                elevation.text(self.correct_scale((elevation_x, elevetion_y)), elevation_text, font=self.fonts["default"][0])

            # Отрисовываем их горизонты.

            # Для главного самолета.
            horizon_indicator_main = self.imgs["aircraft"]["main"]["horizonIndicator"][self.aircraft_main.get_pitch()]
            background.alpha_composite(horizon_indicator_main, self.correct_scale((1193, 80)))

            # Для самолета нарушителя.
            horizon_indicator_intruder = self.imgs["aircraft"]["intruder"]["horizonIndicator"][self.aircraft_intruder.get_pitch()]
            background.alpha_composite(horizon_indicator_intruder, self.correct_scale((104, 85)))

            # Отображаем знак столкновения.
            if self.aircraft_intruder.collision_occurred:
                attention_img = self.imgs["collision"]["attention"]
                background.alpha_composite(attention_img, self.correct_scale((980, 430)))

            # Иначе, если полет завершен.
            elif self.aircraft_intruder.flight_finished:
                ok_img = self.imgs["collision"]["ok"]
                background.alpha_composite(ok_img, self.correct_scale((980, 430)))

            background_photo = ImageTk.PhotoImage(background)
            self.panel_background.configure(image=background_photo)
            self.panel_background.image = background_photo

            time.sleep(0.1)

            if self.value('needLoadInfo'):
                self.value('showingInfo', True)
                self.value('needLoadInfo', False)
                self.load_info()


if __name__ == "__main__":
    ui = SalimStepaApp()
    ui.load()
