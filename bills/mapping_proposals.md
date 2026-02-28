# bill.json → Ontology Mapping: Proposals for Unclear/Incomplete Mappings

Proposals for fields where a relevant class or individual already exists but the
mapping is incomplete or ambiguous.

---

## Implementation status (Feb 2026)

| # | Topic | Status |
|---|---|---|
| 1 | `billNo`/`billYear`/`actNo`/`actYear` — `:legislativeYear` + annotations | **Done** |
| 2 | `stageOutcome: "Enacted"` — `eli-dl:process_status` annotation | **Done** |
| 3 | `source`/`sourceURI` — named individuals in `agents.owl.ttl` | **Done** |
| 4 | `originHouse` — `:originHouse` property | **Done** |
| 5 | `versions[].docType` — `eli:type_document` annotation | **Done** |
| 6 | `debates[].chamber.uri` — committee URI pattern + `:CommitteeTypeTable` | **Done** |
| 7A | Correction: remove `:hasBillType`; retype `:PublicBill`/`:PrivateBill` as `eli-dl:ProcessType` | **Done** |
| 7B | Correction: remove `:mostRecentStage`; annotate `eli-dl:latest_activity` | **Done** |

---

## 1. `billNo` / `billYear` / `actNo` / `actYear` — decomposed identifiers

### Problem

`eli:id_local` carries the full compound identifier (e.g. `2025/60`) but there
are no properties for the year and number components individually.

### Proposals

**`billNo`:** `eli-dl:process_number` (`xsd:string`, domain `eli-dl:Process`)
is the exact equivalent. No new property needed — annotate it:

```turtle
### In legislation.owl.ttl — annotation on imported ELI-DL property
eli-dl:process_number
    rdfs:comment "For Oireachtas bills: carries the bill number (e.g. \"60\")
    as a string. The compound identifier {year}/{number} is expressed via
    eli:id_local on the DraftLegislationWork."@en .
```

**`billYear` / `actYear`:** ELI-DL does not decompose the year. Add a single
datatype property covering both bill and act year:

```turtle
### In legislation.owl.ttl
:legislativeYear rdf:type owl:DatatypeProperty ;
    rdfs:range xsd:gYear ;
    rdfs:comment "The calendar year component of the bill or act identifier
    (from eli:id_local). Applied to eli-dl:DraftLegislationWork (billYear)
    and eli:LegalResource Act instances (actYear)."@en ;
    skos:prefLabel "Legislative year"@en .
```

> **Implemented with range `xsd:integer`** — `xsd:gYear` is not in the OWL 2
> DL datatype map and causes HermiT to error; `xsd:integer` is used instead.
> A comment on the property records this deviation.

**`actNo`:** Reuse `eli-dl:process_number` on the Act `eli:LegalResource`
instance. Annotate `eli:id_local` to clarify the compound/component split:

```turtle
### In legislation.owl.ttl — annotation on imported ELI property
eli:id_local
    rdfs:comment "For Oireachtas bills: the full compound identifier,
    e.g. \"2025/60\" for the bill or \"2025/18\" for the resulting act
    (eli:LegalResource). The year component alone is expressed via
    :legislativeYear; the number component alone via
    eli-dl:process_number."@en .
```

---

## 2. `stages[].stageOutcome: "Enacted"` — bridging `ProcessStatus` and `BillEventOutcome`

### Problem

`:EnactedBill` is an `eli-dl:ProcessStatus` (whole-process level). The JSON's
`stageOutcome` on the final stage event is an activity-level result, for which
the `BillEventOutcome` hierarchy would normally be used. There is no
`:BillEventOutcome` individual covering "Enacted", creating an apparent gap.

### Analysis

The string "Enacted" on the final stage activity is not a voted decision outcome
like `:Agreed` or `:DeclaredCarried` — it is the process-level result. The
correct modelling is:

- `eli-dl:process_status :EnactedBill` on the `LegislativeProcess` — process
  status.
- `eli-dl:activity_completed true` on the final `LegislativeActivity` — stage
  completion.

The `stageOutcome` string is redundant with process status and does **not**
require a new `BillEventOutcome` individual.

### Proposal

Annotation only — no new individual:

```turtle
### In legislation.owl.ttl
eli-dl:process_status
    rdfs:comment "For Oireachtas bills: set on the eli-dl:LegislativeProcess
    instance. The stages[].stageOutcome string \"Enacted\" maps here as
    :EnactedBill, not as a :BillEventOutcome. The final stage completion is
    separately recorded via eli-dl:activity_completed true on the final
    eli-dl:LegislativeActivity."@en .
```

---

## 3. `source` / `sourceURI` — API definition URIs not aligned to ontology individuals

