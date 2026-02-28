# Plan: Replace Metalex with ELI-DL

## 1. Class & Property Mapping

### legislation.owl.ttl

| Legislation entity | Current Metalex superclass | ELI-DL / ELI replacement |
|---|---|---|
| `:BillResource` | `metalex:BibliographicWork` | `eli-dl:DraftLegislationWork` (⊂ `eli:Work`) |
| `:BillExpression` | `metalex:BibliographicExpression` | Drop — `eli:LegalExpression` already declared as superclass; no ELI-DL expression class needed |
| `:BillFormat` | `metalex:BibliographicManifestation` | Drop — `eli:Format` already declared as superclass; ELI-DL has no manifestation class (only `eli-dl:produced_manifestation` property) |
| `:AmendmentList` | `metalex:BibliographicWork` | `eli-dl:AmendmentToDraftLegislationWork` (supports `has_part` for individual amendments) |
| `:BillAmendment` | (via `:AmendingStage` → `metalex:LegislativeModification`) | **Eliminate.** Split into: document → `eli-dl:AmendmentToDraftLegislationWork`; event → `eli-dl:LegislativeActivity`. Link with `eli-dl:created_a_realization_of`. |

### events.owl.ttl

| Events entity | Current Metalex superclass | ELI-DL replacement |
|---|---|---|
| `:JournalEvent` | `metalex:LegislativeCreation` | `eli-dl:LegislativeActivity` |
| `:AmendingStage` | `metalex:LegislativeModification` | `eli-dl:LegislativeActivity` (amendment semantics now on the Work via `eli-dl:AmendmentToDraftLegislationWork`) |
| `:BillDelivery` | `metalex:LegislativeDelivery` | `eli-dl:LegislativeActivity` (type the activity with an `eli-dl:ActivityType` individual, e.g. `:DeliveryActivity`) |
| `:BillDeliveryOutcome` | `metalex:Result` | `eli-dl:DecisionOutcome` |
| `:BillEventOutcome` | `metalex:Result` | `eli-dl:DecisionOutcome` |

---

## 2. Changes Required to Remove Metalex

### legislation.owl.ttl
1. **Remove `owl:imports` of `<http://www.metalex.eu/metalex/2008-05-02>`** — replace with `owl:imports <http://data.europa.eu/eli/eli-draft-legislation-ontology#>`.
2. **`:BillResource`** — remove `rdfs:subClassOf metalex:BibliographicWork`; add `rdfs:subClassOf eli-dl:DraftLegislationWork`.
3. **`:BillExpression`** — remove `rdfs:subClassOf metalex:BibliographicExpression` (retain `eli:LegalExpression`).
4. **`:BillFormat`** — remove `rdfs:subClassOf metalex:BibliographicManifestation` (retain `eli:Format`).
5. **`:AmendmentList`** — remove `rdfs:subClassOf metalex:BibliographicWork`; add `rdfs:subClassOf eli-dl:AmendmentToDraftLegislationWork`.
6. **`:BillAmendment`** — **eliminate entirely.** Replace with:
   - Document side: use `eli-dl:AmendmentToDraftLegislationWork` directly (link to draft via `eli-dl:amends_draft`).
   - Event side: use `eli-dl:LegislativeActivity` directly (link to document via `eli-dl:created_a_realization_of`, to stage via `eli-dl:occured_at_stage`).
   - Capture "amending stage" distinction as an annotation/property on `eli-dl:ProcessStage` individuals rather than a class.
7. Add `@prefix eli-dl:` declaration.

### events.owl.ttl
1. **Remove `owl:imports` of `<http://www.metalex.eu/metalex/2008-05-02>`** — add `owl:imports <http://data.europa.eu/eli/eli-draft-legislation-ontology#>`.
2. **`:JournalEvent`** — replace `rdfs:subClassOf metalex:LegislativeCreation` with `rdfs:subClassOf eli-dl:LegislativeActivity`.
3. **`:AmendingStage`** — replace `rdfs:subClassOf metalex:LegislativeModification` with `rdfs:subClassOf eli-dl:LegislativeActivity`.
4. **`:BillDelivery`** — replace `rdfs:subClassOf metalex:LegislativeDelivery` with `rdfs:subClassOf eli-dl:LegislativeActivity`.
5. **`:BillDeliveryOutcome`** — replace `rdfs:subClassOf metalex:Result` with `rdfs:subClassOf eli-dl:DecisionOutcome`.
6. **`:BillEventOutcome`** — replace `rdfs:subClassOf metalex:Result` with `rdfs:subClassOf eli-dl:DecisionOutcome`.
7. Add `@prefix eli-dl:` declaration.
8. Create `eli-dl:ActivityType` individuals: `:LegislativeCreationActivity`, `:LegislativeDeliveryActivity`, `:LegislativeModificationActivity` (see §5).

### Other files
- **README.md** — update references to Metalex; document ELI-DL adoption.
- **data/house.ttl** — remove `@prefix metalex:` if no metalex terms remain in use after migration.

