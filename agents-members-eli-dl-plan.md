# Plan: Align agents.owl and members.owl with ELI-DL

## Overview

This document describes the ELI-DL alignment changes made to `agents.owl.ttl` and `members.owl.ttl`, following the same migration pattern established for `legislation.owl.ttl` and `events.owl.ttl` (documented in `metalex-to-eli-dl-plan.md`).

Unlike the Metalex migration — where local subclasses were replaced one-for-one with ELI-DL equivalents — most classes in `agents.owl` and `members.owl` have no direct ELI-DL counterpart and are retained. Changes here are **additive**: ELI-DL imports and prefixes are introduced, two structurally problematic classes are eliminated, and ELI-DL primitives are added as complements to the existing `org:` hierarchy.

---

## 1. Decisions

| Question | Decision |
|---|---|
| How to align `:House` with `eli-dl:ParliamentaryTerm`? | Retain `:House` as `org:FormalOrganization` subclass. Instances additionally typed `eli-dl:ParliamentaryTerm`. No `rdfs:subClassOf` relationship — the two have incompatible superclasses (`org:FormalOrganization` vs `skos:Concept / crm:E55_Type`). |
| What to do with `:BillSource`? | **Eliminate the class.** Use `eli-dl:was_submitted_by` (Process → Agent) as the canonical submitter link. `:Government`, `:PrivateMember` and `:PrivateSponsor` lose the `:BillSource` superclass but are otherwise retained. |
| Namespace split between the two files? | **Partially resolved.** `members.owl` now imports `agents.owl`. `members:Member` eliminated (see §2.4 / §3.8). Remaining duplicates (Chamber, Government, Minister, HousesOfTheOireachtas) documented in §5. |
| Add `eli-dl:Participation` + `eli-dl:ParticipationRole`? | **Yes** — add both to `members.owl`. Add `:MoverRole` and `:RapporteurRole` as `eli-dl:ParticipationRole` named individuals. These replace the structurally unsatisfiable `:Mover` class. |

---

## 2. Changes to `agents.owl.ttl`

### 2.1 ELI-DL import and prefix

Added:

```turtle
@prefix eli-dl: <http://data.europa.eu/eli/eli-draft-legislation-ontology#> .
```

Added to `owl:imports`:

```turtle
owl:imports <http://data.europa.eu/eli/eli-draft-legislation-ontology#> ,
            <http://data.europa.eu/eli/ontology#> ,
            org: .
```

### 2.2 Eliminate `:BillSource`

Removed the `:BillSource` class declaration entirely.

Removed `rdfs:subClassOf :BillSource` from:
- `:Government`
- `:PrivateMember`
- `:PrivateSponsor`

### 2.3 Eliminate `:Mover`

Removed the `:Mover` class declaration. `:Mover` was declared as a subclass of both `:Minister` and `:PrivateMember`. Because `:Minister rdfs:subClassOf :Member` and `:PrivateMember rdfs:subClassOf :Member` with `rdfs:comment "not also a Member of Government"`, the intersection was structurally suspect. The activity-level distinction is now expressed via `eli-dl:Participation` with `:MoverRole` (see §3.4).

### 2.4 Annotations on imported ELI-DL properties

Added a section *"Annotations and restrictions on imported properties"* (replacing the former *"Restriction on imported property"* section):

- `eli:passed_by` — range restricted to `:Oireachtas` (unchanged)
- `eli-dl:was_submitted_by` — `rdfs:comment` documenting that range includes `:Government`, `:PrivateMember`, `:PrivateSponsor`; replaces `:BillSource`
- `eli-dl:had_participation` — `rdfs:comment` documenting use with `:MoverRole` / `:RapporteurRole` on `:JournalEvent` activities; replaces `:Mover`

### 2.5 Auxiliary class declarations

Added to the auxiliary section:

```turtle
eli-dl:ParliamentaryTerm rdf:type owl:Class .
eli-dl:Participation     rdf:type owl:Class .
```

### 2.6 `:House` — ELI-DL documentation

Added to `:House rdfs:comment` guidance that instances should additionally be typed as `eli-dl:ParliamentaryTerm`, explaining why `rdfs:subClassOf eli-dl:ParliamentaryTerm` is not added (the class is `skos:Concept / crm:E55_Type`, incompatible with `org:FormalOrganization`).

### 2.7 Label normalisation on named individuals

The `seanad` individual previously used `dc:title`; normalised to `dct:title` to match the `dail` individual and the rest of the ontologies.

### 2.8 Add `foaf:Person` superclass to `:Member`

