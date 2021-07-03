---
layout: page
title: Массивы (Arrays)
nav_order: 4
has_children: true
permalink: /arrays/
has_toc: false
---

# Массивы
{: .no_toc}

Sfall вводит новый метод хранения переменных - массивы.

Массив - это в основном контейнер, в котором может храниться переменное количество значений (элементов). Каждый элемент в массиве может быть любого типа.
Массивы могут быть чрезвычайно полезны для некоторых более сложных сценариев в сочетании с циклами.<br>

Описание всех функций массивов [здесь]({{ site.baseurl }}/array-functions/) и [здесь]({{ site.baseurl }}/lists/).

* TOC
{:toc}

***
## Концепция массивов

Массивы создаются и управляются с помощью функций массива. Для начала массив должен быть создан с помощью функций `create_array` или `temp_array`, указав, сколько элементов данных может содержать массив. Вы можете хранить любые типы данных `int`, `float` или `string` в массиве, также можно смешивать все 3 типа в одном массиве.  
Идентификатор массива, возвращаемый функциями `create_array` или `temp_array`, может использоваться в других функциях для доступа к созданному массиву. Массивы являются общими для всех сценариев (т.е. вы можете вызвать `create_array` в одном сценарии, а затем использовать возвращенный идентификатор в совершенно другом сценарии для доступа к массиву).
Массивы также могут быть сохранены в файлах сохранения игры.

Массивы, созданные с помощью `temp_array`, будут автоматически удалены в конце кадра выполнения сценария.
`create_array` - единственная функция, которая возвращает постоянный массив, все остальные функции, возвращающие массивы (`string_split`, `list_as_array` и т.д.), создают временные массивы. Вы можете использовать функцию `fix_array`, чтобы сделать временный массив постоянным.  
Функции массивов полностью безопасны в том смысле, что использование неверного идентификатора или попытки доступа к элементам вне размера массива не приведут к сбою в сценарии.  

Доступ к элементам массива осуществляется по индексу или ключу. 

_Пример:_
```c
    // this code puts some string in array "list" at index 5:
    list[5] := "Value";
```

В настоящее время доступно 2 различных типа массива:

1. **Lists** - предоставляет коллекцию значений, определенного размера (количество элементов), где элементы имеют числовые индексы, первый индекс элемента всегда начинается с нуля (0) до конца всей длины массива минус единица.

    _Пример:_
    ```c
    // this creates list with 3 elements. Element "A" has index 0, element "B" has index 1, element "C" - 2
    list := ["A", "B", "C"];
    ```
    Ограничения:
      - все индексы являются числовыми, и начинаются с 0
      - чтобы присвоить значение элементу списка по определенному индексу, необходимо для сначала изменить размер массива, чтобы список содержал этот индекс  
        например, если список имеет размер 3 (индексы от 0 до 2), вы не можете присвоить значение по индексу 4, если сначала не измените размер списка на 5

2. **Maps** - ассоциативные массивы содержат наборы пар **key=>value**, где все элементы (значения) доступны с помощью соответствующих ключей.

    Отличия Maps (карт) от List (списка):
    - ассоциативные массивы не имеют определенного размера (для присвоения значений вам не нужно изменять размер массива)
    - ключи, как и значения, могут быть любого типа (но избегайте использования -1 в качестве ключей массива, иначе вы не сможете надежно использовать некоторые функции)

Оба типа массива имеют свои плюсы и минусы и подходят для решения различных задач.

___
## Синтаксис массивов

В основном массивы реализуются с использованием ряда новых операторов (функций сценариев). Но для удобства использования есть некоторые новые элементы синтаксиса:

1. Доступ к элементам. Используйте квадратные скобки:
```c
    display_msg(arr[5]);
    mymap["price"] := 515.23;
```

2. Альтернативный доступ к картам. Используйте точку:
```c
    display_msg(mymap.name);
    mymap.price := 232.23;
```

