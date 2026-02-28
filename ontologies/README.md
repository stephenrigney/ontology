## Oireachtas Ontology — Structure and Contents

The ontology is split into six sub-ontologies, each covering one of the four declared areas of the Oireachtas ontology, plus a shared controlled vocabulary layer and a detailed membership model. A root umbrella file imports all six.

---

### File Overview

| File | Ontology IRI | Description |
|---|---|---|
| [oireachtas.owl.ttl](oireachtas.owl.ttl) | `https://data.oireachtas.ie/ontology` | Root umbrella — imports the six sub-ontologies below |
| [agents.owl.ttl](agents.owl.ttl) | `https://data.oireachtas.ie/ontology/agents` | Persons, roles and organisations |
| [events.owl.ttl](events.owl.ttl) | `https://data.oireachtas.ie/ontology/events` | Journal events, bill stages and procedural outcomes |
| [legislation.owl.ttl](legislation.owl.ttl) | `https://data.oireachtas.ie/ontology/legislation` | Legislative documents, versions and statuses |
| [members.owl.ttl](members.owl.ttl) | `https://data.oireachtas.ie/ontology/members` | Membership, roles, party groupings and government tiers |
| [vocabulary.owl.ttl](vocabulary.owl.ttl) | `https://data.oireachtas.ie/ontology/vocabulary` | SKOS controlled vocabularies (concept schemes) |
| [debates.owl.ttl](debates.owl.ttl) | `https://data.oireachtas.ie/ontology/debates` | Official Report and debates *(stub — reserved for future use)* |

---

### Import Chain

```
oireachtas.owl
├── agents.owl
│   └── (imports: ELI, ELI-DL, W3C org)
├── events.owl
│   └── (imports: agents.owl, ELI-DL, W3C time)
├── legislative.owl
│   └── (imports: events.owl, ELI, ELI-DL)
├── members.owl
│   └── (imports: agents.owl, ELI-DL, W3C org, FOAF)
├── vocabulary.owl
│   └── (imports: events.owl, legislative.owl)
└── debates.owl
    └── (imports: events.owl, agents.owl)
```

---

### agents.owl

**IRI:** `https://data.oireachtas.ie/ontology/agents`

Defines the organisations, roles and persons involved in the legislative process.

> **ELI-DL alignment (2026):** `eli-dl` import added. `:BillSource` class and `:Mover` class eliminated. `:Government`, `:PrivateMember` and `:PrivateSponsor` no longer subclasses of `:BillSource`. Canonical submitter linking now via `eli-dl:was_submitted_by`. Activity-level participation (e.g. who moved a bill) now via `eli-dl:had_participation` with `eli-dl:ParticipationRole` individuals defined in `members.owl`.
>
> **Namespace reconciliation (2026):** `foaf:Person` added as second superclass on `:Member` alongside `rda:C10004` (required for ELI-DL `eli:Person` range entailment via `eli:Person rdfs:subClassOf foaf:Person`).
>
> **RDA cleanup (2026):** `rda:C10005` removed as superclass of `:Oireachtas` (retains `org:FormalOrganization`). `rda:C10004` removed as superclass of `:Member` (retains `foaf:Person`, the direct superclass satisfying ELI-DL entailments). `rda:C10004` + `rda:C10005` removed from `:PrivateSponsor` (replaced with `foaf:Agent` — the common FOAF supertype covering both individual and corporate sponsors; already in the import chain via ELI-DL). The RDA namespace is no longer referenced anywhere in the ontology.
>
> **House / HouseTerm refactoring (2026):** `:Chamber` renamed to `:House` (continuous constitutional institution). Former `:House` (bounded sitting period) renamed to `:HouseTerm`. Two disjoint subclasses `:DailTerm` and `:SeanadTerm` added under `:HouseTerm`. Named individuals `<.../house/dail>` and `<.../house/seanad>` now typed `:House`. The `:hasTerm` / `:termOf` property pair updated accordingly.
>
> **Government three-tier refactoring (2026):** `:Government` gains `skos:altLabel "Cabinet"@en` and an updated `rdfs:comment` explaining the constitutional basis and three-tier structure. See `members.owl` for the new `:GovernmentBenches`, `:GovernmentExecutive` and `:MinisterOfState` classes.

#### Classes

