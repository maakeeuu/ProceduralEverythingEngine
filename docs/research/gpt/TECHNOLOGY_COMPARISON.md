# Сравнение технологических вариантов

Дата проверки источников: 2026-11-21. Статус: исследовательская оценка. Ни один стек не утверждён и не собран. Производительность ниже — ожидаемые свойства/издержки, **не результаты измерений**. Источники S01–S19: [SOURCES](SOURCES.md).

## Критерии до выбора
Общая корректность typed graphs и междоменных контрактов; время до рабочей вертикали; GPU residency/throughput/latency; стоимость UI fit/accessibility; доступные навыки; геометрические/изобразительные зависимости; лицензии; supply-chain и sandbox; поддержка Win/Linux/macOS; стоимость сопровождения и migration. Не использовать суммарный балл с выдуманными весами: platforms/license/hardware пока OPEN.

## A — лучший баланс как проверяемая гипотеза

**Стек-кандидат:** Rust core, egui/eframe native shell, egui-wgpu + wgpu, WGSL, CPU worker pool (Rayon-кандидат после spike), Cargo workspace. Shared GPU device там, где public интеграция eframe это разрешает; версии egui/wgpu подбирать совместно. Headless domain modules независимы от UI. Scripting сначала visual graphs, затем Wasmtime; Python automation отдельно по потребности. C ABI/out-of-process для native SDK позднее.

**Архитектура:** document/commands → typed graph → demand executor → domain kernels → resource broker → wgpu viewport. UI и compute на одной native стороне без обязательной IPC-копии каждого preview. CPU image buffers и editable mesh отдельно от GPU draw resources. Начальный mesh — arrays + indexed triangles + attributes; general topology и subdivision позже через адаптер. OIIO/OCIO/OpenSubdiv возможны через изолированный FFI или converter tool, но не подключать весь VFX ecosystem ради одной картинки.

**Преимущества (оценка):** один основной язык; memory-safety в safe Rust; mature cross-API abstraction вместо собственного Vulkan/Metal layer; нативный preview без обязательного webview bridge. egui даёт быстрый inspector/editor tooling, custom painting и доступ к wgpu [S03–S05].

**Недостатки:** продуктовый polished UI, docking/node UX, текст/IME/accessibility требуют собственной работы; immediate mode не гарантирует ни лёгкость сложного UX, ни малый idle CPU. Geometry/VFX экосистема часто C++, FFI остаётся. wgpu feature set не равен максимуму Vulkan/Metal; нельзя заявлять compute на downlevel WebGL/GLES только по слову «поддерживается».

**Performance:** высокий потенциал CPU и portable GPU, меньше обязательных process transfers; реальная скорость определяется kernels, formats, precision, memory и scheduling. UI requests demand-driven, не перерисовка дорогого графа каждый frame.

**Сложность/поддержка:** средняя относительно B; version churn Rust UI/GPU, shader validation и ffi review регулярны. Не считать memory safety гарантией правильных алгоритмов или безопасных host APIs. Cross-platform статус API не доказывает готовый application packaging.

**Расширения:** strong typed internal registry; Wasm для bounded compute с ограничениями, native C ABI для trusted accelerated kernels. Новые типы требуют согласованной сериализации/inspectors, не magic dynamic Rust structs.

**Горизонт:** может вырасти в серьёзный продукт, если P2/P3 подтвердят UX и GPU; при провале UI возможна замена оболочки при сохранении headless core, но это не бесплатно.

## B — максимальный контроль над производительностью

**Стек-кандидат:** C++20 baseline (C++23 только по реальной потребности и toolchain matrix), Qt 6 Widgets/Quick shell после license/UI spike, CMake, low-level Vulkan backend на Windows/Linux; отдельный Metal backend либо проверенный portability driver для macOS. SPIR-V shader toolchain для Vulkan; MSL/перевод на Apple требует отдельной валидации. CPU task system выбирается по нагрузке; oneTBB кандидат, не принятая зависимость. OIIO/OCIO/OpenSubdiv как наиболее естественные C++ интеграции; CGAL только per-package license audit [S10–S16]. Python worker для automation, Wasmtime или эквивалентный sandbox для untrusted compute.

