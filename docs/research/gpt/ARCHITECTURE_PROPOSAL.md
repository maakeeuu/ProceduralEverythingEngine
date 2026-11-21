# Архитектурное предложение

2026-11-21 · PROP/HYP · не утверждено. Источники [SOURCES.md](SOURCES.md); сравнение стеков отдельно. Все описания компонентов ниже — проектируемое поведение, **не существующая реализация**.

## 1. Продуктовая интерпретация
Это local-first процедурный редактор с одним документом проекта и несколькими специализированными представлениями. Его отличительная ценность — не количество генераторов, а исследуемость алгоритма и композиция данных между доменами: один и тот же scalar field используется как маска, геометрическая высота и материал без ручного промежуточного экспорта. 2D — самостоятельный полноценный рабочий процесс, а не окно настройки 3D.

Требования R01–R44 зафиксированы в MASTER_CONTEXT. Нельзя считать утверждёнными конкретный язык, графический API, формат файла, full history, Explore или полный набор физических симуляций. Предлагается небольшой набор согласованных контрактов вместо одного «универсального объекта».

## 2. Границы подсистем
- **Project/document:** стабильные ID, графы, сцены, композиции слоёв, ссылки на ресурсы/зависимости, команды undo/redo. Не хранит GPU handles как постоянные данные.
- **Graph model:** узлы, порты, параметры, связи и группы; независим от canvas UI и исполнения.
- **Registry:** версии определений типов и нод, метаданные/UI descriptors, схемы параметров, доступные kernels и converters. Внешний код не получает прямую мутацию всего проекта.
- **Evaluation core:** валидирует и планирует зависимости, исполняет запросы, управляет cache/cancellation/resources. Не знает алгоритм растения или смысл слоя Photoshop.
- **Domain modules:** image/field, geometry, materials, scene, compositing, simulation; владеют семантикой, алгоритмами и специальными инвариантами.
- **Resource broker:** immutable handles, CPU buffers/GPU textures, lifetime, memory accounting, transfers, device generation. Не обещает zero-copy между всеми API/процессами.
- **Presentation:** editor shell, node canvas, parameter inspectors, 2D/3D viewers, thumbnails. UI посылает команды и subscribes на результаты, а не вычисляет дорогие ноды на UI thread.
- **Persistence/export adapters:** отдельно версионируемые DTO и профили форматов, без связи с layout renderer.
- **Extension host:** разрешения, лимиты, загрузка, сбои; native и sandboxed — разные уровни доверия.

На старте — модульный монолит с worker pool и отдельным host для недоверенного исполнения, не микросервисы и не distributed scheduler. Стабильный public ABI не нужен для каждой внутренней границы.

## 3. Междоменные данные

### 3.1. Типы и семантические метаданные
| Семейство | Начальный контракт | Почему отдельный тип |
|---|---|---|
| Scalar / Integer / Boolean / Vector / Color | Числовой формат, единицы, color-space для цвета | Вектор не цвет, число не angle без контекста |
| Field2D | Размерность/координаты и способ sample либо явно rasterized field | Непрерывное поле не готовая текстура; разрешение выбирается при materialize |
| Image2D | Размеры, channels, scalar format, color-space/data semantic, alpha mode, origin, pixel aspect | Raw height не должен проходить sRGB transform |
| Mask / HeightField | Скалярные данные, диапазон, boundary, physical extent/height units | Чёрно-белая цветная картинка и физическая высота не эквивалентны |
| Mesh | Positions, indexed faces, typed point/corner/face attributes, topology version, bounds | Render triangles и editable polygon topology различаются |
| Curve / Instances | Параметризация/атрибуты; transforms и ссылки на prototype | Не раздувать повторения в полную mesh по умолчанию |
| Material | Versioned material description, texture/field bindings, declared shader capabilities | CPU evaluator не исполняет произвольный BSDF как обычную картинку |
| Scene | Objects, transforms, cameras/lights, references | Сцена не единый mesh и не вычислительный граф |
| LayerComposition | Упорядоченные элементы, masks, blend/opacity, grouping | Порядок композитинга и граф — разные модели |
| SimulationState | Algorithm/version, step/time, checkpoint, seed/solver config | Stateful переход не чистая stateless-нода |

Новые типы регистрируются namespaced ID и schema version. Для начала встроенный закрытый набор payload representations + расширяемые descriptors; позже opaque plugin type с inspector/serializer/converters. Не обещать произвольный host ABI/zero-copy для неизвестного payload.

### 3.2. Handles и владение
Результат — immutable handle + descriptor + revision/fingerprint. Handle удерживает ресурс; чтение не копирует его автоматически. Copy-on-write разрешён внутри алгоритма при доказанном exclusive ownership. Ссылки на host pointers не пересекают процессный/SDK барьер. Render proxy может быть GPU-resident; export явно запрашивает CPU-readable representation. Срок жизни привязан к in-flight заданиям/fences и подписчикам, а не только видимости ноды.

