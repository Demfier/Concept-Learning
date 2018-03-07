# Concept-Learning
> A module for FCA and Query-Learning

Contains the implementation of algorithms mentioned in
  * [Queries and Concept Learning](https://link.springer.com/content/pdf/10.1023/A:1022821128753.pdf) (1988): Dana Angluin
  * [On the Usability of Probably Approximately Correct Implication Bases](https://arxiv.org/pdf/1701.00877.pdf) (2017): Daniel Borchmann, Tom Hanika and Sergei Obiedkov
  * [Optimizations in computing the Duquenne–Guigues
basis of implications](https://link.springer.com/content/pdf/10.1007%2Fs10472-013-9353-y.pdf) (2014): Konstantin Bazhanov, Sergei Obiedkov


ToDo list:
- [x] FCA Part
- [x] PAC Learning
  - [x] Implement the dataset sampler
  - [x] Complete the approx-equivalent function
  - [x] Implement HORN1
- [ ] Regex Learning
  - [ ] Without POS
  - [ ] Incorporate POS information for potential regex conflicts for different
        clusters
- [ ] Evaluation
  - [x] Simple overlapping words evaluation
  - [ ] Original task metric (would require to implement regex)
- [x] Make automated pipeline for the entire dataset and get cumulative results
- [ ] Modulify the code
  - [ ] Change directory structure
  - [ ] Add tests
  - [ ] Add usage documentation
