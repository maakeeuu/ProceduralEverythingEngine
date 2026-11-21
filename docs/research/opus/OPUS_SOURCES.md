# OPUS_SOURCES — реестр проверенных источников

- Версия: v4. O01–O24 проверены 2026-11-21 (сессия 2); O25–O31 — 2026-11-21 (сессия 6, раздел 10); O32–O38 — 2026-11-21 (сессия 7, раздел 11). Маркер конца файла добавлен в v2; в v1 (blob 0122bf6) его не было.
- Ветка: `research/opus-review-continuation-2026-11-21`.
- Назначение: проверить изменчивые факты (версии, статусы стандартов, лицензии), на которые опираются исследование GPT (PR #1) и снимок `00_PRE_GPT_POSITION.md`. Попутно закрыть часть пробелов, которые GPT сам перечислил в разделе «Неустановленное и отложенное» своего реестра.

## 0. Метод и ограничения

- Проверка выполнена web-поиском и загрузкой страниц первоисточников: официальные сайты, репозитории, release notes, тексты лицензий. Цитаты даны на языке оригинала.
- Ничего не собиралось и не запускалось. Запись в реестре не означает, что технология проверена в коде проекта.
- Маркеры: **[Ф]** факт из источника на дату проверки; **[О]** оценка рецензента; **[П]** предположение; **[?]** открытый вопрос.
- Статусы:
  - **Подтверждено** — совпадает с реестром GPT или со снимком;
  - **Уточнение** — GPT не ошибся, но формулировка неполна или неточна;
  - **Устарело** — вышла новая версия или другая страница проекта показывает другую;
  - **Новое** — у GPT записи нет;
  - **Не перепроверено** — принято без повторной проверки в сессии 2.
- Нумерация O01–O24 собственная. S01–S21 — записи `docs/research/gpt/SOURCES.md` (ветка `research/gpt-architecture-2026-11-21`, коммит 0cc3eb8).
- Лицензионные выводы — техническое прочтение текстов, а не юридическое заключение.

## 1. Сводка для архитектуры

| # | Находка | Статус | Влияние |
|---|---|---|---|
| F1 | MoltenVK deprecated; на Apple Silicon Khronos рекомендует KosmicKrisp. KosmicKrisp требует macOS 26+ и Metal 4, Intel Mac не поддерживает | Подтверждено (S16), новое о KosmicKrisp | Средняя для варианта B: два Vulkan-пути на macOS. Низкая для A: wgpu использует Metal напрямую |
| F2 | Slint Royalty-Free: обязательна атрибуция; запрещены Embedded Systems и распространение приложения, которое «exposes the APIs» Slint | Уточнение (S18) | Средняя: ограничивает UI-API для плагинов, если UI построен на Slint |
| F3 | Qt 6.12 — LTS (30.09.2026), «maintenance over a 5-year period» | Уточнение (S01, S20) | Низкая–средняя: база варианта B; условия LTS для LGPL не проверены |
| F4 | OCIO: актуальная линия 2.6 (PyPI 2.6.0) | Устарело (S11: сайт показывал 2.5.0) | Низкая |
| F5 | WebGPU — W3C Candidate Recommendation; wasi:webgpu остаётся в WASI, остальное wasi-gfx уходит в отдельное пространство имён; wasi:graphics-context устарел | Новое | Средняя для GPU-плагинов: стандарт ещё движется |
| F6 | f64 в WGSL не стандартизован (gpuweb #2805 открыт, milestone «4+»); в wgpu 64-битные типы — native-only расширения | Новое, подтверждает риск снимка | Средняя: глубокий зум фракталов и точная геометрия на GPU |
| F7 | Free-threaded Python официально поддерживается с 3.14 (PEP 779), но остаётся отдельной сборкой | Новое | Низкая: Python не становится песочницей |
| F8 | Прецеденты: Graphite (слои поверх нодового графа), Copernicus (типизированные провода, GPU-резидентность), TouchDesigner (вычисление по требованию), Blender (fields, zones), Substance (Pixel Processor, FX-Map), Material Maker (GLSL-ноды) | Новое | Высокое для Э3–Э5: у подходов снимка есть работающие аналоги |
| F9 | Кандидаты на пробелы, отмеченные GPT: Manifold (булевы операции), Vello (2D-вектор на GPU), Slang (язык шейдеров), webgpu.h (C-ABI к WebGPU) | Новое | Среднее: входят в сравнение стеков (Э7) |
| F10 | Patch-дрейф: wgpu 30.0.2 (S04 показывал 30.0.0), egui 0.37.0 | Подтверждено | Низкое: фиксировать версии в lock-файлах прототипов, а не в архитектурных документах |

## 2. Графические API, шейдеры, GPU

### O01. MoltenVK
Статус: **Подтверждено** (S16). Источник: https://github.com/KhronosGroup/MoltenVK (README).

- [Ф] «Deprecation notice: Khronos has deprecated MoltenVK… now maintained by the community on a best-effort basis. For Vulkan on Metal, Khronos now recommends KosmicKrisp on Apple Silicon Macs. MoltenVK remains the recommended option for Intel-based Macs and for iOS.»
- [Ф] README описывает MoltenVK как «Vulkan 1.4 subset». KosmicKrisp распространяется через Vulkan SDK для macOS или из исходников Mesa.
- [О] GPT зафиксировал этот статус верно. Дополнение — требования KosmicKrisp (O02).

### O02. KosmicKrisp (LunarG)
Статус: **Новое**. Источники:
- https://www.lunarg.com/products/kosmickrisp
- https://www.lunarg.com/kosmickrisp-achieves-vulkan-1-4-conformance-on-apple-silicon
- https://www.lunarg.com/the-state-of-vulkan-on-apple-oct-2026/
- https://www.lunarg.com/lunarg-at-xdc-2026-kosmickrisp-update/

Факты и выводы:
- [Ф] Драйвер Mesa, реализующий Vulkan поверх Metal 4. Conformant Vulkan 1.4 «as of September 2026»; входит в LunarG SDK и upstream Mesa.
- [Ф] Не поддерживает Intel Mac и macOS ниже 26. По докладу XDC 2026 (28.09.2026): conformant ICD на macOS 26+ для M1–M5 и A18 Pro.
- [Ф] Обзор LunarG за октябрь 2026: MoltenVK не полностью conformant, KosmicKrisp полностью conformant; разработку спонсирует Google.
- [?] В посте о conformance заголовок датирован 25.09.2026, а в тексте стоит «September 25, 2025». Опираться на формулировку продуктовой страницы.
- [О] Для варианта B прямой Vulkan на macOS означает либо два пути (KosmicKrisp и MoltenVK в режиме best-effort), либо отказ от Intel Mac и macOS ниже 26. Это аргумент за абстракцию над Metal (wgpu, QRhi или собственный Metal-бэкенд), а не за «Vulkan везде».

### O03. wgpu
Статус: **Подтверждено** (S03, S04), patch-дрейф. Источники: https://github.com/gfx-rs/wgpu/releases, https://crates.io/crates/wgpu, https://docs.rs/crate/wgpu/latest

- [Ф] Последний релиз v30.0.2 (12.11.2026); есть backport v29.0.4; naga 30.0.2.
- [Ф] Бэкенды: Vulkan, Metal, D3D12, OpenGL; на wasm — WebGPU и WebGL2.
- [О] Мажорные версии выходят часто. В прототипах фиксировать версию и закладывать стоимость миграций; типы wgpu не выставлять в публичный SDK плагинов.

### O04. f64 в WGSL и wgpu
Статус: **Новое**, подтверждает риск снимка. Источники: https://github.com/gpuweb/gpuweb/issues/2805, https://github.com/gfx-rs/wgpu/issues/4410, https://docs.rs/wgpu/latest/wgpu/struct.Features.html

- [Ф] Issue «Double precision floats (IEEE-754 binary64)» открыт с 28.04.2022, метка wgsl, milestone «4+».
- [Ф] В wgpu 64-битные типы — native-only расширения Naga (issue #4410, метка «feature: 64-bit types (i64, u64, and f64)»).
- [?] Поддержка SHADER_F64 по бэкендам (в частности, Metal) в загруженных фрагментах не подтверждена.
- [О] GPU-путь проектировать в f32. Глубокий зум фракталов — через эмуляцию повышенной точности или CPU f64. Точную геометрию держать на CPU.

### O05. Vulkan 1.4
Статус: **Подтверждено**. Источники: http://www.khronos.org/news/press/khronos-streamlines-development-and-deployment-of-gpu-accelerated-applications-with-vulkan-1.4, https://www.phoronix.com/news/Vulkan-1.4-Released

- [Ф] Vulkan 1.4 анонсирован в декабре 2024: пресс-релиз Khronos с SIGGRAPH Asia; в архиве новостей — 2 декабря 2024.

### O06. Slang
Статус: **Новое**; у GPT языки шейдеров — пробел по собственной пометке. Источники:
- https://shader-slang.org/
- https://github.com/shader-slang/slang
- https://www.khronos.org/news/tags/tag/slang
- https://www.khronos.org/assets/uploads/developers/presentations/Slang_BOF_-_SIGGRAPH_Jul26.pdf

Факты и выводы:
- [Ф] Slang развивается под эгидой Khronos. В презентации BOF (SIGGRAPH, июль 2026): «preferred shading language» по LunarG 2026 Vulkan Ecosystem Survey, более 5400 звёзд на GitHub, более 250 коммитов в месяц.
- [Ф] 22.01.2026: «MaterialX Adds Support for Slang Shader Generation».
- [О] Сильный кандидат для варианта B и для генерации шейдеров материалов. Для варианта A — возможный исходный язык с выводом в WGSL [П]: качество WGSL-бэкенда не проверено.

### O07. webgpu.h
Статус: **Новое**. Источники: https://github.com/webgpu-native/webgpu-headers, https://developer.chrome.com/blog/new-in-webgpu-141, https://github.com/gfx-rs/wgpu-native

- [Ф] webgpu.h — общий C-заголовок Dawn/Emdawnwebgpu и wgpu-native («multi-vendor standard»), BSD-3-Clause. С Chrome 141 (24.09.2025) core API заголовка «is now finally considered stable».
- [О] Даёт C-ABI к WebGPU для нативного SDK независимо от языка ядра и снижает привязку к одной реализации (Dawn или wgpu).

### O08. wasi-gfx и wasi:webgpu
Статус: **Новое**, подтверждает тезис T11 снимка. Источники: https://wasi-gfx.dev/blog/posts/future-of-wasi-gfx, https://github.com/WebAssembly/wasi-webgpu, https://github.com/wasi-gfx/wasi-gfx

- [Ф] Пост 07.06.2026: «With WebGPU reaching stability as a W3C Candidate Recommendation, wasi:webgpu should continue to live in the wasi namespace… The rest of wasi-gfx will be lifted out to its own namespace and governance.»
- [Ф] wasi:graphics-context устарел; wasi:surface и wasi:frame-buffer переходят в пространство имён wasi-gfx. Предложение wasi-webgpu — Phase 2.
- [О] GPU из WASM-плагинов через стандарт возможен, но стандарт не стабилен. Для v1 надёжнее, чтобы плагин передавал хосту шейдер или IR, а хост валидировал и исполнял его (T11).

### O09. Vello
Статус: **Новое**; у GPT векторный рендеринг — пробел. Источник: https://github.com/linebender/vello

- [Ф] «A GPU compute-centric 2D renderer»; на странице репозитория указана Apache-2.0 [?] полный набор лицензий не сверялся.
- [Ф] ARCHITECTURE.md: семейство vello_cpu и vello_gpu (Sparse Strips) и экспериментальный compute-рендерер vello. Последние релизы: Vello Research v0.12.0 (11 ноября), Sparse Strips v0.4.0.
- [О] Кандидат на 2D-векторный рендеринг в Rust-вариантах. Экспорт SVG и PDF он не решает: для этого нужен собственный сериализатор векторной модели.

## 3. UI-фреймворки

### O10. egui, eframe, egui-wgpu
Статус: **Подтверждено** (S04, S05). Источники: https://github.com/emilk/egui/releases, https://github.com/emilk/egui/blob/main/crates/egui-wgpu/CHANGELOG.md

- [Ф] egui 0.37.0 «Colored emojis!» — 15.10.2026; в changelog eframe — «0.37.0 - 2026-10-15».
- [Ф] Верхняя запись changelog egui-wgpu — 0.36.2 (08.09.2026); 0.36.0 (05.08.2026) — «Upgrade wgpu to v30». При этом S04 видел в eframe re-export egui-wgpu 0.37.0.
- [?] Changelog egui-wgpu, по-видимому, отстаёт от выпусков [П]. Сверить по crates.io при пиннинге.
- [О] Главный риск egui — не версии, а объём работы до продуктового качества: доступность, IME, сложные текстовые поля, визуальная полировка. Это гипотеза H6; её проверяет прототип, а не документация.

### O11. Qt 6.12 LTS
Статус: **Уточнение**: S01 и S02 видели Qt 6.12, но LTS-статус не отмечен. Источники: https://www.qt.io/blog/qt-6.12-released, https://www.qt.io/development/qt-framework/latest-releases

- [Ф] Qt 6.12 выпущен 30.09.2026 как LTS: «maintenance over a 5-year period». В релизе — соответствие EU CRA, QML hot reload, HarmonyOS.
- [Ф] Страница последних релизов: 6.12 LTS, 6.11, 6.10, 6.9, 6.8 LTS.
- [?] Какие LTS-обновления 6.12 получат пользователи open-source (LGPL), не проверено. Осторожность GPT («не обещать долгую бесплатную поддержку любого Qt 6.x», S20) остаётся верной.
- [О] Если выбирается Qt, базовая версия — 6.12 LTS.

### O12. Slint
Статус: **Уточнение** (S18). Источники:
- https://slint.dev/pricing
- https://slint.dev/faqs
- https://slint.dev/agreements/slint-royalty-free-license.pdf
- https://slint.dev/terms-and-conditions

Факты и выводы:
- [Ф] Три лицензии: GPLv3, Royalty-Free, коммерческая (Slint Software License 3.0.5).
- [Ф] Royalty-Free License v2.0 — для «proprietary applications excluding Embedded Systems». Обязательна атрибуция: виджет AboutSlint в экране About или на заставке, либо бейдж Slint на публичной веб-странице.
- [Ф] Royalty-Free не разрешает: распространять Software отдельно; использовать в Embedded Systems; «distribution of Application that exposes the APIs, in part or in total, of the Software».
- [Ф] Тарифы: Royalty-Free; Startup & Individual (до 10 сотрудников, до 2 млн EUR, менее 5 лет с регистрации); Small Enterprise (до 50 сотрудников / 10 млн EUR); Enterprise.
- [О] S18 называет условие «disclosure»; по тексту лицензии это атрибуция. Существеннее запрет «exposes the APIs». Если плагины получат UI-API, который напрямую передаёт API Slint (например, описание UI плагина на языке .slint), это может попасть под запрет. Собственный декларативный UI-слой поверх Slint, вероятно, ограничения не нарушает [?]; нужна юридическая проверка.

## 4. Скриптинг

### O13. Python free-threading (PEP 779)
Статус: **Новое**. Источники:
- https://peps.python.org/pep-0779
- https://blog.python.org/2025/10/python-3140-final-is-here
- https://www.python.org/downloads/release/python-3150
- https://docs.python.org/3/howto/free-threading-python.html

Факты и выводы:
- [Ф] PEP 779 — Final (решение 16.06.2025): free-threaded сборка официально поддерживается с Python 3.14 (выпуск 07.10.2025).
- [Ф] Python 3.15.0 выпущен 09.10.2026; документация показывает версию 3.15.2. Howto по free-threading по-прежнему описывает отдельную сборку.
- [?] Стала ли free-threaded сборка сборкой по умолчанию в 3.15, явно не подтверждено.
- [О] Free-threading снимает ограничение GIL, но не даёт изоляции: in-process Python нельзя считать песочницей. Вывод T10 снимка (Python — доверенная автоматизация, недоверенный код — Luau или WASM) в силе.

## 5. Библиотеки изображений, геометрии и материалов

### O14. OpenColorIO
Статус: **Устарело** (S11). Источники: https://opencolorio.readthedocs.io/en/latest/releases/ocio_2_6.html, https://pypi.org/project/opencolorio/2.6.0

- [Ф] Есть release notes OCIO 2.6; на PyPI — 2.6.0. По S11 сайт opencolorio.org показывал 2.5.0.
- [О] Это не ошибка GPT, а расхождение страниц проекта. Для воспроизводимости фиксировать версию OCIO и конфиг, как и требует S11.

### O15. OpenSubdiv
Статус: **Подтверждено** (S12). Источники: https://www.opensubdiv.com/docs/release_notes.html, https://opensubdiv.org/docs/release_38.html

- [Ф] 3.8.0 — октябрь 2026; 3.7.0 — октябрь 2025; 3.6.1 — июнь 2025.
- [Ф] Лицензия Apache-2.0 — по пакету Arch Linux 3.8.0-2 (вторичный источник).

### O16. CGAL
Статус: **Подтверждено** (S15). Источники: https://www.cgal.org/releases.html, https://www.cgal.org/license.html

- [Ф] 6.2.1 — сентябрь 2026. С версии 4.0 пакеты распространяются под GPL v3+ или LGPL v3+; есть коммерческая лицензия.
- [О] Согласен с GPT: нужен поштучный аудит пакетов. Для булевых операций над сетками есть альтернатива с разрешительной лицензией — Manifold (O18).

### O17. MaterialX
Статус: **Подтверждено** (S14). Источник: https://github.com/AcademySoftwareFoundation/MaterialX/releases

- [Ф] Последний релиз — 1.39.5. [?] Дата в загруженном фрагменте не видна (S14: 2026-05-22).
- [Ф] С января 2026 MaterialX генерирует шейдеры Slang (новость Khronos, O06).

### O18. Manifold
Статус: **Новое**; у GPT обзор geometry kernels — пробел. Источники: https://github.com/elalish/manifold, https://manifoldcad.org/docs/html

- [Ф] «Geometry library for topological robustness», Apache-2.0. Работает с manifold-сетками из треугольников, гарантирует manifold-результат, хранит произвольные свойства вершин; есть JS/TS/WASM API.
- [?] Мелкое расхождение версий: PyPI manifold3d 3.5.5, на GitHub последний релиз v3.5.4.
- [О] Кандидат на булевы операции в любом варианте стека. Ограничение: только треугольники. Полигональную модель ядра (H4) придётся триангулировать на входе и восстанавливать атрибуты на выходе. Скорость относительно CGAL не измерялась [П].

## 6. Прецеденты продуктов

### O19. Graphite
Статус: **Новое**. Источники: https://graphite.rs/, https://github.com/GraphiteEditor/Graphite, http://graphite.art/volunteer/guide/graphene

- [Ф] «free, open source vector graphics editor and animation engine, available now in alpha»; «fully nondestructive editing workflow that combines layer-based compositing with node-based generative design».
- [Ф] Rust, Apache-2.0; нодовый движок Graphene; в руководстве участника есть раздел о миграциях документов.
- [О] Ближайший прецедент для вопроса «слои и ноды»: панель слоёв как представление нодового графа. Проект в альфе, поэтому это прецедент подхода, а не доказательство зрелости. Изучить в Э5 устройство миграций документов и поведение больших графов.

### O20. Material Maker
Статус: **Новое**. Источники: https://www.materialmaker.org/, https://github.com/rodzill4/material-maker

- [Ф] Open source (MIT), на Godot, более 200 нод. Новые ноды создаются группировкой существующих или написанием GLSL. Экспорт PBR в Godot, Unity и Unreal; последний релиз 1.7.
- [О] Прецедент генерации одного шейдера из цепочки нод (гипотеза H2) и пользовательских нод на языке шейдеров.

### O21. TouchDesigner
Статус: **Новое**. Источники: https://docs.derivative.ca/Operator_Family, https://derivative.ca/UserGuide/Cook

- [Ф] Операторы разделены на семейства по типу данных (COMP, TOP, CHOP, SOP, MAT, DAT и др.).
- [Ф] Страница Cook: «…will cook a node only when it needs to - it doesn't cook every node every frame». Потребность определяют видимые вьюеры, панели и выходы.
- [О] Прецедент pull-модели «вычисляется только то, что нужно» (T3, T4) в продукте реального времени.

### O22. Houdini Copernicus
Статус: **Новое**. Источники: https://www.sidefx.com/docs/houdini/news/20_5/copernicus.html, http://www.sidefx.com/docs/houdini/nodes/cop/opencl.html

- [Ф] «2D and 3D GPU image processing framework». Провод несёт либо слой изображения, либо геометрию; результаты экспортируются как изображения или volumes; контекст совместим с SOPs. Появился как BETA в Houdini 20.5.
- [Ф] Документация OpenCL COP подчёркивает: все вычисления COP важно держать на GPU.
- [О] Прецедент типизированных проводов между доменами и GPU-резидентности промежуточных данных.

### O23. Substance 3D Designer
Статус: **Новое**. Источники: https://helpx.adobe.com/substance-3d-designer/function-graphs.html, https://experienceleague.adobe.com/en/docs/substance-3d-designer/using/substance-function-graphs/fx-maps/fxmaps

- [Ф] Function graphs — отдельный вид графа для значений. FX-Map — «special type of graph, known as a Markov Chain… repeatedly replicating and subdividing an image». Pixel Processor исполняет функциональный граф для каждого пикселя.
- [О] Прецедент для Field<T> (T2): функция точки домена отделена от материализованного изображения.

### O24. Blender Geometry Nodes
Статус: **Новое**. Источники:
- https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html
- https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/repeat_zone.html
- https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
- https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/for_each_geometry_zone.html

Факты и выводы:
- [Ф] «Fundamentally, a field is a function… calculated many times with different input data.»
- [Ф] Зоны: Repeat, Simulation («result of one frame to influence the next one»), For Each Geometry Element. Актуальный мануал — 5.2 LTS.
- [О] Прецедент для правила «циклы только внутри явных зон» (T8) и для полей как ленивых функций (T2).

## 7. Не перепроверено в сессии 2

- Реестр GPT: S02 (QRhi), S06 (Tauri), S07–S09 (Wasmtime), S10 (OIIO), S13 (glTF 2.0), S17 (Pearson, 1993), S19 (Witkin и Kass, 1991), S21 (Sanderson и др., 2006). Приняты как есть.
- Ссылки снимка `00_PRE_GPT_POSITION.md`: Luau sandbox, Wasmtime (прерывание, Store, безопасность), Salsa, «Build Systems à la Carte» (ICFP 2018), Blender implicit sharing, атрибуты Houdini, обязательства Qt LGPL.
- [О] Научные публикации устаревают мало. Tauri, OIIO и Wasmtime нужно перепроверить перед выбором стека.

## 8. Замечания к реестру и документам GPT

1. TECHNOLOGY_COMPARISON.md указывает диапазон «S01–S19», но цитирует S20; в SOURCES.md 21 запись (S01–S21). Исправление: обновить диапазон. Если в `tools/validate_docs.py` нет проверки ссылок Sxx, добавить её.
2. S18: «disclosure» заменить на атрибуцию; добавить запрет «exposes the APIs» и связать его с риском UI-API плагинов.
3. S01 и S20: отметить, что 6.12 — LTS (30.09.2026), сохранив осторожную формулировку о бесплатной поддержке.
4. S11: актуальная линия OCIO — 2.6.
5. S16 верен. Дополнить требованиями KosmicKrisp: macOS 26+, Metal 4, только Apple Silicon.
6. Пробелы, которые GPT сам отметил, здесь закрыты частично: geometry kernels (Manifold, CGAL), векторный рендеринг (Vello), языки шейдеров (Slang, WGSL, webgpu.h). Text shaping и runtimes скриптов остаются открытыми.

[О] Общая оценка реестра GPT: честные границы доказательств, явные пометки excerpt, выдуманных результатов нет. Найденные проблемы — оформление и дрейф версий, а не искажение фактов.

## 9. Открытые вопросы по источникам

- QS1. Поддержка SHADER_F64 по бэкендам wgpu, особенно Metal.
- QS2. Объём LTS-обновлений Qt 6.12 для пользователей LGPL.
- QS3. Стала ли free-threaded сборка Python сборкой по умолчанию в 3.15.
- QS4. Трактовка «exposes the APIs» в лицензии Slint для UI плагинов (юридическая проверка).
- QS5. Дата релиза MaterialX 1.39.5 и лицензия по файлу LICENSE.
- QS6. Год conformance KosmicKrisp в посте LunarG (2025 или 2026).
- QS7. Синхронность egui-wgpu и egui 0.37 (changelog против docs.rs).

## 10. Источники для D4 (сессия 6, проверка 2026-11-21)

- Метод тот же, что в разделе 0: web-поиск и загрузка страниц первоисточников. Ничего не собиралось и не запускалось.
- O29 дополняет O15, не заменяя его.

### O25. OpenFX: регион интереса
Статус: **Новое**. Источники:
- https://openfx.readthedocs.io/en/latest/Reference/api/file/ofxImageEffect_8h.html (документация OpenFX 1.5.1)
- https://openfx.readthedocs.io/en/latest/Reference/ofxProcessingArch.html
- https://github.com/AcademySoftwareFoundation/openfx/blob/main/include/ofxImageEffect.h

- [Ф] kOfxImageEffectActionGetRegionsOfInterest: «This action allows a host to ask an effect, given a region I want to render, what region do you need from each of your input clips. In that way, depending on the host architecture, a host can fetch the minimal amount of the image needed as input.» По умолчанию RoI равен запрошенному региону.
- [Ф] Region of definition — «the rectangular section of the 2D image plane that it is capable of filling». Архитектура описана как бесконечная 2D-плоскость, на которой заполняются пиксели.
- [О] Прецедент для D4: footprint объявляет нода, регион вычисляет хост.

### O26. Halide (PLDI 2013)
Статус: **Новое**. Источники:
- J. Ragan-Kelley, C. Barnes, A. Adams, S. Paris, F. Durand, S. Amarasinghe. «Halide: A Language and Compiler for Optimizing Parallelism, Locality, and Recomputation in Image Processing Pipelines». PLDI 2013, DOI 10.1145/2491956.2462176. PDF: https://people.csail.mit.edu/jrk/halide-pldi13.pdf
- Обзор: Communications of the ACM, январь 2018, https://cacm.acm.org/magazines/2018/1/223877-halide/fulltext

- [Ф] Конвейеры состоят из «large graphs of different stencil stages, as well as complex reductions, and stages with global or data-dependent access patterns».
- [Ф] Редукция задаётся начальной функцией и рекурсивной функцией редукции; «Unlike a pure function, the meaning of a reduction depends on the order in which the reduction function is applied».
- [Ф] CACM 2018: язык «separates the algorithm from its schedule».
- Не удалось подтвердить цитатой в этой сессии описание bounds inference. Выводы D4 на нём не строятся.
- [О] Классы «стенсил / редукция / глобальный доступ» совпадают с классификацией D4.

### O27. Параллельная редукция на GPU
Статус: **Новое**. Источник: M. Harris, «Optimizing Parallel Reduction in CUDA», NVIDIA Developer Technology (слайды, дата не указана), https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf

- [Ф] «Tree-based approach used within each thread block»; «But how do we communicate partial results between thread blocks?»; раздел «Problem: Global Synchronization».
- Не удалось подтвердить дословно продолжение слайда с решением (фрагмент обрезан). [О] Без глобальной синхронизации внутри одного запуска редукция требует нескольких проходов или атомарных операций.
- [О] Документ про CUDA; перенос на WGSL/wgpu — аналогия, а не проверенный факт.

### O28. Pearson, модель Gray–Scott
Статус: **Подтверждено** библиографически (S17 GPT). Источники:
- J. E. Pearson, «Complex Patterns in a Simple System», Science 261(5118), 189–192, 9 июля 1993, DOI 10.1126/science.261.5118.189
- Препринт arXiv:patt-sol/9304003 (17.04.1993): https://arxiv.org/abs/patt-sol/9304003

- [Ф] Аннотация: «Numerical simulations of a simple reaction--diffusion model reveal a surprising variety of irregular spatio--temporal patterns. These patterns arise in response to finite--amplitude perturbations.»
- Полный текст в этой сессии не читался.

### O29. OpenSubdiv: статическая топология (дополняет O15)
Статус: **Новое**. Источники: https://graphics.pixar.com/opensubdiv/docs/intro.html, https://graphics.pixar.com/opensubdiv/docs/mod_notes.html (документация 3.7.0).

- [Ф] «This code path is optimized for drawing deforming surfaces with static topology at interactive framerates.»
- [Ф] Хорошие сетки для subdivision «consist primarily of regular faces (quads for Catmull-Clark, tris for Loop)».
- [О] Быстрый путь рассчитан на статическую топологию; при её смене анализ повторяется. Для D4 смена топологии — отдельный класс нагрузки.
- Документация показывает версию 3.7.0, а O15 фиксирует релиз 3.8.0; на выводы это не влияет.

### O30. Blender: Full Frame Compositor (#88150)
Статус: **Новое**. Источники:
- https://projects.blender.org/blender/blender/issues/88150 (Manuel Castilla, 09.05.2021; задача закрыта)
- https://archive.blender.org/developer/differential/0011/0011686/index.html (D11686, 2021)

- [Ф] «Current compositor implementation is tile-based having the priority of displaying first tiles as quickly as possible. Memory usage can be very high for complex/long trees as buffers are kept from tree execution start to finish.»
- [Ф] Цель: «convert current tiled/per-pixel implementation to full-frame»; «All nodes/operations are buffered, creating buffers on first read and freeing them as soon as all their readers have finished.»
- [Ф] D11686: full-frame Mix node «2.3x faster than tiled fallback on average». Это замер разработчиков Blender, не наш.

### O31. Blender 4.2 LTS: композитор
Статус: **Новое**. Источник: https://developer.blender.org/docs/release_notes/4.2/compositor/

- [Ф] «The render compositor CPU backend has also been rewritten to improve performance, often making it several times faster than before. There are some changes in behavior. These were made so that the final render and 3D viewport compositor work consistently, and can run efficiently on the GPU.»
- [Ф] Композитинг финального рендера может выполняться на GPU; ожидается, что CPU и GPU дают одинаковый результат «with minimal differences between devices».
- Не удалось подтвердить в этой сессии, что тайловый режим удалён именно в 4.2: в примечаниях к выпуску это не найдено.

### Не удалось подтвердить в сессии 6
- Перечень типов atomics в WGSL и наличие атомарного min/max для f32. Страница спецификации W3C (Candidate Recommendation Draft от 06.11.2026) загружена, но нужный фрагмент не извлечён.
- Условие устойчивости явной схемы для диффузии. В D4 не используется; отложено до D8.

## 11. Источники для D5 (сессия 7, проверка 2026-11-21)

- Метод тот же, что в разделе 0, но страницы целиком не загружались: цитаты взяты из выдержек web-поиска по первоисточникам. Ничего не собиралось и не запускалось.
- O35 дополняет O22, O36 — O30–O31, O37 — O23.

### O32. OpenFX: системы координат и пространственные параметры
Статус: **Новое**. Источники (документация OpenFX 1.5.1, Academy Software Foundation; даты страниц не указаны):
- https://openfx.readthedocs.io/en/latest/Reference/ofxCoordSystem.html
- https://openfx.readthedocs.io/en/latest/Reference/ofxParameter.html
- https://openfx.readthedocs.io/en/main/Reference/api/file/ofxParam_8h.html
- https://openfx.readthedocs.io/en/main/Reference/api/file/ofxImageEffect_8h.html
- https://openfx.readthedocs.io/en/latest/Guide/ofxExample5_Circle.html

- [Ф] «OFX has three spatial coordinate systems»: Canonical («the idealised image plane»), Pixel («coordinates in addressable pixels») и Normalised Canonical («resolution independent description of parameters»).
- [Ф] Canonical — «a coordinate system of square unscaled pixels»; «parameter values are expressed in them».
- [Ф] Перевод в пиксели: X' = (X * SX)/PAR, Y' = Y * SY * FS, где SX и SY берутся из kOfxImageEffectPropRenderScale.
- [Ф] Spatial-параметры: «The host and plug-in get and set values in this coordinate system. Scaling to Pixel Coordinate is the responsibility of the effect.» Типы: kOfxParamDoubleTypeX (размер), kOfxParamDoubleTypeXAbsolute (позиция), а также XY и XYAbsolute.
- [Ф] «The original OFX API only specified normalised parameters, this proved to be somewhat more of a problem than expected. With the 1.2 version of the API, spatial parameters were introduced.» Нормализованная система «being deprecated».
- [Ф] kOfxImageEffectPropRenderScale: «The proxy render scale currently being applied. This should be applied to any spatial parameters to position them correctly.»
- [Ф] kOfxImageEffectPropThumbnailRender — необязательное свойство, «if the host considers this render a “thumbnail”».

### O33. After Effects C++ SDK: downsample
Статус: **Новое**. Источники:
- https://ae-plugins.docsforadobe.dev/effect-basics/PF_InData
- https://ae-plugins.docsforadobe.dev/effect-details/pixel-aspect-ratio
- After Effects CC 2015 SDK Guide (Adobe), раздел PF_InData: та же формулировка в копии на scribd.com.

- [Ф] downsample_x/y: «Effects need the downsampling factors to interpret scalar parameters representing pixel distances in the image (like sliders). For example, a blur of 4 pixels should be interpreted as a blur of 2 pixels if the downsample factor is 1/2 in each direction».
- [Ф] «Point parameters are given to the effect scaled for downsample factor and pixel aspect ratio»; «any slider which defines a size in pixels will be a problem when the image is rendered downsampled».
- Ограничение: docsforadobe — сайт сообщества, воспроизводящий SDK Guide. Текущий официальный PDF Adobe не открывался.

### O34. Nuke: proxy mode
Статус: **Новое**. Источники (Foundry Learn; текущая документация Nuke 17.x и Nuke 11.2):
- https://learn.foundry.com/nuke/content/getting_started/managing_scripts/managing_scripts.html
- https://learn.foundry.com/nuke/11.2/content/getting_started/managing_scripts/proxy_mode.html

- [Ф] «In the full-size mode, images are read in exactly as they are on the disk, and all positions are in actual pixels in these images.»
- [Ф] «In proxy mode, instead, a proxy scale factor is used. All images and all x/y positions are scaled by this factor. This produces the same (or at least very similar) composite at a different scale.»
- [?] Как пересчитываются скалярные размеры (радиус Blur и подобные), в выдержках не сказано.

### O35. Houdini Copernicus: Units у Blur и пространства
Статус: **Новое**, дополняет O22. Источники (SideFX, документация Houdini 22.0 и 20.5):
- https://www.sidefx.com/docs/houdini/nodes/cop/blur.html
- https://www.sidefx.com/docs/houdini/copernicus/spaces.html
- https://www.sidefx.com/docs/houdini20.5/nodes/cop2/blur.html (старая сеть COP2)

- [Ф] Blur, Units: «Image (default) Sets the blur radius to use units of the Image Space»; «Pixels Sets the blur radius to use units of the number of pixels»; в 22.0 есть также Local.
- [Ф] Пространства: Buffer, Pixel, Texture, Image, Local, World. Image «Maps from -1 through 1 across the display window, which scales the image to fit to preserve the pixel aspect ratio».
- [Ф] «The preview thumbnail for a COP node displays the output in a -1 to 1 window.»
- [Ф] «Copernicus values are in their natural space (a requirement for HDR) instead of being normalized.»
- [Ф] COP2 Blur, Units: «UV Coords Values are expressed between 0 and 1 ... This is resolution independent.»; «Pixels The blur is expressed in pixels.»

### O36. Blender: опция Relative у Blur в композиторе
Статус: **Новое**, дополняет O30–O31. Источники:
- https://docs.blender.org/manual/en/4.0/compositing/types/filter/blur/blur.html (обновлено 15.01.2024)
- https://docs.blender.org/api/4.5/bpy.types.CompositorNodeBlur.html
- https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/blur.html (5.2 LTS, обновлено 26.10.2026)

- [Ф] 4.0: «Relative Percentage Value of the blur radius relative to the image size»; «X, Y Values set the ellipsoid radius in numbers of pixels».
- [Ф] API 4.5: use_relative «Use relative (percent) values to define blur radius. (Deprecated: Unused.)»; size_x «(Deprecated: Use Size input instead.)».
- [Ф] В руководстве 5.2 LTS у Blur нет опции Relative.
- [?] Единицы входа Size в 5.x и причина отказа от Relative не найдены.

### O37. Substance 3D Designer: наследование разрешения
Статус: **Новое**, дополняет O23. Источники (Adobe):
- https://helpx.adobe.com/substance-3d-designer/substance-compositing-graphs/inheritance-in-substance-compositing-graphs.html (обновлено 26.02.2026)
- https://helpx.adobe.com/substance-3d-designer/best-practices/performance-optimization-guidelines.html
- https://helpx.adobe.com/substance-3d-designer/using/export.html

- [Ф] Методы наследования: «Absolute», «Relative to input», «Relative to parent». Base parameters: «Output Size, Output Format (i.e., bitdepth), Pixel Size, Pixel Ratio, Tiling Mode, Random Seed».
- [Ф] Рекомендация по производительности: Uniform Color ставить в «Absolute [16px x 16px]», а следующую ноду — в Relative to Parent.
- [Ф] Предупреждение при публикации «Non-Relative to parent x1 output size parameter» означает, что «it won't be possible to generate textures from this package at a resolution of your choosing».
- [?] Единицы Intensity у Blur HQ и смысл Pixel Size не проверены.

### O38. Линдеберг: дискретное масштабное пространство
Статус: **Новое**. Источники:
- T. Lindeberg, «Scale-Space for Discrete Signals», IEEE TPAMI, vol. 12, no. 3, 1990, pp. 234–254, DOI 10.1109/34.49051: https://www.computer.org/csdl/journal/tp/1990/03/i0234/13rRUx0xPnO
- T. Lindeberg, «Discrete approximations of Gaussian smoothing and Gaussian derivatives», arXiv:2311.11317v7, 13.05.2024: https://arxiv.org/pdf/2311.11317v7

- [Ф] 1990: «Special attention is given to discretization effects, which occur when results from the continuous scale-space theory are to be implemented computationally.»
- [Ф] 2024: дискретный аналог гауссиана «has the best theoretical properties»; «For scale values when the standard deviation of the continuous Gaussian kernel is above 0.75 or 1, the sampled Gaussian kernel does also have very good properties, and leads to very good approximations of the corresponding fully continuous results.»
- [Ф] 2024: у нормированного дискретизированного гауссиана на малых масштабах дисперсия «substantially smaller» дисперсии непрерывного ядра.

### Не удалось подтвердить в сессии 7
- Единицы Size у Blur в Blender 5.x и причина отказа от Relative.
- Единицы Intensity у Blur HQ и смысл Pixel Size в Substance 3D Designer.
- Пересчёт скалярных размеров в proxy mode Nuke.
- Текущая официальная версия After Effects SDK Guide: использованы сайт сообщества и текст 2015 года.

## 12. Источники для D6 (сессия 8, проверка 2026-11-21)

- Метод: web-поиск инструментом Notion по официальным сайтам и трекерам. Страницы целиком не загружались; цитаты взяты из выдержек поиска.

### O39. Tauri 2: версии WebView
Статус: **Новое**. Источник:
- https://v2.tauri.app/reference/webview-versions

- [Ф] «Tauri uses WebView2 which is based on Microsoft Edge and therefore Chromium. WebView2 can update itself»; WebView2 «is supported on Windows 7 and newer and comes preinstalled on Windows 11. On versions older than Windows 11 the installer generated by Tauri takes care of ensuring WebView2 is installed».
- [Ф] Для Android: «Tauri does not bundle a WebView with your app».
- [?] Разделы о macOS (WKWebView) и Linux (WebKitGTK) в выдержке не видны. Использование системного WebView подтверждают реестр GPT (S06) и вторичный источник из O42.

### O40. Tauri 2.0: переписанный IPC
Статус: **Новое**. Источник:
- https://v2.tauri.app/blog/tauri-20 (дата публикации в выдержке не видна)

- [Ф] «Previously all IPC payloads were json serialized and deserialized which caused an overhead. This was noticeable once more than a few kilobytes were transferred»; новая система поддерживает «Raw Requests», можно «use raw bytes directly».
- [Ф] Для чтения файлов в WebView по-прежнему рекомендуется convertFileSrc.
- [Ф] «Added multiwebview support behind the unstable feature flag».

### O41. Tauri 2: модель процессов, команды, каналы, события
Статус: **Новое**. Источники:
- https://v2.tauri.app/concept/process-model
- https://v2.tauri.app/concept/inter-process-communication
- https://v2.tauri.app/develop/calling-frontend
- https://v2.tauri.app/reference/javascript/api/namespacecore

- [Ф] Core-процесс «routes all Inter-Process Communication»; IPC — «Asynchronous Message Passing»; передача сообщений названа «a safer technique than shared memory».
- [Ф] События: «not designed for low latency or high throughput situations»; payload событий — «always JSON strings».
- [Ф] Channel: «Raw byte payloads are delivered to the frontend as an ArrayBuffer»; сообщения доставляются в порядке отправки.
- [?] Число копий на пути Rust → WebView в документации не указано; zero-copy не обещается.

### O42. WebGPU в системных WebView
Статус: **Новое**; данные противоречивы. Источники:
- WebKit, «WebKit Features in Safari 26.0», 15.09.2025: https://webkit.org/blog/17333/webkit-features-in-safari-26-0 — в Safari 26.0 появился WebGPU.
- WebKit Bugzilla #284621 (2024-12-13, RESOLVED INVALID): https://bugs.webkit.org/show_bug.cgi?id=284621 — при включённом флаге WebGPU в Safari на iOS 18.2 «WKWebView still doesn't have GPU access».
- Сторонний проект kaya-go, заметка от 2026-05-03: https://github.com/kaya-go/kaya/blob/main/specs/2026-05-03-webgpu-unavailable-in-tauri-webview.md — «navigator.gpu is undefined inside WKWebView (macOS) and WebKitGTK (Linux)»; про WebView2: «should work… Untested». Вторичный источник; версии ОС в выдержке не указаны.
- Tauri, issue #6381 «WebGPU support?»: https://github.com/tauri-apps/tauri/issues/6381 — закрыт как «not planned».
- caniwebview.com, WebGPU: https://caniwebview.com/features/web-feature-webgpu — данные по WKWebView в выдержке не читаются.

- [О] WebGPU в Safari не доказывает WebGPU во встраиваемом WKWebView и тем более общего с нативным wgpu GPU-хэндла.
- [?] Статус WebGPU во WKWebView (macOS 26) и WebKitGTK на ноябрь 2026 подтвердить не удалось.

### O43. egui-wgpu: свой wgpu-рендер и общее устройство
Статус: **Новое**; дополняет O10. Источники:
- https://docs.rs/egui-wgpu/latest/egui_wgpu/trait.CallbackTrait.html
- https://docs.rs/egui-wgpu/latest/egui_wgpu/struct.RenderState.html
- https://github.com/emilk/egui/blob/main/crates/egui-wgpu/src/renderer.rs

- [Ф] «You can use this to do custom wgpu rendering in an egui app. Implement CallbackTrait and call Callback::new_paint_callback».
- [Ф] RenderState содержит adapter, available_adapters, instance, device, queue, target_format, renderer; в примерах его берут из CreationContext eframe (wgpu_render_state).
- [Ф] Сигнатуры в docs.rs (latest) ссылаются на epaint 0.37.0 и wgpu 30.0.0.
- [?] Совместный доступ ядра к тому же устройству из рабочих потоков и поведение при device lost не проверялись.

### Не удалось подтвердить в сессии 8
- Разделы macOS и Linux страницы версий WebView Tauri (O39).
- Статус WebGPU во WKWebView и WebKitGTK на ноябрь 2026 (O42).
- Число копий на пути Rust → WebView в Tauri 2 (O41).
- Зрелость крейтов Rust для EXR, булевых операций и субдивизии.
- Дату публикации блога Tauri 2.0 (O40).

## 13. Источники для D7 (сессия 9, IN PROGRESS)

- Checkpoint 0: новых источников нет. Нумерация продолжится с O44; последний ID перед работой — O43 (проверено по blob c8875a3).
- Лимит HANDOFF: не более пяти новых источников для D7.
- CP1: новых источников нет. Таблица D7.A опирается на текст GPT (0cc3eb8) и на уже проверенный O32 (виды параметров OpenFX XY и XYAbsolute), повторно источник не открывался.
- Промежуточный checkpoint (PROGRESS v9.3): добавлены O44–O46. Израсходовано 3 из 5; в запасе O47–O48 — только для спорного пункта. По Blender актуальных данных нет, см. ниже.
- CP2-A (сессия 10, PROGRESS v9.4): новых источников нет. Раздел D7.C рецензии опирается на O32 и O44–O46; повторно они не открывались. Резерв O47–O48 не использован.
- CP2-B (сессия 10, PROGRESS v9.5): новых источников нет. Раздел D7.D опирается на O32 (OpenFX), O35 (Copernicus Image space) и O38 (Lindeberg); повторно не открывались. Соглашения об UV origin в форматах обмена не проверялись, в D7.D помечены [?]. Итог CP2: 0 новых источников, резерв O47–O48 не использован.
- CP3 (сессия 11, PROGRESS v9.6): новых источников нет. Синтез D7.E опирается на уже записанные O44–O46, а через D7.C и D7.D — на O32, O35 и O38; повторно они не открывались. Резерв O47–O48 не использован.

### O44. OpenUSD: роли типов значений Sdf
Статус: **Новое**. Источники:
- https://openusd.org/docs/api/_usd__page__datatypes.html (дев-версия: https://openusd.org/dev/api/_usd__page__datatypes.html)
- https://openusd.org/25.11/api/usd_2sdf_2types_8h_source.html
- https://github.com/PixarAnimationStudios/OpenUSD/blob/release/pxr/usd/sdf/schema.cpp

- [Ф] «Value types may also be specified by one of a set of special type names. These names correspond to the basic data types listed above but provide extra semantics about how the data should be interpreted.»
- [Ф] Таблица ролей: point3d/point3f/point3h — Vec3 с ролью Point, «transform as a position»; normal3* — роль Normal, «transform as a normal»; vector3* — роль Vector, «transform as a direction».
- [Ф] Токены ролей SDF_VALUE_ROLE_NAME_TOKENS: Point, Normal, Vector, Color, Frame и другие. В schema.cpp есть также роль TextureCoordinate.
- [Ф] schema.cpp: point3f и vector3f объявлены с DefaultUnit(length) и Role(point) или Role(vector). Роль и единица задаются поверх одного хранения.
- [Ф] Базовый float2 (GfVec2f, «vector of 2 floats») роли не несёт.
- [?] Строку texCoord2f в выдержке не видел.

### O45. Houdini 22.0, VEX: метаданные типа атрибута
Статус: **Новое**. Источники:
- https://www.sidefx.com/docs/houdini/vex/attribtypeinfo_suite.html
- https://www.sidefx.com/docs/houdini/vex/functions/setattribtypeinfo.html

- [Ф] «Houdini's geometry attributes have a bit of metadata specifying whether the data in the attribute represents some kind of transformation (for example, a position or rotation), and if so, whether/how it should be modified when the geometry itself is transformed.»
- [Ф] Значения: "point" — «Apply scales, rotations, and transformations»; "vector" — «Apply scales and rotations, but not transformations»; "normal" — «Apply rotations, apply scales with inverse-transpose»; "color" — «Don't transform»; "texturecoord" — «Don't transform, and try to preserve seams when interpolating»; "none" — «Don't transform».
- [Ф] Тот же текст есть в документации 20.0 и 20.5.
- [О] Это метаданные поверх общего float-хранения. Они управляют трансформацией, но арифметику не запрещают.

### O46. Rust euclid 0.22.14: типизированные точки, векторы и размеры
Статус: **Новое**. Источники:
- https://docs.rs/euclid/latest/euclid/ (крейт 0.22.14)
- https://docs.rs/euclid/0.22.14/euclid/struct.Point2D.html, а также страницы Vector2D и Size2D

- [Ф] «A collection of strongly typed math tools for computer graphics with an inclination towards 2d graphics and layout. All types are generic over the scalar type… and tagged with a generic Unit parameter which is useful to prevent mixing values from different spaces. For example it should not be legal to translate a screen-space position by a world-space vector…»
- [Ф] Тег по умолчанию — UnknownUnit; есть from_untyped и to_untyped.
- [Ф] Отдельные структуры: «A 2d Point tagged with a unit», «A 2d Vector tagged with a unit», «A 2d size tagged with a unit».
- [Ф] Point2D реализует Sub<Vector2D> и Sub<Size2D>: точка минус размер даёт точку. Это прагматичное послабление.
- [Ф] Vector2D::to_point («Cast this vector into a point. Equivalent to adding this vector to the origin»), Size2D::to_vector, Vector2D::extend(z) → Vector3D.
- [?] Что Point + Point не реализовано, в выдержке явно не подтверждено.

### Не удалось подтвердить в сессии 9
- Текущую размерность и подтипы сокета Vector в Blender. Поиск нашёл только устаревшие API: 2.64 — NodeSocketVectorXYZ с подтипами VECTOR_NONE, VECTOR_TRANSLATION, VECTOR_DIRECTION, VECTOR_VELOCITY, VECTOR_ACCELERATION, VECTOR_EULER, VECTOR_XYZ (http://www.blender.org/documentation/blender_python_api_2_64_release/bpy.types.NodeSocketVectorXYZ.html); 2.93 — NodeSocketVector, «3D vector socket of a node» (https://docs.blender.org/api/2.93/bpy.types.NodeSocketVector.html). Задача руководства https://projects.blender.org/blender/blender-manual/issues/105379 упоминает «Attributes: Add 4D float vector type». Страница текущего API https://docs.blender.org/api/current/bpy.types.NodeTreeInterfaceSocketVector.html не загрузилась, повторно не запрашивал. Как источник в реестр не вношу.
- Строку texCoord2f в таблице OpenUSD (O44) и отсутствие Point + Point в euclid (O46).

<!-- EOF OPUS_SOURCES (O01–O46; раздел 13 IN PROGRESS) -->