### 3.3. Явные конверсии
- Field2D → Rasterize: extent, resolution, sampling/filtering, boundary, quality.
- Color image → Luminance/Channel → Mask: channel selection, transfer/color interpretation, range, clamp policy. Нельзя по ошибке применять display transform к данным.
- Mask → HeightField: physical extent, height scale, units, origin.
- HeightField + Grid → DisplaceMesh: sampling/UVs, edge boundary, normals recompute; tessellation density отдельно от image resolution.
- Image/Field → Material texture binding: UV/space и color semantic явно заданы.
- Curve → Mesh либо Instances → realized geometry — только явная операция с оценкой стоимости.

UI может предложить вставить подходящий converter, но не менять тип связи молча. Конверсия с потерями показывает предупреждение. Defaults доступны новичку, advanced controls — специалисту.

### 3.4. Единицы, цвет и координаты
Внутренние соглашения ещё подлежат ADR: предложение — SI-метаданные, radians для углов, явно объявленная handedness/up axis и UV origin. Важнее переносить эти сведения, чем объявить выбранный axis вечным. glTF имеет собственные правила [S13]; exporter должен преобразовывать, а не просто переименовывать поля.

Image operations выполняются в объявленном working-linear пространстве; blend policy включает premultiplied/straight alpha. Height/normal/mask — data, не display color. View transform применяется только при показе. OCIO — кандидат зрелой интеграции, не обязательная тяжёлая зависимость первого headless spike [S11].

## 4. Universal Compute Core

### 4.1. Минимальный контракт
Определение ноды содержит node_type_id/version, typed port schemas/cardinality/defaults, parameter schema, deterministic/pure/stateful/effectful flags, supported CPU/GPU kernels, quality/region constraints, cost/memory estimate и diagnostics. EvalContext несёт immutable project revision, request ID, requested outputs, ROI/LOD/resolution, seed, cancellation token, budget и device capabilities. Kernel возвращает typed outputs или structured error; частичный/старый результат маркируется.

**Ядро обязано:** вычислять demand subgraph, проверять связи/циклы, отслеживать revision, запускать задачи, дедуплицировать общий upstream, ограничивать ресурсы, обновлять diagnostics. **Не обязано:** знать half-edge edit rules, реализовывать subdivision, компилировать весь граф в shader, автоматически распределять любые операции CPU/GPU.

### 4.2. План выполнения
1. UI-команда атомарно создаёт новый document revision; история команд отделена от compute cache.
2. Compile/validate проверяет обязательные inputs, схемы/версии, type constraints, missing node/dependency, cycles. Обычный граф — DAG. Циклы допускаются только внутри специальной iteration/simulation конструкции с явно ограниченными шагами.
3. Output request определяет достижимый подграф; топологическая сортировка и dependency counters готовят исполнимые задачи.
4. Сначала cache lookup; одинаковые in-flight outputs объединяются. Приоритеты: active output → selected/pinned preview → visible thumbnails; скрытые ноды не рендерят все previews сами.
5. CPU worker pool исполняет независимые pure tasks. Число задач ограничено: не создавать отдельный OS thread для каждого node/pixel. Stateful/effectful задачи идут через явную сериализацию/барьеры.
6. GPU backend исполняет поддержанные kernels группами с сохранением residency. Не мигрировать каждый узел на «самое быстрое устройство» по отдельности: стоимость transfer/синхронизации может доминировать.
7. Публикация результата только если generation/request соответствует текущей подписке. UI может показать старый результат с индикатором «обновляется», но не обозначать его актуальным.

### 4.3. Инкрементальность и кэш
Cache key включает node definition/algorithm version, canonical parameters, input result fingerprints, seed substream, requested output, extent/region, resolution/LOD, working color configuration, quality mode, relevant environment/dependency versions и при необходимости device/backend identity. Внешний файл меняет fingerprint при изменении содержимого; один mtime недостаточен. UI-позиция ноды не инвалидирует compute.

Runtime revision IDs подходят для быстрой инвалидации внутри сессии; для persistent cache нужны content/dependency hashes и отдельная политика доверия. Не хэшировать гигабайты GPU texture после каждой правки ради кэша — вычислять provenance key по входам и версии детерминированного kernel. Недетерминированные/effectful outputs не выдавать за reusable pure cache.

MVP кэш — memory-only, budgeted LRU/pinned active outputs, раздельный CPU/GPU учёт. Disk cache и shader fusion — позже, только после измерений. Неполные, отменённые и errored outputs не переиспользуются как успешные. Для tile/ROI фильтров нужны halo regions; global normalisation и distance transforms не pretend-local.

