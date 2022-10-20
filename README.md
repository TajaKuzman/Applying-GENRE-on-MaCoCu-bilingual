# Applying-GENRE-on-MaCoCu-bilingual

Summary:

I applied the genre classifier, developed in previous experiments (see https://github.com/TajaKuzman/Genre-Datasets-Comparison, especially "Data" and "The distribution of X-GENRE labels in the joined dataset (X-GENRE dataset)" under [Joint schema](https://github.com/TajaKuzman/Genre-Datasets-Comparison#joint-schema-x-genre), and [X-GENRE classifier](https://github.com/TajaKuzman/Genre-Datasets-Comparison#x-genre-classifier)) to the English documents extracted from MaCoCu bilingual corpora.

This consisted of the following steps:

1. [Preparation of data](#preparation-of-the-data): converted TMX file to CSV, discarded sentences where English and text in other language come from different domain, discarded duplicated English sentences, merged sentences into documents based on source URL.
2. Pre-processing: discarded all documents, shorter than the median length; discarded non-textual documents based on a no. of punctuations per no. of words heuristic
3. Applying the X-GENRE classifier to the data (see [manual analysis of the results](#genre-prediction))
4. Post-processing: discarded unreliable predictions - labels "Other" and "Forum", and labels predicted with confidence lower than 0.9
5. Analysis of results for [MaCoCu-sl-en](#macocu-sl-en), [MaCoCu-is-en](#macocu-is-en), [MaCoCu-mt-en](#macocu-mt-en), [MaCoCu-mk-en](#macocu-mk-en), [MaCoCu-tr-en](#macocu-tr-en), [MaCoCu-bg-en](#macocu-bg-en), [MaCoCu-hr-en](#macocu-hr-en) also in regards to varieties of English language.

Sizes of datasets:

| Dataset      | Original no. of texts | Pre-processed dataset (texts) | Texts with genre labels |
|--------------|-----------------------|-------------------------------|-------------------------|
| MaCoCu-sl-en | 285,892               | 101,807                       | 91,459                  |
| MaCoCu-mt-en | 47,206                | 23,999                        | 21,376                  |
| MaCoCu-is-en | 40,340                | 13,174                        | 11,639                  |
| MaCoCu-mk-en | 54,957                | 22,055                        | 20,108                  |
| MaCoCu-tr-en | 796,473               | 213,147                       | 193,782                 |
| MaCoCu-bg-en | 287,456               | 107,404                       | 88,544 (18% discarded!) |

- Turkish: much more texts were discarded (only ¼ remaining) - 45% of all sentences (42% of all texts) came from different domains; 48% of remaining English sentences were duplicated
- Bulgarian: in other datasets, we lost around 10% of genre labels with post-processing, in MaCoCu-bg, there were much more texts “Other” → labels discarded from 18% of all texts

Comparison of the datasets:

| Dataset                                               | MaCoCu-sl-en     | MaCoCu-is-en   | MaCoCu-mt-en             | MaCoCu-mk-en     | MaCoCu-tr-en     | MaCoCu-bg-en         |
|-------------------------------------------------------|------------------|----------------|--------------------------|------------------|------------------|----------------------|
| English   variants (doc level)                        | B: 42%, A: 17%   | B: 39%, A: 18% | B: 63%, A: 9%            | B: 19 %, A: 31%  | B: 12%, A: 34%   | B: 18%, A: 33%       |
| English   variants (domain level)                     | B: 57%, A: 14%   | B: 59%, A: 13% | B: 88%, A: 11%           | B: 20%, A: 49%   | 100% UNK (??)    | B: 30%, A: 40%       |
| Translation   direction (en-orig)                     | 12%              | 23%            | 59%                      | 41%              | 33%              | 46%                  |
| English   text length (words; median)                 | 190              | 201            | 300                      | 194              | 184              | 170                  |
| Average   bi-cleaner score (median)                   | 0.91             | 0.88           | 0.93                     | 0.93             | 0.88             | 0.91                 |
| Number of   domains which cover more than 1% of texts | 5                | 16             | 13                       | 26               | 7                | 7                    |
| Sum of %   covered by these domains                   | 10%              | 35%            | 77%                      | 38%              | 15%              | 25%                  |
| Most   frequent domain (frequency)                    | oblacila.si (4%) | norden (7%)    | europarl.europa.eu (23%) | stat.gov.mk (6%) | booking.com (7%) | goldenpages.bg (12%) |

Distribution of genres:

![](figures/Genre-distribution-comparison.png)

- There is much more News in Macedonian parallel corpus (MaCoCu-mk-en) than in others.
- There is much more Legal in Maltese corpus (MaCoCu-mt-en) than in others.
- Slovene (MaCoCu-sl-en), Bulgarian (MaCoCu-bg-en) and Turkish (MaCoCu-tr-en) corpora have much more Promotion than others.
- There is very little Opinion/Argumentation in Turkish (MaCoCu-tr-en) corpus.

## Interesting findings

- MaCoCu-tr-en: Errors in identification of English variant on domain level: 100% UNK (?)
- Very worrying distribution of domains in MaCoCu-mt-en: 13 most frequent domains cover 77% of all texts; many genres are mostly represented by texts from one or a very small number of domains (Opinion/Argumentation, News, Legal, Prose/Lyrical)
- quite a lot of Poetry/Lyrical consists of Bible, Islam texts (noticed in all corpora)
- MaCoCu-sl-en: 48% of all Legal texts come from 2 sites: eur-lex.europa.eu (32%), europarl.europa.eu: 16%
- MaCoCu-bg-en: 41% of Opinion/Argumentation come from one domain - goldenpages.bg


## Steps

1. Copy the notebook "Complete-Pipeline.ipynb" from the root folder to a folder dedicated to the new parallel corpus.
2. Convert TMX file to JSON and pre-process data by runing the Complete-Pipeline.ipynb notebook; add information on the discarded texts and general statistics of the corpus to the README.
4. Apply genre prediction to the file: define the file path in predict_genres.py and run the code in the terminal: ```nohup python predict_genres.py```
5. Post-process the data and analyse the results by using the notebook "Complete-Pipeline.ipynb"; add information on the results to the README.

## Preparation of the data

Steps:
- converted TMX file to JSON file, opened JSON as a dataframe
- sorted all sentences based on the English source and then English sentence id to get the correct order of sentences
- discarded sentences where English text and text in other language come from different domains to assure that English documents are connected with the national domain in interest (appear in Slovene, Maltese etc. web)
- discarded duplicated English sentences with the same par id (they exist because one English sentence was shown to be alligned to more than one sentence in another language from different documents - discarding duplicated sentences assures that there are no duplicates in English text, however it can destroy the structure of texts in the other language. We are only interested in English texts in this preparation of data.)
- merged all sentences into English and Slovene/Maltese/etc. documents (based on the English source (web page URL) and Slovene/Maltese/etc. source (URL) each)
- converted the dataframe where each sentence is one row into a dataframe where each document is one row (by discarding duplicated English documents)
- discarded documents that have less than the median no. of words (English length) - less than 75 for Slovene, 79 for all other
- discarded documents that have punctuation per no. of words ratio less than 0.015 or more than 0.2 (non-textual documents)
- saved the document format to CSV

Analysis showed that all sentences from the original TMX file have bicleaner score higher than 0.50 - bad sentences must have been cleaned out before.

## Genre prediction

### Analysis of a sample of 100 texts - first round

I detected some issues that need to be addressed:
- many English texts have duplicated sentences (234244, 1001538, 834122, 574769, 779376, 220580 etc.) --> we discarded duplicated sentences with the same ID which removed 8 out of 13 "non-textual" texts
- 13% of texts are non-textual (1887229, 798879, 477792 etc.) --> discarded texts based on the ratio of punctuation per words -> this discarded 2 of the remaining 5 "non-textual" texts

The following results were calculated after removing 13% of texts that were revealed to be non-textual: Macro f1: 0.663, Micro f1: 0.908

<!-- 

Confusion matrix:

![](figures/Confusion-matrix-predicted-sample.png)

 -->

Macro F1 is so low solely due to very infrequent categories being miss-classified (Other) and the fact that there is no instance, belonging to Forum. Micro F1 is very high, on the other hand.

<!--
Classification report:

![](figures/Classification-report-prediction-on-sample.png)
-->

Other notes:
- there are some obvious machine translations (1353811, 1844711 - oblacila.si)
- some English texts do not correspond to Slovene texts (1481642, 183369, 1944325)

### Analysis of a sample of 150 texts (second round - pre-processed corpus)

I created a sample from the pre-processed MaCoCu-sl-en to which we applied the classifier by spliting the corpus with sci-kit learn, stratifying based on the predicted label distribution. To be able to analyse the performance on less frequent categories as well, I added 10 instances of each of categories that previously had less than 10 instances in the sample corpus ('Opinion/Argumentation', 'Legal',  'Other', 'Prose/Lyrical', 'Forum'). Then I discarded any duplicates (there were none) and shuffled the texts. Then I performed manual annotation where I confirmed that the label is correctly predicted in any case where this could be the label.

The distribution of predicted labels in the sample:

|                         |   X-GENRE |
|:------------------------|----------:|
| Information/Explanation |        32 |
| Promotion               |        31 |
| Legal                   |        16 |
| Opinion/Argumentation   |        15 |
| News                    |        13 |
| Other                   |        12 |
| Instruction             |        11 |
| Forum                   |        10 |
| Prose/Lyrical           |        10 |

I found 2 "Non-textual" instances in the sample. They were removed from the following analysis.

Macro F1: 0.713, Micro F1: 0.777

Confusion matrix:

![](figures/Confusion-matrix-predicted-sample-150-instances-second-round.png)

Classification report:

![](figures/Classification-report-manual-analysis-on-150-instances.png)

What I learnt from the analysis:
- "Other" is assigned to texts about which the classifier is not certain about (which is how this category is intended to work) --> we can discard predictions for these texts (2.2k texts - 0.2% of all texts).
- There are still some "Non-textual" instances (2 - 0.17% of all instances), but they fall under Information/Explanation which technically is not horribly wrong.
- the most frequent categories (Information/Explanation, Promotion, News, Instruction, Legal) have a high precision - 0.73-0.97
- Prose/Lyrical is identified suprisingly well despite being less frequent category in the training dataset (F1 score 0.95)
- Forum was not identified well, but this is mostly due to the fact that there were no nice instances of forum in the sample.

If the analysis would be performed on a stratified sample (following the distribution of labels in the entire corpus), the micro and macro F1 scores are even better: Macro f1: 0.71, Micro f1: 0.867.

To get more reliable predictions, I suggest:
- discarding predicted labels of all texts, labelled as "Other"
- discarding predicted labels of all texts with the certainty of prediction lower than 0.9 ("chosen_category_distribution") - (after discarding Other,) we discarded 25% of incorrectly predicted labels with this method while losing 5% of correctly predicted labels.
- discarding predicted labels of all texts, labelled as "Forum" since most were incorrect (due to this category not being present in the data)

Results of manual analysis after proposed post-processing:

- if we discard "Other" and predictions with certainty under 0.9, 26 instances are without a label (17%): Macro f1: 0.827, Micro f1: 0.871;
- if we also discard "Forum", in total, 35 instances are without a label (23%): Macro f1: 0.92, Micro f1: 0.922; on a balanced sample (stratified based on labels): Macro f1: 0.87-0.90, Micro f1: 0.91-0.92 (scores could be also a bit smaller - depends on which instances of Opinion and Legal are sampled out)

Results after discarding "Other", "Forum" and predictions with certainty under 0.9 (on the entire sample - not stratified):

![](figures/Confusion-matrix-predicted-sample-cleaned-115-instances-second-round.png)

Classification report:

![](figures/Classification-report-manual-analysis-on-cleaned-sample-115-instances.png)

Results on the stratified sample:

![](figures/Confusion-matrix-predicted-sample-cleaned-stratified-92-instances-second-round.png)

## MaCoCu-sl-en

Initial no. of texts: 285,892 (no. of sentences: 3,176,311); final no. of texts: 101,807

Pre-processing:
- discarded sentences where English text and text in other language come from different domains (829,191 sentences)
- discarded duplicated English sentences (with the same par id) (299,167 sentences)
- discarded texts that have length less than the median - 75 words --> we are left with 103,281 texts
- discarded non-textual documents based on a heuristic - discarded 1,474 texts

<!--
Initial length of English texts, without deduplicaton of English sentences (before removal of domains that do not match):

![](figures/Initial-English-length.png)
-->

Final length of English texts:

![](figures/Initial-length-after-filtering.png)


### Statistics for Macocu-sl-en after pre-processing

English variants (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.421287  |
| UNK |    0.351813  |
| A   |    0.165755  |
| MIX |    0.0611451 |

English variants (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |   0.567122   |
| MIX |   0.281886   |
| A   |   0.140992   |
| UNK |   0.00999931 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| sl-orig |                  0.8893 |
| en-orig |                  0.1107 |

Average bi-cleaner score on document level

|       |   average_score |
|:------|----------------:|
| count |  101807         |
| mean  |       0.897452  |
| std   |       0.0634431 |
| min   |       0.502     |
| 25%   |       0.868429  |
| 50%   |       0.913667  |
| 75%   |       0.942684  |
| max   |       0.9905    |

As we can see, almost all of the documents were originally written in Slovene (89%). Most of them are identified as British (42%), followed by "unknown" and much less American texts (English variety detection on document level). On the domain level, most of them (57%) were identified to be British. Most of the texts have quality higher than 0.90 based on the bicleaner score.

<!--

Manual analysis of 20 random instances:
- 13 were okay, 7 not okay
- 4 out of 7 bad instances had different domains, 1 out 13 good instances had different domains > based on this, we discarded instances from different domains
- lowest bicleaner score of good instances was 0.81, bad instances had average scores between 0.73 and 0.88.
- for 4 out of 7 instances there was a huge difference in length of Slovene and English text (205 vs. 55, 139 vs. 3, 625 vs. 55 etc.)

-->

Statistics on English domains: there are 6,066 different domains.

There are only 5 domains which cover more than 1% of data, the domain with the largest frequency is oblacila.si which covers 3.5% of the data.

|                                            |   Count |   Percentage |
|:-------------------------------------------|--------:|-------------:|
| oblacila.si (95% Promotion)                               |    3600 |  3.5361      |
| europarl.europa.eu   (40% Legal, 39% News)                      |    2444 |  2.40062     |
| eur-lex.europa.eu   (84% Legal)                       |    2128 |  2.09023     |
| eu2008.si  (80% News)                               |    1355 |  1.33095     |
| gov.si     (56% News, 26% Information/Explanation)                                |    1087 |  1.06771     |

### Prediction of genres to the entire MaCoCu-sl-en corpus

By predicting on batches of 8 instances, the prediction was much faster - 6 hours for around 100k texts (without using batches, it would be 14 days).

<!--
### Results of predictions before pre-processing

General statistics:

|                         |   X-GENRE (count)|
|:------------------------|----------:|
| Information/Explanation |     32368 |
| Promotion               |     31384 |
| News                    |     13605 |
| Instruction             |     10846 |
| Legal                   |      5866 |
| Opinion/Argumentation   |      4863 |
| Other                   |      2194 |
| Forum                   |       405 |
| Prose/Lyrical           |       276 |

|                         |    X-GENRE (percentages)|
|:------------------------|-----------:|
| Information/Explanation | 0.317935   |
| Promotion               | 0.30827    |
| News                    | 0.133635   |
| Instruction             | 0.106535   |
| Legal                   | 0.0576188  |
| Opinion/Argumentation   | 0.0477669  |
| Other                   | 0.0215506  |
| Forum                   | 0.00397812 |
| Prose/Lyrical           | 0.00271101 |

The certainty of prediction (softmax scores of the raw output):

|       |   chosen_category_distr |
|:------|------------------------:|
| mean  |                0.970066 |
| std   |                0.089027 |
| min   |                0.247184 |
| 25%   |                0.995622 |
| 50%   |                0.998666 |
| 75%   |                0.998966 |
| max   |                0.999145 |



Distribution of English varieties in genres (doc level):

Distribution in entire corpus:

English variants (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.421287  |
| UNK |    0.351813  |
| A   |    0.165755  |
| MIX |    0.0611451 |

Very similar distribution of variants than the distribution in entire corpus: Opinion/Argumentation, Information/Explanation, Other

More British than in general distribution: News (0.55), Legal (0.68)

More American than in general distribution: Promotion (0.22), Instruction (0.21), Prose/Lyrical (0.23)

More Unknown than in general distribution: Forum (0.51)

-->

Post-processing:
- discarded labels "Other" and "Forum"
- discarded labels where prediction certainty is less than 0.9.

Post-processing discarded predictions of 10,348 texts (10%). Number of texts with predicted labels: 91,459.

Final distribution of labels:

|                         |   final-X-GENRE (count) |
|:------------------------|----------------:|
| Information/Explanation |           30307 |
| Promotion               |           29629 |
| News                    |           12207 |
| Instruction             |            9801 |
| Legal                   |            5317 |
| Opinion/Argumentation   |            3980 |
| Prose/Lyrical           |             218 |

|                         |   final-X-GENRE (percentages) |
|:------------------------|----------------:|
| Information/Explanation |      0.331373   |
| Promotion               |      0.323959   |
| News                    |      0.13347    |
| Instruction             |      0.107163   |
| Legal                   |      0.0581353  |
| Opinion/Argumentation   |      0.0435168  |
| Prose/Lyrical           |      0.00238358 |

**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 0; most frequent domain: ourspace.si (5% of all Opinion/Argumentation)
- News: domains with more than 10%: 0; most frequent domain: eu2008.si (8% of all News)
- Legal: domains with more than 10%: 2; most frequent domain: eur-lex.europa.eu (32% of all Legal), europarl.europa.eu: 16%
- Information/Explanation:  domains with more than 10%: 0; most frequent domain: ricinus2.mf.uni-lj.si (3%)
- Promotion:  domains with more than 10%: 1; most frequent domain: oblacila.si (11%)
- Instruction: domains with more than 10%: 1; most frequent domain: support.apple.com (10%)
- Prose/Lyrical: domains with more than 10%: 2; most frequent domain: jw.org (26%), bsf.si (22%)

**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.42  |
| UNK |    0.35  |
| A   |    0.17  |
| MIX |    0.06 |

- Opinion/Argumentation: 0.43 B, 0.17 A; 1 point more B, same A --> same distribution
- News: 0.55 B, 0.09 A; 13 points more B, 8 points less A --> more B, less A
- Legal: 0.69 B, 0.06 A; 27 points more B, 11 points less A --> more B, less A
- Information/Explanation: 0.43 B, 0.14 A; 1 point more B, 3 points less A --> same distribution
- Promotion: 0.36 B, 0.22 A; 6 points less B, 5 points more A --> less B, more A
- Instruction: 0.26 B, 0.22 A; 16 points less B, 5 points more A --> less B, more A
- Prose/Lyrical: 0.33 B, 0.25 A; 9 points less B, 8 points more A --> less B, more A


**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| mean  |     428.811 |
| std   |    1694.06  |
| min   |      75     |
| 25%   |     119     |
| 50%   |     190     |
| 75%   |     346     |
| max   |   98761     |

Median lengths:
- Information/Explanation: 179
- Promotion: 159
- Prose/Lyrical: 155
- Opinion/Argumentation: 230
- News: 232
- Instruction: 226
- Legal: 429

Similar length to the general length (10 words difference): 
Slightly shorter (10-100 words difference): Information/Explanation, Promotion, Prose/Lyrical
Much shorter (more than 100 words difference): 
Slightly longer (10-100 words difference): Opinion/Argumentation, News, Instruction
Much longer (more than 100 words difference): Legal


## MaCoCu-is-en

Initial number of segments (English sentences): 355,100, initial number of texts: 40,340.

Pre-processing:
- discarded sentences where source and target are from different domains (97,943 sentences and 13,691 texts discarded)
- discarded duplicated English sentences (with the same par id and text - 14,169 sentences and 346 texts discarded)
- discarded duplicated English texts: 26,218 texts remaining

Initial length of remaining texts:

|       |   en_length |
|:------|------------:|
| count |   26218     |
| mean  |     190.974 |
| std   |     389.449 |
| min   |       1     |
| 25%   |      30     |
| 50%   |      79     |
| 75%   |     203     |
| max   |   11125     |

- all texts with length, lower than the median (79 words) were discarded --> 13,174 texts remaining

### Statistics for MaCoCu-is-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.391908  |
| UNK |    0.371186  |
| A   |    0.178306  |
| MIX |    0.0586003 |

English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |    0.5879    |
| MIX |    0.26317   |
| A   |    0.134735  |
| UNK |    0.0141946 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| is-orig |                0.770609 |
| en-orig |                0.229391 |


Average bicleaner score

|       |   average_score |
|:------|----------------:|
| count |   13174         |
| mean  |       0.865217  |
| std   |       0.0589788 |
| min   |       0.512     |
| 25%   |       0.836195  |
| 50%   |       0.875971  |
| 75%   |       0.905872  |
| max   |       0.9735    |

Length of English text

|       |   en_length |
|:------|------------:|
| count |   13174     |
| mean  |     346.647 |
| std   |     502.707 |
| min   |      79     |
| 25%   |     124     |
| 50%   |     201     |
| 75%   |     380     |
| max   |   11125     |

As we can see, almost all of the documents were originally written in Icelandic (77%), but less than in MaCoCu-sl-en (Slovene: 89%). Most of them are identified as British (39%; in MaCoCu-sl-en: 42%), followed by "unknown" and much less American texts (English variety detection on document level). On the domain level, most of them (59%; in MaCoCu-sl-en: 57%) were identified to be British. Most of the texts have quality higher than 0.88 based on the bicleaner score (in MaCoCu-sl-en the score is higher - median is 0.90).

Statistics on English domains: there are 1,112 different domains.

There are 16 domains which cover more than 1% of data, the domain with the largest frequency is norden which covers 7% of the data.

|                                  |   Count |   Percentage |
|:---------------------------------|--------:|-------------:|
| norden (46% News, 25% Information/Explanation)                          |     913 |   6.93032    |
| eso (69% Information/Explanation, 30% News)                             |     528 |   4.00789    |
| landssjodir  (96% News)                    |     373 |   2.83133    |
| rnh   (70% News, 29% Information/Explanation)                           |     336 |   2.55048    |
| lhi  (48% Information/Explanation, 24% Opinion/Argumentation)                            |     320 |   2.42903    |
| booking    (54% Promotion, 44 Instruction)                      |     310 |   2.35312    |
| neway  (38% Instruction, 23% News)                          |     274 |   2.07985    |
| efling  (63% News)                         |     264 |   2.00395    |
| garnstudio   (94% Instruction)                    |     251 |   1.90527    |
| laeknabladid (100% Information/Explanation)                    |     219 |   1.66237    |
| skaftfell   (40% Information/Explanation, 36% News)                     |     170 |   1.29042    |
| linde-gas   (55% Promotion, 34% Information/Explanation)                     |     147 |   1.11583    |
| land  (45% Instruction, 33% Legal)                           |     140 |   1.0627     |
| landsbokasafn (60% Information/Explanation, 35% News)                   |     138 |   1.04752    |
| arionbanki (68% News)                       |     135 |   1.02475    |
| borgarbokasafn  (64% Promotion)                 |     132 |   1.00197    |

### Results of genre prediction on MaCoCu-is-en

Distribution of labels:

|                         |   X-GENRE (count) |
|:------------------------|----------:|
| Information/Explanation |      4025 |
| News                    |      3160 |
| Instruction             |      2061 |
| Promotion               |      1994 |
| Legal                   |       758 |
| Opinion/Argumentation   |       709 |
| Other                   |       323 |
| Forum                   |        92 |
| Prose/Lyrical           |        52 |

|                         |    X-GENRE (percentages) |
|:------------------------|-----------:|
| Information/Explanation | 0.305526   |
| News                    | 0.239866   |
| Instruction             | 0.156445   |
| Promotion               | 0.151359   |
| Legal                   | 0.0575376  |
| Opinion/Argumentation   | 0.0538181  |
| Other                   | 0.024518   |
| Forum                   | 0.00698345 |
| Prose/Lyrical           | 0.00394717 |

Post-processing:
- discarded labels where the category is "Other" (323 labels, 2%) and "Forum" (92 labels, 0.7%)
- discarded labels where prediction confidence was below 0.9 (1120 labels, 10%).

Final no. of texts with predicted labels: 11,639.

**Final results**

Distribution of labels:

|                         |   final-X-GENRE (count) |
|:------------------------|----------------:|
| Information/Explanation |            3753 |
| News                    |            2916 |
| Instruction             |            1851 |
| Promotion               |            1806 |
| Legal                   |             672 |
| Opinion/Argumentation   |             595 |
| Prose/Lyrical           |              46 |

|                         |   final-X-GENRE (percentage) |
|:------------------------|----------------:|
| Information/Explanation |      0.32245    |
| News                    |      0.250537   |
| Instruction             |      0.159034   |
| Promotion               |      0.155168   |
| Legal                   |      0.0577369  |
| Opinion/Argumentation   |      0.0511212  |
| Prose/Lyrical           |      0.00395223 |

Compared to MaCoCu-sl-en, there is much more News in Icelandic corpus (25% versus 13% in MaCoCu-sl-en), much less Promotion (15% versus 32%) and similar distributions of other labels.

**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 2; most frequent domain: norden (16% of all Opinion), lhi (10%)
- News: domains with more than 10%: 2; most frequent domain: norden (13% of all News), landssjodir (12%)
- Legal: domains with more than 10%: 0; most frequent domain: randa (8%)
- Information/Explanation:  domains with more than 10%: 0; most frequent domain: eso (9%)
- Promotion:  domains with more than 10%: 0; most frequent domain: booking (5%)
- Instruction: domains with more than 10%: 1; most frequent domain: garnstudio (13%)
- Prose/Lyrical: domains with more than 10%: 2; most frequent domain: biblegateway (33%), heathengods (13%)

**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.39  |
| UNK |    0.37  |
| A   |    0.18  |
| MIX |    0.06 |

- Instruction: 0.35 B, 0.21 A; 4 points less B, 3 points more A --> similar distribution
- News: 0.50 B, 0.11 A; 11 points more B, 7 points less A --> more B, less A
- Promotion: 0.28 A, 0.25 B; 10 points more A, 14 points less B --> more A, less B
- Information/Explanation: 0.40 B, 0.15 A; 1 point more B, 3 points less B --> similar distribution
- Legal: 0.50 B, 0.13 A; 11 points more B, 5 points less A --> more B, less A
- Opinion/Argumentation: 0.36 B, 0.25 A; 3 points less B, 7 points more A; more A
- Prose/Lyrical: 0.30 B, 0.28 A; 9 points less B, 10 points more A --> less B, more A


**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| mean  |     346.647 |
| std   |     502.707 |
| min   |      79     |
| 25%   |     124     |
| 50%   |     201     |
| 75%   |     380     |
| max   |   11125     |

Length in terms of median:
- Instruction: 248
- News: 243
- Promotion: 140
- Information/Explanation: 170
- Legal: 345
- Opinion/Argumentation: 270
- Prose/Lyrical: 400

Similar length to the general length (10 words difference): 
Slightly shorter (10-100 words difference): Promotion, Information/Explanation
Much shorter (more than 100 words difference):
Slightly longer (10-100 words difference): Instruction, News, Opinion/Argumentation
Much longer (more than 100 words difference): Legal, Prose/Lyrical


## MaCoCu-mt-en

Initial no. of sentences: 1,231,654; no. of texts: 47,206

Pre-processing:
- discarded instances where English and Maltese come from different domains (129,097 sentences, 9257 texts)
- discarded duplicated English sentences (with the same par id - 64,188 sentences, 283 texts)
- discarded duplicated documents (85 texts) --> no. of remaining texts: 37,581

Initial length of texts:

|       |   en_length |
|:------|------------:|
| count |   37581     |
| mean  |     838.355 |
| std   |    3183.44  |
| min   |       2     |
| 25%   |      48     |
| 50%   |     142     |
| 75%   |     440     |
| max   |  123935     |

- texts are in general longer than in other datasets, so we will not discard texts based on the median (we would lose useful texts which could change the distribution of genres). I discarded the texts with length less than 79 which is similar to the other two MaCoCu datasets. --> remaining no. of texts: 24,104
- non-textual texts filtered out based on a heuristic (105 texts) -> final no. of texts: 23,999

### Statistics for MaCoCu-mt-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.63386   |
| UNK |    0.241593  |
| A   |    0.0928372 |
| MIX |    0.0317097 |


English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |  0.881245    |
| A   |  0.113005    |
| MIX |  0.00504188  |
| UNK |  0.000708363 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| en-orig |                  0.5909 |
| mt-orig |                  0.4091 |


Average bicleaner score

|       |   average_score |
|:------|----------------:|
| mean  |       0.91717   |
| std   |       0.0637326 |
| min   |       0.5       |
| 25%   |       0.883162  |
| 50%   |       0.929562  |
| 75%   |       0.962129  |
| max   |       1         |

Length of English text

|       |   en_length |
|:------|------------:|
| count |    23999    |
| mean  |     1290.69 |
| std   |     3911.68 |
| min   |       79    |
| 25%   |      153    |
| 50%   |      300    |
| 75%   |      853    |
| max   |   123935    |

In contrast to the other two datasets where almost all of the documents were originally written in Icelandic (77%) or Slovene (89%), here, most of the texts were originally written in English (59%), not Maltese. There is much more British, and much less American and Unknown in this corpus in comparison to the other two (63%; MaCoCu-is-en: 39%, MaCoCu-sl-en: 42%) (English variety detection on document level). On the domain level, 88% of texts were identified to be British (MaCoCu-is-en: 59%, MaCoCu-sl-en: 57%). Most of the texts have quality higher than 0.93 based on the bicleaner score (in MaCoCu-sl-en the score is lower - median is 0.90, even lower in MaCoCu-is-en: 0.88). Texts are generally longer than in other two corpora.

The distribution of domains in the Maltese corpus is much more worrying than in the others - there are 13 domains which cover more than 1% of data, three of them cover more than 10 % (jointly they cover 49% of data); the domain with the largest frequency is europarl.europa.eu which covers 23% of the data.

|                                    |   Count |   Percentage |
|:-----------------------------------|--------:|-------------:|
| europarl.europa.eu  (42% Legal, 41% News)               |    5589 |  23.2885     |
| newsbook.com.mt  (94% News)                  |    3139 |  13.0797     |
| eur-lex.europa.eu (84% Legal)                 |    3101 |  12.9214     |
| wol.jw.org (45% Information/Explanation, 38% Prose/Lyrical)                        |    1632 |   6.80028    |
| dg-justice-portal-demo.eurodyn.com (60% Legal, 21 % Instruction) |    1255 |   5.22938    |
| jw.org   (48% Information/Explanation, 27% Instruction)                          |     749 |   3.12096    |
| europa.eu (51% Instruction, 25% Information/Explanation)                         |     617 |   2.57094    |
| ec.europa.eu   (44% Information/Explanation, 22% News)                    |     528 |   2.20009    |
| tvm.com.mt  (97% News)                       |     445 |   1.85424    |
| cor.europa.eu  (89% News)                    |     422 |   1.75841    |
| weekly.uhm.org.mt (76% News)                 |     384 |   1.60007    |
| cnimalta.org  (63% Opinion/Argumentation)                     |     267 |   1.11255    |
| ecb.europa.eu   (54% News)                   |     241 |   1.00421    |

### Results of genre prediction on MaCoCu-mt-en

Distribution of labels:

|                         |   X-GENRE (count) |
|:------------------------|----------:|
| News                    |      8046 |
| Legal                   |      6443 |
| Information/Explanation |      4677 |
| Instruction             |      2075 |
| Opinion/Argumentation   |      1025 |
| Promotion               |       687 |
| Prose/Lyrical           |       653 |
| Other                   |       345 |
| Forum                   |        48 |

|                         |    X-GENRE (percentages) |
|:------------------------|-----------:|
| News                    | 0.335264   |
| Legal                   | 0.26847    |
| Information/Explanation | 0.194883   |
| Instruction             | 0.0864619  |
| Opinion/Argumentation   | 0.0427101  |
| Promotion               | 0.0286262  |
| Prose/Lyrical           | 0.0272095  |
| Other                   | 0.0143756  |
| Forum                   | 0.00200008 |

Post-processing:
- discarded labels where the category is "Other" (345 labels, 1.4%) and "Forum" (48 labels, 0.2%)
- discarded labels where prediction confidence was below 0.9 (2230 labels, 9%).

Final no. of texts with predicted labels: 21,376.

**Final results**

Distribution of labels:

|                         |   final-X-GENRE (count) |
|:------------------------|----------------:|
| News                    |            7481 |
| Legal                   |            5962 |
| Information/Explanation |            4107 |
| Instruction             |            1829 |
| Opinion/Argumentation   |             820 |
| Prose/Lyrical           |             589 |
| Promotion               |             588 |


|                         |   final-X-GENRE (percentages) |
|:------------------------|----------------:|
| News                    |       0.349972  |
| Legal                   |       0.278911  |
| Information/Explanation |       0.192131  |
| Instruction             |       0.0855632 |
| Opinion/Argumentation   |       0.0383608 |
| Prose/Lyrical           |       0.0275543 |
| Promotion               |       0.0275075 |

Compared to other two corpora, there is much more News (35% versus Icelandic: 25%, Slovene: 13%), Legal (28% versus Icelandic 6%) and Prose/Lyrical (3% versus Icelandic: 0.3%), and much less Information/Explanation (19% versus Icelandic: 32%) and Promotion (3% versus Icelandic: 16%, Slovene: 32%).

**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 4 (covering 56% of this genre class); most frequent domains: cnimalta.org (18% of all Opinion), wol.jw.org (17%), churchofjesuschrist.org (11%), jw.org (11%)
- News: domains with more than 10%: 2 (covering 63% of this genre class); most frequent domain: newsbook.com.mt (38% of all News), europarl.europa.eu (26%)
- Legal: domains with more than 10%: 3 (covering 85% of all Legal); most frequent domain: eur-lex.europa.eu (41%), europarl.europa.eu (33%), dg-justice-portal-demo.eurodyn.com (11%)
- Information/Explanation:  domains with more than 10%: 2; most frequent domain: europarl.europa.eu (19%), wol.jw.org (15%)
- Promotion:  domains with more than 10%: 1; most frequent domain: airmalta.com (11%)
- Instruction: domains with more than 10%: 3; most frequent domain: europa.eu (15%), dg-justice-portal-demo.eurodyn.com (12%), jw.org (10%)
- Prose/Lyrical: domains with more than 10%: 1 (covering 88% of Prose/Lyrical); most frequent domain: wol.jw.org (88%)

**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.63   |
| UNK |    0.24  |
| A   |    0.09 |
| MIX |    0.03 |

Distribution in each genre:
- News: 0.68 B, 0.02 A; 5 points more B, 7 points less A --> more B, less A
- Opinion/Argumentation: 0.40 B, 0.34 A; 23 less B, 25 more A --> less B, more A
- Promotion: 0.52 B, 0.07 A; 11 less B, 2 less A --> less B
- Instruction: 0.51 B, 0.14 A; 12 less B, 5 more A --> less B, more A
- Information/Explanation: 0.59 B, 0.16 A --> 4 points less B, 7 points more A --> more A
- Legal: 0.75 B, 0.04 A --> 12 points more B, 5 points less A --> more B, less A
- Prose/Lyrical: 0.04 B, 0.50 A; 59 points less B, 41 points more A --> less B, more A


**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| mean  |     1290.69 |
| std   |     3911.68 |
| min   |       79    |
| 25%   |      153    |
| 50%   |      300    |
| 75%   |      853    |
| max   |   123935    |

Length in specific genres (median):
- Promotion: 172
- Poetry/Lyrical: 169
- Instruction: 284
- Information/Explanation: 320
- News: 213
- Opinion/Argumentation: 498
- Legal: 606

Similar length to the general length (10 words difference):
Slightly shorter (10-100 words difference): Instruction, News
Much shorter (more than 100 words difference): Promotion, Poetry/Lyrical
Slightly longer (10-100 words difference): Information/Explanation
Much longer (more than 100 words difference): Opinion/Argumentation, Legal


## MaCoCu-mk-en

Initial no. of sentences: 478,059; no. of texts: 54,957

Pre-processing:
- discarded instances where English and Macedonian come from different domains (140,613 sentences, 14,429 texts)
- discarded duplicated English sentences (with the same par id - 21,607 sentences, 318 texts)
- discarded duplicated documents (100 texts) --> no. of remaining texts: 40,110

Initial length of texts:

|       |   en_length |
|:------|------------:|
| count |   40110     |
| mean  |     194.265 |
| std   |     426.053 |
| min   |       1     |
| 25%   |      36     |
| 50%   |      94     |
| 75%   |     210     |
| max   |   16139     |

- texts are in general longer than in other datasets, so we will not discard texts based on the median (we would lose useful texts which could change the distribution of genres). I discarded the texts with length less than 79 which is similar to the other two MaCoCu datasets (18,029 texts discarded). --> remaining no. of texts: 22,081
- non-textual texts filtered out based on a heuristic (26 texts) -> final no. of texts: 22,055

### Statistics for MaCoCu-mk-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| UNK |    0.44652   |
| A   |    0.310905  |
| B   |    0.188121  |
| MIX |    0.0544548 |


English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| A   |     0.492315 |
| MIX |     0.293448 |
| B   |     0.200952 |
| UNK |     0.013285 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| mk-orig |                0.587304 |
| en-orig |                0.412696 |

Average bicleaner score

|       |   average_score |
|:------|----------------:|
| count |   22055         |
| mean  |       0.918045  |
| std   |       0.0546798 |
| min   |       0.5185    |
| 25%   |       0.892667  |
| 50%   |       0.93      |
| 75%   |       0.957333  |
| max   |       0.9935    |

Length of English text

|       |   en_length |
|:------|------------:|
| count |   22055     |
| mean  |     323.598 |
| std   |     540.894 |
| min   |      79     |
| 25%   |     125     |
| 50%   |     194     |
| 75%   |     330     |
| max   |   16139     |

Statistics on English domains: there are 6,066 different domains.

There are 26 domains which cover more than 1% of data, the domain with the largest frequency is stat.gov.mk which covers 5.7% of the data.

|                                  |   Count |   Percentage |
|:---------------------------------|--------:|-------------:|
| stat.gov.mk (63% Information/Explanation, 36% News)                     |    1264 |   5.73113    |
| meta.mk   (96% News)                       |    1216 |   5.51349    |
| seeu.edu.mk    (78% News, 19% Information/Explanation)                  |     981 |   4.44797    |
| finance.gov.mk (96% News)                  |     668 |   3.02879    |
| ssm.org.mk   (87% News)                    |     598 |   2.7114     |
| sobranie.mk   (65% News, 13% Information/Explanation)                   |     586 |   2.65699    |
| loging.mk  (65% Promotion, 28% Information/Explanation)                      |     474 |   2.14917    |
| eprints.ugd.edu.mk  (97% Information/Explanation)             |     410 |   1.85899    |
| ckrm.org.mk (85% News)                     |     373 |   1.69123    |
| rkmetalurg.mk  (99% News)                  |     337 |   1.528      |
| customs.gov.mk    (85% News, 8% Legal)               |     315 |   1.42825    |
| mcms.mk   (80% Information/Explanation, 14% News)                       |     270 |   1.22421    |
| alkaloid.com.mk  (38% News, 37% Promotion)                |     263 |   1.19247    |
| atamacedonia.org.mk (81% News)             |     251 |   1.13806    |
| bujinkan.koryu.mk (44% Opinion/Argumentation, 35% News)               |     241 |   1.09272    |
| clp.mk    (87% News)                       |     226 |   1.02471    |

### Results of genre prediction on MaCoCu-mk-en

Distribution of labels:

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| News                    |    9695 |    43.9583   |
| Information/Explanation |    5794 |    26.2707   |
| Promotion               |    3336 |    15.1258   |
| Legal                   |     875 |     3.96735  |
| Opinion/Argumentation   |     861 |     3.90388  |
| Instruction             |     830 |     3.76332  |
| Other                   |     382 |     1.73203  |
| Prose/Lyrical           |     249 |     1.129    |
| Forum                   |      33 |     0.149626 |

Post-processing:
- discarded labels where the category is "Other" (382 labels, 1.7%) and "Forum" (33 labels, 0.2%)
- discarded labels where prediction confidence was below 0.9 (1532 labels, 7%).

Final no. of texts with predicted labels: 20,108.

**Final results**

Distribution of labels:

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| News                    |    9225 |     45.8773  |
| Information/Explanation |    5298 |     26.3477  |
| Promotion               |    3140 |     15.6157  |
| Legal                   |     775 |      3.85419 |
| Instruction             |     718 |      3.57072 |
| Opinion/Argumentation   |     713 |      3.54585 |
| Prose/Lyrical           |     239 |      1.18858 |

Compared to other two corpora, there is much more News (46%, versus Icelandic: 25%, Slovene: 13%, Maltese: 35%).

**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 1; most frequent domain: bujinkan.koryu.mk (12%)
- News: domains with more than 10%: 1; most frequent domain: meta.mk (12%)
- Legal: domains with more than 10%: 1; most frequent domain: ustavensud.mk (12%)
- Information/Explanation:  domains with more than 10%: 1; most frequent domain: stat.gov.mk (13%)
- Promotion:  domains with more than 10%: 1; most frequent domain: loging.mk (10%)
- Instruction: domains with more than 10%: 0; most frequent domain: samsung.com (7%)
- Prose/Lyrical: domains with more than 10%: 2; most frequent domain: biblegateway (68%), mpc.org.mk (11%)


**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| UNK |    0.45   |
| A   |    0.31  |
| B   |    0.19  |
| MIX |    0.05 |

- News: 0.29 A, 0.20 B - 2 points less A, 1 point more B --> similar distribution
- Opinion/Argumentation: 0.36 A, 0.25 B - 5 points more A, 6 points more B --> more A, more B
- Promotion: 0.35 A, 0.15 B - 4 points more A, 4 points less B --> similar distribution
- Instruction: 0.32 A, 0.16 B - 1 point more A, 3 points less B --> similar distribution
- Information/Explanation: 0.32 A, 0.17 B - 1 point more A, 2 points less B --> similar distribution
- Legal: 0.23 A, 0.25 B - 8 points less A, 6 points more B --> more B, less A
- Prose/Lyrical: 0.39 A, 0.22 B - 8 points more A, 3 points more B --> more A

**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| mean  |     323.598 |
| std   |     540.894 |
| min   |      79     |
| 25%   |     125     |
| 50%   |     194     |
| 75%   |     330     |
| max   |   16139     |

Length in terms of median:
- News: 201
- Opinion/Argumentation: 399
- Promotion: 155
- Instruction: 223
- Information/Explanation: 172
- Legal: 269
- Prose/Lyrical: 432

Similar length to the general length (10 words difference): News
Slightly shorter (10-100 words difference): Promotion, Information/Explanation
Much shorter (more than 100 words difference):
Slightly longer (10-100 words difference): Instruction, Legal
Much longer (more than 100 words difference): Opinion/Argumentation, Prose/Lyrical

## MaCoCu-tr-en

Initial no. of sentences: 10,323,996; no. of texts: 796,473

Pre-processing:
- discarded instances where English and Turkish come from different domains (4,619,933 sentences - 45% of all sentences!!, 330,753 texts - 42% of all texts)
- discarded duplicated English sentences (with the same par id - 2,732,066 sentences - 48% of all sentences!, 9,942 texts - 2 % of all texts)
- discarded duplicated documents (2133 texts) --> no. of remaining texts: 453,645

Initial length of texts:

|       |   en_length |
|:------|------------:|
| count |  453645     |
| mean  |     163.379 |
| std   |     311.403 |
| min   |       1     |
| 25%   |      33     |
| 50%   |      74     |
| 75%   |     175     |
| max   |   26552     |

- I discarded the texts with length less than 79 which is similar to the other MaCoCu datasets (235,091 texts - 52% discarded). --> remaining no. of texts: 218,554
- non-textual texts filtered out based on a heuristic (5,407 texts) -> final no. of texts: 213,147

### Statistics for MaCoCu-tr-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| UNK |   0.530268   |
| A   |   0.338189   |
| B   |   0.124989   |
| MIX |   0.00655416 |


English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| UNK |            1 |

?!?!

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| tr-orig |                0.669256 |
| en-orig |                0.330744 |

Average bicleaner score

|       |   average_score |
|:------|----------------:|
| count |  213147         |
| mean  |       0.867585  |
| std   |       0.0812931 |
| min   |       0.5       |
| 25%   |       0.817786  |
| 50%   |       0.879833  |
| 75%   |       0.9305    |
| max   |       0.9975    |

Length of English text

|       |   en_length |
|:------|------------:|
| count |  213147     |
| mean  |     303.056 |
| std   |     410.13  |
| min   |      79     |
| 25%   |     116     |
| 50%   |     184     |
| 75%   |     339     |
| max   |   26552     |

Statistics on English domains: there are 12,937 different domains.

There are 7 domains which cover more than 1% of data, the domain with the largest frequency is booking.com which covers 6.5% of the data.

|                                                    |   Count |   Percentage |
|:---------------------------------------------------|--------:|-------------:|
| booking.com  (92% Promotion)                                      |   13928 |   6.53446    |
| support.apple.com   (93% Instruction)                               |    6443 |   3.0228     |
| debis.deu.edu.tr (97% Information/Explanation)                                  |    3390 |   1.59045    |
| atilim.edu.tr  (78% Information/Explanation, 8% News)                                    |    2292 |   1.07531    |
| dergipark.org.tr  (63% Information/Explanation, 32% Legal)                                 |    2283 |   1.07109    |
| yandex.com.tr  (97% Information/Explanation)                                    |    2180 |   1.02277    |
| ninova.itu.edu.tr   (99% Information/Explanation)                               |    2166 |   1.0162     |

### Results of genre prediction on MaCoCu-tr-en

As this is by far the largest corpus, the prediction took much longer: almost 21 hours.

Distribution of labels before post-processing

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Promotion               |   77954 |    36.5729   |
| Information/Explanation |   56954 |    26.7205   |
| Instruction             |   34483 |    16.178    |
| News                    |   28021 |    13.1463   |
| Legal                   |    7054 |     3.30945  |
| Other                   |    3496 |     1.64018  |
| Opinion/Argumentation   |    3211 |     1.50647  |
| Forum                   |    1589 |     0.745495 |
| Prose/Lyrical           |     385 |     0.180627 |

Post-processing:
- discarded labels where the category is "Other" (3496 labels, 1.6%) and "Forum" (1589 labels, 0.75%)
- discarded labels where prediction confidence was below 0.9 (14,280 labels, 7%).

Total number of labels discarded due to post-processing: 19,365, percentage: 9%

Final no. of texts with predicted labels: 193,782.

**Final results**

Final genre distribution:

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Promotion               |   73624 |    37.9932   |
| Information/Explanation |   53808 |    27.7673   |
| Instruction             |   31239 |    16.1207   |
| News                    |   26105 |    13.4713   |
| Legal                   |    6157 |     3.17728  |
| Opinion/Argumentation   |    2540 |     1.31075  |
| Prose/Lyrical           |     309 |     0.159458 |


**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 0; most frequent domain: raillife.com.tr(7%)
- News: domains with more than 10%: 0; most frequent domain: bbc.com (6%)
- Legal: domains with more than 10%: 1; most frequent domain: dergipark.org.tr (11%)
- Information/Explanation:  domains with more than 10%: 0; most frequent domain: debis.deu.edu.tr (6%)
- Promotion:  domains with more than 10%: 1; most frequent domain: booking.com (13%)
- Instruction: domains with more than 10%: 1; most frequent domain: support.apple.com (19%)
- Prose/Lyrical: domains with more than 10%: 1; most frequent domain: imanilmihali.com (21%) (Islam page)


**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| UNK |   0.53   |
| A   |   0.34   |
| B   |   0.12   |
| MIX |   0.01 |

- News: 0.29 A, 0.15 B; 5 point less A, 3 points more B --> less A
- Opinion/Argumentation: 0.38 A, 0.09 B; 4 points more A, 3 points less B --> similar distribution
- Promotion: 0.38 A, 0.22 B; 4 points more A, 10 points more B --> more B
- Instruction: 0.25 A, 0.06 B; 9 points less A, 6 points less B --> less A, less B
- Information/Explanation: 0.30 A, 0.04 B; 4 points less A, 8 points less B --> less B
- Legal: 0.48 A, 0.09 B; 14 points more A, 3 points less B --> more A
- Prose/Lyrical: 0.43 A, 0.03 B; 9 points more A, 9 points less B --> more A, less B

**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| count |  213147     |
| mean  |     303.056 |
| std   |     410.13  |
| min   |      79     |
| 25%   |     116     |
| 50%   |     184     |
| 75%   |     339     |
| max   |   26552     |

Length in terms of median:
- News: 198
- Opinion/Argumentation: 199
- Promotion: 180
- Instruction: 244
- Information/Explanation: 149
- Legal: 310
- Prose/Lyrical: 205

Similar length to the general length (10 words difference): Promotion
Slightly shorter (10-100 words difference): Information/Explanation
Much shorter (more than 100 words difference):
Slightly longer (10-100 words difference): News, Opinion/Argumentation, Instruction, Prose/Lyrical
Much longer (more than 100 words difference): Legal

## MaCoCu-bg-en

Initial no. of sentences: 3,857,653; no. of texts: 287,456

Pre-processing:
- discarded instances where English and Bulgarian come from different domains (1,498,549 sentences - 39% of all sentences, 71,802 texts - 25% of all texts)
- discarded duplicated English sentences (with the same par id - 585,333 sentences - 25% of all sentences, 2,395 texts - 1% of all texts)
- discarded duplicated documents (1,058 texts) --> no. of remaining texts: 212,201

Initial length of texts:

|       |   en_length |
|:------|------------:|
| count |  212201     |
| mean  |     173.37  |
| std   |     414.393 |
| min   |       2     |
| 25%   |      38     |
| 50%   |      81     |
| 75%   |     174     |
| max   |   68422     |

- I discarded the texts with length less than 79 which is similar to the other MaCoCu datasets (102,579 texts - 48% discarded). --> remaining no. of texts: 109,622
- non-textual texts filtered out based on a heuristic (2,218 texts) -> final no. of texts: 107,404


### Statistics for MaCoCu-bg-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| UNK |    0.427666  |
| A   |    0.32874   |
| B   |    0.178755  |
| MIX |    0.0648393 |


English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| A   |   0.402918   |
| B   |   0.304793   |
| MIX |   0.282885   |
| UNK |   0.00940375 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| bg-orig |                0.538602 |
| en-orig |                0.461398 |

Average bicleaner score

|       |   average_score |
|:------|----------------:|
| count |  107404         |
| mean  |       0.890131  |
| std   |       0.0727416 |
| min   |       0.5025    |
| 25%   |       0.847292  |
| 50%   |       0.91      |
| 75%   |       0.9463    |
| max   |       0.99225   |

Length of English text

|       |   en_length |
|:------|------------:|
| count |  107404     |
| mean  |     301.515 |
| std   |     552.041 |
| min   |      79     |
| 25%   |     107     |
| 50%   |     170     |
| 75%   |     318     |
| max   |   68422     |

Statistics on English domains: there are 5,362 different domains.

There are 7 domains which cover more than 1% of data, the domain with the largest frequency is goldenpages.bg which covers 12% of the data.

|                        |   Count |   Percentage |
|:-----------------------|--------:|-------------:|
| goldenpages.bg (87% Opinion/Argumentation)         |   13020 |    12.1225   |
| rooms.bg (92% Promotion)              |    3951 |     3.67863  |
| drehi.bg  (92% Promotion)             |    3465 |     3.22614  |
| mirela.bg (97% Information/Explanation)             |    2279 |     2.12189  |
| vikiwat.com (50% Information/Explanation, 47% Promotion)           |    1596 |     1.48598  |
| campingrocks.bg (98% Promotion)       |    1108 |     1.03162  |
| bivol.bg  (82% News)             |    1088 |     1.013    |


### Results of genre prediction on MaCoCu-bg-en

Distribution of labels before post-processing

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Promotion               |   36397 |    33.8879   |
| Information/Explanation |   22651 |    21.0895   |
| News                    |   18278 |    17.018    |
| Other                   |    9860 |     9.18029  |
| Instruction             |    7697 |     7.1664   |
| Opinion/Argumentation   |    7648 |     7.12078  |
| Legal                   |    3113 |     2.8984   |
| Forum                   |    1186 |     1.10424  |
| Prose/Lyrical           |     574 |     0.534431 |


Post-processing:
- discarded labels where the category is "Other" (9860 labels, 9%) and "Forum" (1186 labels, 1%)
- discarded labels where prediction confidence was below 0.9 (7814 labels, 8%).

Total number of labels discarded due to post-processing: 18,860, percentage: 18%

Final no. of texts with predicted labels: 88,544.

**Final results**

Final genre distribution:

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Promotion               |   34829 |    39.3352   |
| Information/Explanation |   21120 |    23.8525   |
| News                    |   16993 |    19.1916   |
| Instruction             |    6786 |     7.66399  |
| Opinion/Argumentation   |    5702 |     6.43974  |
| Legal                   |    2718 |     3.06966  |
| Prose/Lyrical           |     396 |     0.447235 |


**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 1; most frequent domain: goldenpages.bg (41% !!)
- News: domains with more than 10%: 0; most frequent domain: archive.eufunds.bg (5%)
- Legal: domains with more than 10%: 0; most frequent domain: mi.government.bg (3%)
- Information/Explanation:  domains with more than 10%: 1; most frequent domain: mirela.bg (10%)
- Promotion:  domains with more than 10%: 1; most frequent domain: rooms.bg (10%)
- Instruction: domains with more than 10%: 0; most frequent domain: angelcosmetics.bg (4%)
- Prose/Lyrical: domains with more than 10%: 2; most frequent domain: wordplanet.org (22%), jw.org (20%) (together 42% of all Prose/Lyrical!)


**Distribution of English varieties in genres (doc level)**

Distribution in entire corpus (document level):

|     |   en_var_doc |
|:----|-------------:|
| UNK |    0.43  |
| A   |    0.33   |
| B   |    0.18  |
| MIX |    0.06 |


- News: 0.28 A, 0.23 B -> 5 points less A, 5 points more B --> more B, less A
- Opinion/Argumentation: 0.26 A, 0.13 B -> 7 points less A, 5 points less B --> less A, less B
- Promotion: 0.43 A, 0.16 B; 10 points more A, 2 points less B --> more A
- Instruction: 0.37 A, 0.17 B: 4 points more A, 1 point less B -> similar distribution
- Information/Explanation: 0.36 A, 0.21 B; 3 points more A, 3 points more B -> similar distribution
- Legal: 0.25 A, 0.30 B; 8 points less A, 12 points more B -> more B, less A
- Prose/Lyrical: 0.31 A, 0.30 B; 2 points less A, 12 points more B --> more B

**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| mean  |     301.515 |
| std   |     552.041 |
| min   |      79     |
| 25%   |     107     |
| 50%   |     170     |
| 75%   |     318     |
| max   |   68422     |

Length in terms of median:
- News: 196
- Opinion/Argumentation: 126
- Promotion: 166
- Instruction: 306
- Information/Explanation: 188
- Legal: 404
- Prose/Lyrical: 311

Similar length to the general length (10 words difference): Promotion
Slightly shorter (10-100 words difference): Opinion/Argumentation 
Much shorter (more than 100 words difference):
Slightly longer (10-100 words difference): News, Information/Explanation
Much longer (more than 100 words difference): Instruction, Legal, Prose/Lyrical

## MaCoCu-hr-en

Initial no. of sentences: 3,097,282; no. of texts: 324,666


Pre-processing:
- discarded instances where English and Croatian come from different domains (973,709 sentences - 30% of all sentences, 85,608 texts - 26% of all texts)
- discarded duplicated English sentences (with the same par id - 382,621 sentences - 18% of all sentences, 4,368 texts - 2% of all texts)
- discarded duplicated documents (1,742 texts, 1%) --> no. of remaining texts: 232,948

Initial length of texts:

|       |   en_length |
|:------|------------:|
| count |  232948     |
| mean  |     171.623 |
| std   |     796.894 |
| min   |       1     |
| 25%   |      26     |
| 50%   |      65     |
| 75%   |     153     |
| max   |   77040     |

- I discarded the texts with length less than 79 which is similar to the other MaCoCu datasets (129,899 texts - 56% discarded). --> remaining no. of texts: 103,049
- non-textual texts filtered out based on a heuristic (1297 texts, 1%) -> final no. of texts: 101,752


### Statistics for MaCoCu-hr-en after pre-processing

English variant (document level)

|     |   en_var_doc |
|:----|-------------:|
| B   |    0.337369  |
| UNK |    0.329989  |
| A   |    0.263769  |
| MIX |    0.0688733 |


English variant (domain level)

|     |   en_var_dom |
|:----|-------------:|
| B   |   0.397378   |
| MIX |   0.317212   |
| A   |   0.278363   |
| UNK |   0.00704654 |

Translation direction

|         |   translation_direction |
|:--------|------------------------:|
| hr-orig |                 0.90354 |
| en-orig |                 0.09646 |

Average bicleaner score

|       |   average_score |
|:------|----------------:|
| count |  101752         |
| mean  |       0.900225  |
| std   |       0.0638587 |
| min   |       0.501     |
| 25%   |       0.869327  |
| 50%   |       0.915375  |
| 75%   |       0.947167  |
| max   |       0.9916    |

Length of English text

|       |   en_length |
|:------|------------:|
| count |  101752     |
| mean  |     347.735 |
| std   |    1182.31  |
| min   |      79     |
| 25%   |     114     |
| 50%   |     172     |
| 75%   |     298     |
| max   |   77040     |

Statistics on English domains: there are 6,258 different domains.

There are 9 domains which cover more than 1% of data, the domain with the largest frequency is support.apple.com which covers 2% of the data.

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| support.apple.com (92% Instruction)      |    2522 |     2.47858  |
| mzos.hr (99% Information/Explanation)                |    2414 |     2.37243  |
| europarl.europa.eu (43% News, 34% Legal)     |    2352 |     2.3115   |
| eur-lex.europa.eu (86% Legal)      |    1977 |     1.94296  |
| adriatic.hr (79% Promotion)            |    1950 |     1.91642  |
| prijatelji-zivotinja.hr (71% News) |    1945 |     1.91151  |
| hrcak.srce.hr (98% Information/Explanation)          |    1512 |     1.48597  |
| bib.irb.hr (99% Information/Explanation)             |    1434 |     1.40931  |
| zagrebdox.net (37% Information/Explanation, 28% News)          |    1150 |     1.1302   |

### Results of genre prediction on MaCoCu-hr-en

Distribution of labels before post-processing

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Information/Explanation |   30758 |    30.2284   |
| Promotion               |   28524 |    28.0329   |
| News                    |   17003 |    16.7102   |
| Instruction             |   12152 |    11.9428   |
| Legal                   |    5290 |     5.19892  |
| Opinion/Argumentation   |    4520 |     4.44217  |
| Other                   |    1956 |     1.92232  |
| Forum                   |     883 |     0.867796 |
| Prose/Lyrical           |     666 |     0.654533 |


Post-processing:
- discarded labels where the category is "Other" (1956 labels, 2%) and "Forum" (883 labels, 1%)
- discarded labels where prediction confidence was below 0.9 (7294 labels, 7%).

Total number of labels discarded due to post-processing: 10,133 percentage: 10%

Final no. of texts with predicted labels: 91,619.

**Final results**

Final genre distribution:

|                         |   Count |   Percentage |
|:------------------------|--------:|-------------:|
| Information/Explanation |   28958 |     31.607   |
| Promotion               |   26790 |     29.2407  |
| News                    |   15653 |     17.0849  |
| Instruction             |   11102 |     12.1176  |
| Legal                   |    4851 |      5.29475 |
| Opinion/Argumentation   |    3696 |      4.0341  |
| Prose/Lyrical           |     569 |      0.62105 |


**Distribution of domains in genres**

- Opinion/Argumentation: domains with more than 10%: 0; most frequent domain: vanipedia.org (6% !!)
- News: domains with more than 10%: 0; most frequent domain: prijatelji-zivotinja.hr (8%)
- Legal: domains with more than 10%: 2; most frequent domain: eur-lex.europa.eu (33%), europarl.europa.eu (14%)
- Information/Explanation:  domains with more than 10%: 0; most frequent domain: mzos.hr (8%)
- Promotion:  domains with more than 10%: 0; most frequent domain: adriatic.hr (4%)
- Instruction: domains with more than 10%: 1; most frequent domain: support.apple.com (21%)
- Prose/Lyrical: domains with more than 10%: 4; most frequent domain: pouke.org (30%), biblegateway.com (15%), vanipedia.org (14%),  storyboardthat.com (13%) (together 72% of all Prose/Lyrical!)

**Length of texts per genre**

Length in entire corpus:

|       |   en_length |
|:------|------------:|
| count |  101752     |
| mean  |     347.735 |
| std   |    1182.31  |
| min   |      79     |
| 25%   |     114     |
| 50%   |     172     |
| 75%   |     298     |
| max   |   77040     |

Length in terms of median:
- News: 193
- Opinion/Argumentation: 205
- Promotion: 149
- Instruction: 199
- Information/Explanation: 158
- Legal: 400
- Prose/Lyrical: 196

Similar length to the general length (10 words difference): 
Slightly shorter (10-100 words difference): Promotion, Information/Explanation
Much shorter (more than 100 words difference):
Slightly longer (10-100 words difference): News, Opinion/Argumentation, Instruction, Prose/Lyrical
Much longer (more than 100 words difference): Legal