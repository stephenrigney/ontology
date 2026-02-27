## Oireachtas Ontology — Structure and Contents

The ontology is split into five sub-ontologies, each covering one of the four declared areas of the Oireachtas ontology, plus a shared controlled vocabulary layer. A root umbrella file imports all five.

---

### File Overview

| File | Ontology IRI | Description |
|---|---|---|
| [oireachtas.owl](oireachtas.owl) | `http://www.oireachtas.ie/ontology` | Root umbrella — imports the five sub-ontologies below |
| [agents.owl](agents.owl) | `http://www.oireachtas.ie/ontology/agents` | Persons, roles and organisations |
| [events.owl](events.owl) | `http://www.oireachtas.ie/ontology/events` | Journal events, bill stages and procedural outcomes |
| [legislative.owl](legislative.owl) | `http://www.oireachtas.ie/ontology/legislative` | Legislative documents, versions and statuses |
| [vocabulary.owl](vocabulary.owl) | `http://www.oireachtas.ie/ontology/vocabulary` | SKOS controlled vocabularies (concept schemes) |
| [debates.owl](debates.owl) | `http://www.oireachtas.ie/ontology/debates` | Official Report and debates *(stub — reserved for future use)* |

---

### Import Chain

```
oireachtas.owl
├── agents.owl
│   └── (imports: ELI, Metalex, W3C org)
├── events.owl
│   └── (imports: agents.owl, Metalex, W3C time)
├── legislative.owl
│   └── (imports: events.owl, ELI, Metalex)
├── vocabulary.owl
│   └── (imports: events.owl, legislative.owl)
└── debates.owl
    └── (imports: events.owl, agents.owl)
```

---

### agents.owl

**IRI:** `http://www.oireachtas.ie/ontology/agents`

Defines the organisations, roles and persons involved in the legislative process.

#### Classes

| Class | Superclass(es) | Description |
|---|---|---|
| `:Oireachtas` | `rda:C10005`, `org:FormalOrganization` | The Houses of the Oireachtas as a legislative body |
| `:Chamber` | `:Oireachtas` | Continuous debating chamber (Dáil, Seanad or committee) |
| `:House` | `:Oireachtas` | A single bounded term of the Dáil or Seanad |
| `:Government` | `metalex:Legislator`, `:BillSource`, `:Oireachtas` | The Government as defined by the Constitution |
| `:BillSource` | `metalex:Legislator` | Abstract type: Government, Private Member or Private Sponsor |
| `:Member` | `rda:C10004`, `metalex:Legislator` | A Member of one of the Houses |
| `:Minister` | `:Member` | A Member who is also a Minister |
| `:Mover` | `:Minister`, `:PrivateMember` | A Member who moves a Bill or amendment |
| `:PrivateMember` | `metalex:Legislator`, `:BillSource`, `:Member` | A Member who is not a Member of Government |
| `:PrivateSponsor` | `rda:C10004`, `rda:C10005`, `:BillSource` | A non-Member person or body that introduces legislation |

#### Object Properties

| Property | Domain | Range | Notes |
|---|---|---|---|
| `:hasTerm` | `:Chamber` | `:House` | `owl:inverseOf :termOf` |
| `:termOf` | `:House` | `:Chamber` | |

#### Range Restriction

`eli:passed_by` — range restricted to `:Oireachtas`.

#### Named Individuals

| Individual | Type | Label |
|---|---|---|
| `<.../house/dail>` | `:Chamber` | Dáil Éireann |
| `<.../house/seanad>` | `:Chamber` | Seanad Éireann |

---

### events.owl

**IRI:** `http://www.oireachtas.ie/ontology/events`

Defines the procedural events that occur during a Bill's lifecycle, including stages, delivery methods and outcomes.

#### Classes

