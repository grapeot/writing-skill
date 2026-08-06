# Analytical Perspectives for External Articles (Thesis Catalog)

## Metadata

- **Type**: Reference
- **Use cases**: Thesis discovery and brainstorming for external articles.
- **Created**: 2026-07-06

---

## Thesis Catalog: L1-L8 Analytical Perspectives

These perspectives distill recurring analytical habits from the author's published work. Use them as an inspiration library. Never expose L numbers or perspective labels in a reader-visible final article.

### L1: Feedback-Loop Judgment
A system's capability ceiling depends on whether it can perceive its own output and correct itself. The key question is whether the model can see the consequences of its behavior and iterate, as in image-generation systems using screenshot feedback or agents observing code execution. Open-loop control drifts; closed-loop control supports reliability.
*(Related axioms: A02 Amplifier, A04 Reliability, M01 Closed-loop calibration)*

### L2: Reconstructing Cost-Structure Economics
When the cost of a resource changes by orders of magnitude, compare the old and new economics systematically. Explain why older optimal strategies such as DRY, intuition-based decisions, or defensive code were rational under the old cost structure, and why disposable code, spending tokens for certainty, or accumulating context infrastructure may become optimal under the new one.
*(Related axioms: X03 Bottlenecks determine efficiency, T05 Cognition is an asset/code is consumable)*

### L3: The Consensus Ceiling
An LLM's default output is consensus. Safety alignment and probabilistic generation pull it toward the mean. Differentiation and depth require non-consensus personal context and wide research rather than endlessly upgrading the model.
*(Related axioms: A10 Familiarity over raw intelligence, Context infrastructure thesis)*

### L4: Tracing Technology Lineage
No technology release appears from nowhere. Trace two to four generations, identifying the problem each generation solved and the limitation it left behind. Locate the current event on that line, distinguish a genuinely new development from productization of an existing path, and infer the likely next generation.
*(Related axioms: M06 Connections over isolated knowledge, A13 Three stages of technology adoption)*

### L5: Surface Diagnosis and Underlying Mechanism
Media and vendor narratives such as "AI can do design" or "AI became lazy" often hide the technical mechanism and constraints that drive the result. Redirect attention from the surface description to the underlying logic rather than stopping at anthropomorphic interpretation.
*(Related axioms: T04 Data over opinion, V02 Verifiability)*

### L6: Value Redistribution After Execution Friction Falls
When tools remove execution friction, advantage shifts from executing faster to judging better. Tool mastery loses value while taste and direction gain it. Human roles move from IC to Manager, User to Builder, and executor to the person who defines the problem and evaluates the result.
*(Related axioms: T05 Cognition is an asset, A02 Amplifier)*

### L7: Translating Management Frameworks
AI unreliability, hallucination, avoidance, and communication cost have counterparts in human organizations, such as managing a new hire. Instead of inventing mystical concepts, apply mature management practices including hiring, delegation, situational leadership, acceptance checks, and hierarchical scaling to constrain and orchestrate AI.
*(Related axioms: A03 IC to Manager, A04 Reliability is a management problem)*

### L8: Context and Information Architecture
An LLM system's failure modes and capability limits begin with the information architecture inside its context window: what it can see, whether the information is clean, and whether roles are isolated. Design or diagnosis starts by clarifying that information foundation, then evaluating the feedback mechanism that acts on it.
*(Related axioms: M01 Closed-loop calibration, Context infrastructure thesis)*
