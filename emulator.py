import sys

def main():
    # Имя нашей виртуальной файловой системы по умолчанию
    vfs_name = "my_vfs"
    
    print("--- Эмулятор командной строки UNIX (Прототип REPL) ---")
    print("Для выхода введите команду 'exit'.\n")
    
    # Запускаем бесконечный цикл REPL
    while True:
        try:
            # 1. Приглашение к вводу содержит имя VFS (Пункт 2)
            prompt = f"{vfs_name} $> "
            user_input = input(prompt).strip()
            
            # Если пользователь просто нажал Enter, идем на следующую итерацию
            if not user_input:
                continue
                
            # 2. Простой парсер: разделяет ввод по пробелам (Пункт 3)
            tokens = user_input.split()
            command = tokens[0]
            args = tokens[1:]
            
            # 3. Обработка команды exit (Пункт 6)
            if command == "exit":
                if args:
                    print("Ошибка: команда 'exit' не принимает аргументы.")
                    continue
                print("Завершение работы эмулятора.")
                sys.exit(0)
                
            # 4. Реализация команд-заглушек ls и cd (Пункт 5)
            elif command == "ls":
                print(f"[Заглушка] Вызвана команда: ls. Аргументы: {args}")
                
            elif command == "cd":
                if len(args) > 1:
                    print("Ошибка: команда 'cd' принимает не более одного аргумента.")
                else:
                    print(f"[Заглушка] Вызвана команда: cd. Аргументы: {args}")
            
            # 5. Сообщение об ошибке для неизвестных команд (Пункт 4)
            else:
                print(f"Ошибка: неизвестная команда '{command}'.")
                
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы эмулятора.")
            sys.exit(0)

if __name__ == "__main__":
    main()