### 4.4. Детерминизм
Project seed + stable node instance ID + seed namespace/version + explicitly indexed samples. Порядок thread execution не должен менять случайную последовательность. Дублирование узла требует продуктового выбора: сохранить seed или создать новый substream — это видимый параметр/команда.

Точное byte equality требовать только для указанного CPU backend/algorithm version. GPU/CPU сравнивать с объявленными tolerances; float order, FMA, transcendental functions и chaotic simulation исключают обещание побитовой одинаковости на всех GPU. Seed без версии алгоритма не гарантирует воспроизводимость после обновления.

### 4.5. Отмена, ошибки, лимиты
Cooperative cancellation в CPU циклах/tile boundaries. GPU уже отправленную работу обычно нельзя произвольно прервать: короткие bounded dispatch, проверка между passes, stale result discard. Long shader может заблокировать driver — arbitrary GPU code не разрешать автоматически.

Проверять размеры до allocation, арифметическое переполнение, topology bounds, NaN/Inf, missing inputs, shader compilation failure и device loss. Error содержит node/port/context, actionable message и ссылку на diagnostic detail, но не секреты. Downstream отмечается blocked-by-upstream, а не отдельной загадочной ошибкой.

GPU loss сбрасывает device-generation resources и caches; CPU fallback только для поддержанных kernels с явной индикацией. Глобальный backpressure не даёт thumbnails съесть ресурсы export. Нельзя освобождать ресурс, пока его использует in-flight command.

### 4.6. Simulation
Сначала bounded Gray–Scott/клеточный автомат как кандидат; не полноценная жидкость/cloth/rigid body платформа. Step size, boundary conditions, grid spacing, precision, initial perturbation и iteration count — входы модели. State transition S(t+Δt) не кэшируется как stateless function без checkpoint/time в ключе. Изменение upstream reset/branch state с видимым предупреждением. История симуляции ограничена бюджетом; timeline/audio runtime сейчас не строить.

## 5. Нодовая система — редактор над реальным графом
Стабильные instance IDs не зависят от названия/позиции UI. Graph groups имеют явный interface, параметризацию, версии и recursion checks. Generator package на ранней стадии — graph asset + public parameters + thumbnails + dependency/version metadata, а не отдельный секретный evaluator.

У canvas есть selection/multi-select, pan/zoom, connect/reconnect/delete, поиск и категории, undo/redo и типовые ошибки. Компактный режим оставляет основные параметры/ports/preview; расширенный раскрывает настройки и diagnostics. Port type обозначается не только цветом, но icon/text для color-vision доступности. Node palette preview использует демонстрационный input, ясно отличимый от actual graph output.

Для начинающего: готовый generator с небольшим inspector; команда «Открыть граф» сохраняет семантику/результат. Для опытного: пустой граф, explicit conversions, grouping и возможность pin любого промежуточного результата. Миниатюра — подписка на evaluator с более низким LOD, не PNG-обманка. При zoom-out сокращаются частота и детализация; preview не обещает export resolution.

Граф ошибки валидируются и headless; неверную связь UI блокирует, а повреждённый project fixture отклоняется без crash. Не привязывать evaluator к конкретной canvas-библиотеке.

## 6. Рабочие пространства и дизайн
2D viewer: pan/zoom, 1:1 pixels, checkerboard alpha, data/false-color view, sampling info; compositor использует отдельную layer model. 3D viewer: orbit/pan/dolly, camera, lights, shaded/wireframe/normals, bounds и статус LOD. Quick Preview и полноценный viewport используют один result handle там, где возможно, но свои presentation state.

Токены: neutral surfaces/borders/text, focus/error/warning/success, spacing scale, type scale, radii, selection и domain colors. Предлагаемый акцент cyan/teal — **не утверждённый бренд**; purple не основной. Keyboard navigation, focus visibility, scaling/HiDPI, Cyrillic text/IME и screen reader проверить до ставки на UI toolkit. Привлекательность Apple — ориентир ясности, не pixel-copy.

## 7. Scripting, Native и пакеты
Сначала встроенные kernels с тем же registry contract. Затем расширения:
- **Visual:** graphs/presets, только declared node dependencies. Даже data-only проект ограничивает nesting, texture sizes, iteration count.
- **Sandboxed compute:** кандидат Wasmtime с explicit imports/capabilities, fuel или epochs, memory/table limits, wall deadline и OS process budget [S07–S09]. ResourceLimiter не покрывает все host allocations. Host callbacks тоже имеют quotas/timeouts. Нет FS/network по умолчанию; выбранные пользователем ресурсы через broker. Компиляция Wasm тоже ограничена по времени/памяти.
- **Scripting:** Python удобен для автоматизации/экосистемы, но не безопасный embedded sandbox. Рассмотреть процесс с минимальными разрешениями; запрет imports не security boundary. Малый expression language/Wasm SDK — альтернатива для pixel-safe функций. Язык пока OPEN.
- **Native:** versioned C ABI/opaque handles и explicit ownership либо out-of-process protocol; Rust ABI/компиляторный C++ ABI не обещать стабильными. In-process native — только доверенный режим с предупреждением; отдельный процесс без OS sandbox не защищает файлы.