Added `@prefix foaf: <http://xmlns.com/foaf/0.1/>` to the prefix declarations.

Added `foaf:Person` as a second superclass on `:Member` alongside the existing `rda:C10004`:

```turtle
:Member rdfs:subClassOf <http://rdaregistry.info/Elements/c/C10004> ,
                        foaf:Person .
```

Rationale: ELI-DL properties `eli-dl:had_participant_person` and `eli-dl:had_responsible_person` have `rdfs:range eli:Person`. ELI declares `eli:Person rdfs:subClassOf foaf:Person`, making `foaf:Person` the broader class. Adding `foaf:Person` as a superclass of `agents:Member` ensures the range entailment holds for Oireachtas member instances used with those properties.

---

## 3. Changes to `members.owl.ttl`

### 3.1 ELI-DL import and prefix

Added:

```turtle
@prefix eli-dl: <http://data.europa.eu/eli/eli-draft-legislation-ontology#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
```

Added to `owl:imports`:

```turtle
owl:imports <http://data.europa.eu/eli/eli-draft-legislation-ontology#>,
            org:,
            foaf: .
```

### 3.2 Import `agents.owl` and add prefix (namespace reconciliation — Member)

Added:

```turtle
@prefix agents: <https://data.oireachtas.ie/ontology#> .
```

Added to `owl:imports`:

```turtle
<https://data.oireachtas.ie/ontology/agents>
```

### 3.3 Eliminate `members:Member`

Removed the `:Member` class declaration and its standalone restriction entirely:

```turtle
# REMOVED:
:Member a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasMembersMembership ;
            owl:someValuesFrom :OireachtasMembership ],
        foaf:Person .
```

The standalone restriction (`hasMembersMembership some OireachtasMembership`) was not moved to `agents:Member` — doing so would create a downward import dependency (agents importing members terms) and is redundant with the intersection expressions on all concrete subclasses.

All 8 references to `:Member` replaced with `agents:Member`:

| Location | Property or expression |
|---|---|
| `:hasMembers` | `rdfs:range` |
| `:hasMembersMembership` | `rdfs:domain` |
| `:DailSelectCommitteeMembership` | `owl:intersectionOf` |
| `:JointCommittee` | `owl:intersectionOf` |
| `:SeanadSelectCommitteeMembership` | `owl:intersectionOf` |
| `:Deputy` | `owl:intersectionOf` |
| `:OireachtasMember` | `rdfs:subClassOf` intersection |
| `:OireachtasMember` | `owl:equivalentClass` intersection |

### 3.4 Fix reversed `org:Role` axiom

The original file contained:

```turtle
org:Role rdfs:subClassOf :OireachtasMember .
```

This incorrectly made every `org:Role` instance in the world an `OireachtasMember`. Corrected to:

```turtle
:OireachtasMember rdfs:subClassOf org:Role .
```

(`:OireachtasMember` already had `org:Role` recorded as a superclass via its complex intersection definition; the standalone axiom is now consistent with that.)

### 3.5 Auxiliary class declarations

Added:

```turtle
eli-dl:Participation      a owl:Class .
eli-dl:ParticipationRole  a owl:Class .
eli-dl:ParliamentaryTerm  a owl:Class .
```

### 3.6 New named individuals — ELI-DL Participation Roles

Added a section *"Individuals — ELI-DL Participation Roles"*:

| Individual | Type | Purpose |
|---|---|---|
| `:MoverRole` | `eli-dl:ParticipationRole` | Role of a Member who moves a Bill, amendment or motion. Set via `eli-dl:participation_role` on `eli-dl:Participation` associated with `eli-dl:LegislativeActivity`. Replaces `agents:Mover`. |
| `:RapporteurRole` | `eli-dl:ParticipationRole` | Role of a Member appointed as rapporteur. Set via `eli-dl:participation_role`; see also `eli-dl:had_responsible_person`. |

**Usage pattern:**

```turtle
<https://data.oireachtas.ie/bill/2024/42/oireachtas/FirstStage/dail/participation/1>
    a eli-dl:Participation ;
    eli-dl:had_participant_person <https://data.oireachtas.ie/member/TDSmith1> ;
    eli-dl:participation_role     :MoverRole .

<https://data.oireachtas.ie/bill/2024/42/oireachtas/FirstStage/dail>
    a :FirstStage ;           # a :BillEvent, a eli-dl:LegislativeActivity
    eli-dl:had_participation  <.../participation/1> .
```

### 3.7 Annotation on `eli-dl:was_submitted_by`

