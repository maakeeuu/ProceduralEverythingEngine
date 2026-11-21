# Источники и границы доказательств

Дата обращения ко всем источникам: **2026-11-21**. Источники проверены через публичный web-search и, где отмечено, целевую загрузку страницы. Это не аудит исходников, не проверка сборки/лицензий юристом и не полный literature review. Даты и версии ниже — то, что показал источник при обращении; moving `latest`/`main` не закреплённый snapshot. Перед принятой зависимостью сохранить конкретный release/tag, license files и platform support evidence.

Технические ссылки Sxx в документах относятся к этому реестру. Источник подтверждает узкое утверждение о технологии; рекомендации о пригодности проекта — оценки автора. Поиск, отображающий snippet, отмечен как excerpt; полный текст научных paywall статей не заявляется прочитанным.

## UI, GPU, переносимость

### S01 — Qt Licensing
https://doc.qt.io/qt-6/licensing.html

Официальная документация Qt; прочитан расширенный excerpt. Qt имеет разные licensing routes; список отдельных GPLv3/commercial modules включает Quick 3D. Подтверждает необходимость module-level license review, не утверждение «Qt нельзя в закрытом продукте». Извлечение отображало семейство Qt 6.12. Продуктовая модель лицензирования проекта пока OPEN.

### S02 — QRhi Class
https://doc.qt.io/qt-6/qrhi.html

Целевая загрузка релевантных разделов. Заголовок отображал Qt 6.12.0. Официально QRhi/QShader/QShaderDescription имеют limited compatibility guarantees, без source/binary guarantees. Связь с GuiPrivate явно показана. Подтверждает риск привязки публичного SDK к внутреннему renderer Qt. Не измеряет стоимость Qt/Vulkan interop.

### S03 — wgpu API
https://docs.rs/wgpu/latest/wgpu/

Расширенный официальный crate-doc excerpt. Native Vulkan/Metal/DX12, отдельные OpenGL/GLES и web backends, shader inputs WGSL и feature-gated SPIR-V/GLSL. Наличие backend не означает поддержку всех функций compute/форматов на каждом устройстве. Не подтверждает качество конкретного procedural renderer.

### S04 — eframe API
https://docs.rs/eframe/latest/eframe/

Целевая загрузка usage/features/re-exports. Native/web framework; wgpu painting, accesskit feature, возможность renderer integration. Отображались re-exports egui-wgpu 0.37.0 и wgpu 30.0.0. Эти версии не приняты в lockfile; совместимость и shipped stable release ещё проверять. Наличие accessibility integration не доказывает доступность собственного node canvas.

### S05 — egui
https://github.com/emilk/egui

Целевая загрузка README: immediate-mode модель, custom painting, стабильные widget IDs, MIT OR Apache-2.0. Заявленные author goals (например 60Hz) — цели upstream, не измеренный performance нашего продукта. Toolkit не является готовым профессиональным procedural editor.

### S06 — Tauri process/security model
https://v2.tauri.app/concept/process-model/
https://v2.tauri.app/security/
https://tauri.app/security/capabilities/

Прочитаны расширенные excerpts официальных docs. Core process/Rust и system WebView разделены IPC; capabilities ограничивают frontend→host доступ. Rust/core plugins имеют системный доступ и не становятся sandboxed автоматически. Не подтверждает zero-copy preview, одинаковый WebGPU feature set или стоимость каждого OS WebView. Версионное семейство: Tauri 2, не проверенный patch release.

### S16 — MoltenVK status
https://github.com/KhronosGroup/MoltenVK
https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/Whats_New.md

Официальный README проверен целевой загрузкой после поискового excerpt. Он **на дату обращения** содержит deprecation notice, community best-effort maintenance и рекомендацию KosmicKrisp для Apple Silicon; MoltenVK остаётся указанным вариантом для Intel Macs/iOS. Это существенный сигнал риска, но не собственный тест альтернативы. Release-notes excerpt показывал поддержку Vulkan 1.4 и запись 1.4.2 от 2026-07-20; не считать это проверенным последним release artifact. До выбора Mac backend отдельно проверить закреплённый SDK, device features и состояние driver distribution.

### S18 — Slint rendering/licensing
https://docs.slint.dev/latest/docs/slint/guide/backends-and-renderers/backends_and_renderers
https://github.com/slint-ui/slint/blob/master/LICENSE.md
https://slint.dev/

Прочитаны расширенные excerpts. Разные backends/renderers имеют ограничения; framework предлагает royalty-free/GPL/commercial варианты, а не общее MIT для всего. У royalty-free есть условия, включая disclosure и ограничения применения; точный текст выбранного release подлежит проверке. Slint — резервный retained UI кандидат, не принятое решение. Коммерческая license PDF также встречалась в результатах, но не использовалась для заявления «все desktop приложения платные».

### S20 — Qt releases/support policy
https://doc.qt.io/qt-6/qt-releases.html

Официальный excerpt: semantic versioning, compatibility exceptions для preview/subject-to-change APIs, общая политика релизов/LTS. Точный support entitlement и end-of-support конкретного релиза в этой сессии не установлены. Не обещать долгую бесплатную поддержку любого Qt 6.x.

## Расширения и безопасность

### S07 — Wasmtime security
https://docs.wasmtime.dev/security

Официальный расширенный excerpt: linear-memory isolation, checked control transfers, explicit imports/exports. Эти свойства касаются модели Wasm; host callbacks и runtime/OS attack surface остаются ответственностью приложения.

