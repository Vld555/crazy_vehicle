# Test Case Specification — «Бабкин Экспресс»

Соглашение:
- `TC-01…TC-39` — модульные тесты (module, SPEC 4.1, паттерн AAA), `tests/test_walking_hut.py`;
- `TC-40…TC-47` — сценарные тесты (scenario, SPEC 4.2, паттерн GWT, через пилота «Баба Яга»), `tests/test_scenarios.py`;
- соотношение module / scenario = 39 / 8 ≈ 83 / 17.
- Имя тест-метода содержит ID (`test_tc07_...`), docstring начинается с ID (`"""TC-07: ..."""`).
- «Базовая избушка» — `WalkingHut("Избушка", mass_kg=1000.0, leg_length_m=2.0)`: `firewood=100.0`, `pose="standing"`, `facing="forest"`, `healthy_legs=2`, `position_m=0.0`.
- Предусловие задаётся только через публичный интерфейс: «сидит» = `sit_down()`, «1 нога» = `damage_leg()` ×1, «0 ног» = `damage_leg()` ×2.
- Если ожидается исключение, дополнительно проверяется, что состояние не изменилось, а доменное исключение — наследник `WalkingHutError` и `CrazyVehicleError`.

## Модульные тесты

| ID | Тип | Источник | Предусловие | Вход | Ожидание | Приоритет |
|---|---|---|---|---|---|---|
| TC-01 | module | SPEC 3.2, 3.3 | — | `WalkingHut("Избушка", 1000.0, 2.0)` | `name="Избушка"`, `mass_kg=1000.0`, `leg_length_m=2.0`, `firewood=100.0`, `position_m=0.0`, `pose="standing"`, `facing="forest"`, `healthy_legs=2` | high |
| TC-02 | module | SPEC 3.2 | — | `WalkingHut("Избушка", 1500.0, 3.0, 40.0)` | `mass_kg=1500.0`, `leg_length_m=3.0`, `firewood=40.0` | medium |
| TC-03 | module | SPEC 3.2, 5 | — | `WalkingHut("Избушка", 300.0, 0.5, 0.0)` | создан; `mass_kg=300.0`, `leg_length_m=0.5`, `firewood=0.0` | medium |
| TC-04 | module | SPEC 3.2 | — | `name=""` | `ValueError` "Имя не может быть пустым." | high |
| TC-05 | module | SPEC 3.2 | — | `name="   "` | `ValueError` "Имя не может быть пустым." | medium |
| TC-06 | module | SPEC 3.2 | — | `mass_kg=299.9` | `ValueError` "Масса должна быть в диапазоне 300…3000 кг." | high |
| TC-07 | module | SPEC 3.2 | — | `mass_kg=3000.1` | `ValueError` "Масса должна быть в диапазоне 300…3000 кг." | medium |
| TC-08 | module | SPEC 3.2 | — | `leg_length_m=0.4` | `ValueError` "Длина ног должна быть в диапазоне 0.5…5.0 м." | high |
| TC-09 | module | SPEC 3.2 | — | `leg_length_m=5.1` | `ValueError` "Длина ног должна быть в диапазоне 0.5…5.0 м." | medium |
| TC-10 | module | SPEC 3.2 | — | `firewood=100.5` | `ValueError` "Запас дров должен быть в диапазоне 0…100." | medium |
| TC-11 | module | SPEC 3.2 | — | `mass_kg="1000"` | `TypeError` | medium |
| TC-12 | module | SPEC 3.4.1 | базовая | `walk(100)` | возвращает `5.0`; `position_m=100.0`, `firewood=98.0` | high |
| TC-13 | module | SPEC 3.4.1 | базовая, 1 нога | `walk(100)` | возвращает `10.0`; `position_m=100.0`, `firewood=96.0` | high |
| TC-14 | module | SPEC 3.4.1 | базовая | `walk(0)` | `ValueError` "Расстояние должно быть больше 0."; `position_m=0.0`, `firewood=100.0` | high |
| TC-15 | module | SPEC 3.4.1 | базовая | `walk("abc")` | `TypeError` | medium |
| TC-16 | module | SPEC 3.4.1 | базовая, сидит | `walk(10)` | `HutIsSitting` "Избушка сидит. Сначала встаньте."; `position_m=0.0`, `firewood=100.0` | high |
| TC-17 | module | SPEC 3.4.1 | `firewood=1.0` | `walk(100)` | `HutOutOfFirewood` "Не хватает дров в печи."; `position_m=0.0`, `firewood=1.0` | high |
| TC-18 | module | SPEC 3.4.1, 5 | `firewood=2.0` | `walk(100)` | `position_m=100.0`, `firewood=0.0` | high |
| TC-19 | module | SPEC 3.4.2 | базовая | `run(100)` | возвращает `2.5`; `position_m=100.0`, `firewood=94.0` | high |
| TC-20 | module | SPEC 3.4.2 | базовая, 1 нога | `run(10)` | `HutIsLame` "Избушка хромает: действие требует двух здоровых ног."; `position_m=0.0`, `firewood=100.0` | high |
| TC-21 | module | SPEC 3.4.3 | базовая | `sit_down()` | `pose="sitting"`, `firewood=100.0` | high |
| TC-22 | module | SPEC 3.4.4 | базовая, сидит | `stand_up()` | `pose="standing"`, `firewood=99.0` | high |
| TC-23 | module | SPEC 3.4.4 | базовая | `stand_up()` | `HutWrongPose` "Избушка уже стоит."; `firewood=100.0` | medium |
| TC-24 | module | SPEC 3.4.4 | базовая, 0 ног | `stand_up()` | `HutCannotWalk` "Избушка не может идти: обе ноги сломаны."; `pose="sitting"`, `firewood=100.0` | high |
| TC-25 | module | SPEC 3.4.5 | базовая | `turn_around()` | `facing="traveler"`, `firewood=99.5`, `position_m=0.0` | high |
| TC-26 | module | SPEC 3.4.5 | базовая, сидит | `turn_around()` | `HutIsSitting` "Избушка сидит. Сначала встаньте."; `facing="forest"`, `firewood=100.0` | medium |
| TC-27 | module | SPEC 3.4.6 | базовая | `can_step_over("fence")` | `True`; `firewood=100.0` | high |
| TC-28 | module | SPEC 3.4.6 | базовая | `can_step_over("boulder")` | `False`; `firewood=100.0` | high |
| TC-29 | module | SPEC 3.4.7 | базовая | `step_over("fence")` | `firewood=97.0`, `position_m=0.0` | high |
| TC-30 | module | SPEC 3.4.7 | базовая | `step_over("wall")` | `HutCannotStepOver` "Ноги слишком короткие для этого препятствия."; `firewood=100.0` | high |
| TC-31 | module | SPEC 3.4.6, 3.4.7 | базовая | `step_over("river")` | `ValueError` "Неизвестное препятствие."; `firewood=100.0` | medium |
| TC-32 | module | SPEC 3.4.8 | `firewood=50.0`, сидит | `add_firewood(30)` | `firewood=80.0` | high |
| TC-33 | module | SPEC 3.4.8, 5 | `firewood=50.0`, сидит | `add_firewood(1000)` | `firewood=100.0` | high |
| TC-34 | module | SPEC 3.4.8 | `firewood=50.0` | `add_firewood(10)` | `HutWrongPose` "Подбросить дров можно только когда избушка сидит."; `firewood=50.0` | high |
| TC-35 | module | SPEC 3.4.8 | базовая, сидит | `add_firewood(0)` | `ValueError` "Количество дров должно быть больше 0."; `firewood=100.0` | medium |
| TC-36 | module | SPEC 3.4.9 | базовая | `damage_leg()` | `healthy_legs=1`, `pose="standing"` | high |
| TC-37 | module | SPEC 3.4.9 | базовая | `damage_leg()` ×2 | `healthy_legs=0`, `pose="sitting"` | high |
| TC-38 | module | SPEC 3.4.9 | базовая, 0 ног | `damage_leg()` | `HutCannotWalk` "Обе ноги уже сломаны."; `healthy_legs=0` | medium |
| TC-39 | module | SPEC 3.4.10 | базовая | `get_status()` | `{"name": "Избушка", "position_m": 0.0, "firewood": 100.0, "pose": "standing", "facing": "forest", "healthy_legs": 2}` | medium |