3. Выражения массива. Создавайте и заполняйте массивы просто используя одно выражение:
```c
    // create list with 5 values
    [5, 777, 0, 3.14, "Cool Value"]

    // create map:
    {5: "Five", "health": 50, "speed": 0.252}
```
__NOTES:__
Обязательно вызовите `fix_array`, если вы хотите, чтобы новый массив был доступен в следующем фрейме выполнения сценария, или `save_array`, если вы хотите использовать его в течение более длительного периода (подробнее см. следующий раздел).

4. Перебор элементов массива в цикле. Используйте ключевое слово `foreach` следующим образом:
```c
    foreach (item in myarray) begin
        // этот блок выполняется для каждого элемента массива, где "item" содержит текущее значение на каждом шаге итерации
    end

    // альтернативный синтаксис:
    foreach (key: item in myarray) begin
        // "key" будет содержать текущий ключ (или числовой индекс, для списков)
    end
```

Обратитесь к описанию копмилятра [sslc]({{ site.baseurl }}/sslc/) или к файлу **sslc_readme.md** для получения полной информации о новых функциях синтаксиса SSL.

___
## Хранение массивов

Часть массивов списков и карт разделена по способу их хранения.

Существует 3 типа массивов:

* **Temporary**: Они создаются с помощью функции `temp_array` или при использовании выражений массива. Массивы этого типа автоматически удаляются в конце кадра выполнения сценария. Так, например, если у вас есть глобальный сценарий, который выполняется через регулярные промежутки времени, где вы создаете `temp_array`, то массив не будет доступен при следующем выполнении вашего глобального сценария.

* **Permanent**: Они создаются с помощью функций `create_array` или `fix_array` (из уже существующего временного массива). Массивы этого типа всегда доступны (по их идентификатору) до тех пор, пока вы не начнете новую игру или не загрузите сохраненную игру (после чего они будут удалены).

* **Saved**: Если вы хотите, чтобы ваш массив действительно оставался на некоторое время, используйте функцию `save_array`, чтобы сделать любой массив "сохраняемым". Однако они, как и постоянные массивы, "удаляются" из памяти при загрузке игры. Чтобы правильно их использовать, вы должны загружать их из сохраненной игры с помощью `load_array` всякий раз, когда вы хотите их использовать.<br>

    _Пример:_
    ```c
    variable savedArray;
    procedure start begin
        if game_loaded then begin
            savedArray := load_array("traps");
        end else begin
            foreach trap in traps begin
                ....
            end
        end
    end
    ```

___
## Практические примеры

Используйте массивы для реализации процедур с переменными аргументами:
```c
    // define it
    procedure give_item(variable critter, variable pidList) begin
        foreach (pid: qty in pidList) begin
            give_pid_qty(critter, pid, qty);
        end
    end

    // call it:
    call give_item(dude_obj, {PID_SHOTGUN: 1, PID_SHOTGUN_SHELLS: 4, PID_STIMPAK: 3});
```

Создание массивов объектов (карт) для продвинутого скриптинга:
```c
    variable traps;
    procedure init_traps begin
        // just a quick example, there is a better way of doing it...
        traps := load_array("traps");
        if (traps == 0) then begin
            traps := [];
            save_array("traps", traps);
        end
        foreach k: v in traps begin
            traps[k] := load_array("trap_"+k); // каждый объект хранится отдельно
        end
    end

    procedure add_trap(variable trapArray) begin
        variable index;
        index := len_array(traps);
        save_array("trap_"+k, trapArray);
        array_push(traps, trapArray);
    end

    // use them:
    foreach trap in traps begin
        if (self_elevation == trap["elev"] and tile_distance(self_tile, trap["tile"]) < trap["radius"]) then
            // kaboom!!!
        end
    end
```
___
## Примечания по обратной совместимости

Для тех, кто использовал массивы в своих модах до sfall 3.4:

1. Существует INI параметр **ArraysBehavior** в **Misc** разделе файла "ddraw.ini". Если его значение установлено в 0, то все сценарии, которые ранее использовали массивы sfall, должны работать. Это в основном меняет то, что `create_array` создает постоянные массивы, которые "сохраняются" по умолчанию, и их идентификатор также является постоянным. По умолчанию этот параметр равен 1.

