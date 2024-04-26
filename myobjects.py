class Positions:
    up = "p_up"
    middle = "p_middle"
    down = "p_down"


class Directions:
    up_fast = "d_up_fast"
    up = "d_up"
    straight = "d_straight"
    down = "d_down"
    down_fast = "d_down_fast"


class FlightLevels:
    level_50 = {"tara": 25, "ta": 40, "numb": 50}
    level_100 = {"tara": 30, "ta": 45, "numb": 100}
    level_200 = {"tara": 35, "ta": 48, "numb": 200}


class Variometer:
    def __init__(self):
        self.rotation = 0
        self.finish_rotation = 0

    def reset(self):
        self.finish_rotation = 0
        self.rotation = 0

    def get_rotation(self) -> int:
        return int(90 + self.rotation)

    def update(self, direction: Directions, vert_speed: float | int):
        angle_by_direction = {
            Directions.up_fast: -110,
            Directions.up: -70,
            Directions.straight: 0,
            Directions.down: 70,
            Directions.down_fast: 110,
        }

        if direction and not vert_speed:
            self.finish_rotation = angle_by_direction[direction]
        else:
            max_vert_speed = 1

            if 0 <= abs(vert_speed) <= 0.2:
                angle = vert_speed / 0.2 * -70
            elif 0.2 < abs(vert_speed) <= 0.4:
                angle = (vert_speed / 0.2 * -40) + (vert_speed / abs(vert_speed) * -70)
            else:
                sign = vert_speed / abs(vert_speed)
                vert_speed = sign * max_vert_speed if abs(vert_speed) > max_vert_speed else vert_speed
                angle = sign * ((abs(vert_speed) - 0.4) / (max_vert_speed - 0.4) * -34) + (sign * -110)
            self.finish_rotation = angle

    def rotate(self):
        step = 20
        max_rotation = 144
        deviation = self.finish_rotation - self.rotation

        if abs(deviation) <= step:
            self.rotation = self.finish_rotation
        else:
            self.rotation += deviation / abs(deviation) * step

        if abs(self.rotation) > max_rotation:
            self.rotation = abs(self.rotation) / self.rotation * max_rotation


class Aircraft:
    def __init__(self):
        self.direction = Directions.straight
        self.ta = False
        self.tara = False
        self.vert_speed = 0

        self.xpndr_code = ""

    def update_tcas(self, ta=None, tara=None):
        if ta:
            self.ta = True
            self.tara = False
        elif tara:
            self.ta = False
            self.tara = True
        else:
            self.ta = False
            self.tara = False

    def get_pitch(self) -> int:
        pitch_by_direction = {
            Directions.up_fast: 10,
            Directions.up: 5,
            Directions.straight: 0,
            Directions.down: -5,
            Directions.down_fast: -10
        }
        return pitch_by_direction[self.direction]

    def update_xpndr(self, new_numb: int):
        if len(self.xpndr_code) < 4:
            self.xpndr_code += str(new_numb)

    def set_xpndr(self, new_value: str):
        self.xpndr_code = new_value

    def clear_xpndr(self):
        if self.xpndr_code:
            self.xpndr_code = self.xpndr_code[:-1]

    def reset_xpndr(self):
        self.xpndr_code = ""

    def get_xpndr_text(self) -> str:
        return (self.xpndr_code + "----")[:4]