## Сценарные тесты

Все шаги выполняются через пилота `BabaYaga` и объект среды `Kapkan` (`tests/pilot.py`), итог — через `осмотреться()` (`get_status()`).

| ID | Тип | Источник | Вход | Ожидание | Приоритет |
|---|---|---|---|---|---|
| TC-40 | scenario | SPEC 4.2, сц. 40 «Путник у леса» | базовая; `пройти(300)`, `стань_ко_мне_передом()`, `присесть()`, `подкинуть_дров(20)` | время 15.0; `position_m=300.0`, `firewood=100.0`, `pose="sitting"`, `facing="traveler"`, `healthy_legs=2` | high |
| TC-41 | scenario | SPEC 4.2, сц. 41 «Полоса препятствий» | базовая; `перешагнуть("log")`, `можно_перешагнуть("boulder")`, `пройти(50)`, `перешагнуть("fence")`, `перешагнуть("wall")` | `False` на валун; `HutCannotStepOver` на стену; `position_m=50.0`, `firewood=93.0`, `pose="standing"` | high |
| TC-42 | scenario | SPEC 4.2, сц. 42 «Капкан в чаще» | базовая; `пройти(100)`, `Kapkan.защемить`, `пройти(100)`, `пробежать(10)`, `перешагнуть("log")` | время хромой ходьбы 10.0; `HutIsLame` ×2; `position_m=200.0`, `firewood=94.0`, `healthy_legs=1`, `pose="standing"` | high |
| TC-43 | scenario | SPEC 4.2, сц. 43 «Дрова кончились в пути» | `firewood=10`; `пробежать(100)`, `пройти(300)`, `присесть()`, `подкинуть_дров(50)`, `встать()`, `пройти(300)` | время бега 2.5; `HutOutOfFirewood` на первом `пройти(300)` при `firewood=4.0`; итог `position_m=400.0`, `firewood=47.0`, `pose="standing"` | high |
| TC-44 | scenario | SPEC 4.2, сц. 44 «Двойной капкан» | базовая; `Kapkan.защемить` ×2, `встать()`, `пройти(10)`, `Kapkan.защемить` | `HutCannotWalk` ×3 (последний — "Обе ноги уже сломаны."); `position_m=0.0`, `firewood=100.0`, `pose="sitting"`, `healthy_legs=0` | medium |
| TC-45 | scenario | SPEC 4.2, сц. 45 «Сидячая забастовка» | базовая; `присесть()`, `пройти(10)`, `стань_ко_мне_передом()`, `присесть()`, `встать()`, `подкинуть_дров(1)` | `HutIsSitting` ×2, `HutWrongPose` "Избушка уже сидит.", `HutWrongPose` на дрова стоя; `position_m=0.0`, `firewood=99.0`, `pose="standing"`, `facing="forest"` | medium |
| TC-46 | scenario | SPEC 4.2, сц. 46 «Великан на длинных ногах» | `2500 кг`, ноги `5.0`; `перешагнуть("wall")`, `пробежать(200)`, `пройти(500)`, `стань_ко_мне_передом()` ×2 | время бега 2.0, ходьбы 10.0; `position_m=700.0`, `firewood=41.0`, `facing="forest"` | medium |
| TC-47 | scenario | SPEC 4.2, сц. 47 «Экономная малышка» | `300 кг`, ноги `0.5`, `firewood=3`; `можно_перешагнуть("log")`, `перешагнуть("log")`, `пройти(1)`, `присесть()`, `подкинуть_дров(100)`, `встать()`, `пройти(100)` | `True` на бревно; `HutOutOfFirewood` при `firewood=0.0`; время 20.0; `position_m=100.0`, `firewood=98.4` | medium |