Added `rdfs:comment` on `eli-dl:was_submitted_by` noting the Oireachtas range (`:Government`, `:PrivateMember`, `:PrivateSponsor`).

### 3.8 `:DateRange` alignment annotation

Added `rdfs:comment` on `:DateRange` documenting the ELI-DL parallel (`eli-dl:activity_start_date` / `eli-dl:activity_end_date` on activities) and confirming the `:DateRange` pattern fills the gap for `org:Membership` subclasses.

### 3.9 Date range datatype

`:StartDate` and `:EndDate` retain `xsd:dateTime` as their range. Although ELI-DL uses `xsd:date` for `eli-dl:activity_start_date` / `eli-dl:activity_end_date`, `xsd:date` is **not** in the OWL 2 DL datatype map and is rejected by the HermiT reasoner with an `UnsupportedDatatypeException`. `xsd:dateTime` is used for OWL 2 DL compatibility. The `:DateRange` `rdfs:comment` documents this constraint.

---

## 4. Class and Property Mapping

### 4.1 `agents.owl` — ELI-DL alignment

| agents.owl entity | Action | ELI-DL alignment |
|---|---|---|
| `:BillSource` | **Eliminated** | Use `eli-dl:was_submitted_by` on `eli-dl:LegislativeProcess` |
| `:Mover` | **Eliminated** | Use `eli-dl:had_participation` + `members:MoverRole` on activity instances |
| `:House` | Retain; instance-level typing added | Instances typed `eli-dl:ParliamentaryTerm` for `eli-dl:parliamentary_term` usage |
| `:Oireachtas` | Retain | Already within range of `eli:passed_by` and `eli-dl:was_submitted_by` via `eli:Agent` |
| `:Government`, `:PrivateMember`, `:PrivateSponsor` | Retain; remove `:BillSource` superclass | Range members of `eli-dl:was_submitted_by` |
| `:Chamber`, `:Member`, `:Minister` | Retain unchanged | No ELI-DL equivalent; purely Oireachtas-specific |

> **Updated (namespace reconciliation):** `:Member` is no longer "unchanged" — `foaf:Person` was added as a second superclass (see §2.4). The entry below reflects the full picture.

| `:Member` | `foaf:Person` superclass added | Satisfies `eli:Person` range entailment for ELI-DL participation properties; canonical class replacing `members:Member` |

### 4.2 `members.owl` — ELI-DL alignment

| members.owl entity | Action | ELI-DL alignment |
|---|---|---|
| `org:Role rdfs:subClassOf :OireachtasMember` | **Corrected** — reversed back | Bug fix; was making all `org:Role` instances OireachtasMembers |
| `members:Member` | **Eliminated** | Replaced by `agents:Member` (canonical class). `members.owl` now imports `agents.owl`; all 8 internal references updated to `agents:Member`. Standalone restriction dropped (see §3.3). |
| `:OireachtasMember`, `:CabinetMember`, `:Whip`, `:Chair` (all `org:Role` subclasses) | Retain | These model institutional standing; `eli-dl:ParticipationRole` is additive for activity-level roles |
| `:OireachtasMembership` (subclassOf `org:Membership`) | Retain | Complementary to — not replaceable by — `eli-dl:Participation`, which is activity-centric |
| `:DateRange` | Retain; align datatype | `xsd:date` (was `xsd:dateTime`); consistent with ELI-DL |
| `:MoverRole`, `:RapporteurRole` | **New** | `eli-dl:ParticipationRole` individuals; replace `agents:Mover` class |

### 4.3 No direct ELI-DL equivalent — retained as-is

The following classes have no ELI-DL counterpart and are retained unchanged:

- `agents.owl`: `:Chamber`, `:Oireachtas`, `:Minister`
- `members.owl`: all committee, constituency, party grouping, and membership classes; `:SidesOfHouse`, `:HousesOfTheOireachtas`, `:Temporal`

---

## 5. Future Work — Namespace Reconciliation (remaining)

`members.owl` now imports `agents.owl` and `members:Member` has been eliminated. The following duplicates remain unresolved:

