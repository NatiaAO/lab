Лабораторная работа по заданию для студентов МИИГАиК - Вариант 1 (2024г).

Используя любой скриптовый язык (например, Python, Ruby, Javascript, Perl) написать скрипт, извлекающий новости (отдельно заголовок, аннотацию, авторов) из веб-страницы новостного агентства, но не используя RSS.

Требуется написать такой скрипт, который будучи запущен на определенное время (например, 4 часа) автоматически выделит и отобразит/запишет в лог все статьи, которые будут опубликованы за этот период (то есть, только новые), при этом выводить нужно новости, содержащие упоминания Республиканской и Демократической партии США.

Работа сдается в виде:
Одиночного файла скрипта, готового для запуска
Указание на зависимые библиотеки (если есть)
Скриншот и лог работы скрипта на протяжении 4 часов с выводом всех найденных новостей (если за 4 часа не нашлось - выбирайте другое новостное агентство)
Возможно предоставление решения в виде публичной песочницы, например на http://repl.it.

https://moodle.tsu.ru/mod/assign/view.php?id=795900

В коде используемы библеотки
- requests
- BeautifulSoup
- time
- re
- threading
