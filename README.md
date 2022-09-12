# Applying-GENRE-on-MaCoCu-bilingual
 
## Preparation of the data

Steps:
- converted TMX file to JSON file, opened JSON as a dataframe (*1-Bitextor-TMX-to-JSON.ipynb)*
- sorted all sentences based on the English source and then English sentence id to get the correct order of sentences (from here onwards: *2-JSON-sentence-file-to-doc-format.ipynb*)
- merged all sentences into English and Slovene documents (based on the English source (web page URL) and Slovene source (URL) each)
- converted the dataframe where each sentence is one row into a dataframe where each document is one row (by discarding duplicated English documents)
- discarded documents that have less than the median no. of words (English length) - less than 79 --> we are left with 141,066 texts
- discarded documents where Slovene and English text come from different domains (36213 texts) to assure that English documents are connected with Slovene (appear on Slovene web)
- saved the document format to CSV

Analysis showed that all sentences from the original TMX file have bicleaner score higher than 0.50 - bad sentences must have been cleaned out before.

Initial no. of sentences: 3,176,311, initial no. of documents: 281,475, final no. of texts: 104,853

Initial length of English texts:

<img style="width:100%" src="figures/Initial-English-length.png">

### Statistics for Macocu-sl-en after pre-processing

English variants (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.390137  |
| UNK |    0.389793  |
| A   |    0.162199  |
| MIX |    0.0578715 |

English variants (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |   0.539765   |
| MIX |   0.284293   |
| A   |   0.16629    |
| UNK |   0.00965161 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| sl-orig |                0.886241 |
| en-orig |                0.113759 |

Average bi-cleaner score on document level

|       |   average_score |
|:------|----------------:|
| count |  104853         |
| mean  |       0.886736  |
| std   |       0.0682533 |
| min   |       0.502     |
| 25%   |       0.8519    |
| 50%   |       0.904     |
| 75%   |       0.93675   |
| max   |       0.9905    |

As we can see, almost all of the documents were originally written in Slovene (89%). Most of them are identified as British (39%), followed by "unknown" and much less American texts (English variety detection on document level). On the domain level, most of them (54%) were identified to be British. Most of the texts have quality higher than 0.90 based on the bicleaner score.

Manual analysis of 20 random instances:
- 13 were okay, 7 not okay
- 4 out of 7 bad instances had different domains, 1 out 13 good instances had different domains --> based on this, we discarded instances from different domains
- lowest bicleaner score of good instances was 0.81, bad instances had average scores between 0.73 and 0.88.
- for 4 out of 7 instances there was a huge difference in length of Slovene and English text (205 vs. 55, 139 vs. 3, 625 vs. 55 etc.)

### Analysis of a sample of 100 texts

I detected some issues that need to be addressed:
- many English texts have duplicated sentences (234244, 1001538, 834122, 574769, 779376, 220580 etc.)- should I duplicate English sentences before joining them into texts? Slovene sentences do not seem to be duplicated - maybe this is a problem with different alignment of sentences and one English sentence is aligned with multiple Slovene sentences and therefore appears multiple times. I am afraid that I will loose some structure of Slovene texts if I remove all duplicated English sentences - however, if we are interested only in English texts, that does not matter. 
- 13% of texts are non-textual (1887229, 798879, 477792 etc.) - should we apply some heuristics to try to discard them beforehand?

The following results were calculated after removing 13% of texts that were revealed to be non-textual.

**Results**

Macro f1: 0.663, Micro f1: 0.908

Confusion matrix:

<img style="width:100%" src="Applying-GENRE-on-MaCoCu-bilingual/figures/Confusion-matrix-predicted-sample.png">

Based on the confusion matrix we can see that the macro F1 is so low solely due to very infrequent categories being miss-classified (Other) and the fact that there is no instance, belonging to Forum. Micro F1 is very high, on the other hand.

Classification report:

<img style="width:100%" src="Applying-GENRE-on-MaCoCu-bilingual/figures/Classification-report-prediction-on-sample.png">

Other notes:
- there are some obvious machine translation (1353811, 1844711 - oblacila.si)
- some English texts do not correspond to Slovene texts (1481642, 183369, 1944325)