import threading
import time
import random


class Animal:
    weight = 100  # kg
    food = 'еда'
    voice = 'РЫЫ-РЫЫ!'
    gives_meet = 0.5  # % from weight

    def __init__(self, name):
        self._life_functions_ = {}
        self.name = name
        self.dead = False
        self.hunger = 0
        self.live = threading.Thread(target=self._living_)
        self.live.deamon = True
        self._life_functions_[self._eat_] = 3
        self._life_functions_[self._sleep_] = 1
        # print([x for x in self._life_functions_.items()])
        self.live.start()

    def _talk_(self, message):
        print('{}: {}'.format(self.name, message))

    def _eat_(self):
        self.hunger += 1
        if self.hunger > 7:
            self._talk_('Покорми меня!!!')
            self.weight *= 0.9
        else:
            self._talk_(self.voice)
            self.weight *= 1.05
        if self.hunger > 11:
            self._die_()
        time.sleep(15)

    def _sleep_(self):
        self._talk_('я - спать')
        time.sleep(30)

    def _living_(self):
        while not self.dead:
            for func, cycles in self._life_functions_.items():
                for n in range(cycles):
                    if not self.dead:
                        func()

    def _die_(self):
        self._talk_('AAAAA!')
        self.dead = True

    def feed(self, food):
        if food == self.food:
            if self.hunger > 0:
                self.hunger -= 3
                self._talk_(('Ням-ням! ', self.hunger))
        else:
            print('УУИЕЭЭ!')

    def butch(self):
        self._die_()
        self._talk_('идет под нож!')
        self._talk_('получено {0:.1f} кг мяса'.format(self.weight * self.gives_meet))


class Fowl(Animal):
    weight = 2
    food = 'пшено'
    voice = 'кудах!'
    gives_meet = 0.6
    egg_production = 9  # probability in % to laid 1 egg per day 1-50%, 2-66%, 3-75% etc

    def __init__(self, name):
        self._life_functions_[self._laid_egg_] = 1
        super().__init__(name)

    def _laid_egg_(self):
        if random.randint(0, self.egg_production) > 0:
            self._talk_('снесла яйцо!')


class Cattle(Animal):
    weight = 200
    food = 'сено'
    voice = "муу!"
    milk_production = 10  # liters per day
    need_milking = 0

    def __init__(self, name):
        self._life_functions_[self._need_milking_] = 1
        super().__init__(name)

    def milking(self):
        if self.need_milking > 0:
            self.need_milking = 0
        self._talk_("удой {} литров"
                    .format(self.milk_production * ((10 - self.hunger) / 10)))

    def _need_milking_(self):
        if self.need_milking > 1:
            self._talk_('подои меня !!')
        if self.need_milking > 3:
            self._talk_('умирает от разрыва вымени')
            self._die_()


class Cow(Cattle):
    _life_functions_ = {}


class Goat(Cattle):
    weight = 35
    voice = 'ме!'
    milk_production = 5
    _life_functions_ = {}


class Sheep(Cattle):
    weight = 70
    voice = 'бэ!'
    milk_production = 1
    _life_functions_ = {}

    def cut_wool(self):
        pass


class Chicken(Fowl):
    _life_functions_ = {}


class Duck(Fowl):
    weight = 4
    food = 'трава'
    voice = 'кря!'
    gives_meet = 0.65
    egg_production = 3
    _life_functions_ = {}


class Goose(Fowl):
    weight = 8
    food = 'трава'
    voice = 'ГА!'
    gives_meet = 0.8
    egg_production = 2
    _life_functions_ = {}


class Pig(Animal):
    weight = 150
    food = 'комбикорм'
    voice = 'хрю!'
    gives_meet = 0.7
    _life_functions_ = {}


def farm_management():
    print('Введите имя животного и команду через пробел')
    print('Список команд:')
    print('<название еды> - покормить зверя. Каждому животнрму своя еда')
    print('д - подоить животное')
    print('з - забить животное на мясо')
    print('x x(икс) - выход')

    chicken = Chicken('Наседка')
    duck = Duck('Дональд')
    goose = Goose('Мартин')
    cow = Cow('Бурёнка')
    goat = Goat('Дереза')
    sheep = Sheep('Кудряшка')
    pig = Pig('Хавронья')

    animal = {
        'Наседка': chicken,
        'Дональд': duck,
        'Мартин': goose,
        'Бурёнка': cow,
        'Дереза': goat,
        'Кудряшка': sheep,
        'Хавронья': pig,
    }

    while True:
        try:
            command = input('_').split(' ')
            if command[1] == 'з':
                animal[command[0]].butch()
            elif command[1] == 'д':
                animal[command[0]].milking()
            elif command[0] == 'x':
                break
            else:
                animal[command[0]].feed(command[1])
        except IndexError:
            print('напишите что-нибудь через пробел')
        except KeyError:
            print('wrong name')

farm_management()
