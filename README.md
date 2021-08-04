# bot-detector
We propose to develop and maintain an open-source bot detector for BitClout, initially based on heuristics and later on Machine Learning models based on data crowdsourced and contributed by the community. The purpose of this model is to help flag existing bots in the network to both prevent spam and other malicious activity performed by these bots and to facilitate in-depth analysis of social network structure and interactions based on the activity of real people.

**Stage 1 - Preliminary**

- Gather a set of basic heuristics which can be used to automatically detect the most flagrant bots - for example, excessive activity (such as a post every minute), excessive repetition (such as spam), any malicious activity (such as phishing or virus distribution), etc. These should help us identify a small set of obvious bots but will be unlikely to incorrectly flag humans as bots, meaning that the heuristics-based approach will likely have high precision but low recall.
- During this stage, we will attempt to independently verify the bot status of all bots detected by the system by actual humans, to ensure that the system does not lead to false positives (real humans being flagged as bots).
- In addition, we will build a comminity-driven platform to tag and label accounts as bots. This consus-based tagging and voting system will help us agree on what is a bot and help build a long-term golden dataset for future models and for Nodes to use at their discretion.  

**Stage 2 - Action**

- If we have verified to the community's satisfaction that the heuristics work, they can then be applied in order to automatically ban existing bots (with something like an appeals system in place to protect real humans from being falsely banned). Otherwise, we will wait for the next step to complete first before relying on the system to ban bots automatically.
- Once we believe sufficient data has been collected, the community can use this dataset to build a Machine Learning (ML) system that can automatically detect bots with a greater recall but similar precision, that is, catch more bots without a significantly increased number of false positives. This will happen in tandem with the ongoing data collection effort, and all data will be public so that the community can inspect it and build and contribute bot detection systems using the crowdsourced data.

***Progress***

The build_dataset.py script can be used to generate data based on a user's posts using a simple heuristic to determine whether a given user is a bot based on how often they copy other's posts. The bots_detector source code folder contains an example of how to write and run models, and evaluate them against existing data.