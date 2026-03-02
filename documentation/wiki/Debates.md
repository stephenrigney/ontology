# [Debates](#debates)

1. [FRBR Metadata](#frbr-metadata)
2. [Voting Metadata](#voting-metadata)
3. [TLC Metadata](#top-level-class-metadata)
4. [Debate Body](Debates-body#debate-body)


Debates refer to the oral deliberations held by Members of the Oireachtas in the Dáil, Seanad or a committee of one of the Houses. For the most part debates are held in public session but committee debates may be private. Public debates are recorded on video and audio, as well as reported, or transcribed, in text form. While this page deals mainly with an ontology for textual representations of debates, the metadata elements of the ontology are applicable to multi-media formats also.

The textual representations of debates are transcribed and lightly edited for the Official Report of Debates of the Dáil and Seanad (or `report` for short). The report is published as XML based on the [Akoma Ntoso](http://akomantoso.org) schema. The fields used and, where relevant, their mapping to the Oireachtas ontology are set out below; refer to the [Akoma Ntoso OASIS technical specifications](http://docs.oasis-open.org/legaldocml/akn-core/v1.0/csprd01/) for more complete documentation.



## Akoma Ntoso

The version of Akoma Ntoso used is:

 ```
 http://docs.oasis-open.org/legaldocml/akn-core/v1.0/csprd01/part1-vocabulary/akn-core-v1.0-csprd01-part1-vocabulary.html
 ```


Debates are published in Akoma Ntoso XML using the ``debate`` subschema. Master XML files contains the debates in the Seanad, Dáil or Committee for a specified date.

XML files comprise two sections, `akn:meta`, which contains metadata for the debate, and `akn:debateBody`, which contains the text of the debate.


### Metadata

**Note on path element descriptions**

In the following tables, element paths are denoted as `parent/child`. For brevity, only the immediate parent of an element is shown. Attributes are denoted by an `@` symbol.

### FRBR metadata

Akoma Ntoso uses the FRBR ontology to describe document life cycles. For debates XML, the FRBR lifecycle comprises `FRBRWork`, `FRBRExpression` and `FRBRManifestation`. These map to the Oireachtas ontology as follows:


| Akoma Ntoso| Oireachtas ontology| Describes|
|----------|---------|--------|
| FRBRWork | RDA:Work | A debate as a distinct (collective) intellectual creation |
| FRBRExpression | RDA:Expression | Representation of a debate as text, video or audio |
| FRBRManifestation | RDA:Manifestation | The physical embodiment of a debate in electronic or other form|


FRBR attributes in debates XML are as follows:

|  FRBR  |  Describes  |
|----------|---------|
| identification/FRBRWork| FRBR Work elements|
| identification/FRBRExpression| FRBR Expression elements |
| identification/FRBRManifestation| FRBR Manifestation elements |
| FRBRuri/@value |  Work (master) IRI for debate document |
| FRBRthis/@value| IRI for specific component of document, if retrieved as fraction of document |
| FRBRWork/FRBRdate/@date |Date debate was held |
| FBRWork/FRBRauthor/@href | URI for house or committee holding debate in Oireachtas namespace |


#### FRBR IRIs

The IRIs identifying FRBR elements follow the Akoma Ntoso naming convention. Currently, only the features described below are used.

FRBRWork IRIs take the following pattern:

For `FRBRWork/FRBRuri/@value`:

```
http://oireachtas.ie/akn/ie/ontology/debateRecord/{house}/{date}
http://oireachtas.ie/akn/ie/ontology/debateRecord/committee_of_public_accounts/2014-03-03
```
Or, for the Dáil, where written answers are stored separately to the oral debate:

```
http://oireachtas.ie/akn/ie/ontology/debateRecord/dail/2015-07-02/writtens
http://oireachtas.ie/akn/ie/ontology/debateRecord/dail/2015-07-02/debate
```

In this case, the values ``writtens`` and ``debate`` are recorded as a FRBRname/@value attribute

For `FRBRWork/FRBRthis/@value`

```
http://oireachtas.ie/akn/ie/ontology/debateRecord/{house}/{date}/{main or optional sub-part eId}
http://oireachtas.ie/akn/ie/ontology/debateRecord/dail/2015-07-02/debate/dbsect_3
```

Where `house` is `dail`, `seanad` or lowercase committee name, with spaces replaced by underscores. Date is the date of debate. The eId is the internally unique (ie, unique for that date) identifier for a sub-element of the debate file. If the entire document is being retrieved, rather than a sub-component, it is identified as `main`, eg:

```
http://oireachtas.ie/akn/ie/ontology/debateRecord/dail/2015-07-02/writtens/main
```


FRBRExpression IRIs extend FRBRWork IRIs with the following pattern:


- For `FRBRExpression/FRBRuri/@value`:


```
<FRBRWork-URI>/{lang}
http://oireachtas.ie/akn/ie/ontology/debateRecord/committee_of_public_accounts/2014-03-03/mul
```

- For `FRBRExpression/FRBRthis/@value`:


```
<FRBRWork-URI>/{lang}/{main or optional sub-part eId}
http://oireachtas.ie/akn/ie/ontology/debateRecord/committee_of_public_accounts/2014-03-03/mul/dbsect_3
```

Where {lang} is language used to transcribe the debate in a three letter code corresponding to ISO 639-2 alpha-3. The main codes used are as follows (as it is usually not possible to determine where Irish is spoken in a debate, the most common identifier `mul`):

| Code | Describes |
|----|----|
| mul | Multiple languages |
| eng | English |
| gle | Irish |




FRBRManifestation IRIs extend FRBRExpression IRIs by the addition of the relevant file format.

```
<FRBRWork-URI>/{lang}/main.xml
http://oireachtas.ie/akn/ie/ontology/debateRecord/committee_of_public_accounts/2014-03-03/mul/main.xml
```

### Voting metadata

Voting metadata is taken from the [`<debateSection name="division">`](Debates-body#division) element. 

| Voting | Describes |
|------|----------|
|analysis/parliamentary/voting|Summary information on divisions (votes)|
|voting/@eId|Internally unique id, begins with `vote_`|
|voting/@href|eId in which proposal was put|
|voting/@outcome|Either `#carried` or `#lost`, (refers to voting vocab)|
|voting/@refersTo|eId for subject(proposal) of vote, either internal or OIR:BillEvent|
|voting/count|Summary of aggregate votes cast for or against a proposal|
|eId|Format vote_{n}-count_{n}|
|count/@refersTo|Whether count refers to votes in support(`#ta`) or against(`#nil`)|
|count/@value|Count of votes cast in category|
|count/@qty|refers to eId in which vote count is recorded|

**Issues**

It was not always possible to capture the value for `voting/@outcome` from the debate text. In such cases, the value is '#??'

### Top Level Class Metadata

|References|Describes|
|-----------|-----------------|
|meta/references|Mapping to external entities (TLC entities)|
|references/TLCConcept|A class in the Oireachtas ontology|
|references/TLCEvent|An instance of [OIR:BillEvent](Bills) class|
|references/TLCPerson|An instance of [OIR:Member](Members) class|
|references/TLCRole|An instance of OIR:Role class|
|references/*/@eId|Internally unique identifier of entity|
|references/*/@href|entity URI as Oireachtas namespace|
|references/*/@showAs|Human readable label of entity|

**Issues**

It has not always been possible to correctly identify the OIR:BillEvent of a debate about a Bill. In these cases, the Bill itself (OIR:BillResource) is referenced where it can be identified. While the correct Top Level Class for an OIR:BillResource is TLCReference, they are instead included as TLCEvent