| Concept | `agents.owl` IRI | `members.owl` IRI | Conflict |
|---|---|---|---|
| ~~Member~~ | ~~`agents:Member` (subclassOf `rda:C10004`)~~ | ~~`members:Member` (subclassOf `foaf:Person`)~~ | **Resolved** — `members:Member` eliminated; `agents:Member` is canonical |
| Chamber | `…/ontology#Chamber` (includes committees; continuous entity) | `…/members#Chamber` (≡ `Dail ∪ Seanad`; excludes committees) | Directly incompatible semantics |
| Government | `…/ontology#Government` (subclassOf `:Oireachtas`; constitutional body) | `…/members#Government` (subclassOf `:SidesOfHouse`; whip side) | Entirely different concepts sharing a name |
| Minister | `…/ontology#Minister` (class of persons) | `…/members#Minister` (subclassOf `org:Role`) | Person class vs role class |
| HousesOfTheOireachtas / Oireachtas | `agents:Oireachtas` | `members:HousesOfTheOireachtas` | Conceptually co-extensive |

### Likely resolution approaches

1. **`members:Government`** — rename to `:GovernmentSide` to eliminate the name collision. Both classes survive under distinct names.
2. **`members:HousesOfTheOireachtas`** — assert `owl:equivalentClass agents:Oireachtas`; both are `org:FormalOrganization` subclasses describing the same institution.
3. **`members:Chamber`** — retain as a subclass of `agents:Chamber` restricted to plenary chambers (`Dail ∪ Seanad`). `agents:Chamber` remains the broader class (includes committees).
4. **`members:Minister`** — no `owl:equivalentClass` bridge (person vs role are incompatible). Link at instance level via `org:holds`/`org:heldBy`. Rename `members:Minister` to `:MinisterRole` to reduce confusion.

---

### 5.1 Chamber — Detailed Semantic Analysis

#### The two definitions

**`agents:Chamber`** — `rdfs:subClassOf :Oireachtas` (`org:FormalOrganization`). Open class with no `owl:equivalentClass` restriction. Comment: *"the Dáil, the Seanad or a committee chamber … a continuous entity associated with the physical location and the abstract concept of the debating chamber … It is also the physical site of a particular House."* Covers the Dáil chamber, Seanad chamber, and any committee chamber. Named individuals `<.../house/dail>` and `<.../house/seanad>` are instances of this class.

**`members:Chamber`** — `rdfs:subClassOf :HousesOfTheOireachtas` with `owl:equivalentClass [ owl:unionOf ( :Dail :Seanad ) ]` — a **closed enumeration**. `:Dail` and `:Seanad` are modelled as **classes** (subtypes of `members:Chamber`). `:Committee rdfs:subClassOf :HousesOfTheOireachtas` sits at the same level and is explicitly excluded from `members:Chamber`. Used as range of `:isOireachtasMembershipOf` — memberships are of a Dáil or Seanad, not a committee.

#### Three dimensions of incompatibility

**1. Extension: broad vs. closed**

`agents:Chamber` is extensionally open and includes committee chambers. `members:Chamber ≡ Dail ∪ Seanad` is a closed-world enumeration — the reasoner treats it as exhaustive. A `rdfs:subClassOf` bridge (`members:Chamber ⊑ agents:Chamber`) is safe: every `Dail ∪ Seanad` entity is also a chamber in the agents sense. An `owl:equivalentClass` bridge would be unsound: the reasoner would infer `agents:Chamber ≡ Dail ∪ Seanad`, potentially making any committee chamber instance unsatisfiable.

**2. Individual vs. class — OWL punning**

`agents:Chamber` is a class of *individuals*: `<.../house/dail>` is a named individual of type `agents:Chamber`. `members:Dail` and `members:Seanad` are *classes* — subtypes of `members:Chamber`. They model the same institution at different levels of the OWL hierarchy. Bridging them requires either OWL punning or a structural decision about which level is canonical.

**3. Continuous entity vs. organisational type**

`agents:Chamber` is the Dáil *as a place and institution* — a continuant. `members:Chamber` is a *category* of parliamentary body within the membership model, whose job is to anchor `isOireachtasMembershipOf`. These are different modelling frames: institutional continuant vs. membership container.

#### Resolution

Add `rdfs:subClassOf agents:Chamber` to `members:Chamber` (one-way bridge only). Do not assert `owl:equivalentClass`. Document in `members:Chamber` comment that the class is restricted to plenary chambers; committee chambers are `agents:Chamber` instances not in the `members:Chamber` extension.

---

### 5.2 `agents:House`, `agents:Chamber` and `eli-dl:ParliamentaryTerm`

#### The three concepts

| Concept | File | What it models |
|---|---|---|
| `agents:Chamber` | agents.owl | The continuous institutional chamber (the Dáil chamber — forever) |
| `agents:House` | agents.owl | A single bounded term: *the 33rd Dáil*, 2020–2025 |
| `eli-dl:ParliamentaryTerm` | ELI-DL | A type/classifier annotating activities and works with *which term they occurred in* |

