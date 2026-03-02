# Debates Ontology — High-Level Outline

## Design Anchors

- **FRBR document layer** — `:DebateRecord` is a `foaf:Document`; legislative connection is optional, not structural
- **Sitting as activity** maps to `eli-dl:Activity` — kept broad because a sitting may mix legislation with questions, statements, etc.
- **Legislative section** — a `:DebateSection` with `refersToEvent` is *additionally* typed `eli-dl:LegislativeActivity` (multiple typing, valid OWL); this is the correct granularity because ELI-DL scopes that class to a bounded legislative activity, which a section matches better than a whole mixed sitting
- **Division / vote** maps to `eli-dl:Vote` + `eli-dl:Decision`
- **Speaker participation** maps to `eli-dl:Participation` + `eli-dl:ParticipationRole`
- All classes import from `events.owl` and `agents.owl` per the existing chain

---

## Source files examined

| File | Lines | Notes |
|---|---|---|
| `data/debates/dail_2015-07-02.akn.xml` | 8355 | Report Stage (Resumed) with amendments and divisions; questions |
| `data/debates/dail_2026-02-26.akn.xml` | 6989 | Topical issues, statements, motions, divisions with staon (abstain) |

---

## Classes

| Class | Superclass(es) | Maps to AKN |
|---|---|---|
| `:DebateRecord` | `foaf:Document` | `FRBRWork` — the debate as a distinct intellectual work for a house/date |
| `:DebateExpression` | *(bare OWL class)* | `FRBRExpression` — language-specific version (eng / gle / mul); `rdfs:comment` notes FRBR correspondence; no superclass added to avoid FRBR import dependency |
| `:DebateSitting` | `eli-dl:Activity` | The sitting *activity* that produces a `:DebateRecord`; `eli-dl:activity_date` carries the date. Always `eli-dl:Activity`; never typed `eli-dl:LegislativeActivity` because a sitting may be mixed |
| `:DebateSection` | — | `debateSection` — a topic-bounded section; nests recursively; actual `@name` values in use: `debate`, `question`, `questions`, `amendment`, `division`, `ta`, `nil`, `staon`, `prelude`, `topical`, `statement`, `motion`. Instances with `:refersToEvent` are *additionally* typed `eli-dl:LegislativeActivity` (see Typing Conventions below) |
| `:Speech` | — | `speech` — oral contribution by a Member or witness |
| `:Summary` | — | `summary` — narrative / procedural text not attributed to a speaker |
| `:ParliamentaryQuestion` | — | `question` — a parliamentary question (oral or written) |
| `:Division` | `eli-dl:Vote` | `debateSection[@name='division']` — a division in the chamber; three sub-sections: `ta`, `nil`, `staon` |

---

## Properties

### On `:DebateRecord`

| Property | Range | Note |
|---|---|---|
| `eli-dl:parliamentary_term` | `:HouseTerm` | Which Dáil / Seanad term |
| `:inHouse` | `:House` | House or committee; reuses `agents.owl` `:House` |
| `:debateDate` | `xsd:dateTime` | Date of sitting; from AKN `FRBRWork/FRBRdate`. `xsd:dateTime` used for OWL 2 DL compatibility (HermiT does not support `xsd:date`) |
| `:debateType` | `xsd:string` | AKN `FRBRname/@value` sub-type where present (e.g. `"debate"`, `"writtens"`) |
| `:hasSection` | `:DebateSection` | Top-level sections of the record |

### On `:DebateSitting`

| Property | Range | Note |
|---|---|---|
| `eli-dl:activity_date` | `xsd:date` | ELI-DL activity date |
| `:relatedProcess` | `eli-dl:LegislativeProcess` | 0..* — convenience link; present when the sitting contains at least one legislative section |
| `eli-dl:had_participation` | `eli-dl:Participation` | Chair / presiding officer participation |
| `:producedRecord` | `:DebateRecord` | Links the activity to its documentary output |

### On `:DebateSection`

| Property | Range | Note |
|---|---|---|
| `:sectionName` | `xsd:string` | AKN `@name` value; see class table above for values observed in the wild |
| `:refersToEvent` | `:BillEvent` or `eli:LegalResource` | 0..1 — AKN `debateSection/@refersTo`; range covers both bill stages (`TLCEvent`) and bill works (`TLCReference`) as found in the XML. Presence triggers additional `eli-dl:LegislativeActivity` typing |
| `eli-dl:occured_at_stage` | `eli-dl:ProcessStage` | Present when additionally typed `eli-dl:LegislativeActivity`; records the bill stage (e.g. Second Stage, Report Stage) |
| `eli-dl:forms_part_of` | `eli-dl:LegislativeProcess` | ELI-DL standard link from activity to process; use on legislative sections in preference to a custom property |
| `:hasSubSection` | `:DebateSection` | Nested sections; used for amendment sub-sections, division ta/nil/staon, question threads |
| `:hasSpeech` | `:Speech` | |
| `:hasSummary` | `:Summary` | |
| `:hasDivision` | `:Division` | |

