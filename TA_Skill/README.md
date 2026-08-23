# PDC Course TA — AI Skill

An AI teaching assistant for **Process Dynamics and Control** ([apmonitor.com/pdc](https://apmonitor.com/pdc)). Install it in your AI tool of choice and it becomes a course-aware TA: it knows the schedule, every assignment and TCLab activity, the [simulation and control apps](https://apmonitor.com/apps), the course's standard notation (FOPDT, IMC tuning, PID forms, the TCLab energy balance), and — most importantly — the course AI policy. It tutors, quizzes, and debugs *with* you; it does not do your graded work *for* you.

The same TA is packaged for **Claude**, **ChatGPT / Codex**, and **Google Gemini**. Pick your tool below.

## Files in this directory

| File | For | Purpose |
|---|---|---|
| [`pdc-course-ta.skill`](pdc-course-ta.skill) | Claude | Installable skill package (zip of `SKILL.md` + reference files). |
| [`pdc-course-ta-SKILL.md`](pdc-course-ta-SKILL.md) | Claude (readable) | The Claude skill's main instruction file, viewable on GitHub. |
| [`pdc-course-ta-instructions.md`](pdc-course-ta-instructions.md) | ChatGPT Custom GPT / Project, Gemini Gem | Condensed TA instructions (under the 8,000-character GPT instruction limit) to paste into the instructions box. |
| [`pdc-course-ta-knowledge.md`](pdc-course-ta-knowledge.md) | ChatGPT, Gemini, any tool | Combined knowledge file: full course map + course notes. Upload as a knowledge/reference file, or paste as context. |
| [`AGENTS.md`](AGENTS.md) | OpenAI Codex (and other agents that read AGENTS.md) | Drop-in agent instructions for working in a course folder or repo clone. |
| [`GEMINI.md`](GEMINI.md) | Gemini CLI | Identical agent instructions under the filename Gemini CLI reads. |
| [`pdc-course-ta-review.html`](pdc-course-ta-review.html) | Anyone curious | Side-by-side test results, with vs. without the skill, on three student scenarios. |

## Install — Claude

1. Download [`pdc-course-ta.skill`](https://github.com/APMonitor/pdc/raw/master/TA_Skill/pdc-course-ta.skill).
2. In Claude, open **Settings → Capabilities → Skills** and upload the file (or attach the `.skill` file to a chat — if your account allows skill creation, the file card shows a **Save skill** button).
3. Ask a course question in a new conversation; the skill triggers automatically, or invoke it with `/pdc-course-ta`.

**Claude Code (terminal):**

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills
curl -LO https://github.com/APMonitor/pdc/raw/master/TA_Skill/pdc-course-ta.skill
unzip pdc-course-ta.skill && rm pdc-course-ta.skill
```

## Install — ChatGPT

**Custom GPT** (needs a plan that includes GPT creation):

1. Go to **Explore GPTs → Create** (or chatgpt.com/gpts/editor) and open the **Configure** tab.
2. Name it *PDC Course TA*. Paste everything below the horizontal rule of [`pdc-course-ta-instructions.md`](pdc-course-ta-instructions.md) into **Instructions**.
3. Under **Knowledge**, upload [`pdc-course-ta-knowledge.md`](pdc-course-ta-knowledge.md).
4. Save (keep it private, or share the link with classmates per your instructor's guidance).

**ChatGPT Projects** (alternative, no GPT creation needed): create a Project, paste the same instructions into the project's custom instructions, and add the knowledge file to the project files.

**Codex** (the agentic coding tool / CLI): copy [`AGENTS.md`](AGENTS.md) and [`pdc-course-ta-knowledge.md`](pdc-course-ta-knowledge.md) into the folder where you run Codex — e.g., your course work folder or a clone of this repository (both files are at the repo's `TA_Skill/`; Codex picks up `AGENTS.md` automatically from the working directory tree).

## Install — Google Gemini

**Gemini Gem:**

1. In Gemini, open **Gems → New Gem** (gem manager).
2. Name it *PDC Course TA*. Paste everything below the horizontal rule of [`pdc-course-ta-instructions.md`](pdc-course-ta-instructions.md) into the Gem's instructions.
3. Add [`pdc-course-ta-knowledge.md`](pdc-course-ta-knowledge.md) as a knowledge file (if your Gemini version doesn't support knowledge uploads, paste its contents at the end of the instructions or into your first message).
4. Save and start chatting.

**Gemini CLI:** copy [`GEMINI.md`](GEMINI.md) and [`pdc-course-ta-knowledge.md`](pdc-course-ta-knowledge.md) into the folder where you run the CLI; it reads `GEMINI.md` automatically.

**No special features available?** Every tool falls back to the same trick: paste `pdc-course-ta-instructions.md` (below its horizontal rule) plus `pdc-course-ta-knowledge.md` as the first message of a conversation.

## Use

Talk to it like a TA at office hours. Examples of things it does well:

- **Concept help** — *"Why does integral action remove offset but cause windup when the heater saturates?"*
- **Homework coaching** — *"I got Kp = 8.5 °C/% and θp = 140 s from my TCLab step test and my PI controller is sluggish — what am I doing wrong?"* (It will sanity-check your fit and coach you to re-read the plot rather than just handing you numbers.)
- **Quiz me** — *"Quiz me on second-order systems, one question at a time, and keep score."* Every assignment's Generative AI Learning section has ready-made prompts like this.
- **TCLab and code debugging** — paste your Python error or controller code; it knows the `tclab` package, the digital twin (`tclab.setup(connected=False)`), and the velocity-form PID used in the course apps.
- **Report coaching** — bring your plots and numbers and it will critique your "What to Turn In" report against the assignment's questions.
- **Project + EE support (classes 26–41)** — circuits, sensors, actuator drive circuits, power budgets, SCADA architecture, and the electrical safety review for your microcontroller project.
- **Going deeper** — ask about Bode plots, state space, Smith predictors, or MPC; it will teach beyond the course and point you to follow-on resources like [Dynamic Optimization](https://apmonitor.com/do).

## What it will not do

The TA enforces the course AI policy in every tool, so expect it to redirect you if you ask it to:

- solve your specific graded assignment problem outright or write your report's results for you;
- answer quiz or exam questions being taken for a grade;
- invent data, plots, or "observations" for a lab you didn't run (it will point you to the TCLab digital twin or the browser apps instead — real data in minutes).

You are the engineer of record for everything you submit. Use the TA to learn faster, verify your work, and push further — then own the result.

## For instructors

All packages share the same three pieces of content: the TA instructions (policy + tutoring behavior), the course map, and the course notes. To adapt for your own course, edit those and re-export:

- **Claude**: the `.skill` file is a zip — extract, edit `SKILL.md` and `references/*.md`, re-zip, rename to `.skill`.
- **ChatGPT / Gemini**: edit `pdc-course-ta-instructions.md` (keep it under ~8,000 characters for GPT instruction boxes) and `pdc-course-ta-knowledge.md`, then re-paste/re-upload.
- **Codex / Gemini CLI**: edit `AGENTS.md` / `GEMINI.md` (they are identical) and the knowledge file.

`pdc-course-ta-review.html` shows the kind of behavioral testing used to check that the TA coaches instead of solving — worth re-running if you change the policy sections.