Package manifest: ID/version, supported host/API range, node/type schemas, dependencies, platform targets, capabilities, hashes, origin/signature metadata. Install сначала validate/extract с size/depth/path traversal guards, затем permission review и atomic activation; конфликты не overwrite чужих ID. Revocation/disable/rollback не должны автоматически удалять пользовательские projects. Подпись показывает издателя, не безопасность.

SDK сначала internal/experimental. Удалённые update/install не обязательны. Для неизвестной ноды сохраняются metadata и connections для восстановления после установки зависимости; без её кода граф не исполняется и файл не разрушается при открытии.

## 8. Сохранение и экспорт без преждевременного формата
Разделить runtime objects, persistent DTO и export data. Нужны stable IDs, explicit schema versions, migration chain, dependency/resource references, missing-resource recovery, bounded parsing, transactional save, backup/recovery и round-trip tests. Не хранить device handles и derived cache как единственный источник правды.

**Не выбираем сейчас** расширение, JSON/другой текст/binary, archive/container и открытость спецификации. В spike допустим test-only snapshot в заранее помеченном временном формате без пользовательской совместимости. Перед usable alpha — отдельный persistence ADR и согласование; нельзя откладывать сохранение до самого конца.

Export — профиль с предупреждениями потерь. PNG candidate для растрового proof, EXR для float/data, SVG для настоящих vectors, glTF/GLB для mesh + baked PBR, OBJ как простой mesh baseline, MaterialX для исследования совместимого subset. Это кандидаты, не утверждённый список. glTF не универсальный перенос arbitrary node graph или BSDF [S13–S14]. Для Photoshop/Unity/Unreal/Blender нужны проверенные импортные профили конкретных версий; обещание «формат поддержан» не означает fidelity во всех приложениях.

## 9. Содержательные алгоритмы по этапам
- Первые: seeded Voronoi distance/boundary fields, domain warp с ограниченным frequency/amplitude, symmetry transforms и color ramps; контролируемые tileable boundary conditions.
- Следом: bounded Gray–Scott для органики, fractal/escape-time или IFS, multi-scale patterns; параметры и stability guards, presets с раскрываемым графом. Pearson и Witkin/Kass подтверждают потенциал RD, но не точность копирования краба/дыни [S17, S19, S21].
- Terrain: height fields, erosion отдельно после bounded numerical studies, не сразу гидрология промышленного уровня.
- Nature: L-system/space-colonization сравнить отдельно; curves/instances и deterministic branching до leaf photorealism.
- Architecture: repeat/align/scatter/attribute rules на тех же geometry/instance contracts, не отдельный CAD kernel.
- Materials: сначала sampled PBR subset с baking, позже более богатые graphs; path tracer не условие раннего результата.

## 10. Вертикальный срез и критерии
Один документ: **Seeded Voronoi → Warp → Symmetry → ScalarRange → HeightField → DisplaceGrid**; параллельно scalar/color ramp → material base color. 2D layer composition с дополнительной mask демонстрирует, что слой не нода и не scene object. Параметры доступны готовым generator inspector и через построение с нуля.

Пользователь меняет seed/warp; актуальный pattern, pinned thumbnail и 3D-сетка обновляются; изменение material не пересчитывает Voronoi; invalid port/cycle отклоняются; быстрая серия правок не публикует старый результат как новый. Mesh normals/UVs и physical height проверяются. Междоменный обмен использует handles, без ручных файлов между нодами. Test-only snapshot сохраняется/восстанавливается; export image/mesh проверяется внешним reader. Product save format решается отдельно до пользовательской alpha.

Сначала CPU-референс и базовый GPU-rendered viewport, затем тот же supported field/image subset на GPU. CPU-only proof может показать корректность архитектуры, но не считается доказательством GPU-производительности.

**Не входит:** все домены, production plugin marketplace, полный SDK, arbitrary native scripts, animation/audio, сложная физика, полный color pipeline всех DCC, industrial CAD или renderer уровня offline production.

## 11. Почему это пока не доказанная архитектура
Проектирование закрывает семантические противоречия, но не измеряет стоимость. Доказательство пригодности требует spike P1–P6 из EXPERIMENT_PLAN, одинаковых fixtures в A/C и критических путей B при необходимости, анализа лицензий, независимой рецензии и решения владельца. До этого рекомендация A условна и обратима. Нет оснований обещать сроки выпуска или сравнение «в N раз быстрее».
