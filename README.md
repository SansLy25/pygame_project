## Название проекта
Eclipse Legacy
## Авторы
Степанов Роберт
Сутидзе Александр
Сергей Кабанов

## Описание идеи
Платформер-рпг(рогалик) c несколькими уровнями(этажами). На каждом этаже есть комнаты, в которых спавнятся враги.
Убивая этих врагов, игрок получает уровень, который может обменять на улучшение(одно из предложенных). В конце всех
этажей финальный босс
## Описание реализации
Движок, это основа игры, мы сделали полноценный движок для pygame, полное руководство лежит в файлике engine_guide.md, 
движок физический, поэтому основа это вектора (класс Vector), позволяет совершать все операции с векторами, Speed и Acceleration это
классы векторных величин, нужны для описания движения, далее идут классы игровых объектов: GameObject - базовый класс объекта, 
VelocityObject - класс объекта движущегося линейно, AccelerationObject - класс объекта движущегося с ускорением, SolidObject - класс твердого объекта, BackgroundObject - класс объекта фона, Item - класс предмета, Player - игрок, Enemy - враг, Boss - Босс, Background это фон с парралаксом 

Комнаты генерируются исходя из файлов в rooms/, файлы содержат символы которые описывают что в этих местах будет стоят (например # - это твердый блок), блоки соединяются в конструкции (объединение хитбоксов для оптимизации) и выбирают текстуру в зависимости от соседа, комната описывается классом Room, конструктор уровней лежит в rooms_editor (PyQt6), некоторые объекты на уровне могут быть только вы единичном экземпляре (портал например), для части объектов уровней используются классы в entities

Анимация является частью GameObject, это класс Animation, позволяет управлять и задавать
анимацию

Для интерфейса используются отдельные классы(Button, Slider, Text).
от которого наследуются другие классы.

Сутидзе Александр - создавал интерфейс и механику игроков и врагов, а также навыки и предметы
Степанов Роберт - движок, физика, столкновения, объекты, комнаты, конструктор комнат, анимации, результаты, структура проекта, спрайты
Сергей Кабанов - комнаты

## Зависимости
pygame, 
PyQt6
![Снимок экрана 2025-02-07 154234](https://github.com/user-attachments/assets/9cfd6ae7-3e45-4144-b1c1-e5a9b21216c7)
![Снимок экрана 2025-02-07 154349](https://github.com/user-attachments/assets/7d7f3c5b-e9e9-4a6f-a8a2-5fde7c62226c)
![Снимок экрана 2025-02-07 154559](https://github.com/user-attachments/assets/a6c4e6f0-f4f4-4d37-bc36-f863c072ad0f)
