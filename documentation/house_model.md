# Modelling of `:House` in the Oireachtas Ontology

## What a "House" means in this ontology

The concept is deliberately split into two layers: the **permanent institution** and the **numbered sitting**.

---

### The permanent institution (`agents:House`)

Defined in `ontologies/agents.owl.ttl`, `agents:House` represents Dáil Éireann or Seanad Éireann as a **continuous constitutional body** — the same legal entity that has existed since the State was founded, regardless of elections. Two named individuals are used as the concrete identifiers:

- `<https://data.oireachtas.ie/house/dail>`
- `<https://data.oireachtas.ie/house/seanad>`

Parliamentary committees are also modelled as `agents:House` instances (the Oireachtas treats committees as delegated chambers). The Houses sit inside a broader hierarchy: `agents:House` → `agents:Oireachtas` → `org:FormalOrganization`.

---

### Numbered sittings (`agents:HouseTerm`)

Because a House changes composition after each election, the ontology separates the institution from any specific sitting. A `HouseTerm` is a **bounded period** — for example, the 33rd Dáil (2020–2025). Two subclasses exist: `DailTerm` and `SeanadTerm`. The link between the institution and its sittings runs through two inverse properties:

- `:hasTerm` — from a House to its terms
- `:termOf` — from a term back to its House

Each `HouseTerm` also carries a short `houseCode` (e.g. `"dail"`) and an ordinal `termNo` (e.g. `33`).

---

### The plenary houses as membership containers (`members:House`)

`ontologies/members.owl.ttl` adds a second `House` class in the members namespace. This is strictly the **two plenary houses** (Dáil and Seanad) acting as containers for membership records. It is defined as exactly equal to the union of `:Dail` and `:Seanad`, and committees are deliberately excluded. The key modelling choices here are:

| Class / Property | Meaning |
|---|---|
| `members:House` | The Dáil or Seanad as a container for member records |
| `members:Dail` | A Dáil-specific subclass; also a subclass of `agents:DailTerm` |
| `members:Seanad` | A Seanad-specific subclass; also a subclass of `agents:SeanadTerm` |
| `:isOireachtasMembershipOf` | Links a membership record to the `agents:House` it belongs to |
| `:inHouseTerm` | Links that membership to the specific numbered term |

---

### How the two files relate

`agents.owl.ttl` models the institution (what a House *is*); `members.owl.ttl` models membership (who belongs to it and when). The bridge is a one-way subclass relationship: every `members:House` instance is also an `agents:House`, but not vice versa — committees remain `agents:House` instances without being `members:House`.

---

### Summary

The Dáil or Seanad is the same legal body across time (`agents:House`), each election produces a new numbered term (`HouseTerm`), and membership records hang off the combination of house and term.
