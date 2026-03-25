
## Houses of the Oireachtas Ontology

*This is a work in progress*

1. [Introduction](#introduction)
1. [Bills](Bills)
1. [Debates](Debates)
1. [Members and Agents](Members)
1. [Agents — Organisations and Roles](Agents)
1. [Departments](Departments)
1. [Concept Schemes](Concept-Schemes)
1. [Ordering Business](Ordering-Business)
2. [Namespaces](#namespaces)


### Introduction

The Houses of the Oireachtas ontology attempts to describe the business processes and publications produced by the Houses of the Oireachtas within a formal vocabulary that allows documents, legislative events and entities to be linked programmatically.

The ontology is being developed using the [web ontology language (OWL)](http://www.w3.org/TR/owl-features/) and reuses other ontology schema wherever possible. The Oireachtas ontology extensively reuses the [European Legislative Identifier (ELI)](http://publications.europa.eu/mdr/eli/documentation/) ontology and its draft-legislation extension [ELI-DL](http://data.europa.eu/eli/eli-draft-legislation-ontology), as well as the [Akoma Ntoso](http://www.akomantoso.org/) schema, all of which were designed for legislation and the legislative process.

It is envisaged that the ontology will ultimately describe the following datasets from the Houses of the Oireachtas:
- Bills and other legislation, including motions and amendments
- Sub-units of the Houses of the Oireachtas, such as the Dáil, the Seanad and committees
- the Official Report (debates), including parliamentary questions
- Members
- Departments and other relevant bodies, including political parties
- Roles within the Houses of the Oireachtas (eg, Ministers or Chairs)
- Order papers and journals, including voting records
- Documents laid before the Houses
- Committee reports and submissions

One of the core functions of any Parliament is to decide on the legal basis for the creation and dissolution of State bodies, and to set the scope of their functions. Where relevant and feasible, the descriptions of Departments, roles and offices in this ontology will include a link to the decision of the Oireachtas on their creation, modification or dissolution, thereby allowing the Oireachtas dataset to be used as an authority vocabulary for Departments and Ministerial roles.

For the current technical structure of the ontology, see the [ontology README](https://github.com/Oireachtas/ontology/blob/master/ontology/README.md).

#### Terms used

As the Houses of the Oireachtas can be understand as different things depending on the context, it is useful to clarify at the outset to define how certain terms are being used in this document, as follows:
- A ``thing`` refers to the top level category in the ontology. Every object in the ontology is a thing. A thing might also refer to entities existing outside of the Oireachtas ontology, purely for convenience.
-  The ``Oireachtas`` refers to the Houses of the Oireachtas as a legislative body or parliament.
- The ``Service`` refers to the administrative functions that support the Oireachtas, as set out by the Houses of the Oireachtas Commission Act 2003.
- The ``Houses of the Oireachtas`` refer to the Oireachtas and Service collectively.
- The ``Houses`` refer to the Dáil and Seanad collectively, while individual houses are referred to as ``House``, ``Dáil`` or ``Seanad`` depending on the context.
- A ``committee`` is a subset of one or both Houses given delegated powers either by direction of a House, under Standing Orders of a House or by law.
- A ``Member`` is an elected Member of the Oireachtas, a ``Deputy`` is a Member of the Dáil and a ``Senator`` is a Member of the Seanad.

#### OWL and RDF syntax

OWL uses the [resource description framework (RDF)](http://www.w3.org/RDF/) syntax. The RDF syntax describes data as a series of three-part statements linking things to other things.

The three parts of the statement are called the subject, predicate and object, with the predicate expressing the relationship that the subject has with the object. Thus the sentence ``Enda Kenny holds the office of Taoiseach`` could be expressed in pseudo-rdf as ``<Enda Kenny><holds><office of Taoiseach``, with ``<Enda Kenny>`` as the object of the statement, ``<holds>`` as predicate and ``<office of the Taoiseach>`` as object.

The predicate expresses the relationship from the subject to the object unidirectionally, so the statement cannot be reversed. In other words, one cannot state ``<office of Taoiseach><holds><Enda Kenny>`` but must instead use a new predicate: ``<office of Taoiseach><is held by><Enda Kenny>`` subject-object relations. This statement demonstrates that subjects and objects are mutable, that is, the object of one statement can become the subject of another. Indeed predicates can also be subjects or objects, as with the OWL property ``inverseOf``, which describes two predicates as the inverse of each other: ``<holds><owl:inverseOf><is held by>``.

Each element in an RDF statement is either a [Internationalised resource identifier (IRI)] (http://www.w3.org/Addressing/#background) (an IRI is a generalisation of URIs which permit a wider range of characters) or a literal (or a blank node but these are not important in this discussion). An IRI is a string of characters which can uniquely identify the element. A literal is an element which is not denoted by an IRI, such as a string of text, a number or a date.

OWL ontologies can be divided into three primary types, ``classes``, ``properties`` ``literals``.  A ``class`` corresponds to an RDF subject or object, while a ``property`` corresponds to a predicate. It is possible to sub-class both ``classes`` and ``properties`` in a hierarchical manner, and a particular class or property may be the sub-class of multiple parent classes.

OWL permits the reuse and adaptation of existing ontologies in the development of new ones. This is in fact quite important because describing things using terms common to multiple datasets facilitates the sharing of information across the web. For this reason, the Oireachtas ontology reuses a number of other ontologies, including in particular the [European Legislative Identifier (ELI)](http://publications.europa.eu/mdr/eli/documentation/) ontology, which is designed to facilitate sharing and integration of legal resources across the European Union, and its extension [ELI-DL](http://data.europa.eu/eli/eli-draft-legislation-ontology), which covers draft legislation and the legislative process. However, given the particular nature of the material published by the Houses of the Oireachtas, as well as the procedures through which they are accorded legal status, it is also necessary in some cases to create our own models to properly describe things.

At a document level, [Akoma Ntoso](http://www.akomantoso.org/) is being adopted as an XML schema for publication of the Official Report of Debates, and is being evaluated for Bills. Akoma Ntoso was developed to represent legal, parliamentary and judicial documents in XML format, and is currently under review as an [OASIS](https://www.oasis-open.org/) open standard.

To describe categories and taxonomies of things, including controlled vocabularies as ways to describe them, the [Simple Knowledge Organising Scheme (SKOS)](www.w3.org/TR/skos-reference/) ontology is used. Concept scheme tables can be found in [Concept-Schemes](Concept-Schemes).

Elements of the [Data Catalog vocabulary (DCAT)](www.w3.org/TR/vocab-dcat/) will also be reused.

#### URIs

The namespace for the Oireachtas ontology is ``https://data.oireachtas.ie/ontology#``. The string ``oir:`` denotes that the following term is in the Oireachtas namespace. Class names are in camel case with all first letters of words capitalised: ``oir:BillFormat``. Property names are camel case with the very first letter in lower case: ``oir:amendedBy``

The namespace for URLs of instances of classes is ``https://data.oireachtas.ie`` and the patterns will be further described in the relevant sections.

#### Schema Overview

The OWL ontology is split into six sub-ontologies. See the [ontology README](https://github.com/Oireachtas/ontology/blob/master/ontology/README.md) for the full class, property and named individual reference.

| Sub-ontology | Description |
|---|---|
| `agents.owl` | Persons, roles and organisations (Houses, Government, Members, Committees) |
| `events.owl` | Journal events, bill stages and procedural outcomes |
| `legislation.owl` | Legislative documents, versions and statuses |
| `members.owl` | Membership, roles, party groupings and government tiers |
| `vocabulary.owl` | SKOS controlled vocabularies (concept schemes) |
| `debates.owl` | Official Report and debates — Akoma Ntoso structure, speeches, divisions and participation |

Conceptually, the subject matter falls into four areas: **Legislative Documents**, **Journal Events**, **Debates** and **Oireachtas Agents**. Some things straddle multiple areas — for example, an amendment to a Bill is both a legislative document and a journal event; such things are classified under multiple classes.



### Namespaces

| prefix  | namespace                                                              |
|---------|------------------------------------------------------------------------|
| oir     | https://data.oireachtas.ie/ontology#                                   |
| eli     | http://data.europa.eu/eli/ontology#                                    |
| eli-dl  | http://data.europa.eu/eli/eli-draft-legislation-ontology#              |
| org     | http://www.w3.org/ns/org#                                              |
| foaf    | http://xmlns.com/foaf/0.1/                                             |
| skos    | http://www.w3.org/2004/02/skos/core#                                   |
| dct     | http://purl.org/dc/terms/                                              |
| dcat    | http://www.w3.org/ns/dcat#                                             |
| lang    | http://publications.europa.eu/resource/authority/language              |
| iana    | http://www.iana.org/assignments/media-types/                           |