### On `:Speech`

| Property | Range | Note |
|---|---|---|
| `eli-dl:had_participation` | `eli-dl:Participation` | Canonical path for speaker + role; `speech/@by` → person, `speech/@as` → `TLCRole` |
| `:speaker` | `:Member` | Direct shortcut to speaker; `eli-dl:Participation` is canonical |
| `:recordedTime` | `xsd:dateTime` | Timestamp from AKN `from/recordedTime/@time`; accurate to ~5–10 min |

### On `:ParliamentaryQuestion`

| Property | Range | Note |
|---|---|---|
| `:askedBy` | `:Member` | `question/@by` → `TLCPerson` |
| `:directedTo` | `eli-dl:ParticipationRole` | `question/@to` → `TLCRole` for the Minister to whom the question is addressed |

### On `:Division`

| Property | Range | Note |
|---|---|---|
| `:taCount` | `xsd:integer` | Votes in favour (`#ta`) |
| `:nilCount` | `xsd:integer` | Votes against (`#nil`) |
| `:staonCount` | `xsd:integer` | Abstentions (`#staon`); present in 2026 data, absent in older data |
| `:divisionOutcome` | `eli-dl:DecisionOutcome` | Named individual `:DeclaredCarried` or `:DeclaredLost` |
| `:refersToProposal` | `:DebateSection` or `:BillEvent` | Subject of the vote; from `voting/@refersTo` in AKN analysis block |
| `:votedFor` | `:Member` | Members voting Tá; from `debateSection[@name='ta']/p/person` |
| `:votedAgainst` | `:Member` | Members voting Níl; from `debateSection[@name='nil']/p/person` |
| `:abstained` | `:Member` | Members recorded Staon; from `debateSection[@name='staon']/p/person` |

---

## Named Individuals

### Decision outcomes (typed `eli-dl:DecisionOutcome`)

| Individual | AKN `TLCConcept` | IRI in 2026 data |
|---|---|---|
| `:DeclaredCarried` | `#carried` | `oireachtas#DeclaredCarried` |
| `:DeclaredLost` | `#lost` | `oireachtas#DeclaredLost` |

### Vote categories (typed `skos:Concept`; used in `count/@refersTo`)

| Individual | AKN `TLCConcept` | Note |
|---|---|---|
| `:TáVote` | `#ta` | Votes in favour |
| `:NílVote` | `#nil` | Votes against |
| `:StaonVote` | `#staon` | Abstentions |

### Participation roles (typed `eli-dl:ParticipationRole`)

| Individual | Note |
|---|---|
| `:ChairRole` | Ceann Comhairle / Cathaoirleach acting as presiding officer; from `TLCRole` `ceann_comhairle` / `cathaoirleach` |
| `:WitnessRole` | Non-member witness at committee |

---

## Typing Conventions

| Condition | Additional type on `:DebateSection` instance |
|---|---|
| `debateSection/@refersTo` links to a bill stage or bill work | `eli-dl:LegislativeActivity` |
| No `@refersTo` present (questions, statements, topical, motion, prelude, etc.) | none — remains plain `:DebateSection` |

When a `:DebateSection` is typed `eli-dl:LegislativeActivity`, the following ELI-DL properties become applicable on that instance:
- `eli-dl:occured_at_stage` → the bill stage (e.g. Second Stage)
- `eli-dl:forms_part_of` → the `eli-dl:LegislativeProcess` for the bill
- `eli-dl:had_participation` → mover / rapporteur roles at that stage

---

## Non-legislative Debate Modelling

| Debate type | `:DebateSitting` type | Section-level `eli-dl:LegislativeActivity`? | `:relatedProcess` on sitting |
|---|---|---|---|
| Question Time, Statements, Topical Debates, Motions | `eli-dl:Activity` only | No | absent |
| Purely legislative sitting (e.g. Committee Stage only) | `eli-dl:Activity` only | Yes — on the debate section(s) | present |
| Mixed sitting (common in Dáil) | `eli-dl:Activity` only | Yes — on legislative sections only; non-legislative sections untyped | present |

---

## Open Questions

1. ~~**`DebateExpression` superclass**~~ — resolved: bare OWL class with `rdfs:comment` noting FRBR correspondence. Superclass can be added if FRBR is ever imported for another reason.
2. **`answer` element** — not observed in the two sample files, but described in the schema documentation. Hold for future data.
3. **`rollCall`** — similarly described but absent from samples. Hold for future data.

---

## Deferred / Out of Scope (stub)

- Full FRBR Manifestation layer (XML file IRIs)
- Inline `entity/@refersTo` markup for amendments
- Image and table content
- Bilingual heading deduplication
