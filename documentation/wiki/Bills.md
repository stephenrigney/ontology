## Bills

1. [Bill Classes](Bill-Classes)
2. [Bill Properties](Bill-Properties)
3. [Concept Schemes](Concept-Schemes)

A Bill is a proposed law which, after a formal process of deliberation by the Oireachtas, may or may not eventually be enacted after being passed by the Oireachtas and signed by the President, at which stage it becomes an Act.

In this ontology, Bills are described as ``legislative documents`` and as ``journal events``, corresponding to the Bill as a text document and to the procedures which give a Bill its legal standing, respectively.

### Bills as legislative documents

As a legislative document, a Bill is described with the [functional requirements for bibliographic records (FRBR)](http://www.loc.gov/cds/downloads/FRBR.PDF) entity-relationship model used by both CEN-Metalex and ELI. In this model, a Bill is created as an individual intellectual work  (``eli:LegislativeResource``) and expressed as a series of versions during its lifecycle (``eli:LegalExpression``) which are manifested in a physical form, such as a PDF or XML file (``eli:Format``).

The Bill as legislative document is also associated with certain metadata about it, such as its sponsor, dates of publication and entry into force (enactment) and the Act it became, if relevant.

![Bill diagram](https://github.com/Oireachtas/ontology/blob/master/bills/Bills.jpg)


#### Bill document URI patterns

URIs for Bills as legislative documents have the following pattern:

    http://oireachtas.ie/ie/oireachtas/bill/{year}/{order number}/{language}@{version}/{main component}/{sub component}.{format extension}

The following table provides example uses of the pattern:

| Class               | Example Value                         | Describes                                                      |
|---------------------|---------------------------------------|----------------------------------------------------------------|
| oir:BillResource   | ie/oireachtas/bill/2015/44                       | The Bill as a distinct intellectual creation/ as a concept     |
| oir:BillExpression | ie/oireachtas/bill/2015/44/eng@initiated         | Bill as initiated, English version                             |
|                     | ie/oireachtas/bill/2015/44/gle@initiated         | Bill as initiated, Irish version                               |
|                     | ie/oireachtas/bill/2015/44/mul@/dail             | Bill as initiated, multilingual version (eg, referendum Bills) |
|                     | ie/oireachtas/bill/2015/44/eng@ver_a             | 2nd version of Bill                                            |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b             | 3rd version of Bill                                            |
|                     | ie/oireachtas/bill/2015/44/eng@passed            | Bill as passed by both Houses                                  |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b/main        | Main component of Bill (ie, the Bill in its entirety)          |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b/main/part_1 | Part 1 of the Bill                                             |
| oir:BillFormat          | ie/oireachtas/bill/2015/44/eng@ver_b/main.xml    | Bill in XML (eg, Akoma Ntoso) format                           |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b/main.pdf    | Bill in pdf format                                             |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b/main.htm    | Bill in html format                                            |
|                     | ie/oireachtas/bill/2015/44/eng@ver_b/main.odt    | Bill in open office format                                     |



### Bills as journal events

### Bill event URIs

The URI pattern for Bill events is as follows:

    http://oireachtas.ie/ie/oireachtas/bill/{year}/{order number}/{house}/{event context}/{event topic}


The following table lists the label and skos:conceptScheme vocabulary for Bill in events along with example URIs (to add concept scheme vocabulary):

| Event                                                     | URI                                          |
|-----------------------------------------------------------|----------------------------------------------|
| First Stage                                               | ie/oireachtas/bill/2015/44/dail/1                       |
| All Stages                                                | ie/oireachtas/bill/2015/44/dail/all                     |
| Second Stage                                              | ie/oireachtas/bill/2015/44/dail/2                       |
| Second and Subsequent Stages                              | ie/oireachtas/bill/2015/44/dail/2_sub                   |
| Order for Second Stage                                    | ie/oireachtas/bill/2015/44/dail/2_ord                   |
| Committee Stage                                           | ie/oireachtas/bill/2015/44/dail/3                       |
| Committee and Remaining Stages                            | ie/oireachtas/bill/2015/44/dail/3_sub                   |
| Order for Committee Stage                                 | ie/oireachtas/bill/2015/44/dail/3_ord                   |
| Report Stage                                              | ie/oireachtas/bill/2015/44/dail/4                       |
| Report and Final Stages                                   | ie/oireachtas/bill/2015/44/dail/4_sub                   |
| Order for Report Stage                                    | ie/oireachtas/bill/2015/44/dail/2_ord                   |
| Fifth Stage                                               | ie/oireachtas/bill/2015/44/dail/5                       |
| Enactment (signed by President)                           | ie/oireachtas/bill/2015/44/enacted                       |
| Financial Resolution(s)                                   | ie/oireachtas/bill/2015/44/dail/motion/finance_res      |
| Leave to Withdraw   | ie/oireachtas/bill/2015/44/dail/motion/withdrawn       |
| Leave to Introduce                                        | ie/oireachtas/bill/2015/44/dail/motion/introduce      |
| Instruction to committee                                  | ie/oireachtas/bill/2015/44/dail/motion/instruction      |
| Referral to Select Committee                              | ie/oireachtas/bill/2015/44/dail/motion/referral         |
| From the Seanad                                           | ie/oireachtas/bill/2015/44/dail/seanad_amd              |
| [Seanad Bill amended by the Dáil] Report and Final Stages | ie/oireachtas/bill/2015/44/seanad/dail_amd        |
| Motion for Earlier Signature                              | ie/oireachtas/bill/2015/44/dail/motion/early            |
| Motion to Discharge Order for Second Stage                | ie/oireachtas/bill/2015/44/dail/motion/2_ord_withdrawn |
| Motion to Discharge Committee Stage                       | ie/oireachtas/bill/2015/44/dail/motion/3_withdraw       |
| Statement for Information of Voters: Motion               | ie/oireachtas/bill/2015/44/dail/motion/ref_info         |
| Referendum (Ballot Paper) Order 1998: Motion              | ie/oireachtas/bill/2015/44/dail/motion/ref_ballot       |
| Motion to Recommit           | ie/oireachtas/bill/2015/44/dail/motion/recommit         |
| Restoration of Bill                                       | ie/oireachtas/bill/2015/44/restored          |
| Lapsed Bill                                       | ie/oireachtas/bill/2015/44/lapsed          |
| Withdrawn Bill                                       | ie/oireachtas/bill/2015/44/withdrawn |
| Bill amendment                                            | ie/oireachtas/bill/2015/44/dail/3/amd_1                 |
| Bill recommendation (Seanad)                              | ie/oireachtas/bill/2015/44/seanad/3/rec_1               |
| Bill amendment to amendment                               | ie/oireachtas/bill/2015/44/dail/3/amd_1_1               |


