## Debate Body

5. [Preface](#debate-preface)
6. [Debate Sections](#debate-section)
7. [Headings](#heading)
8. [Summary](#summary)
9. [Questions and Answers](#questions-and-answers)
10. [Speeches](#speech)
11. [Paragraph](#paragraph)
12. [Entity](#entity)
13. [Table](#table)
14. [Division](#division)
15. [Roll Call](#roll-call)
16. [Text Styles](#text-styles)
17. [Inline Elements](#inline-elements)

The body of the debate is described in a hierarchical structure with a preface followed by individual debates on a particular date structured as `debateSection` elements, recording the contributions and procedural formalities that took place during the debate.

### Debate Preface

The preface section presents human readable information relating to the title, author, status and generative date of the debate, contained in a series of `block` elements, as follows:

| block | Describes |
|-----|-----|
|block[@name='title_ga']/docTitle| Irish title of document |
|block[@name='title_en']/docTitle| English title of document |
|block[@name='proponent_en (ga)']/docProponent| Creator of document, in English (Irish)
|block[@name='status_en(ga)']/docStatus| Status of document, in English (Irish)|
|block[@name='date_en(ga)']/docDate| Generative date of document, in English (Irish)|

### Debate Section

A `debateSection` contains a debate if its `name` attribute is "prelude", "debate", "questions", "privateNoticeQuestion" or `writtenAnswers`.  The children of a `debateSection` are:

- [speech](#speech)
- [summary](#summary)
- [debateSection](#division) if its `name` attribute is "division"
- [table](#table)
- [rollCall](#roll-call)
- [question](#question)
- [answer](#question)
- A nested debateSection containing a debate.

A `debateSection` refers to a [division or vote](#division) if its `name` attribute is "division". A division has two child debateSections with `name` attributes of "ta" and "nil", respectively. A debateSection with a `name` value of "prelude" contains the prelude to a day's debate (including the attendance list  or [`rollCall`](#roll-call) in the case of committees).


|Akoma Ntoso|Describes|
|----------|-------|-------------|
|debate|The debate on a specific date in a named house or committee|
|debateBody/debateSection|A debate on a specific topic|
|debateSection/@eId|Internally unique identifier, begins with `dbsect_`|
|debateSection/@refersTo|For debates on Bills, links to TLCEvent reference to OIR:BillEvent or OIR:BillResource|
|debateSection/@name|Type of debateSection, see above.|

**Issues**

Due to the way the XML was originally generated, sometimes debate sections contain only a `heading` and no other children. This is most evident in bilingual debates, where the Irish language heading precedes the English language heading - here the first debate section contains only the Irish heading and the actual debate is in the second debate section.

### Heading

The `Heading` element contains the text for the name of the debate. It is usually but not always present.  

|Akoma Ntoso|Describes|
|----------|-------|-------------|
|debateSection/heading|The heading for the debate|
|heading/recordedTime/@time|Inline element containing xsd:dateTime accurate within ten minutes|

**Issues**

There is a problem with duplicate headings in earlier debates (until around the 1980s) which occurred when the historic debates were originally digitised. Headings are copied into the start of subsequent headings. This problem is not easy to solve because of the difficulty in differentiating between intentional and accidental duplicates.

### Text styles

A simplified version of the orthographic markup in the original XML has been carried into the Akoma Ntoso XML for debates. Formatting tags are `i`, `b` and `u`, and they have the same meaning as their html namesakes.

In addition, `summary` and `p` tags can include a `class` attribute with the following values:

- "center" for centred text; and
- indent_{n} for indented text, where n is a positive integer

### Inline Elements

In addition to formatting elements, the following inline elements occur:

- `from` and `heading` elements may contain `recordedTime`, with an attribute of `time` that records the time as an xsd:dateTime value. The timestamp is accurate to five or ten minutes.

- `p` and `summary` elements may contain `img`, with an attribute of `src` that currently points to same a relative file location recorded in the original XML.

**Issues**
Fix `src` URI reference with a URI reference for image files - tentatively: `

```
http://oireachtas.ie/ie/oireachtas/images/debateRecord/{house}/{date}/{img eId}
```

### Summary

A `summary` element contains text that was not directly reported as spoken in a debate. This may be a narrative summary of procedural tasks and decisions:

> Question put declared carried.

> Debate resumed on Amendment No. 1:
>> On page 43, line 4, to replace "may" with "shall".
>
> The Seanad adjourned at 4.30 p.m., _sine die_

A `summary` may also contain a description of events that were not directly attributable to specific speakers:

> (Interruptions.)

> Deputy Corry withdrew from the Chamber.

> Grave disorder ensuing, the Leas-Cheann Comhairle, under the provisions of Standing Order 52, ajdourned the Dáil at 10.55 p.m. until 10.30 a.m. on Thursday, 7th December, 1950.


|Akoma Ntoso|Describes|
|----------|-------|-------------|
|debateSection/summary|Summaries of procedural or other incidents|
|summary@eId|Internally unique, starts with "sum_"|
|summary/@title|Used where summary refers to a vote outcome or TLCEvent, the type of action described (to do: summary vocab)|
|summary/@refersTo | reference to TLCClass/@eId where summary/@title='decision'|
|summary/@class|Style markup - either center or indent_{n}|
|summary/i, summary/b, summary/u| italicise, bold and underline, respectively|



### Speech

An oral contribution from a Member, a witness to a committee or, on occasion, a visiting Head of State is recorded in a `speech` element.

|Akoma Ntoso|Describes|
|----------|-------|-------------|
|debateSection/speech|A contribution by a Member or a witness|
|speech/@eId|Internally unique, begins with "spk_"|
|speech/@by|Reference to TLCPerson eId for speaker|
|speech/@as|Optional - refers to TLCRole eId for speaker role, eg, Taoiseach|
|speech/from|The handle for a speaker as published|
|  |  |
|from/recordedTime|Inline element containing xsd:dateTime|
|  |  |
|speech/p|A paragraph in a speech, containing text of the speech|

**Issues**

1. In earlier debates the `speech\@by` field sometimes does identify the speaker. In such cases, the value for the attribute is recorded as "#"
2. In some cases `from` text identifying the speaker spills over into the following `p` element.
3. Sometimes procedural text which should be contained in `summary` elements are contained in `p` elements within `speech` elements.

### Questions and Answers

A `question` is a parliamentary question responded to during the course of business as an Oral Question or separately as a Written Answer.

A parliamentary question is submitted in advance of a debate and published in a Questions list for the day's sitting. Questions are numbered sequentially for a given date, which allows them to be uniquely identified by a combination of the date and their sequential numbering.

See [Parliamentary Questions](ordering-business#parliamentary-questions) for further information.

|Akoma Ntoso|Describes|
|----------|-------|-------------|
|debateSection/question | A parliamentary question |
|question/@eId | The reference number of a question, same as published in Questions list|
|question/@by | Reference to TLCPerson/@eId of the Member asking the question |
|question/@to | Reference to the TLCRole/@eId of the Minister to whom the question is directed |
|question/p | The text of the question |


### Paragraph

|Akoma Ntoso|Describes|
|----------|-------|-------------|
|p/@eId|Internally unique identifier, starts with `para_`|
|p/@class|Style markup - either center or indent_{n}|
|p/i, p/b, p/u| italicise, bold and underline, respectively|


### Entity

Currently the `entity` element inserts references to the relevant TLCEvent eId for amendments to Bills and Bill sections; or else internal references from the outcome of a question to the element of the debate in which a question was proposed or put.

For example:

```xml
<summary eId="sum_8">
  Question put: "That the Bill be now read a Second Time."
</summary>
...
<summary title="decision" refersTo="#lost" eId="sum_11">
  Question put and declared lost
  <entity name="reference" refersTo="#sum_8"/>
</summary>
```

```xml
<p eId="para_1330">
  I move amendment No. 1:
  <entity name="amendment" refersTo="#bill.2014.86.dail.4.amd_1"/>
</p>
...
<summary title="decision" refersTo="#agreed" eId="sum_46">
  <entity name="amendment" refersTo="#bill.2014.86.dail.4.amd_1.agreed"/>
</summary>
```


|Akoma Ntoso|Describes|
|----------|-------|-------------|
|entity/@refersTo|Internal reference to TLCEvent/@eId|
|entity/@name|Type of entity, either "reference" or "amendment"|

### Table

A table may be the child of `debateSection`, `speech`, `rollCall` or `answer`.

|Akoma Ntoso|Describes|
|----------|-------|-------------|
|table/tr| Corresponds to html `tr`|
|table/caption| Table title text|
|tr/td| Corresponds to html `td` |
|td/p | Contains the text of a cell |


### Division

A division is contained in a `debateSection` element with the `name` attribute of "division". Divisions usually have a consistent format, as in the following example, although the first summary tag may precede the division `debateSection` in older debates.

The information recorded in `meta/analysis/parliamentary/voting` is drawn from `<summary title="division">` `quantity` sub-nodes, the `<debateSection name="division">` `eId` contents and `<summary title="decision">` `eId` and `refersTo` attributes.

Example division:

```xml
<debateSection name="division" eId="dbsect_16">
  <summary eId="sum_4">
    Question put:
    <entity name="reference" refersTo="#para_174"/>
  </summary>
  <summary title="division" eId="sum_5">
    The Dáil divided: Tá,
    <quantity refersTo="#ta" eId="qty_1" normalized="63">63</quantity>
    ; Níl,
    <quantity refersTo="#nil" eId="qty_2" normalized="37">37</quantity>
    .
  </summary>
  <debateSection name="ta" eId="dbsect_17">
    <p eId="para_178">Tá</p>
    <p eId="para_179">
      <person refersTo="#JamesBannon">Bannon, James</person>
    </p>
    ...
  </debateSection>
  <debateSection name="nil" eId="dbsect_18">
    <p eId="para_242">Níl</p>
    <p eId="para_243">
      <person refersTo="#BobbyAylward">Aylward, Bobby</person>
    </p>
  </debateSection>
  <summary title="tellers" eId="sum_6">Tá...Níl...</summary>
  <summary title="decision" refersTo="#carried" eId="sum_7">
    Question declared carried.
    <entity name="reference" refersTo="dbsect_15"/>
  </summary>
</debateSection>
```

|Akoma Ntoso|Describes|
|----------|-------|
|summary/@title="division"|Summary description of division and its outcome|
|debateSection/debateSection/@name="ta"|Lists Members voting in favour of proposal|
|debateSection/debateSection/@name="nil"|Lists Members voting against proposal|
|debateSection/debateSection[@name=("nil" or "ta")/p/person|Name of individual voting member|
|person/@refersTo|Reference to `TLCPerson/@eId`|
|summary/@title="tellers"|Tellers for the division|
|summary/@title="decision"|Outcome of division|
|summary[@title="decision"]/@refersTo|Reference to `TLCConcept/@eId`; one of "#carried" or "#lost"|

**Issues**

As can be seen in the final entity reference, it was not always possible to identify the element eId containing the question. In such cases the reference defaults to the `debateSection` containing the debate. Results were more accurate for Bill amendments and sections than for general questions.

In older debates, voting Members have not been linked to TLCPerson. In such cases, `person\@refersTo` has a value of "#".

### Roll Call
