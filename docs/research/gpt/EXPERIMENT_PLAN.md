# План доказательных экспериментов

2026-11-21 · предложения, **ещё не выполнены**. Каждый spike — отдельная короткая ветка с исходниками, fixture, командой запуска и сырыми результатами. Перед запуском согласовать ОС/железо и acceptance budgets; ниже provisional targets, не обещание продукта. Не разрабатывать большие три независимых движка ради сравнения стеков.

## Общий протокол
Зафиксировать commit/toolchain/dependencies, OS/GPU/driver/CPU/RAM, power mode, debug/release flags, precision, workload и warm/cold cache. CPU single-thread reference — oracle там, где он корректен. Сначала correctness, затем measurement. Отдельно замерять compile/pipeline warm-up, compute, transfer, scheduling и presentation. Не сравнивать A CPU с B GPU и не подменять фактическое время одним GPU timestamp.

Для latency: после прогрева минимум 30 одинаковых edits, p50/p95 и все сырые sample; для memory — peak RSS/VRAM/allocations. Сравнения только одинаковых resolution/quality/iterations/geometry. Ошибки чисел проверять абсолютной и относительной нормой на объявленном диапазоне; финальный tolerance уточняется по algorithm/precision, а не выбирается после провала. Скриншот не заменяет numeric test.

## P1 — headless граф и правильность ядра
**Гипотеза:** тонкий DAG executor с immutable outputs покрывает первый междоменный сценарий без собственного универсального JIT.

Fixtures: diamond/shared upstream; независимая ветка; invalid type/arity; cycle; missing dependency; nodes error; 100/1000 дешёвых нод как scheduler stress, не обещание UX scale. Node invocation counters показывают, какие ветви реально пересчитаны. Повторный запрос без изменений = cache reuse; изменение UI позиции = ноль kernel calls; material-only edit не трогает field/mesh; field edit инвалидирует downstream.

Seed: одинаковые input/seed/algorithm version на выбранном CPU backend → одинаковые bytes. Parallel execution сохраняет stable sample-index RNG. 100 rapid revisions и cancellation не могут опубликовать старый output как новый. Error/NaN/overflow fixtures не приводят к crash.

**Приёмка:** все инварианты в automated tests; latest result соответствует последней revision, нет unbounded queue/cache. Первоначальная цель cancel acknowledgement ≤100 ms для chunked CPU workload; не гарантия фактического завершения уже запущенного kernel. Отдельно зафиксировать исключения.

## P2 — GPU residency и междоменный граф
**Гипотеза:** поддержанный image/field subset проходит GPU pipeline без полного readback после каждой ноды, сохраняя семантику CPU reference.

Workload: seeded Voronoi/warp/symmetry/range, 512²/2048²/4096² scalar/image buffers; displacement grid 257×257, затем 513×513. Same output scalar field → height → mesh and color → PBR. GPU direct displacement view не выдавать за export-ready CPU mesh: отдельно материализовать mesh для численной проверки/export.

Log: upload/download bytes, number of fences, graph evaluation and presented-preview latency, VRAM peak, kernel compile/warm time; downsampled thumbnails отдельно. Сравнить all-CPU+upload, GPU resident chain, deliberately readback-each-stage baseline. Хранение mask не означает обязательный RGBA32F; single-channel valid format выбирается по capabilities.

**Приёмка correctness:** CPU/GPU outputs within predeclared tolerances, explicit image origin/UV/unit/color fixtures; отсутствие readback между чисто GPU compatible stages. Memory eviction не освобождает in-flight resources. Device-loss behavior воспроизводится доступной controlled simulation/test hook; не утверждать реальный driver fault tolerance без проверки.

**Provisional UX target:** на согласованном baseline железе 512² quick preview p95 ≤150 ms для этой короткой stateless цепочки после прогрева; 3D navigation frame p95 ≤33 ms во время работы; high-res export отдельной очередью. Если цель не достигнута — найти transfers/kernel/scheduling причину, не скрывать сниженное качество.

## P3 — UI-fit и доступность
**Гипотеза:** выбранная native оболочка обеспечивает комфортный серьёзный editor, а не только dev-tool panel.

Собрать только живой минимальный editor поверх P1/P2: palette/search, empty graph vs preset, connect/reconnect, inspector, компактный/расширенный node, актуальная thumbnail, 2D/3D viewers, undo/redo. No fake static results. Проверить keyboard-only flow, focus, Cyrillic text/IME, HiDPI, screen reader basic path, pan/zoom/selection, warning/error discoverability. Дизайн-токены с начала.

**Приёмка:** создание сквозного графа с нуля без hidden console, preset раскрывается в тот же graph, типы видимы без одного только цвета, долгий compute не блокирует typing/navigation. Если toolkit не проходит critical UX — small Slint/Qt/web alternative test с той же моделью; не переписывать core ради UI.

## P4 — конкурентный IPC/preview spike для C
**Гипотеза:** web shell экономит UI разработку, не создавая недопустимых затрат для целевого graph workload.

Use same Rust CPU outputs as P2; Tauri preview transport 512²/2K/4K и mesh sizes, command churn, cancellation/out-of-order responses. Binary/shared-memory candidate path сравнить с наивным JSON/base64 baseline. Измерить actual host→WebView copy bytes, p95 presented latency, RSS и platform behavior. Native GPU texture → WebView sharing не предполагается поддержанным.

**Приёмка:** те же functional/UX бюджеты и семантика latest-only; не скрытые sidecar windows и не global FS permissions. Если копии недопустимы и нет bounded portable пути, C отклоняется для GPU-first workload либо явно меняет product envelope. Не строить собственный browser engine.

## P5 — adversarial extensions
**Гипотеза:** разрешения, Wasm quotas и OS boundaries позволяют ограничить класс сторонних CPU extensions.

Tests: infinite loop; memory/table growth; host callback allocating large image; recursion/stack; oversized input/module compilation; archive traversal/symlinks/zip bomb; dependency cycle/version conflict; attempted FS/network access; endless native worker. MemoryLimiter сам по себе не покрывает host allocations [S09].

**Приёмка:** guest no FS/network без разрешения; host quotas; loop/fuel/epoch termination; bounded wall-time/RSS с проверенным OS mechanism, сохранение responsive host и пользовательского проекта. Pure process isolation без OS policy не засчитывать как защиту файлов. Shader hangs и driver attacks остаются отдельным открытым риском; arbitrary third-party GPU code в раннем безопасном режиме запрещён.

## P6 — состояние, recovery и экспорт
**Гипотеза:** независимые DTO и adapters позволяют сохранить семантику без привязки к runtime/GPU objects.

Test-only snapshot фиксируется как нестабильный fixture, **не формат продукта**. Сохранить/восстановить graph/seed/scene/layers/params/resource references; missing node/resource отображается без уничтожения unknown data. Interrupted save не повреждает предыдущий checkpoint. Product-format spike отдельно сравнит контейнеры/миграции/внешние assets и потребует согласования.

Export PNG/data-image/mesh candidate profile: независимый reader/importer подтверждает размеры, units, normals, UV origin, color, material map packing и topology; сравнить numeric bounds и визуальный fixture. Report baked/lost features. Реальные Blender/Unity/Unreal/Photoshop tests выполняются только при доступности приложений; отсутствие теста явно указать.

## Ворота после spikes
Результат каждого: подтверждено/опровергнуто/недостаточно данных, сырые samples, команды, known failures и условия пересмотра. Независимый архитектор критикует выводы и benchmark fairness. Только после этого владелец утверждает стек/ограничения; ни одна проверка в этом документе ещё не запускалась.