The property chain: `agents:Chamber hasTerm agents:House` — a chamber has many terms; a term belongs to one chamber.

#### Why `agents:House` aligns with `eli-dl:ParliamentaryTerm`

`eli-dl:parliamentary_term` has domain `Activity ∪ Work` and range `eli-dl:ParliamentaryTerm`. It answers: *"In which parliamentary term did this bill stage occur?"* or *"This bill was initiated in the 33rd Dáil."* That is exactly what an `agents:House` instance represents.

`eli-dl:ParliamentaryTerm` is defined as `rdfs:subClassOf crm:E55_Type, skos:Concept` — a type concept / classifier. `agents:House` is `rdfs:subClassOf :Oireachtas` (an `org:FormalOrganization`). These superclass hierarchies are incompatible in OWL DL: an organization is not a SKOS concept. Hence the approach documented in `agents.owl`: the class-level `rdfs:subClassOf eli-dl:ParliamentaryTerm` axiom is deliberately omitted. Instead, individual House instances are **dually typed** at instance level:

```turtle
<https://data.oireachtas.ie/house/dail/33>
    a agents:House ,
      eli-dl:ParliamentaryTerm ,
      owl:NamedIndividual ;
    dct:title "33rd Dáil" .
```

This satisfies `eli-dl:parliamentary_term` range constraints without asserting an unsound class axiom.

#### Consequence for `members:Chamber`

`members:Chamber` (≡ `Dail ∪ Seanad`) is not involved in the `ParliamentaryTerm` alignment — it is a membership container, not a temporal classifier. The `ParliamentaryTerm` alignment runs through **`agents:House` only**. This reinforces that `members:Chamber`, `agents:Chamber`, and `agents:House` are three genuinely distinct modelling concepts that happen to overlap in natural-language usage of the word "chamber".

---

### 5.3 Government — Detailed Semantic Analysis

#### The two definitions

**`agents:Government`** — `rdfs:subClassOf :Oireachtas` (`org:FormalOrganization`). Label: *"The Government"*. Comment: *"The Government, as defined by the Constitution."* This is the Cabinet — the collective executive body of ministers appointed under Articles 13 and 28 of Bunreacht na hÉireann. It is the entity that introduces Government Bills, signs legislation, and appears as the submitter in `eli-dl:was_submitted_by`. It is a persistent constitutional institution, not tied to any one parliamentary term.

**`members:Government`** — `rdfs:subClassOf :SidesOfHouse`, `owl:disjointWith :Opposition`. `:SidesOfHouse rdfs:subClassOf :HousesOfTheOireachtas`. This models the *government benches* — the whip group of TDs and Senators who support the government in any given chamber sitting. It is a chamber-level organisational concept used to classify party membership by political alignment (`:PartyInGovernment`, `:PartyInOpposition`). It is disjoint with `:Opposition`, meaning the reasoner treats them as mutually exclusive categories of the same `SidesOfHouse` taxonomy.

#### Why these are entirely different concepts

| Dimension | `agents:Government` | `members:Government` |
|---|---|---|
| What it is | A constitutional body (the Cabinet) | A whip-side category in the chamber |
| Superclass | `agents:Oireachtas` (`org:FormalOrganization`) | `members:SidesOfHouse` |
| Relation to parliament | Introduces legislation; submits bills | Classifies parties/members by bench |
| Temporal scope | Persists across terms (Governments are numbered) | Relative to current sitting term |
| Disjointness axiom | None | Disjoint with `:Opposition` |

An `owl:equivalentClass` bridge would be unsound — a constitutional Cabinet is not a side of the house, and asserting equivalence would force the reasoner to infer `agents:Government` is disjoint with `agents:Opposition` (which does not exist in agents.owl) and is a subclass of `SidesOfHouse`.

#### Resolution

**Rename `members:Government` to `:GovernmentSide`** in `members.owl`. This eliminates the name collision entirely and makes the whip-side concept self-describing. No bridge axiom between the two is needed or appropriate. Update the range of `:isPartyIn` and the `members:GovernmentSide disjointWith :Opposition` axiom accordingly. The `:PartyInGovernment` and `:PartyInOpposition` class names remain accurate.

---

### 5.4 Minister — Detailed Semantic Analysis

#### The two definitions

**`agents:Minister`** — `rdfs:subClassOf :Member`. A *person* who is both a Member of the Oireachtas and holds ministerial office. Sits in the agent/person hierarchy alongside `:PrivateMember`. Used as the type of an individual such as `<.../person/mary-jones>` when she is serving as a minister.