### S08 — Wasmtime interruption
https://docs.wasmtime.dev/examples-interrupting-wasm.html

Целевая загрузка полного небольшого раздела. Fuel даёт deterministic interruption при тех же условиях исполнения; epochs имеют другой overhead/недетерминированную точку остановки. Документация приводит оценку epoch slowdown; **мы её не используем как benchmark продукта**. Host calls и native/GPU исполнения эти механизмы автоматически не ограничивают.

### S09 — Wasmtime ResourceLimiter
https://docs.rs/wasmtime/latest/wasmtime/trait.ResourceLimiter.html

Целевая загрузка релевантных API-разделов. Limiter управляет Wasm memories/tables/instances; CPU отдельно через fuel/epochs. Официально не покрывает все Store/host allocations. Основание для separate host quotas и OS-level process limits; не доказательство полной безопасности пакетов.

## Imaging, geometry, materials, export

### S10 — OpenImageIO
https://github.com/AcademySoftwareFoundation/OpenImageIO

Официальный расширенный README excerpt. Format-agnostic image read/write/process APIs и plugin codecs для VFX. Не весь перечисленный codec набор обязателен первому выпуску; codec/dependency licenses и attack surface требуют отдельной проверки. Version pinned/support window не установлены.

### S11 — OpenColorIO
https://opencolorio.org/

Официальный сайт/excerpt. Color management, application integration; сайт отображал OCIO 2.5.0 и Vulkan GPU support. Это не проверка совместимости с выбранным wgpu backend и не замена собственной data-vs-color семантики. Привязка к конкретному OCIO config/version нужна для воспроизводимости.

### S12 — OpenSubdiv
https://www.opensubdiv.org/
https://opensubdiv.org/docs/osd_overview.html

Официальные расширенные excerpts. CPU/GPU subdivision evaluation, библиотека для интеграции, не application и не универсальный geometry/boolean kernel. Introduction отображало 3.8.0. Конкретный evaluator/backend/license/dependency set проверить по выбранному release до внедрения.

### S13 — glTF 2.0
https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html

Целевая загрузка разделов coordinate system/units/UV/materials. Right-handed convention, metres/radians, texture origin, metallic-roughness PBR, linear vs sRGB texture semantics. Подтверждает необходимость explicit conversion/export profiles; не доказывает перенос любого procedural graph, shader или layer stack. Compatibility с целевыми приложениями не тестировалась.

### S14 — MaterialX
https://materialx.org/
https://github.com/AcademySoftwareFoundation/MaterialX
https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.Specification.md?plain=1

Официальные expanded excerpts: описания обмена materials/lookdev, typed values/color-space semantics. Сайт отображал release 1.39.5 (2026-05-22), Apache-2.0. Наличие стандарта не гарантирует единообразное исполнение всех nodes во всех renderers. Export только tested subset, иначе baking или explicit unsupported features.

### S15 — CGAL license
https://doc.cgal.org/latest/Manual/license.html

Официальный expanded excerpt; manual отображал 6.2.1. Packages различаются GPL/LGPL/commercial. Нужен per-package audit; нельзя описывать весь CGAL как unrestricted permissive. Продуктовая лицензия ещё не выбрана.

## Математические и научные основания

### S17 — Pearson, Complex Patterns in a Simple System
https://www.science.org/doi/10.1126/science.261.5118.189

John E. Pearson, Science 261(5118), 189–192, 1993; DOI 10.1126/science.261.5118.189. Доступны bibliographic data и abstract; **полный paywalled текст не прочитан**. Abstract подтверждает разнообразие spatiotemporal patterns reaction-diffusion. Не достаточен как единственный источник реализации численного solver или биологических обещаний.

### S19 — Witkin/Kass, Reaction-diffusion textures
https://dl.acm.org/doi/10.1145/127719.122750

Первичная публикация SIGGRAPH, 1991; DOI 10.1145/127719.122750. Прочитан abstract/excerpt: texture synthesis, anisotropic/non-uniform diffusion и mapping. Полная статья не заявляется прочитанной. Подтверждает содержательное procedural-art направление, а не выбор конкретного solver или параметров.

### S21 — Sanderson et al., Advanced Reaction-Diffusion Models for Texture Synthesis
https://www.sci.utah.edu/~allen/materials/Sanderson_JGT_2006.pdf

Авторский университетский PDF; прочитаны извлечённые abstract/фрагменты о трудности параметризации, стоимости и anisotropic/shaped patterns. Полный вывод discretization и stability analysis в этой сессии не разобран. Для implementation phase нужен отдельный numerical note с уравнениями, boundary conditions, convergence/reference tests; наличие эстетического примера не proof solver.

## Неустановленное и отложенное
- Полный сравнительный обзор геометрических kernels (boolean/remesh/robust predicates), vector rendering/text shaping, shader language toolchains и scripting language runtimes.
- Юридическая оценка всех транзитивных dependencies, точные stable releases/toolchains/support windows, CVE inventory.
- Реальные capabilities target GPUs и стоимость interop; CPU/GPU timings, RAM/VRAM и UI accessibility measurements.
- Round-trip fidelity Blender/Unity/Unreal/Photoshop; файловый формат проекта и его миграции.

Это открытые задачи, а не скрыто «уже проверено». Для первых архитектурных альтернатив доказательств достаточно, чтобы сформулировать проверяемые гипотезы, но **недостаточно для окончательного stack approval**.