| Class | Superclass(es) | Description |
|---|---|---|
| `:Oireachtas` | `org:FormalOrganization` | The Houses of the Oireachtas as a legislative body |
| `:House` | `:Oireachtas` | Dáil Éireann or Seanad Éireann as a continuous constitutional institution, persisting across successive terms. Named individuals `<.../house/dail>` and `<.../house/seanad>` are instances. Committee chambers are also instances. |
| `:HouseTerm` | `:Oireachtas` | A bounded parliamentary sitting period. Instances should additionally be typed as `eli-dl:ParliamentaryTerm` to enable use of `eli-dl:parliamentary_term` on activities and works. |
| `:DailTerm` | `:HouseTerm` | A specific numbered term of Dáil Éireann (e.g. the 33rd Dáil). Disjoint with `:SeanadTerm`. |
| `:SeanadTerm` | `:HouseTerm` | A specific numbered term of Seanad Éireann. |
| `:Government` | `:Oireachtas` | The Government as defined by Article 28 of the Constitution — the collective executive body with legal personality. Also known informally as the Cabinet (`skos:altLabel "Cabinet"`). Membership confined to persons holding a `members:CabinetMember` role (`members:Taoiseach`, `members:Tanaiste` or `members:Minister`). |
| `:Member` | `foaf:Person` | A Member of one of the Houses. Canonical class replacing the former `members:Member`. `foaf:Person` is the direct superclass — satisfies ELI-DL `eli:Person` range entailment via `eli:Person rdfs:subClassOf foaf:Person`. |
| `:Minister` | `:Member` | A Member who also holds a ministerial office. Cross-referenced to `members:MinisterRole` via `org:holds` / `org:heldBy` bridge axioms in `members.owl`. |
| `:PrivateMember` | `:Member` | A Member who is not a Member of Government |
| `:PrivateSponsor` | `foaf:Agent` | A non-Member person or body that introduces legislation. `foaf:Agent` is the common FOAF supertype of `foaf:Person` (individual sponsors) and `foaf:Organization` (corporate bodies). |

#### Eliminated classes

| Former class | Reason | Replacement |
|---|---|---|
| `:BillSource` | Submitter type is expressed via `eli-dl:was_submitted_by` (Process → Agent) | Use `eli-dl:was_submitted_by` on `eli-dl:LegislativeProcess` instances |
| `:Mover` | Activity-level participation is expressed via `eli-dl:Participation` + `eli-dl:ParticipationRole` | Use `eli-dl:had_participation` with `:MoverRole` (defined in `members.owl`) |

#### Object Properties

| Property | Domain | Range | Notes |
|---|---|---|---|
| `:hasTerm` | `:House` | `:HouseTerm` | `owl:inverseOf :termOf` |
| `:termOf` | `:HouseTerm` | `:House` | |

#### Annotations on imported properties

| Property | Annotation |
|---|---|
| `eli:passed_by` | Range restricted to `:Oireachtas` |
| `eli-dl:was_submitted_by` | Documents that range includes `:Government`, `:PrivateMember`, `:PrivateSponsor`; replaces `:BillSource` |
| `eli-dl:had_participation` | Documents use with `:MoverRole` / `:RapporteurRole` on `:JournalEvent` activities; replaces `:Mover` |

#### Named Individuals

| Individual | Type | Label |
|---|---|---|
| `<.../house/dail>` | `:House` | Dáil Éireann |
| `<.../house/seanad>` | `:House` | Seanad Éireann |

---

### members.owl

**IRI:** `https://data.oireachtas.ie/ontology/members`

Defines the detailed membership, role and party structures of the Houses of the Oireachtas. Covers Deputies, Senators, Cabinet membership, committee membership, party groupings and parliamentary titles.

