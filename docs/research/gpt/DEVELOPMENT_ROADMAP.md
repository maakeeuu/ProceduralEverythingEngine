# Дорожная карта по проверяемым воротам

2026-11-21 · PROP. Не календарное обещание. Ресурс команды и baseline hardware неизвестны; оценки в неделях сейчас создали бы ложную точность. Порядок изменён относительно примерного плана: typed core и сквозной сценарий раньше широкого UI, persistence proof раньше usable alpha, безопасность изучается до plugin release, тесты — на всех этапах.

## G0 — требования, исследования, независимая критика
Выход: заполненная постоянная память, A/B/C, риски, open questions, experiments и независимая оценка. Сейчас есть локальная первая оценка; нет второй, нет окончательного решения. Первоначальная блокировка GitHub write устранена: отдельная ветка создана; перенос документации не означает утверждение стека. Владелец определяет платформенный/лицензионный envelope и разрешает bounded spikes; это ещё не утверждение стека.

## G1 — технический headless proof
Зависимость G0/разрешение spikes. CPU reference для одного field/image → height → mesh graph; schema/ports, demand DAG, errors, seed, cache invalidation, cancellation, budgets. Automated P1 tests и воспроизводимая команда. Новый тип/нода добавляется через registry без изменения scheduler; пример extension пока встроенный, не public SDK. Выход: реальные численные результаты и tests, не пустой интерфейс.

## G2 — native/web UI и GPU proof, архитектурное решение
P2/P3, при смысле P4; UI живёт над тем же core, 2D/3D viewers показывают результаты. Проверить platform capability/driver path, versions/build/license inventory. Сопоставление с независимым архитектором → общий recommendation → повторная критическая рецензия → согласование владельца. Только тут ARCHITECTURE.md и accepted ADR; изменение курса допустимо.

## G3 — рабочая вертикаль, не ширина
Продуктовая оболочка и устойчивый node editing поверх доказанного core: empty graph/preset, search, compact/expanded nodes, Quick Preview/Full Workspace, актуальные thumbnails, undo/redo, visible diagnostics, shared field→height→3D→material, базовый layer composition. Budgets и наивный scalar reference не исчезают при оптимизации. Выход: пользователь проходит сценарий от пустого графа до результата; tests latest-only/CPU-GPU/undo.

## G4 — 2D/Generative Art alpha с сохранением и экспортом
Исследовать и отдельно согласовать формат/контейнер/открытость/ресурсы. Реализовать atomic save/recovery/migrations и round-trip fixtures **до выдачи alpha пользователю**. 2D masks/layers/blends, richer Voronoi/warps/symmetry, bounded RD/fractal candidate, presets и reusable graph generators. 3D/materials ровно до нужд vertical slice, затем primitive/subdivision/displacement по доказанной модели. External export profile tests и documented losses обязательны. Выход: сохраняемый проект, который можно повторно открыть и экспортировать с проверенной семантикой.

## G5 — расширяемость как пользовательская функция
Experimental SDK → versioned packages/manifest/dependencies/capabilities → local install/disable/rollback → sandbox and compatibility tests P5. Script language выбирается после threat/interop исследования. Trusted native mode отдельно. Public stable SDK только после двух независимых реальных extensions, созданных не путём специальных core hacks. Каталог/сервер не нужен.

## G6 — расширение доменов
Terrain, Nature, Architecture, более богатые materials/geometry, векторный pipeline и ограниченные simulations добавляются по одному. Каждая фича — отдельный сквозной use case с типами, budgets, errors, save/export и regression tests. General editable topology, erosion и volumetrics не обещаются одновременно. Audio/Animation остаются future initiatives.

## G7 — production hardening и выпуск
Performance regressions, fuzz/property tests, import/project attack surface, device loss, recovery, platform CI/packaging/signing, dependency advisories/SBOM, installation upgrades, documentation и примеры. Release criteria: поддержанные платформы/железо названы, benchmarks опубликованы, critical bugs закрыты, migration/recovery rehearsed, known limitations честны. Не объявлять release только по наличию экранов.

## Оценка необязательных предложений
| Предложение | Рекомендация / этап | Основание |
|---|---|---|
| Non-destructive workflow | Принцип graph/document с G1; UI undo с G3 | Не отдельная вторая engine subsystem |
| Procedural History | Undo command log G3; branching/history UI позже | Не путать compute cache, simulation checkpoints и историю редактирования |
| Seed | G1 | Условие reproducibility и tests; RNG/algorithm version обязательны |
| Caching | Memory budgeted cache G1; disk позднее | Корректная инвалидация важнее количества cache layers |
| Live Preview | G2/G3 с LOD/priorities | Не compute every hidden node every frame |
| Presets / Graph Templates | Единый graph-asset механизм G3/G4 | Отличаются exposed parameters, не требуют двух runtimes |
| Graph Groups | Базовая композиция G3/G4 | Явные порты/версии и recursion limits |
| Generator Library | Локальная curated библиотека G4 | Полезна двум сценариям старта, без сервера |
| Explore | Сначала local examples G4/G6; online gallery deferred | Сначала качественные исполняемые примеры, потом discovery/community |

## Постоянная дисциплина
После каждого G — обновить CURRENT_STATE/TASKS/DECISIONS/DEVELOPMENT_LOG и handoff; всё в отдельных ветках. Независимая рецензия на переходах, где меняется фундаментальный контракт. Ни одного merge в main без подтверждения владельца.
