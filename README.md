# Applying-GENRE-on-MaCoCu-bilingual
 
## Preparation of the data

Steps:
- converted TMX file to JSON file, opened JSON as a dataframe (*1-Bitextor-TMX-to-JSON.ipynb)*
- sorted all sentences based on the English source and then English sentence id to get the correct order of sentences (from here onwards: *2-JSON-sentence-file-to-doc-format.ipynb*)
- discarded sentences where Slovene and English text come from different domains (829,191 sentences) to assure that English documents are connected with Slovene (appear on Slovene web)
- discarded duplicated English sentences with the same par id - 299,167 sentences (they exist because one English sentence was shown to be alligned to more than one Slovene sentence from different documents - discarding duplicated sentences assures that there are no duplicates in English text, however it can destroy the structure of Slovene texts. We are only interested in English texts in this preparation of data.)
- merged all sentences into English and Slovene documents (based on the English source (web page URL) and Slovene source (URL) each)
- converted the dataframe where each sentence is one row into a dataframe where each document is one row (by discarding duplicated English documents)
- discarded documents that have less than the median no. of words (English length) - less than 75 --> we are left with 103,281 texts
- saved the document format to CSV

Analysis showed that all sentences from the original TMX file have bicleaner score higher than 0.50 - bad sentences must have been cleaned out before.

Initial no. of sentences: 3,176,311; final no. of texts: 103,281

Initial length of English texts, without deduplicaton of English sentences (before removal of domains that do not match):

![](figures/Initial-English-length.png)

Initial length of English texts after deduplication and removal of domains that do not match:

![](figures/Initial-length-before-filtering-after-deduplication.png)

After deduplication, texts are slightly shorter. The biggest difference is with the longer texts.

### Statistics for Macocu-sl-en after pre-processing

English variants (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.41818   |
| UNK |    0.355303  |
| A   |    0.165703  |
| MIX |    0.0608147 |

English variants (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |    0.563918  |
| MIX |    0.282075  |
| A   |    0.144092  |
| UNK |    0.0099147 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| sl-orig |                0.889166 |
| en-orig |                0.110834 |

Average bi-cleaner score on document level

|       |   average_score |
|:------|----------------:|
| count |  103281         |
| mean  |       0.896688  |
| std   |       0.0644189 |
| min   |       0.502     |
| 25%   |       0.867333  |
| 50%   |       0.9132    |
| 75%   |       0.942571  |
| max   |       0.9905    |

As we can see, almost all of the documents were originally written in Slovene (89%). Most of them are identified as British (42%), followed by "unknown" and much less American texts (English variety detection on document level). On the domain level, most of them (56%) were identified to be British. Most of the texts have quality higher than 0.90 based on the bicleaner score.

Manual analysis of 20 random instances:
- 13 were okay, 7 not okay
- 4 out of 7 bad instances had different domains, 1 out 13 good instances had different domains --> based on this, we discarded instances from different domains
- lowest bicleaner score of good instances was 0.81, bad instances had average scores between 0.73 and 0.88.
- for 4 out of 7 instances there was a huge difference in length of Slovene and English text (205 vs. 55, 139 vs. 3, 625 vs. 55 etc.)

### Analysis of a sample of 100 texts

I detected some issues that need to be addressed:
- many English texts have duplicated sentences (234244, 1001538, 834122, 574769, 779376, 220580 etc.) --> we discarded duplicated sentences with the same ID which removed 8 out of 13 "non-textual" texts
- 13% of texts are non-textual (1887229, 798879, 477792 etc.) - should we apply some heuristics to try to discard them beforehand?

The following results were calculated after removing 13% of texts that were revealed to be non-textual.

**Results**

Macro f1: 0.663, Micro f1: 0.908

Confusion matrix:

![](figures/Confusion-matrix-predicted-sample.png)

Based on the confusion matrix we can see that the macro F1 is so low solely due to very infrequent categories being miss-classified (Other) and the fact that there is no instance, belonging to Forum. Micro F1 is very high, on the other hand.

Classification report:

![](figures/Classification-report-prediction-on-sample.png)

Other notes:
- there are some obvious machine translations (1353811, 1844711 - oblacila.si)
- some English texts do not correspond to Slovene texts (1481642, 183369, 1944325)