2. Как обрабатывается совместимость с сохраненными играми?.<br>
Сохраненные массивы хранятся в файле **sfallgv.sav** (в сохраненной игре) в новом (более гибком) формате сразу после старых массивов. Таким образом, в принципе, когда вы загружаете старую сохраненную игру, sfall загрузит массивы из старого формата и сохранит их в новом формате при следующем сохранении игры. Если вы загрузите сохраненную игру, созданную с помощью sfall 3.4, используя sfall 3.3 (например), игра не должна завершиться сбоем, но все массивы будут потеряны.

3. Ранее вам приходилось указывать размер в байтах для элементов массива. Этот параметр теперь игнорируется, и вы можете хранить строки произвольной длины в массивах.


## Array operators reference

_*mixed means any type_

* `int create_array(int size, int flags)`:
  - creates permanent array (but not "saved")
  - if `size >= 0`, creates list with given size
  - if `size == -1`, creates map (associative array)
  - if `size == -1` and `flags == 2`, creates a "lookup" map (associative array) in which the values of existing keys are read-only and can't be updated. This type of array allows you to store a zero (0) key value
    * NOTE: in earlier versions (up to 4.1.3/3.8.13) the second argument is not used, just use 0
  - returns arrayID (valid until array is deleted)

* `int temp_array(int size, int flags)`:
  - works exactly like `create_array`, only created array becomes "temporary"

* `void fix_array(int arrayID)`:
  - changes "temporary" array into "permanent" ("permanent" arrays are not automatically saved into savegames)

* `void set_array(int arrayID, mixed key, mixed value)`:
  - sets array value
  - if used on list, "key" must be numeric and within valid index range (0..size-1)
  - if used on map, key can be of any type
  - to "unset" a value from map, just set it to zero (0)
    * NOTE: to add a value of 0 for the key, use the float value of 0.0
  - this works exactly like statement: `arrayID[key] := value;`

* `mixed get_array(int arrayID, mixed key)`:
  - returns array value by key or index
  - if key doesn't exist or index is not in valid range, returns 0
  - works exactly like expression: `(arrayID[key])`

* `void resize_array(int arrayID, int size)`:
  - changes array size
  - applicable to maps too, but only to reduce elements
  - there are number of special negative values of "size" which perform various operations on the array, use macros `sort_array`, `sort_array_reverse`, `reverse_array`, `shuffle_array` from **sfall.h** header

* `void free_array(int arrayID)`:
  - deletes any array
  - if array was "saved", it will be removed from a savegame

* `mixed scan_array(int arrayID, mixed value)`:
  - searches for a first occurence of given value inside given array
  - if value is found, returns it's index (for lists) or key (for maps)
  - if value is not found, returns -1 (be careful, as -1 can be a valid key for a map)

* `int len_array(int arrayID)`:
  - returns number of elements or key=>value pairs in a given array
  - if array is not found, returns -1  (can be used to check if given array exist)

* `mixed array_key(int arrayID, int index)`:
  - don't use it directly; it is generated by the compiler in foreach loops
  - for lists, returns index back (no change)
  - for maps, returns a key at the specified numeric index (don't rely on the order in which keys are stored though)
  - can be checked if given array is associative or not, by using index (-1): 0 - array is list, 1 - array is map

* `int arrayexpr(mixed key, mixed value)`:
  - don't use it directly; it is used by compiler to create array expressions
  - assigns value to a given key in an array, created by last `create_array` or `temp_array` call
  - always returns 0

* `void save_array(mixed key, int arrayID)`:
  - makes the array saveable; it will be saved in **sfallgv.sav** file when saving the game
  - arrayID is associated with given "key"
  - array becomes permanent (if it was temporary) and "saved"
  - key can be of any type (int, float or string)
  - if you specify 0 as the key for the array ID, it will make the array "unsaved"

* `int load_array(mixed key)`:
  - loads array from savegame data by the same key provided in `save_array`
  - returns array ID or zero (0) if none found