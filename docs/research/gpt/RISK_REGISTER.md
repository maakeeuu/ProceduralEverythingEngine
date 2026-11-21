# Регистр технических рисков

2026-11-21. Качественная оценка до прототипов: вероятность Н/С/В — низкая/средняя/высокая, ущерб С/В/К — средний/высокий/критический. Это экспертные предположения, не вычисленная статистика. Архитектурные риски открыты; операционный K16 обновлён после восстановления доступа. Ответственные роли предварительны. План проверки: [EXPERIMENT_PLAN](EXPERIMENT_PLAN.md).

| ID | Риск и вероятность/ущерб | Ранний индикатор | Снижение и проверка | Ответственный / ворота |
|---|---|---|---|---|
| K01 | Scope explosion: В/К | Каждый домен требует свой renderer/runtime до сквозного результата | Один end-to-end fixture, явные non-goals; не параллелить все домены | Lead+владелец / G0–G4 |
| K02 | Ложная универсальность данных: С/К | Mask проходит color transforms, scene превращается в mesh | Separate payloads + semantic descriptors, explicit conversion tests P1/P2 | Core/domain lead / G1 |
| K03 | CPU↔GPU копии уничтожают интерактивность: В/В | Высокий readback/IPC time при дешёвом kernel | Residency tracing, bounded thumbnails, P2/P4; не обещать zero-copy | Graphics / G2 |
| K04 | VRAM/RAM exhaustion: В/К | Большие graphs/tiles/cache растут без budget | Предварительные estimates, resource broker, LRU/pins, overflow checks, workload limits | Core+graphics / G1–G3 |
| K05 | Stale output/races: В/В | После быстрой правки показывается предыдущий seed | Revision-tagged tasks, latest-only publication, P1 cancellation stress | Core / G1 |
| K06 | GPU driver/device loss и platform mismatch: С/К | Optional feature/format не поддержан, зависший shader | Capabilities matrix, short dispatch, CPU fallback subset, реальные ОС/GPUs | Graphics / G2 |
| K07 | Seed не воспроизводит результат: В/В | Порядок потоков/версия меняет output | Versioned RNG/substreams, algorithm version, strict CPU vs tolerant GPU tests | Algorithms / G1–G4 |
| K08 | UI toolkit не годится для продукта: С/В | IME/keyboard/accessibility/node canvas тормозят | P3 early; UI state отдельно от core, alternative shell cost зафиксировать | UI / G2 |
| K09 | Malicious plugin/project: В/К | Unbounded allocations, host callback, traversal, shader hang | Data limits, Wasm+OS policies, host quotas, no arbitrary code on open, P5 | Security / G5 |
| K10 | Color/alpha/units mismatch: В/В | Export выглядит иначе, height изменён gamma, UV перевёрнут | Data-vs-color, OCIO evaluation, premultiplied rules, golden fixtures P2/P6 | Imaging / G2–G4 |
| K11 | Лицензия блокирует поставку: С/К | Зависимость внедрена до выбора модели лицензии | Module-level bill of materials; Qt/CGAL/Slint per-license review | Lead+владелец / до stack approval |
| K12 | Формат проекта ломает старые работы: С/К | Runtime pointers сериализованы, migration необратима | DTO separation, bounded parsing, backups, migration fixtures и отдельный ADR | Core / до alpha |
| K13 | Нереалистичные simulation обещания: В/В | Неизвестная численная устойчивость, нет bounded step | Gray–Scott reference с boundary/dt tests; сложная физика deferred | Algorithms / G4 |
| K14 | SDK/ABI и зависимости конфликтуют: С/В | Плагин иной сборки ломает host | C ABI handles/version negotiation, isolation, capability ranges; native trust explicitly | Extensions / G5 |
| K15 | Совместная AI-разработка расходится: В/В | «Принято» без ADR, одновременная правка одних файлов | Отдельные ветки/dirs, актуальный handoff, review diffs, source-of-truth docs | Lead+рецензент / всегда |
| K16 | Первоначальный отказ GitHub write: устранён для branch create | После изменения прав ветка создана; запись пакета проверяется фактическим commit | Перед записью повторно проверена база; main не трогать; результат commit/PR в CURRENT_STATE | Владелец+lead / перенос |
| K17 | Недооценка native FFI/unsafe: С/В | Rust core объявлен полностью безопасным при C++ plugins | Минимальные wrappers, ownership rules, sanitizers, fuzz parsing, process isolation | Core / G2–G5 |
| K18 | Непроверенная поддержка upstream: С/В | Latest docs приняты за поддержанный pinned release | Release/tag/license/advisory review; platform CI; особый macOS Vulkan path | Lead / stack approval |
| K19 | Lossy export выдан за полную интеграцию: В/В | Arbitrary material graph обещан в glTF | Export profiles, bake report, external importer P6; никогда не обещать round-trip без tests | Interop / G4 |

## Численный sanity-check, не benchmark
Изображение 4096×4096 RGBA32F содержит 268435456 байт = 256 MiB до mipmaps, staging и allocator overhead. Четыре таких одновременно удерживаемых результата — 1 GiB. Это арифметическая нижняя оценка, не измеренный footprint. Поэтому cache/memory policy — раннее требование, а не финишная оптимизация. Реальные peak RSS/VRAM измерить P2.

## Блокирующие критерии
Нельзя утверждать стек при неизвестной лицензионной совместимости, без working end-to-end CPU fixture и GPU/preview proof на целевой платформе. Нельзя публиковать native plugin как безопасный без threat model. Нельзя выпускать пользовательскую alpha без согласованного save/recovery поведения. Нельзя закрывать риск только на основании наличия библиотеки или заявления второго ИИ.