**Архитектура:** тот же typed domain model, но renderer/resource management явнее управляет queues, allocations, barriers, staging и shader pipelines. UI integration изолирована. Не использовать QRhi private/limited-compatibility API как обещанный стабильный SDK: официально нет source/binary guarantees [S02]. Изображение Qt и Vulkan не становится zero-copy автоматически; один из первых spikes — shared-device/texture или цена copy-present.

**Преимущества (оценка):** максимальная свобода GPU profiling, advanced features и специализированной памяти; прямые интеграции со зрелыми C++ imaging/geometry пакетами; Qt — развитая desktop инфраструктура.

**Недостатки:** собственный многобэкендовый renderer и synchronization, higher memory-safety risk, packaging/dependency complexity, смешение Qt graphics и renderer. C++ не делает poorly batched graph быстрее Rust. Требуется опыт graphics engineer и performance tooling.

**Особый текущий риск:** официальный README MoltenVK при проверке содержит deprecation/best-effort notice и рекомендацию другого пути для Apple Silicon [S16]. Поэтому не предлагать «Vulkan + MoltenVK решает macOS навсегда». Закреплённый релиз и конкретный SDK/driver надо проверять отдельно; изменение README не эквивалентно испытанию нового драйвера.

**Performance:** самый высокий контроль, не доказанная самая высокая скорость. Ветка оправдана только если portable API не даёт критическую функцию либо profiling показывает реальный bottleneck, и команда способна сопровождать backend.

**Сложность/поддержка:** высокая/очень высокая. Qt modules лицензируются неодинаково; например Quick 3D не считать автоматически LGPL [S01]. Лицензионное решение до глубокого внедрения. Поддержка macOS/Windows/Linux — отдельный постоянный бюджет.

**Расширения:** C ABI + opaque handles и versioned structs; не экспортировать сырой C++ ABI/STL types как вечный SDK. Native in-process trusted; isolated worker для стороннего кода. Быстрая нативная DLL не sandbox.

**Горизонт:** долгосрочно сильный вариант для graphics-команды, но непропорционально дорогой старт для небольшого R&D без подтверждённых требований к low-level API.

## C — реалистичный для небольшой AI-assisted команды

**Стек-кандидат:** Tauri 2 shell + TypeScript/React frontend + Rust headless core; web node canvas library оценивается отдельно (API/license/keyboard/large graph), native CPU вычисления сначала; 2D browser canvas и Three.js-кандидат для mesh display. Tauri/Cargo + frontend package tooling. GPU acceleration расширяется только после proof транспортного пути; не обещать native wgpu textures напрямую в OS WebView.

**Архитектура:** frontend владеет view state, backend — graph/document authority, validation, CPU domain kernels, jobs/cache, persistence. IPC — commands/handles/diagnostics, не полный RGBA buffer через JSON на каждый mousemove. Малые preview buffers допустимы для proof с измерением; binary protocol/локальная asset-схема/shared memory — предмет P4. Mesh и CPU outputs version-tagged. Native GPU и WebGPU/WebGL — отдельные resource/device domains, нельзя предполагать общий GPU handle.

**Преимущества (оценка):** быстрый поиск качественного node-editor UX, CSS design tokens, web layout/accessibility tooling, большой пул разработчиков и быстрые UI итерации. Rust core сохраняет серьёзный computational потенциал; не генерация на JavaScript main thread.

**Недостатки:** два стека/тестовых контура, IPC и копии, cross-platform различия WebView и GPU capabilities. Tauri использует системный WebView [S06]; capabilities ограничивают frontend доступ к host, но не sandbox malicious Rust plugin. Меньший размер bundle относительно bundled browser не означает меньший рабочий RAM или одинаковое поведение всех ОС.

**Performance:** CPU core может быть сравним с A, но интерактивные большие textures/mesh и GPU resident sharing требуют доказательства. Если renderer переезжает в отдельное native окно, интеграция/UX и риски меняются; это не считать незаметной бесплатной оптимизацией.

**Сложность/поддержка:** низкая/средняя для UI при web-компетенциях, средняя/высокая для interop после GPU роста. AI assistance ускоряет routine coding, не заменяет контроль памяти, security и тестирование на железе. Не обещать минимальную сложность независимо от команды.

