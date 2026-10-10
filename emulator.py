import sys
import argparse
import configparser

def load_config(config_path):
    """Считывает параметры из INI-файла (Пункт 2, 3)"""
    config = configparser.ConfigParser()
    vfs_path = None
    start_script = None
    
    try:
        if config.read(config_path, encoding='utf-8'):
            if 'Emulator' in config:
                vfs_path = config['Emulator'].get('vfs_path')
                start_script = config['Emulator'].get('start_script')
    except Exception as e:
        print(f"Предупреждение: ошибка чтения INI-файла: {e}")
        
    return vfs_path, start_script

def execute_script(script_path, params, vfs_name):
    """Выполняет стартовый скрипт с имитацией ввода-вывода (Пункт 5)"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            print(f"\n--- Выполнение стартового скрипта: {script_path} ---")
            for line in f:
                line = line.strip()
                # Поддержка комментариев (пропускаем их)
                if not line or line.startswith('#'):
                    continue
                # Отображаем эмуляцию ввода пользователя
                print(f"{vfs_name} $> {line}")
                
                # Обработка команд внутри скрипта
                tokens = line.split()
                cmd = tokens[0]
                args = tokens[1:]
                
                if cmd == "exit":
                    print("Завершение работы эмулятора через скрипт.")
                    sys.exit(0)
                elif cmd == "ls":
                    print(f"[Заглушка] Вызвана команда: ls. Аргументы: {args}")
                elif cmd == "cd":
                    print(f"[Заглушка] Вызвана команда: cd. Аргументы: {args}")
                elif cmd == "conf-dump":
                    dump_config(params)
                else:
                    print(f"Ошибка: неизвестная команда '{cmd}'.")
            print("--- Скрипт успешно выполнен ---\n")
    except FileNotFoundError:
        print(f"Предупреждение: стартовый скрипт '{script_path}' не найден.")

def dump_config(params):
    """Служебная команда conf-dump (Пункт 6)"""
    print("\n--- ТЕКУЩАЯ КОНФИГУРАЦИЯ ЭМУЛЯТОРА (conf-dump) ---")
    for key, value in params.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------")

def main():
    # Настраиваем парсер аргументов командной строки (Пункт 1, 3)
    parser = argparse.ArgumentParser(description="UNIX Shell Emulator")
    parser.add_index = False # Отключаем автопомощь, чтобы CLI был похож на UNIX
    parser.add_argument('--vfs', type=str, help='Path to VFS CSV file')
    parser.add_argument('--script', type=str, help='Path to startup script')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to INI config file')
    
    # Парсим то, что прилетело из консоли при запуске
    args, _ = parser.parse_known_args()
    
    # Сначала берем значения из командной строки
    cli_vfs = args.vfs
    cli_script = args.script
    config_path = args.config
    
    # Читаем INI-файл
    ini_vfs, ini_script = load_config(config_path)
    
    # Логика приоритетов: INI-файл имеет ПРИОРИТЕТ над командной строкой (Пункт 4)
    final_vfs = ini_vfs if ini_vfs is not None else cli_vfs
    final_script = ini_script if ini_script is not None else cli_script
    
    params = {
        "VFS Physical Path": final_vfs,
        "Startup Script Path": final_script,
        "Config File Path": config_path
    }
    
    vfs_name = "my_vfs"
    
    # Отладочный вывод всех параметров при запуске эмулятора (Цель этапа)
    print("--- Запуск эмулятора: Инициализация параметров ---")
    for key, value in params.items():
        print(f"⚙️ {key} => {value}")
    print("--------------------------------------------------\n")
    
    # Если задан стартовый скрипт — выполняем его (Пункт 5)
    if final_script:
        execute_script(final_script, params, vfs_name)
    
    # Переходим в стандартный интерактивный режим REPL
    while True:
        try:
            prompt = f"{vfs_name} $> "
            user_input = input(prompt).strip()
            if not user_input:
                continue
                
            tokens = user_input.split()
            command = tokens[0]
            cmd_args = tokens[1:]
            
            if command == "exit":
                print("Завершение работы эмулятора.")
                sys.exit(0)
            elif command == "ls":
                print(f"[Заглушка] Вызвана команда: ls. Аргументы: {cmd_args}")
            elif command == "cd":
                print(f"[Заглушка] Вызвана команда: cd. Аргументы: {cmd_args}")
            # ПУНКТ 6: Вызов служебной команды дампа конфигурации
            elif command == "conf-dump":
                dump_config(params)
            else:
                print(f"Ошибка: неизвестная команда '{command}'.")
                
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы эмулятора.")
            sys.exit(0)

if __name__ == "__main__":
    main()