**`members:Minister`** — `rdfs:subClassOf :CabinetMember`, which is `rdfs:subClassOf org:Role`. An `org:Role` — a *position or role* that a person holds, not the person themselves. Used as the type of a role-holding record that is then linked to a person via `org:heldBy` / `org:holds`.

#### Why `owl:equivalentClass` is unsound

In OWL, a person and a role are not substitutable. If `agents:Minister owl:equivalentClass members:Minister` were asserted:
- The reasoner would infer that every minister *person* is also an `org:Role`, which would propagate `org:Role` domain/range constraints onto person instances.
- `agents:Minister rdfs:subClassOf agents:Member rdfs:subClassOf foaf:Person`. `members:Minister rdfs:subClassOf org:Role`. `foaf:Person` and `org:Role` are not declared disjoint in the W3C org ontology, so this would not produce an unsatisfiability, but it would produce semantically incorrect and misleading inferences.

The W3C org ontology is designed precisely for this pattern: `org:holds` links a `foaf:Agent` (person) to an `org:Role`; `org:heldBy` is the inverse. `agents:Minister` and `members:Minister` are the two ends of this relationship, not synonyms.

#### Resolution

No bridge axiom. Rename `members:Minister` to **`:MinisterRole`** to make the role-vs-person distinction explicit in the IRI. Add `rdfs:comment` to both classes documenting the relationship:
- On `agents:Minister`: *"A Member who holds a ministerial office. The corresponding role is `members:MinisterRole` (an `org:Role`), linked via `org:holds` / `org:heldBy`."*
- On `members:MinisterRole`: *"The ministerial role (an `org:Role`). The person holding this role is of type `agents:Minister`, linked via `org:heldBy`."*

---

### 5.5 `Oireachtas` / `HousesOfTheOireachtas` — Detailed Semantic Analysis

#### The two definitions

**`agents:Oireachtas`** — `rdfs:subClassOf rda:C10005` (RDA Corporate Body), `rdfs:subClassOf org:FormalOrganization`. Labels: *"Houses of the Oireachtas"* / *"Tithe an Oireachtas"*. Comment: *"Houses of the Oireachtas as a legislative and parliamentary body, does not include the Houses of the Oireachtas Service."* Range of `eli:passed_by` (restricted in agents.owl). Range members of `eli-dl:was_submitted_by` (via `:Government`, `:PrivateMember`, `:PrivateSponsor`).

**`members:HousesOfTheOireachtas`** — `rdfs:subClassOf org:FormalOrganization`. No labels or comments. Root of the `members.owl` organisational hierarchy: `:Chamber`, `:Committee`, `:SidesOfHouse`, `:Constituencies` are all direct subclasses. Domain of `:hasMembers`.

#### Why `owl:equivalentClass` is safe here

Both classes:
- Are `org:FormalOrganization` subclasses — same superclass hierarchy, no incompatibility
- Denote the constitutional parliament of Ireland as a formal organisation
- Have no conflicting axioms (no disjointness, no contradictory restrictions)
- Have no logical reason to be distinct — the split is purely an artefact of the two files having been developed independently

The only asymmetry is that `agents:Oireachtas` has an additional `rda:C10005` superclass, which is harmless — `owl:equivalentClass` will propagate it to `members:HousesOfTheOireachtas` instances, which is correct (the Houses of the Oireachtas are also a bibliographic corporate body in the RDA sense).

#### Resolution

Two options, in order of preference:

1. **Eliminate `members:HousesOfTheOireachtas`** — replace all references in `members.owl` with `agents:Oireachtas` directly. Since `members.owl` now imports `agents.owl`, `agents:Oireachtas` is available. Subclasses (`:Chamber`, `:Committee`, `:SidesOfHouse`, `:Constituencies`) gain `agents:Oireachtas` as their superclass, which is semantically correct. Domain of `:hasMembers` updates to `agents:Oireachtas`.

2. **Assert `owl:equivalentClass`** — add `members:HousesOfTheOireachtas owl:equivalentClass agents:Oireachtas` as a bridge. Leaves both IRIs valid for a transition period. Less clean than option 1.

Option 1 is preferred for the same reason `members:Member` was eliminated rather than bridged: fewer IRIs, cleaner import graph, no residual redundancy.

---

## 7. Membership Modelling — Split `isOireachtasMembershipOf` and `inHouseTerm`

### 7.1 Problem