**Расширения:** graph/Wasm/native host в backend; frontend не получает arbitrary shell/FS. JS из скачанного project не выполнять в доверенном WebView. Tauri plugins — host code, не пользовательские безопасные procedural plugins.

**Горизонт:** серьёзный вариант, если workload подтверждает tolerable transfer costs или pipeline остаётся на одной стороне. При high-res procedural GPU продукте усложнение мостов может съесть первоначальную выгоду.

## Сопоставление без фиктивных benchmark
| Критерий | A | B | C |
|---|---|---|---|
| Основной выигрыш | Нативная общая CPU/GPU среда с меньшим backend-кодом | Максимальный низкоуровневый контроль и C++ экосистема | Скорость UI разработки для web-команды |
| Главная цена | UI polish + экосистема/FFI | Renderer/backends + safety + поддержка | IPC/GPU ownership + два стека |
| GPU path | wgpu native Vulkan/Metal/DX12, per-feature checks | Явные Vulkan/Metal или проверенный portability path | CPU-first; web/native GPU bridge OPEN |
| CPU | Native Rust, reference + parallel kernels | Native C++, explicit SIMD/tasks | Native Rust, не JS main thread |
| UI | egui/eframe, custom canvas/inspectors | Qt, сложный renderer interop | Web UI/DOM/canvas + Tauri |
| Изображения | Rust базовый путь; OIIO/OCIO adapter позже | OIIO/OCIO естественнее в C++ | Rust backend + browser display, color consistency audit |
| Geometry | Indexed mesh + attributes, C++ bridge при нужде | C++ libraries, package/license selection | Тот же Rust core, mesh upload cost |
| Materials | Sampled PBR + WGSL; MaterialX subset исследовать | Собственный shader path + MaterialX adapter | Browser PBR subset; не полная MaterialX fidelity |
| Test/build | Cargo + headless/GPU/UI fixtures | CMake + unit/sanitizers/GPU/UI | Cargo + TS tests + IPC integration + WebView E2E |
| Support risk | UI/GPU version alignment | API/driver/platform/licenses | WebView variance + IPC/security/deps |
| Team fit | Небольшая Rust/graphics команда | Опытная C++/graphics команда | Небольшая сильная web + Rust команда |

## Альтернативы не замалчиваются
Slint/Rust — retained/declarative UI кандидат, если egui не проходит UX/accessibility gates; не четвёртый утверждённый стек. Проверены backend docs и license entry [S18]: нельзя объявить весь Slint обычным MIT; есть условия royalty-free/GPL/commercial. Отдельный short UI-fit spike разумнее полного переписывания.

Electron — возможная замена системного WebView на bundled runtime для предсказуемости, но увеличивает distribution/runtime cost; не исследован достаточно для основной рекомендации. Unity/Godot как shell дали бы сцену/rendering быстрее, но требуют оценки editor UX, API/embedding, licensing и core ownership; сейчас не заявляются выбранными. Python-only scientific prototype полезен для проверки формул, но не доказательство product-scale engine.

## Версии и поддержка
Наблюдавшиеся при проверке документы: Qt public docs отображали 6.12/QRhi 6.12.0, eframe docs re-export egui-wgpu 0.37.0 и wgpu 30.0.0; OpenSubdiv introduction 3.8.0, MaterialX site 1.39.5, OCIO site 2.5.0, CGAL manual 6.2.1. Это **отображаемые версии источников**, не проверенный совместимый lockfile и не гарантия срока поддержки. Mutable latest может не соответствовать доступному стабильному toolchain/пакету; release artefacts, MSRV/toolchains, security advisories и supported platform matrix перепроверяются при spike. Qt release/support policy: [S20]. Не выбирать patch-level до сборки и dependency/license audit.

## Условная рекомендация
A проверять первым при отсутствии сильного перекоса навыков. C запускать как конкурентный transport/UI spike, если web expertise меняет стоимость. B — только при измеренном необходимости low-level функций либо подтверждённой C++ команде. До независимой оценки, experiments и решения владельца победитель не назначен.