| Class | Superclass(es) | Description |
|---|---|---|
| `:EventDate` | `time:TemporalEntity` | A date associated with an event |
| `:JournalEvent` | `metalex:LegislativeCreation` | Any event recorded in the Order Paper or Official Report |
| `:BillEvent` | `:JournalEvent` | A procedural event in the lifecycle of a Bill |
| `:BillStage` | `:JournalEvent` | A formal stage of the Bill's passage |
| `:AmendingStage` | `metalex:LegislativeModification`, `:BillStage` | A stage at which amendments may be made |
| `:BillDelivery` | `metalex:LegislativeDelivery` | The method by which a Bill is initiated |
| `:BillDeliveryOutcome` | `metalex:Result` | The outcome of a Bill's introduction |
| `:BillEventOutcome` | `metalex:Result` | The outcome of a motion, question or amendment |

#### Object Properties

| Property | Domain | Range |
|---|---|---|
| `:InChamber` | `:BillEvent` | `:Chamber` |
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

---

### legislative.owl

**IRI:** `http://www.oireachtas.ie/ontology/legislative`

Defines the legislative documents published by the Oireachtas, including Bills, Acts, versions, expressions, formats and statuses.

#### Classes

| Class | Superclass(es) | Description |
|---|---|---|
| `:BillResource` | `eli:LegalResource`, `metalex:BibliographicWork` | A Bill as an abstract work |
| `:BillExpression` | `eli:LegalExpression`, `metalex:BibliographicExpression` | A specific language/version expression of a Bill |
| `:BillFormat` | `eli:Format`, `metalex:BibliographicManifestation` | A digital or physical format of a Bill expression |
| `:BillVersion` | `eli:Version` | A specific printed version of a Bill |
| `:BillsBook` | `skos:OrderedCollection` | The ordered list of Bills before a House (Legislative Observatory) |
| `:AmendmentList` | `eli:LegalResource`, `metalex:BibliographicWork` | A list of amendments to a Bill |
| `:BillAmendment` | `eli:LegalExpression`, `:AmendingStage` | An amendment as both a document and a modifying event |
| `:BillStatus` | — | The current or most recent lifecycle status of a Bill |

#### Data Properties

| Property | Superpropertyof | Description |
|---|---|---|
| `:OriginalTitle` | `dcterms:alternative` | The title of a LegalResource when first published |

#### Annotations on ELI Properties

| Property | Annotation |
|---|---|
| `eli:title_alternative` | `rdfs:label "Long title of a Bill"` |
| `eli:title` | `rdfs:label "Short title of a Bill"` |
| `eli:basis_for` | `rdfs:comment "A Bill is the basis for an Act"` |

#### Named Individuals — ELI Resource Types

`Act`, `Bill`, `DraftBill` (Heads of Bill), `ExplanatoryMemo`

#### Named Individuals — Bill Versions

`AsInitiated`, `VersionA` (2nd printing), `VersionB` (3rd), `VersionC` (4th), `VersionD` (5th)

#### Named Individuals — Bill Statuses

`AwaitingSignatureBill`, `CurrentBill`, `DefeatedBill`, `DraftHeadsOfBill`, `EnactedBill`, `LapsedBill`, `RejectedAtReferendumBill`, `SubjectToReferendumBill`, `WithdrawnBill`

---

### vocabulary.owl

**IRI:** `http://www.oireachtas.ie/ontology/vocabulary`

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

**IRI:** `http://www.oireachtas.ie/ontology/debates`

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
| `metalex:` | `http://www.metalex.eu/metalex/2008-05-02#` | CEN Metalex legislative interchange format |
| `org:` | `http://www.w3.org/ns/org#` | W3C Organisation ontology |
| `time:` | `http://www.w3.org/2006/time#` | W3C Time ontology |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organisation System |
| `rda:` | `http://rdaregistry.info/Elements/c/` | RDA registry (C10004 Person, C10005 Corporate Body) |
| `dct:` | `http://purl.org/dc/terms/` | Dublin Core Terms |