The current property `:isOireachtasMembershipOf` (domain `:OireachtasMembership`, range `:Chamber`) does double duty:
- It records *which house* a membership belongs to (the continuous institution — Dáil Éireann, Seanad Éireann).
- It is also the only hook for recording *which term* (the 32nd Dáil, the 26th Seanad).

After the `agents:Chamber → agents:House` / `agents:House → agents:HouseTerm` refactoring these are two distinct things at two distinct levels of the class hierarchy with two distinct IRIs. A single property cannot correctly range over both without ambiguity.

The Oireachtas API already encodes the split: each membership record carries both `houseCode` (identifying the continuous house, e.g. `"dail"`) and a `uri` containing the term number (e.g. `…/house/dail/32`). The Timmy Dooley membership data confirms this pattern holds across all six of his memberships (30th, 31st, 32nd and 34th Dáil; 22nd and 26th Seanad).

### 7.2 Resolution — split into two properties

| Property | Domain | Range | Answers |
|---|---|---|---|
| `:isOireachtasMembershipOf` | `:OireachtasMembership` | `agents:House` | *Which house?* (`<…/house/dail>`) |
| `:inHouseTerm` | `:OireachtasMembership` | `agents:HouseTerm` | *Which term?* (`<…/house/dail/32>`) |

Both properties are present on every `OireachtasMembership` instance. No property-chain inference is needed: general-membership and term-membership are both stated explicitly in the data.

#### Example data (Timmy Dooley, 32nd Dáil membership)

```turtle
<…/member/Timmy-Dooley.S.2002-09-12/house/dail/32>
    a :DailMembership ;
    :isOireachtasMembershipOf  <https://data.oireachtas.ie/house/dail> ;
    :inHouseTerm               <https://data.oireachtas.ie/ie/oireachtas/house/dail/32> ;
    :isRepresentativeFrom      <…/dail/32/constituency/Clare> .
```

#### Changes to `members.owl.ttl`

1. **Add `:inHouseTerm`** — new `owl:ObjectProperty`, `rdfs:domain :OireachtasMembership`, `rdfs:range agents:HouseTerm`. Add `skos:prefLabel "in house term"@en` and `rdfs:comment` noting that the term individual is the same resource referenced by `eli-dl:parliamentary_term` on the associated `eli-dl:LegislativeActivity`.

2. **Update `:isOireachtasMembershipOf` range** — from `:Chamber` (`:House` after rename) to `agents:House` (the continuous institutional IRI).

3. **Update `owl:allValuesFrom` restrictions on `:Deputy` and `:Senator`** — the current restriction `owl:allValuesFrom :Dail owl:onProperty :isOireachtasMembershipOf` will be superseded by the `DailMembership` / `SeanadMembership` split (see §8). The new `:Deputy` restriction uses `hasMembersMembership someValuesFrom :DailMembership`; `:Senator` uses `hasMembersMembership someValuesFrom :SeanadMembership`.

4. **Update `:OireachtasMember` equivalentClass** intersection — replace `owl:allValuesFrom :Chamber owl:onProperty :isOireachtasMembershipOf` with `owl:allValuesFrom agents:House owl:onProperty :isOireachtasMembershipOf`.

5. **Update `:JointCommittee` restriction** — same `allValuesFrom :Chamber` reference; update to `agents:House`.

6. **Add `:inHouseTerm` to `:CommitteeMembership`** — committee membership records need their own term link independently of any enclosing house membership, because joint and special committees may be anchored to a different house term than the senator's enclosing Seanad membership (the Timmy Dooley data shows a Seanad 26 committee at URI `…/committee/dail/33/…`). Add `:inHouseTerm` with `rdfs:domain org:Membership` (covers both `:OireachtasMembership` and `:CommitteeMembership`) or restrict to `:CommitteeMembership` if a separate property is preferred.

### 7.3 IRI alignment note

The agents.owl named individuals for the continuous houses currently use the short form `<https://data.oireachtas.ie/house/dail>`. All term-level URIs in the API follow the longer form `<https://data.oireachtas.ie/ie/oireachtas/house/dail/32>`. A decision is needed before the data conversion layer is built:

- **Option A** — adopt the `ie/oireachtas` path for the continuous-house IRIs: `<https://data.oireachtas.ie/ie/oireachtas/house/dail>`. Keeps all data IRIs under a single path prefix.
- **Option B** — keep the short form for continuous-house individuals as canonical ontology IRIs, explicitly distinct from numbered term IRIs. Document the distinction in `rdfs:comment`.