> **ELI-DL alignment (2026):** `eli-dl` import added. `org:Role rdfs:subClassOf :OireachtasMember` axiom corrected to `:OireachtasMember rdfs:subClassOf org:Role`. `:MoverRole` and `:RapporteurRole` added as `eli-dl:ParticipationRole` individuals.
>
> **Namespace reconciliation (2026, in progress):** `members.owl` now imports `agents.owl`. The `members:Member` class has been eliminated — all references replaced with `agents:Member` (the canonical class). `members:Government` (whip side) resolved by rename — see three-tier Government refactoring note below. Remaining duplicates (Minister person vs role, HousesOfTheOireachtas) are unresolved — see [Future Work](#future-work--namespace-reconciliation) below.
>
> **House / HouseTerm refactoring (2026):** `members:Chamber` renamed to `members:House`. One-way bridge `members:House rdfs:subClassOf agents:House` added. `members:Dail` and `members:Seanad` gain `agents:DailTerm` and `agents:SeanadTerm` as additional superclasses respectively. `:DailMembership` and `:SeanadMembership` added as disjoint subclasses of `:OireachtasMembership`. `:inHouseTerm` property added (range `agents:HouseTerm`) alongside the re-ranged `:isOireachtasMembershipOf` (range `agents:House`). `Deputy owl:disjointWith Senator` removed from person level; disjointness now expressed via `DailMembership owl:disjointWith SeanadMembership`. Spurious `:Dail` and `:Seanad` superclasses removed from `:DailConstituency` and `:SeanadPanel` respectively.
>
> **Government three-tier refactoring (2026):** `members:Government` (whip side) renamed to `members:GovernmentBenches`. Former vestigial `members:Cabinet` class (incorrectly a subclass of the whip side) removed — the constitutional Cabinet is `agents:Government`. Three tiers now defined: (1) `agents:Government` — constitutional executive body, membership confined to `members:CabinetMember` role-holders (TaoiseachRole, TanaisteRole, MinisterRole); (2) `members:GovernmentExecutive` — Government plus `members:MinisterOfStateRole` role-holders; (3) `members:GovernmentBenches` — GovernmentExecutive plus other OireachtasMembers under the government whip. `members:MinisterOfStateRole` and `members:MinisterOfStateMembership` added; `MinisterOfStateRole owl:disjointWith CabinetMember`. `:isHeadOf` and `:isDeputyHeadOf` re-ranged to `agents:Government`. Four sub-properties added: `:isHeadOfExecutive`, `:isHeadOfBenches` (sub-properties of `:isHeadOf`, domain `:TaoiseachRole`) and `:isDeputyHeadOfExecutive`, `:isDeputyHeadOfBenches` (sub-properties of `:isDeputyHeadOf`, domain `:TanaisteRole`) to assert headship at each wider tier. `:PartyInGovernment` allValuesFrom updated to `members:GovernmentBenches`.
>
> **Role class rename (2026):** All four `members` role classes renamed for unambiguous person/role distinction: `members:Minister` → `members:MinisterRole`, `members:Taoiseach` → `members:TaoiseachRole`, `members:Tanaiste` → `members:TanaisteRole`, `members:MinisterOfState` → `members:MinisterOfStateRole`. `org:holds` / `org:heldBy` bridge axioms added in `members.owl` connecting `agents:Minister` (person) ↔ `members:MinisterRole` (role). `rdfs:comment` added to `agents:Minister` cross-referencing the bridge.

#### Classes (selected)

| Class | Superclass(es) | Description |
|---|---|---|
| `:OireachtasMember` | `org:Role`, `agents:Member` (inferred) | An elected role — equivalentClass `Deputy ∪ Senator`; inferred as subclass of `agents:Member` via intersection expressions |
| `:Deputy` | `:OireachtasMember` | Member elected to the Dáil. Inferred for any `agents:Member` who has a `:DailMembership` record. A person may be both a Deputy and a Senator across their career. |
| `:Senator` | `:OireachtasMember` | Member of the Seanad. Inferred via `:SeanadMembership`. |
| `:MinisterRole` | `:CabinetMember` | Ministerial office role in `agents:Government`. `skos:prefLabel "Minister"`. Counterpart person class: `agents:Minister`. |
| `:TaoiseachRole` | `:CabinetMember` | Role of Taoiseach (Head of Government). `owl:disjointWith :TanaisteRole`. |
| `:TanaisteRole` | `:CabinetMember` | Role of Tánaiste (Deputy Head of Government). `owl:disjointWith :TaoiseachRole`. |
| `:CabinetMember` | `org:Role` | Abstract role in `agents:Government`. Subclasses: `:TaoiseachRole`, `:TanaisteRole`, `:MinisterRole`. Holders must be `:OireachtasMembers`. |
| `:MinisterOfStateRole` | `org:Role` | Role of a Minister of State. `owl:disjointWith :CabinetMember`. Holder must be an `:OireachtasMember`. |
| `:GovernmentExecutive` | `:HousesOfTheOireachtas` | The wider executive — `agents:Government` (TaoiseachRole, TanaisteRole, MinisterRole holders) plus MinisterOfStateRole holders. OWL restriction: `hasMembers allValuesFrom (CabinetMembership ∪ MinisterOfStateMembership)`. |
| `:GovernmentBenches` | `:SidesOfHouse` | The parliamentary whip bloc supporting the Government. Comprises `:GovernmentExecutive` members plus other OireachtasMembers under the government whip. `owl:disjointWith :Opposition`. Replaces the former `:Government` (whip side). |
| `:Opposition` | `:SidesOfHouse` | The opposition |
| `:House` | `:HousesOfTheOireachtas`, `agents:House` | equivalentClass `Dail ∪ Seanad`. Plenary houses only; committee chambers are `agents:House` instances outside this extension. One-way bridge to `agents:House`. |
| `:Dail` | `:House`, `agents:DailTerm` | Dáil Éireann as a membership container. Bridge to `agents:DailTerm` enables term-level typing. |
| `:Seanad` | `:House`, `agents:SeanadTerm` | Seanad Éireann as a membership container. |
| `:Committee` | `:HousesOfTheOireachtas` | A parliamentary committee |
| `:PartyGrouping` | `foaf:Group` | equivalentClass `Independent ∪ Party` |
| `:OireachtasMembership` | `:MembersMembership` | Abstract superclass for house and committee membership records |
| `:DailMembership` | `:OireachtasMembership` | Membership record for a specific Dáil term. Requires `inHouseTerm someValuesFrom agents:DailTerm`. Disjoint with `:SeanadMembership`. |
| `:SeanadMembership` | `:OireachtasMembership` | Membership record for a specific Seanad term. Requires `inHouseTerm someValuesFrom agents:SeanadTerm`. |
| `:CabinetMembership` | `:MembersMembership` | Record of an `agents:Member` holding a `:CabinetMember` role (`:TaoiseachRole`, `:TanaisteRole` or `:MinisterRole`) in `agents:Government`. Linked to role via `:hasCabinetRole`. |
| `:MinisterOfStateMembership` | `:MembersMembership` | Record of an `agents:Member` holding a `:MinisterOfStateRole`. Linked to role via `:hasMinisterOfStateRole`. |
| `:CommitteeMembership` | `:MembersMembership` | Membership of a committee |
| `:DateRange` | `:Temporal` | Temporal extent for org:Membership subclasses; start/end typed `xsd:dateTime` (note: `xsd:date` is not in the OWL 2 DL datatype map) |

#### Object Properties (selected)

| Property | Domain | Range | Notes |
|---|---|---|---|
| `:isOireachtasMembershipOf` | `:OireachtasMembership` | `agents:House` | The continuous house (`<.../house/dail>`) |
| `:inHouseTerm` | `:OireachtasMembership` | `agents:HouseTerm` | The specific numbered term (`<.../house/dail/33>`); same individual as `eli-dl:parliamentary_term` on associated activities |
| `:isHeadOf` | `:TaoiseachRole` | `agents:Government` | Links a TaoiseachRole instance to the constitutional Government it heads |
| `:isHeadOfExecutive` | `:TaoiseachRole` | `:GovernmentExecutive` | Sub-property of `:isHeadOf`; asserts headship of the wider executive (Government + Ministers of State) |
| `:isHeadOfBenches` | `:TaoiseachRole` | `:GovernmentBenches` | Sub-property of `:isHeadOf`; asserts headship of the full parliamentary whip bloc |
| `:isDeputyHeadOf` | `:TanaisteRole` | `agents:Government` | Links a TanaisteRole instance to the constitutional Government |
| `:isDeputyHeadOfExecutive` | `:TanaisteRole` | `:GovernmentExecutive` | Sub-property of `:isDeputyHeadOf`; asserts deputy headship of the GovernmentExecutive |
| `:isDeputyHeadOfBenches` | `:TanaisteRole` | `:GovernmentBenches` | Sub-property of `:isDeputyHeadOf`; asserts deputy headship of the GovernmentBenches |
| `:hasMinisterOfStateRole` | `:MinisterOfStateMembership` | `:MinisterOfStateRole` | Links a membership record to the specific MinisterOfStateRole held |

#### Named Individuals — ELI-DL Participation Roles

| Individual | Type | Purpose |
|---|---|---|
| `:MoverRole` | `eli-dl:ParticipationRole` | Role of a Member who moves a Bill, amendment or motion. Set via `eli-dl:participation_role` on `eli-dl:Participation` instances. Replaces the former `agents:Mover` class. |
| `:RapporteurRole` | `eli-dl:ParticipationRole` | Role of a Member appointed as rapporteur. Set via `eli-dl:participation_role`; see also `eli-dl:had_responsible_person` for the shorthand property. |

---

### Future Work

| Item | Description |
|---|---|
| ~~RDA usage — `:PrivateSponsor`~~ | **Resolved (2026).** `rda:C10004` and `rda:C10005` replaced with `foaf:Agent` on `agents:PrivateSponsor`. The RDA namespace (`http://rdaregistry.info/Elements/c/`) is no longer referenced anywhere in the ontology. `rda:` row removed from Referenced External Schemas. |
| Named individual IRI path | Decide whether continuous-house individual IRIs use the short form `<https://data.oireachtas.ie/house/dail>` (current) or the API-path form `<https://data.oireachtas.ie/ie/oireachtas/house/dail>`. Relevant only when the data conversion layer is built. |

---

### events.owl

**IRI:** `https://data.oireachtas.ie/ontology/events`

Defines the procedural events that occur during a Bill's lifecycle, including stages, delivery methods and outcomes.

#### Classes

| Class | Superclass(es) | Description |
|---|---|---|
| `:EventDate` | `time:TemporalEntity` | A date associated with an event |
| `:JournalEvent` | `eli-dl:LegislativeActivity` | Any event recorded in the Order Paper or Official Report |
| `:BillEvent` | `:JournalEvent` | A procedural event in the lifecycle of a Bill |
| `:BillStage` | `:JournalEvent` | A formal stage of the Bill's passage |
| `:AmendingStage` | `eli-dl:LegislativeActivity`, `:BillStage` | A stage at which amendments may be made |
| `:BillDelivery` | `eli-dl:LegislativeActivity` | The method by which a Bill is initiated |
| `:BillDeliveryOutcome` | `eli-dl:DecisionOutcome` | The outcome of a Bill's introduction |
| `:BillEventOutcome` | `eli-dl:DecisionOutcome` | The outcome of a motion, question or amendment |

#### Object Properties

| Property | Domain | Range |
|---|---|---|
| `:InChamber` | `:BillEvent` | `agents:House` |
| `:commenced` | `time:TemporalEntity` | `:EventDate` |
| `:elected` | `time:TemporalEntity` | `:EventDate` |
| `:ended` | `time:TemporalEntity` | `:EventDate` |

#### Named Individuals — Bill Stages

`FirstStage`, `SecondStage`, `OrderSecondStage`, `SecondSubStages`, `CommitteeStage`, `OrderCommitteeStage`, `CommitteeSubStages`, `ReportStage`, `OrderReportStage`, `ReportSubStages`, `FifthStage`, `AllStages`

#### Named Individuals — Other Bill Events

`BallotOrder`, `BillAmend`, `BillAmend2Amend`, `BillRecommendation`, `DailAmdSeanad`, `DischargeOrderSecondStage`, `DischargeSecondStage`, `EarlySign`, `FinancialResolution`, `InstrCommittee`, `LeaveToWithdraw`, `RecommitBill`, `RefCommittee`, `RestoreBill`, `SeanadAmdDail`, `VoterInfo`

#### Named Individuals — Bill Event Outcomes

`Agreed`, `DeclaredCarried`, `DeclaredLost`, `NotMoved`, `Withdrawn`

#### Named Individuals — Bill Delivery Methods

`Application`, `Introduction`, `Presentation`

#### Named Individuals — Bill Delivery Outcomes

`Examiner`, `Introduced`, `Presented`, `Refused`

#### Named Individuals — ELI-DL Activity Types

| Individual | Replaces | Purpose |
|---|---|---|
| `:LegislativeCreationActivity` | `metalex:LegislativeCreation` | General legislative event type; set via `eli-dl:had_activity_type` on `:JournalEvent` instances |
| `:LegislativeDeliveryActivity` | `metalex:LegislativeDelivery` | Bill delivery/initiation type; set via `eli-dl:had_activity_type` on `:BillDelivery` instances |
| `:LegislativeModificationActivity` | `metalex:LegislativeModification` | Amending activity type; set via `eli-dl:had_activity_type` on `:AmendingStage` and amendment `eli-dl:LegislativeActivity` instances |

---

### legislation.owl

**IRI:** `https://data.oireachtas.ie/ontology/legislation`

Defines the legislative documents published by the Oireachtas, including Bills, Acts, versions, expressions, formats and statuses.

> **ELI-DL migration (2026):** All local subclasses have been eliminated. Each is now replaced by the appropriate ELI-DL or ELI class used directly. The local `metalex` import has been replaced by `eli-dl`. The `:OriginalTitle` data property has been removed in favour of `dct:alternative`.

#### Eliminated local classes — use ELI-DL/ELI equivalents directly

| Former class | Direct replacement | Notes |
|---|---|---|
| `:BillResource` | `eli-dl:DraftLegislationWork` | Use `eli:type_document :Bill` to distinguish bills |
| `:BillExpression` | `eli:LegalExpression` | No Oireachtas-specific properties were defined |
| `:BillFormat` | `eli:Format` | No Oireachtas-specific properties were defined |
| `:BillVersion` | `eli-dl:LegislativeProcessWorkVersion` | Version individuals retyped accordingly |
| `:BillsBook` | `skos:OrderedCollection` | Labels belong on instances |
| `:AmendmentList` | `eli-dl:AmendmentToDraftLegislationWork` | ELI-DL supports amendment lists via `eli-dl:has_part` |
| `:BillAmendment` | `eli-dl:AmendmentToDraftLegislationWork` (document) + `eli-dl:LegislativeActivity` (event) | Linked via `eli-dl:created_a_realization_of` |
| `:BillStatus` | `eli-dl:ProcessStatus` | Status individuals retyped accordingly |

#### Annotations on ELI Properties

| Property | Annotation |
|---|---|
| `eli:title_alternative` | `rdfs:label "Long title of a Bill"` |
| `eli:title` | `rdfs:label "Short title of a Bill"` |
| `eli:basis_for` | `rdfs:comment "A Bill is the basis for an Act"` |

#### Named Individuals — ELI Resource Types

`Act`, `Bill`, `DraftBill` (Heads of Bill), `ExplanatoryMemo`

#### Named Individuals — Bill Versions

Retyped as `eli-dl:LegislativeProcessWorkVersion`: `AsInitiated`, `VersionA` (2nd printing), `VersionB` (3rd), `VersionC` (4th), `VersionD` (5th)

All remain in `eli:VersionTable` via `skos:inScheme`.

#### Named Individuals — Bill Statuses

Retyped as `eli-dl:ProcessStatus`: `AwaitingSignatureBill`, `CurrentBill`, `DefeatedBill`, `DraftHeadsOfBill`, `EnactedBill`, `LapsedBill`, `RejectedAtReferendumBill`, `SubjectToReferendumBill`, `WithdrawnBill`

---

### vocabulary.owl

**IRI:** `https://data.oireachtas.ie/ontology/vocabulary`

Contains the SKOS `ConceptScheme` individuals that act as controlled vocabularies. Concept members are defined in `events.owl` and `legislative.owl` and reference their scheme via `skos:inScheme`.

| Individual | Label | Members defined in |
|---|---|---|
| `:BillEventTable` | Bill event table | `events.owl` |
| `:BillEventResultTable` | Bill event outcome table | `events.owl` |
| `:BillDeliveryTable` | Bill delivery table | `events.owl` |
| `:BillDeliveryOutcomeTable` | Bill delivery outcome table | `events.owl` |
| `:BillStatusTable` | Bill status table | `legislative.owl` |

---

### debates.owl

**IRI:** `https://data.oireachtas.ie/ontology/debates`

*Reserved stub — no classes or individuals defined yet.*

Intended to cover:
- Elements of the Official Report (transcribed record of debates)
- Parliamentary questions and answers
- Contributions (who said what, when, in which chamber)
- Votes and divisions
- References from debates to journal events and legislative documents

Imports `events.owl` and `agents.owl` as anticipated dependencies.

---

### Referenced External Schemas

| Prefix | Namespace | Description |
|---|---|---|
| `eli:` | `http://data.europa.eu/eli/ontology#` | European Legislative Identifier |
| `eli-dl:` | `http://data.europa.eu/eli/eli-draft-legislation-ontology#` | ELI Draft Legislation ontology |
| `org:` | `http://www.w3.org/ns/org#` | W3C Organisation ontology |
| `time:` | `http://www.w3.org/2006/time#` | W3C Time ontology |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organisation System |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | FOAF (Friend of a Friend) — persons, agents, organisations |
| `dct:` | `http://purl.org/dc/terms/` | Dublin Core Terms |