### Problem

`bill.sourceURI` dereferences to
`https://data.oireachtas.ie/ie/oireachtas/def/bill-source/government` (an API
definition path). `eli-dl:was_submitted_by` requires an **instance**, but the
ontology currently only defines `:Government` as a class, not as a named
individual with that URI.

### Proposal

Add named individuals in `agents.owl.ttl` using the API `def/` URIs as the
individual IRIs directly. This avoids a `skos:exactMatch` bridge and means
`eli-dl:was_submitted_by` can point straight at the dereferenceable URI from the
JSON:

```turtle
### In agents.owl.ttl

<https://data.oireachtas.ie/ie/oireachtas/def/bill-source/government>
    rdf:type :Government , owl:NamedIndividual ;
    skos:prefLabel "The Government"@en ;
    skos:altLabel "Cabinet"@en .

<https://data.oireachtas.ie/ie/oireachtas/def/bill-source/private-member>
    rdf:type :PrivateMember , owl:NamedIndividual ;
    skos:prefLabel "Private Member"@en .
```

**Mapping:**
`bill.sourceURI` → `eli-dl:was_submitted_by
<https://data.oireachtas.ie/ie/oireachtas/def/bill-source/government>`

---

## 4. `originHouse` — no property for the house of introduction

### Problem

`eli-dl:was_submitted_by` carries the submitting **agent** (Government,
PrivateMember). No property exists for the originating **house** (Dáil or
Seanad). There is no close ELI-DL equivalent.

### Proposal

New property in `legislation.owl.ttl`:

```turtle
:originHouse rdf:type owl:ObjectProperty ;
    rdfs:domain eli-dl:DraftLegislationWork ;
    rdfs:range agents:House ;
    rdfs:comment "The house (Dáil Éireann or Seanad Éireann) in which the
    Bill was first introduced. Distinct from eli-dl:was_submitted_by, which
    identifies the submitting agent (Government or Private Member)."@en ;
    skos:prefLabel "Origin house"@en .
```

**Mapping:**
`bill.originHouseURI` →
`:originHouse <https://data.oireachtas.ie/house/dail>`

---

## 5. `versions[].docType` — `eli:type_document` placement ambiguous

### Problem

The `docType` field (`"bill"` or `"act"`) appears on version entries (i.e. at
expression level in the JSON). `eli:type_document` and the `:Bill`/`:Act`
individuals exist, but the property is not annotated for which FRBR level (Work
vs Expression) it should sit on.

### Proposal

Annotation on the imported ELI property in `legislation.owl.ttl`:

```turtle
eli:type_document
    rdfs:comment "For Oireachtas bills: apply at Work level
    (eli-dl:DraftLegislationWork or eli:LegalResource) only. Bill-stage
    version expressions (eli:LegalExpression) do not carry
    eli:type_document — their document type is inferred from the Work.
    Exception: the enacted act is a separate eli:LegalResource (typed
    eli:type_document :Act) linked to the DraftLegislationWork via
    eli:basis_for. The JSON field versions[].docType = \"act\" signals this
    transition to the Act LegalResource."@en .
```

No new property needed — modelling guidance annotation only.

---

## 6. `debates[].chamber.uri` for committees — no committee individual naming scheme

### Problem

Specific committee chambers are referred to only by the generic placeholder
`def/committee` plus a `showAs` label string. There are no named individual IRIs
for specific committees and no URI pattern is defined, making it impossible to
dereference or identify a specific committee as a distinct resource.

### Proposals

**Part A — URI pattern convention** (add as `rdfs:comment` on `members:Committee`
in `agents.owl.ttl`):

```
<https://data.oireachtas.ie/ie/oireachtas/committee/{slug}/{term-no}>

Example:
<https://data.oireachtas.ie/ie/oireachtas/committee/
    select_committee_on_finance_public_expenditure_public_service_reform_and_digitalisation_and_taoiseach/34>
```

The `{slug}` matches the segment already used in debate record URIs in the JSON
(e.g. in `debates[].uri`), enabling the IRI to be derived directly from existing
data without additional resolution.

**Part B — CommitteeType vocabulary** (new concept scheme + individuals):