This does not affect OWL axioms and is deferred to data generation design.

---

## 8. Deputy / Senator Disjointness — Person-level vs. Membership-level

### 8.1 The problem

The current axiom `Deputy owl:disjointWith Senator` is declared at the **person class** level. In OWL this means no individual can simultaneously be inferred as both `:Deputy` and `:Senator`.

Timmy Dooley has served in both houses at different points in his career: four Dáil terms (30th, 31st, 32nd, 34th) and two Seanad terms (22nd, 26th). If both roles are ever inferred for the same person individual — which the `someValuesFrom` membership expressions can produce if data is loaded for multiple terms — the reasoner produces an unsatisfiability on that person individual.

The disjointness is correct in intent (a single sitting membership is either Dáil or Seanad, not both) but wrong in placement (it is on the person, not the membership).

### 8.2 Where disjointness belongs

A single `OireachtasMembership` record is always either a Dáil membership or a Seanad membership. That is the correct locus. The person is not disjoint from having both kinds of membership over a career; the membership record is.

Introduce two subclasses:

| Class | Superclass | Disjoint with |
|---|---|---|
| `:DailMembership` | `:OireachtasMembership` | `:SeanadMembership` |
| `:SeanadMembership` | `:OireachtasMembership` | `:DailMembership` |

Each becomes the link between an agent and a term. Type-checking via `:inHouseTerm` is then exact:
- A `:DailMembership` must have `inHouseTerm someValuesFrom agents:DailTerm`.
- A `:SeanadMembership` must have `inHouseTerm someValuesFrom agents:SeanadTerm`.

### 8.3 Changes to `members.owl.ttl`

1. **Add `:DailMembership`** — `rdfs:subClassOf :OireachtasMembership`, `owl:disjointWith :SeanadMembership`, with `rdfs:subClassOf [ owl:onProperty :inHouseTerm ; owl:someValuesFrom agents:DailTerm ]`. Comment: *"A membership record of a specific term of Dáil Éireann. The term is identified via `:inHouseTerm` (range `agents:DailTerm`)."*

2. **Add `:SeanadMembership`** — symmetric: `rdfs:subClassOf :OireachtasMembership`, with `inHouseTerm someValuesFrom agents:SeanadTerm`. Comment noting Seanad panel or electorate as the typical value of `:isRepresentativeFrom`.

3. **Update `:Deputy` restriction** — replace `isOireachtasMembershipOf allValuesFrom :Dail` with `hasMembersMembership someValuesFrom :DailMembership`.

4. **Update `:Senator` restriction** — replace with `hasMembersMembership someValuesFrom :SeanadMembership`.

5. **Remove `Deputy owl:disjointWith Senator`** — disjointness is now expressed at membership level. Add `rdfs:comment` to both `:Deputy` and `:Senator` documenting that a person may over their career be inferred as both a Deputy and a Senator.

6. **Update `:DailSelectCommitteeMembership` and `:SeanadSelectCommitteeMembership` intersection expressions** — replace `allValuesFrom :Dail` / `allValuesFrom :Seanad` on `:isOireachtasMembershipOf` with `someValuesFrom :DailMembership` / `:SeanadMembership` on `:hasMembersMembership`.

---

## 6. Verification

Run `validate.py` after all changes. Load `oireachtas.owl.ttl` in Protégé and run the HermiT reasoner — verify no unsatisfiable classes are introduced. The removal of `:Mover` (structurally suspect intersection of role classes) and the correction of the `org:Role` axiom in `members.owl` should reduce rather than increase the unsatisfiable class count. Additional checks for changes introduced in §7 and §8:

- Confirm that the Timmy Dooley person individual is **not** inferred unsatisfiable after the Deputy/Senator disjointness fix (§8).
- Confirm `members:Dail ⊑ agents:DailTerm ⊑ agents:HouseTerm ⊑ agents:Oireachtas` is inferred transitively.
- Confirm `members:House (≡ Dail ∪ Seanad) ⊑ agents:House` is inferred via the Dail/Seanad subclass bridges.
- Confirm no `org:FormalOrganization` / `org:Site` conflict on any instance (if `org:Site` route is revisited).
- Validate SPARQL queries:
  - *All members of Dáil Éireann (ever)*: `?m :isOireachtasMembershipOf <…/house/dail>`
  - *All members of the 32nd Dáil*: `?m :inHouseTerm <…/house/dail/32>`
  - *Both roles for Timmy Dooley*: confirm two `:DailMembership` records and two `:SeanadMembership` records, with the person individual remaining satisfiable.
