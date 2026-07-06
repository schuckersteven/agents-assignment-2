# Assignment 2 Reflection

**Name:** [Steven Schucker]
**Option:** [A - Calendar]
**Date:** [Jul 5 2026]

---

## Tool Design Decisions

### Tools Implemented
1. **[list-upcoming_events]**: [List upcoming calendar events.]
2. **[find_available_slots]**: [Find open calendar slots for a meeting within the next N days.]
3. **[create_event]**: [Create a calendar event with the provided details.]
4. **[check_conflicts]**: [Check whether a proposed time range conflicts with existing calendar events.]

### Why These Tools?
[Explain why you chose to implement these specific tools. What user needs do they address?
These tools solve the four core problems people face when trying to manage time: visibility, creation, safety, and coordination.]

### Description Strategy
[How did you write your tool descriptions to help the LLM select the right tool? What keywords or patterns did you use?
1. The descriptions were written so that each tool advertises the exact situations where it should be    
   used.
2. The keyword patterns are baked into each tool.
3. The descriptions were written so the LLM can classify user intent into one of four buckets:
   awareness, creation, safety, and coordination]

---

## Challenges Encountered

### Challenge 1: [MCP Test Failed]
- **Problem:** [Node not detected]
- **Solution:** [Downloaded and installed node.js]

### Challenge 2: [GITHUB Personnel Access Token]
- **Problem:** [No write issues scope]
- **Solution:** [Selected write:discussion]

---

## Error Handling Approach

[Describe your approach to error handling. What types of errors did you anticipate? How do you communicate errors to users?
The approach to erro handling is to detect errors and ensure the LLM could understand them, classify them, and respond in a way that feels natural to the user. The tool descriptions were written with three principles:
    1. Anticipate the most common failure modes.
    2. Make each error type easy for the LLM to identify.
    3. Provide a consistent, conversational way to explain what went wrong.]

---

## Ideas for Improvement

If you had more time, what would you add or change?

1. [Strengthen error‑handling]
2. [Add richer guidance for multi‑step scheduling]
3. [Improve cross‑tool reasoning]

---

## Key Learnings

What did you learn from this assignment about building AI agents?

[I learned that the quality of the tool descriptions directly determines the quality of the agent’s behavior. A bad tool description leads to poor tool use. I learned that designing strong intent signals such as verbs, patterns, and examples are more important than designing the tool itself. I learned that agents need explicit guidance on how tools relate to each other. Agents will misorder steps or skip safety checks. I learned that an agent takes on a personality with the workflow. I learned that the agent constraints make the agent smarter. ]
