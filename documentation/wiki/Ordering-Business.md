# Ordering business

1. [Order Papers](#order-papers)
2. [Parliamentary Questions](#parliamentary-questions)
3. [Votes](#votes)


## Order Papers

> **STATUS: Not yet designed. This section is a placeholder.**

## Parliamentary Questions

Parliamentary Questions are questions to Ministers and are answered in the Dáil either orally or in writing. A question is submitted in advance of a sitting and is ordered sequentially for each date. Thus, a question can be identified uniquely by a combination of date of sitting and question number.

The IRI for a parliamentary question as published in a question list is:

```
https://data.oireachtas.ie/ie/oireachtas/question/{date}/pq_{n}
https://data.oireachtas.ie/ie/oireachtas/question/2015-01-27/pq_33
```

where {date} is the date of the sitting on which the question was replied to (or withdrawn) and n is a positive integer corresponding to the number of the question on that day's Question list.

The IRI for a parliamentary question that has been taken in a debate is a sub-component of the [debate IRI](Debates#frbr-metadata). As such it has the following pattern as FRBRWork:

```
https://data.oireachtas.ie/ie/oireachtas/debateRecord/dail/{date}/pq_{n}
https://data.oireachtas.ie/ie/oireachtas/debateRecord/dail/2015-01-27/pq_33
```
where date is the date of the sitting on which the question was replied to (or withdrawn), pq_{n} corresponds to the eId of the element of the debate XML in which the question was recorded and n is a positive integer corresponding to the number of the question on the Question list for that date.

## Votes

> **STATUS: Not yet designed. This section is a placeholder.**