class AircraftMovable(Aircraft):
    def __init__(self):
        super().__init__()
        self.position = Positions.middle
        # Эшелон полета.
        self.fl = FlightLevels.level_200

        # В режиме выбора позиции.
        self.selecting_mode = False
        # Включен режим полета.
        self.fly_mode = False
        # Полет завершен.
        self.flight_finished = False
        # Столкновение произошло.
        self.collision_occurred = False

        # Включен режим исправления траектории.
        self.alt_correction = False

        # Желтой зоне.
        self.in_yellow = False
        # В красной зоне.
        self.in_red = False

        self.altitude = 0
        self.distance = 0
        self.speed = 2

        self.int_hitbox_points = ()
        self.main_hitbox_points = ()
        self.yellow_points = ()
        self.red_points_1 = ()
        self.red_points_2 = ()

    def reload(self):
        self.selecting_mode = False
        self.fly_mode = False
        self.flight_finished = False
        self.collision_occurred = False
        self.alt_correction = False

        self.in_red = False
        self.in_yellow = False

        self.position = Positions.middle
        self.direction = Directions.straight
        self.altitude = 0
        self.distance = 0
        self.vert_speed = 0

        self.int_hitbox_points = ()
        self.main_hitbox_points = ()
        self.yellow_points = ()
        self.red_points_1 = ()
        self.red_points_2 = ()

    def can_launch(self) -> bool:
        return not (self.selecting_mode or self.fly_mode)

    def can_reload(self) -> bool:
        return not self.selecting_mode and self.flight_finished

    def set_position(self, new_position: Positions):
        altitude_by_position = {
            Positions.up: 50,
            Positions.middle: 0,
            Positions.down: -50
        }
        self.position = new_position
        self.altitude = altitude_by_position[new_position]
        self.selecting_mode = False

    def calc_vert_speed(self, oth_direction: Directions, oth_vert_speed: float | int) -> float:
        vert_speeds = {
            Directions.up_fast: 0.4,
            Directions.up: 0.2,
            Directions.straight: 0,
            Directions.down: -0.2,
            Directions.down_fast: -0.4,
        }

        my_vert_speed = self.vert_speed if abs(self.vert_speed) > abs(vert_speeds[self.direction]) else vert_speeds[self.direction]
        oth_vert_speed = oth_vert_speed if abs(oth_vert_speed) > abs(vert_speeds[oth_direction]) else vert_speeds[oth_direction]

        return float(my_vert_speed - oth_vert_speed)

    def move(self, oth_direction: Directions, oth_vert_speed: float | str):
        self.distance += self.speed
        self.altitude += self.calc_vert_speed(oth_direction, oth_vert_speed)

    def calc_position(self) -> tuple:
        return 520 + self.distance, 414 - self.altitude

    def calc_elevation(self) -> int:
        elevation = int(self.altitude / 80 * 8)
        if elevation > 9:
            elevation = 9
        elif elevation < -9:
            elevation = -9
        return elevation

    @staticmethod
    def _in_hitbox(point: tuple, hitbox: tuple[tuple]) -> bool:
        if not (hitbox[0][0] <= point[0] <= hitbox[1][0]):
            return False
        if not (hitbox[0][1] <= point[1] <= hitbox[1][1]):
            return False
        return True

    @staticmethod
    def _touch_hitboxes(hitbox: tuple[tuple], *oth_hitboxes: tuple[tuple[tuple]]) -> bool:
        points = AircraftMovable._make_points(hitbox)

        for oth_hitbox in oth_hitboxes:
            oth_points = AircraftMovable._make_points(oth_hitbox)

            for point in points:
                if AircraftMovable._in_hitbox(point, oth_hitbox):
                    return True

            for oth_point in oth_points:
                if AircraftMovable._in_hitbox(oth_point, hitbox):
                    return True

            for one_points, two_points in ((points, oth_points), (oth_points, points)):
                # Точка 1.
                if not (one_points[0][0] >= two_points[0][0]):
                    continue
                if not (one_points[0][1] <= two_points[0][1]):
                    continue
                # Точка 2.
                if not (one_points[1][0] <= two_points[1][0]):
                    continue
                if not (one_points[1][1] <= two_points[1][1]):
                    continue
                # Точка 3.
                if not (one_points[2][0] <= two_points[2][0]):
                    continue
                if not (one_points[2][1] >= two_points[2][1]):
                    continue
                # Точка 4.
                if not (one_points[3][0] >= two_points[3][0]):
                    continue
                if not (one_points[3][1] >= two_points[3][1]):
                    continue

                return True

        return False

    @staticmethod
    def _make_points(hitbox: tuple[tuple]) -> tuple:
        return (
            hitbox[0],
            (hitbox[1][0], hitbox[0][1]),
            hitbox[1],
            (hitbox[0][0], hitbox[1][1])
        )

    def calc_distance_left(self) -> int:
        if self.main_hitbox_points and self.int_hitbox_points:
            return int(self.main_hitbox_points[0][0] - self.int_hitbox_points[2][0])
        return 0

    def check_collision(self, correction_function):
        y_corrective = 20
        hitbox_main = (correction_function((966, 414 + y_corrective)), correction_function((1046, 494 - y_corrective)))

        int_position = self.calc_position()
        int_position = (int_position[0], int_position[1] + y_corrective)
        int_boundaries = (int_position[0] + 80, int_position[1] + 60 - y_corrective)
        hitbox_intuder = (correction_function(int_position), correction_function(int_boundaries))

        self.main_hitbox_points = self._make_points(hitbox_main)
        self.int_hitbox_points = self._make_points(hitbox_intuder)

        # Проверяем вход в желтую зону.
        hitbox_yellow = ((648, 398), (1069, 506))  # ((628, 378), (1069, 526))
        self.yellow_points = self._make_points(hitbox_yellow)

        self.in_yellow = self._touch_hitboxes(hitbox_intuder, hitbox_yellow)

        # Проверяем вход в красную зону.
        hitbox_red_1 = ((911, 430), (1046, 480))
        self.red_points_1 = self._make_points(hitbox_red_1)
        hitbox_red_2 = ((822, 446), (1046, 470))
        self.red_points_2 = self._make_points(hitbox_red_2)

        self.in_red = self._touch_hitboxes(hitbox_intuder, hitbox_red_1, hitbox_red_2)

        # Проверяем столкновение хитбоксов самолетов.
        for point in self.int_hitbox_points:
            if self._in_hitbox(point, hitbox_main):
                self.collision_occurred = True
                self.flight_finished = True
                break

        # Проверяем выход за переделы зоны.
        hitbox_display = ((405, 327), (1135, 575))
        # Если хотя бы одна точка вышла за зону.
        for point in self.int_hitbox_points:
            if not self._in_hitbox(point, hitbox_display):
                self.flight_finished = True
                break