---

## 3. Direct Metalex → ELI-DL Replacements

These are cases where a metalex class can be swapped one-for-one with an ELI-DL class:

| Metalex class | ELI-DL direct replacement | Notes |
|---|---|---|
| `metalex:BibliographicWork` | `eli-dl:DraftLegislationWork` | Both represent abstract legislative works; ELI-DL is more specific to draft legislation |
| `metalex:LegislativeCreation` | `eli-dl:LegislativeActivity` | Both model legislative process events |
| `metalex:LegislativeModification` | `eli-dl:LegislativeActivity` | ELI-DL separates amendment _document_ (AmendmentToDraftLegislationWork) from amendment _activity_ |
| `metalex:LegislativeDelivery` | `eli-dl:LegislativeActivity` | Type via `eli-dl:had_activity_type` to distinguish delivery from other activities |
| `metalex:Result` | `eli-dl:DecisionOutcome` | Both capture event/decision outcomes as typed concepts |

**No direct replacement exists for:**
- `metalex:BibliographicExpression` — ELI-DL defers to `eli:LegalExpression` (already used)
- `metalex:BibliographicManifestation` — ELI-DL defers to `eli:Format` / `eli:Manifestation` (already used)

---

## 4. Candidates for Direct ELI-DL Use (Eliminate Local Subclass)

These local classes _could_ be replaced by using ELI-DL classes directly, removing the need for an Oireachtas-specific subclass:

| Local class | ELI-DL class | Recommendation |
|---|---|---|
| `:AmendmentList` | `eli-dl:AmendmentToDraftLegislationWork` | **Use directly.** ELI-DL already supports amendment lists via `has_part`. No Oireachtas-specific properties are added. |
| `:BillAmendment` | `eli-dl:AmendmentToDraftLegislationWork` + `eli-dl:LegislativeActivity` | **Eliminate.** Split dual identity: document side → `eli-dl:AmendmentToDraftLegislationWork`; event side → `eli-dl:LegislativeActivity` (typed via `eli-dl:had_activity_type`). Link with `eli-dl:created_a_realization_of`. |
| `:BillResource` | `eli-dl:DraftLegislationWork` | **Use directly.** No Oireachtas-specific properties are defined on the class. Use `eli:type_document :Bill` to distinguish bills from other draft legislation works. |
| `:OriginalTitle` | `dct:alternative` | **Use directly.** `:OriginalTitle` is declared only as `rdfs:subPropertyOf dct:alternative` with no domain restriction and adds no extra semantics. Use `dct:alternative` instead. |
| `:BillStatus` | `eli-dl:ProcessStatus` | **Use directly.** Both are typed concept schemes for process/bill status. Retype status individuals as `eli-dl:ProcessStatus`. |
| `:BillVersion` | `eli-dl:LegislativeProcessWorkVersion` | **Eliminate.** Retype version individuals (`:AsInitiated`, `:VersionA`–`:VersionD`) as `eli-dl:LegislativeProcessWorkVersion`. Move from `eli:VersionTable` to a new `eli-dl:LegislativeProcessWorkVersion` concept scheme, or dual-list in both. |
| `:BillExpression` | `eli:LegalExpression` | **Use directly.** No labels, comments, or local properties defined. After dropping metalex, only `eli:LegalExpression` remains as superclass. |
| `:BillFormat` | `eli:Format` | **Use directly.** No labels, comments, or local properties defined. After dropping metalex, only `eli:Format` remains as superclass. |
| `:BillsBook` | `skos:OrderedCollection` | **Use directly.** Only adds labels ("Bills Book" / "Legislative Observatory") and uses standard `eli:has_part`/`eli:is_part_of`. No local properties. Use `skos:OrderedCollection` directly with labels on instances. |

### Classes to retain as local subclasses

None — all legislation.owl.ttl classes can be replaced by ELI-DL/ELI equivalents.

---

## 5. New `eli-dl:ActivityType` Individuals

Create the following `eli-dl:ActivityType` individuals to replace the distinctions previously expressed via the metalex class hierarchy:

| Individual | Replaces metalex class | Purpose |
|---|---|---|
| `:LegislativeCreationActivity` | `metalex:LegislativeCreation` | General journal/legislative event type (used via `eli-dl:had_activity_type` on `:JournalEvent` instances) |
| `:LegislativeDeliveryActivity` | `metalex:LegislativeDelivery` | Bill delivery/initiation activity type (used on `:BillDelivery` instances) |
| `:LegislativeModificationActivity` | `metalex:LegislativeModification` | Amending activity type (used on amendment-related `eli-dl:LegislativeActivity` instances) |

These are typed as `eli-dl:ActivityType` and placed in a concept scheme. Activities use `eli-dl:had_activity_type` to point to the relevant individual.

---

## Open Questions

1. **data/house.ttl** — Audit instance data for any direct metalex class/property usage beyond the prefix declaration.
