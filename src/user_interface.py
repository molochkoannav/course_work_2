from src.aircraft import Aircraft
from src.aircraft_sourse import AircraftSourse
from src.aircraft_storage import AircraftStorageJSON
from src.geocoder import Geocoder
from pathlib import Path
import logging

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_user = log_dir / "user.log"

logging.getLogger("urllib3").setLevel(logging.WARNING)
log_user_interface = logging.getLogger("user")
log_user_interface.setLevel(logging.DEBUG)


file_handler_user_interface = logging.FileHandler(log_user, mode="w", encoding="utf-8")
file_handler_user_interface.setLevel(logging.DEBUG)


formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler_user_interface.setFormatter(formatter)


log_user_interface.addHandler(file_handler_user_interface)
log_user_interface.propagate = False

def user_main() -> None:
    """Функция для взаимодействия с пользователем."""
    print("\nПривет! Добро пожаловать в программу, которая собирает данные о самолетах")

    while True:
        try:
            log_user_interface.info("Запуск программы")
            print("\nВведите название страны для запроса информации о самолетах из opensky-network.org")
            country = input("Пример ввода - Ireland: ").strip().lower()

            if not country:
                log_user_interface.error("Не правильно введено название страны")
                print("Ошибка: Название страны не может быть пустым. Попробуйте снова.")
                continue

            geocoder = Geocoder(country)
            bounding_box = geocoder.get_bounding_box()

            if not bounding_box:
                log_user_interface.error("Не удалось найти координаты для страны")
                print(f"Ошибка: Не удалось найти координаты для страны '{country}'. Попробуйте снова.")
                continue
            aircraft_source = AircraftSourse(bounding_box)
            states = aircraft_source.get_aeroplanes()

            if states is None:
                log_user_interface.error("Не удалось получить данные от сервера")
                print("Ошибка: Не удалось получить данные от сервера. Проверьте подключение к интернету.")
                print("Попробуйте снова или введите другую страну.")
                continue

            if not states:
                log_user_interface.error("Ни одного самолета не найдено")
                print(f"Над страной '{geocoder.name_country}' не найдено ни одного самолета.")
                print("Попробуйте ввести другую страну.")
                continue

            aircraft_list = []
            for state in states:
                try:
                    aircraft = Aircraft.state_converting(state)
                    if aircraft:
                        aircraft_list.append(aircraft)
                except Exception as e:
                    log_user_interface.error("Не удалось обработать данные самолета")
                    print(f"Предупреждение: Не удалось обработать данные самолета: {e}")
                    continue

            if not aircraft_list:
                log_user_interface.error("Не удалось обработать данные ни одного самолета")
                print("Не удалось обработать данные ни одного самолета. Попробуйте снова.")
                continue

            print(f"Успешно получено {len(aircraft_list)} самолетов над {geocoder.name_country}")
            save_choice = input("\nСохранить данные в файл? (да/нет): ").strip().lower()
            if save_choice not in  ["да", "нет", "д", "н", "yes", "no"]:
                while True:
                    print(f"Вы ввели {save_choice}")
                    confirm_choice = input("Подтвердите сохранение файла ...: ").strip().lower()
                    if confirm_choice == "да" or confirm_choice == "нет":
                        break
                    else:
                        print(f"Вы ввели {confirm_choice}")
                        continue
            else:
                try:
                    aircraft_dict = [obj.__dict__ for obj in aircraft_list]
                    storage = AircraftStorageJSON(f"data/{geocoder.name_country}_aircraft.json")
                    storage.data = aircraft_dict
                    storage.save()
                    print(f"Данные сохранены в файл data/{geocoder.name_country}_aircraft.json")
                except Exception as e:
                    log_user_interface.error(f"Ошибка при сохранении данных: {e}")
                    print(f"Ошибка сохранения данных: {e}")

            while True:
                print("\nВыберите действие:")
                print("1 - Получить топ N самолетов по высоте полета")
                print("2 - Получить самолеты по стране их регистрации")
                print("3 - Показать статистику")
                print("4 - Показать загруженный файл")
                print("5 - Выйти из программы")

                user_input = input("Введите номер пункта: ").strip()
                if user_input == '1':
                    try:
                        n_input = int(input("Введите N: ").strip())
                        if n_input > 0:
                            top_aircraft = aircraft_list
                            print(top_aircraft)
                            sorted_aircraft = Aircraft.get_sort(top_aircraft)[:n_input]
                            print(f"\nТоп {n_input} самолётов по высоте:")
                            for i, aircraft in enumerate(sorted_aircraft, 1):
                                print(f"{i}. Бортовой номер: {aircraft.callsign or 'Нет данных'}, "
                                      f"Страна: {aircraft.country or 'Нет данных'}, "
                                      f"Скорость: {aircraft.velocity or 'Нет данных'} м/с, "
                                      f"Высота: {aircraft.height or 'Нет данных'} м")


                    except ValueError:
                        log_user_interface.error("Ошибка ввода ValueError")
                        print("Пожалуйста, введите целое число")
                        continue
                    break


                elif user_input == '2':
                    param = input("Введите страну для поиска: ").strip()
                    if not param:
                        print("Название страны не может быть пустым")
                        continue
                    result = [aircraft for aircraft in aircraft_list
                              if param.lower() in (aircraft.country or '').lower()]
                    if result:
                        print(f"\nНайдено {len(result)} самолетов из страны '{param}':")
                        for i, aircraft in enumerate(result, 1):
                            callsign = aircraft.callsign or 'Нет данных'
                            height = f"{aircraft.height:.1f}" if aircraft.height is not None else 'Нет данных'
                            velocity = f"{aircraft.velocity:.1f}" if aircraft.velocity is not None else 'Нет данных'
                            print(f"{i}. Бортовой номер: {callsign}, "
                                  f"Высота: {height} м, "
                                  f"Скорость: {velocity} м/с")
                    else:
                        print(f"Самолеты из страны '{param}' не найдены")
                    continue


                elif user_input == '3':
                    print(f"\nСтатистика по самолетам над {geocoder.name_country}:")
                    if not aircraft_list:
                        print("Нет данных для отображения статистики")
                        continue
                    print("\nСТАТИСТИКА")
                    print(f"Всего самолетов: {len(aircraft_list)}")
                    valid_velocity = [a for a in aircraft_list if a.velocity is not None]
                    if valid_velocity:
                        fastest = max(valid_velocity, key=lambda x: x.velocity)
                        slowest = min(valid_velocity, key=lambda x: x.velocity)
                        print(f"Самый быстрый самолет: {fastest.callsign or 'Нет данных'} "
                              f"со скоростью {fastest.velocity:.1f} м/с")
                        print(f"Самый медленный самолет: {slowest.callsign or 'Нет данных'} "
                              f"со скоростью {slowest.velocity:.1f} м/с")
                    else:
                        print("Нет данных о скорости самолетов")
                    valid_height = [a for a in aircraft_list if a.height is not None]
                    if valid_height:
                        highest = max(valid_height, key=lambda x: x.height)
                        lowest = min(valid_height, key=lambda x: x.height)
                        print(f"Самый высокий самолет: {highest.callsign or 'Нет данных'} "
                              f"на высоте {highest.height:.1f} м")
                        print(f"Самый низкий самолет: {lowest.callsign or 'Нет данных'} "
                              f"на высоте {lowest.height:.1f} м")
                    else:
                        print("Нет данных о высоте самолетов")

                    continue
                elif user_input == '4':
                    print(f"\nОткрываю сохраненный файл: data/{geocoder.name_country}_aircraft.json")
                    storage = AircraftStorageJSON(f"data/{geocoder.name_country}_aircraft.json")
                    if storage.data:
                        print(f"Найдено {len(storage.data)} записей в файле:")
                        for i, aircraft in enumerate(storage.data, 1):
                            print(f"{i}. {aircraft}")
                    else:
                        print("Файл пуст или не существует")
                    break
                elif user_input == '5':
                    print("До свидания!")
                    return
                else:
                    print("Неверный выбор. Попробуйте еще раз.")
                break

        except KeyboardInterrupt:
            lo
            print("\nПрограмма прервана пользователем. До свидания!")
            return
        except Exception as e:
            log_user_interface.error(f"Непредвиденная ошибка {e} ")
            print(f"Произошла непредвиденная ошибка: {e}")
            print("Попробуйте начать заново.")