```turtle
### In vocabulary.owl.ttl
:CommitteeTypeTable rdf:type owl:NamedIndividual , skos:ConceptScheme ;
    skos:prefLabel "Committee type table"@en ;
    rdfs:comment "The type of parliamentary committee. Members defined in
    agents.owl."@en .

### In agents.owl.ttl
:hasCommitteeType rdf:type owl:ObjectProperty ;
    rdfs:domain members:Committee ;
    rdfs:range skos:Concept ;
    skos:prefLabel "Has committee type"@en .

:SelectCommitteeType rdf:type owl:NamedIndividual , skos:Concept ;
    skos:prefLabel "Select Committee"@en ;
    skos:inScheme :CommitteeTypeTable ;
    skos:topConceptOf :CommitteeTypeTable .

:JointCommitteeType rdf:type owl:NamedIndividual , skos:Concept ;
    skos:prefLabel "Joint Committee"@en ;
    skos:inScheme :CommitteeTypeTable ;
    skos:topConceptOf :CommitteeTypeTable .

:SpecialCommitteeType rdf:type owl:NamedIndividual , skos:Concept ;
    skos:prefLabel "Special Committee"@en ;
    skos:inScheme :CommitteeTypeTable ;
    skos:topConceptOf :CommitteeTypeTable .
```

---

## 7. Corrections to previous session additions

Two properties added in the previous session duplicate pre-existing ELI-DL
properties and should be corrected before implementation:

| Added previously | Pre-existing ELI-DL equivalent | Action |
|---|---|---|
| `:hasBillType` (domain `DraftLegislationWork`, range `eli:ResourceType`) | `eli-dl:process_type` (domain `Process`, range `eli-dl:ProcessType`) | Remove `:hasBillType`; retype `:PublicBill` / `:PrivateBill` as `eli-dl:ProcessType` individuals |
| `:mostRecentStage` (domain `DraftLegislationWork`, range `LegislativeActivity`) | `eli-dl:latest_activity` (domain `Process`, range `eli-dl:Activity`) | Remove `:mostRecentStage`; annotate `eli-dl:latest_activity` for Oireachtas usage |

### Correction A — `:hasBillType` → `eli-dl:process_type`

Remove `:hasBillType` from `legislation.owl.ttl`. Retype `:PublicBill` and
`:PrivateBill` from `eli:ResourceType` to `eli-dl:ProcessType`, and move them
from `:BillTypeTable` (an `eli:ResourceType` scheme) to a `ProcessType`-based
scheme — or retain `:BillTypeTable` as a `skos:ConceptScheme` with `ProcessType`
members (already valid since `eli-dl:ProcessType rdfs:subClassOf skos:Concept`).

```turtle
### Revised individuals in legislation.owl.ttl
:PublicBill rdf:type eli-dl:ProcessType , owl:NamedIndividual ;
    skos:prefLabel "Public Bill"@en ;
    skos:inScheme :BillTypeTable ;
    skos:topConceptOf :BillTypeTable .

:PrivateBill rdf:type eli-dl:ProcessType , owl:NamedIndividual ;
    skos:prefLabel "Private Bill"@en ;
    skos:inScheme :BillTypeTable ;
    skos:topConceptOf :BillTypeTable .
```

Annotate `eli-dl:process_type` in `legislation.owl.ttl`:

```turtle
eli-dl:process_type
    rdfs:comment "For Oireachtas bills: set to :PublicBill or :PrivateBill
    on the eli-dl:LegislativeProcess instance. Replaces the former
    :hasBillType property (added in Feb 2026 session, now removed)."@en .
```

### Correction B — `:mostRecentStage` → `eli-dl:latest_activity`

Remove `:mostRecentStage` from `events.owl.ttl`. Annotate
`eli-dl:latest_activity` in `legislation.owl.ttl`:

```turtle
eli-dl:latest_activity
    rdfs:comment "For Oireachtas bills: points to the most recently
    completed eli-dl:LegislativeActivity (stage) instance. Maps to the
    JSON field bill.mostRecentStage. Replaces the former :mostRecentStage
    property (added in Feb 2026 session, now removed)."@en .
```

---

## Summary of files to change

| File | Change | Status |
|---|---|---|
| `legislation.owl.ttl` | Add `:legislativeYear`; add `:originHouse`; annotate `eli-dl:process_number`, `eli:id_local`, `eli-dl:process_status`, `eli:type_document`, `eli-dl:process_type`, `eli-dl:latest_activity`; remove `:hasBillType`; retype `:PublicBill`/`:PrivateBill` as `eli-dl:ProcessType` | **Done** |
| `agents.owl.ttl` | Add `<.../def/bill-source/government>` and `<.../def/bill-source/private-member>` named individuals; add `:hasCommitteeType` property + `:SelectCommitteeType`, `:JointCommitteeType`, `:SpecialCommitteeType` individuals; add `rdfs:comment` URI pattern on `members:Committee` | **Done** |
| `events.owl.ttl` | Remove `:mostRecentStage` | **Done** |
| `vocabulary.owl.ttl` | Add `:CommitteeTypeTable` concept scheme | **Done** |
