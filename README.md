# 🌳 Daily Reflection Tree Agent

A CLI-based interactive agent that guides users through a **decision tree** across three axes:

* **Axis 1 — Self (current state)**
* **Axis 2 — Action (execution choices)**
* **Axis 3 — Outcome (results & direction)**

The system dynamically adapts based on user inputs and generates a **personalized reflection summary**.

---

# 📁 Repository Structure

```bash
.
├── agent/
│   └── runnable code.py        # Main CLI agent (run this)
│
├── tree/
│   ├── reflection_tree.json    # Tree definition (nodes + logic)
│   └── tree-diagram.png        # Visual representation of the tree
│
├── transcripts/
│   ├── persona-1-transcript.md # Weak / self-centric path
│   └── persona-2-transcript.md # Strong / action-oriented path
│
├── README.md
└── write-up.md                 # Explanation of design decisions
```

---

# ▶️ How to Run the Agent

## 1. Requirements

* Python 3.8+

## 2. Run

```bash
python "agent/runnable code.py"
```

> ⚠️ Important: Keep the folder structure unchanged.
> The script expects `tree/reflection_tree.json` relative to the repo root.

---

# 🧠 How to Read the Tree

The tree is defined in:

```bash
tree/reflection_tree.json
```

Each node contains:

| Field      | Meaning                               |
| ---------- | ------------------------------------- |
| `id`       | Unique node identifier                |
| `parentId` | Defines tree structure                |
| `type`     | Node type (question, decision, etc.)  |
| `text`     | Message shown to user                 |
| `options`  | Choices (for questions)               |
| `target`   | Routing logic (for decisions/bridges) |
| `signal`   | Stores values used in summary         |

---

## 🔁 Node Types

### 1. Question

* Prompts user input
* Stores answer
* Moves forward

---

### 2. Decision

Routes based on previous answer:

```
answer=Option:A_NODE
```

---

### 3. Reflection

* Provides insight
* Auto-advances

---

### 4. Bridge

* Moves between axes
* Example: Self → Action

---

### 5. Summary

Generates final output using placeholders:

```
{A1_OPEN.answer}
{axis2:strategy}
```

---

# 🔀 How Branching Works

The tree adapts based on decisions.

## Example Differences

### ✅ Strong Path (Persona 1)

* Breaks problems down
* Tracks progress
* Focuses on real output (deployment / users)

→ Output:

> "Consistent execution compounds into measurable success."

---

### ❌ Weak Path (Persona 2)

* Avoids difficult problems
* No tracking
* Only local validation

→ Output:

> "Without discipline, even clear goals will fail."

---

# 📜 Transcripts

See full runs:

* `transcripts/persona-1-transcript.md` → **Strong / action-oriented path**
* `transcripts/persona-2-transcript.md` → **Weak / self-centric path**

These demonstrate how **different choices lead to different outcomes**.

---

# 🖼 Tree Diagram

Visual structure:

```bash
tree/tree-diagram.png
```

---

# ⚙️ How the Agent Works

1. Starts at `START`
2. Traverses nodes using:

   * user input (questions)
   * rules (decisions)
3. Stores:

   * answers
   * signals
4. Replaces placeholders dynamically
5. Outputs summary

---

# ⚠️ Design Notes

* Handles:

  * Missing nodes
  * Inconsistent JSON structure
  * Infinite loop protection
* Decision logic reads from:

  * `options`
  * `target`

---

# 🚀 Improvements (Optional)

* Web UI (Flask / React)
* Tree validator
* Path analytics
* Visualization of traversal

---

# ✅ Summary

This project demonstrates:

* Tree-based decision systems
* Stateful traversal
* Dynamic summary generation
* CLI interaction

The agent is fully runnable and shows how **user choices influence outcomes**.

---
