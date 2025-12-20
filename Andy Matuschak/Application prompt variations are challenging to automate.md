---
URLs:
  - https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ&stackedNotes=zX95uZHiGWNiNTDF3wETWtq&stackedNotes=zAt1K9ARQYguinoHH8cfaqQ&stackedNotes=Cloze_deletion_prompts_seem_to_produce_less_understanding_than_question%2Fanswer_pairs_in_spaced_repetition_memory_systems&stackedNotes=zSiuztCZ594AZuCweRghcXT&stackedNotes=zJoWJEpRvrjnm2zL3gdxBjg&stackedNotes=zSisETSpZBCgZH4rFNHRcnC&stackedNotes=z3NDe3nR9hvqRqWWtvZdxe7
---
# Application prompt variations are challenging to automate
[[The mnemonic medium can help readers apply what they’ve learned through simple application prompts]], but [[Application prompts are much harder to write than recall prompts]]. It’s tempting to try automatically generating these variations, but in practice that seemed challenging in 2020.

For instance, Michael notes:

> Compute the output when you apply the Hadamard gate to ..." versus "Compute the value of H(...)". This kind of thing is an incredibly valuable variation, and hard to do programmatically.

As another data point, Khan Academy spent enormous engineering resources building automatically-generated math exercises so that they could claim an unlimited number. In practice, though, human authors did a vastly better job, and it turned out that enormous numbers of variations simply weren’t necessary.

It probably _will_ be valuable to notice the techniques we use as we generate application prompt variations, and to turn those into a kind of “playbook” for generating future variations; see e.g. [[A pattern language of prompt-writing]]. And maybe 2023-era [[Large language models]] can help: [[GPT-3 can generate shallow variations of spaced repetition prompt questions]].

---
# References
1. [Andy Link](https://notes.andymatuschak.org/%C2%A7Note-writing_systems?stackedNotes=zTnTob5JrFYF9NpU73Zg5a1&stackedNotes=z4aipv9wyMg4qZGANaVjkrJ&stackedNotes=zX95uZHiGWNiNTDF3wETWtq&stackedNotes=zAt1K9ARQYguinoHH8cfaqQ&stackedNotes=Cloze_deletion_prompts_seem_to_produce_less_understanding_than_question%2Fanswer_pairs_in_spaced_repetition_memory_systems&stackedNotes=zSiuztCZ594AZuCweRghcXT&stackedNotes=zJoWJEpRvrjnm2zL3gdxBjg&stackedNotes=zSisETSpZBCgZH4rFNHRcnC&stackedNotes=z3NDe3nR9hvqRqWWtvZdxe7)
Conversation with Michael Nielsen, 2020-01-20