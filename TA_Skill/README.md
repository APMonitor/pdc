# PDC Course TA — AI Skill

An AI teaching assistant for **Process Dynamics and Control** ([apmonitor.com/pdc](https://apmonitor.com/pdc)). Install it in Claude and it turns the AI into a course-aware TA: it knows the schedule, every assignment and TCLab activity, the [simulation and control apps](https://apmonitor.com/apps), the course's standard notation (FOPDT, IMC tuning, PID forms, the TCLab energy balance), and — most importantly — the course AI policy. It tutors, quizzes, and debugs *with* you; it does not do your graded work *for* you.

## Files in this directory

| File | Purpose |
|---|---|
| [`pdc-course-ta.skill`](pdc-course-ta.skill) | The installable skill package (a zip archive containing `SKILL.md` plus two reference files: the course map and the course notes). **This is the file to install.** |
| [`pdc-course-ta-SKILL.md`](pdc-course-ta-SKILL.md) | The skill's main instruction file, readable here on GitHub so you can see exactly what the TA is told to do. |
| [`pdc-course-ta-review.html`](pdc-course-ta-review.html) | Side-by-side test results comparing responses with and without the skill on three student scenarios (download and open in a browser). |

## Install

**Claude (web or desktop app)** — recommended for most students:

1. Download [`pdc-course-ta.skill`](https://github.com/APMonitor/pdc/raw/master/TA_Skill/pdc-course-ta.skill).
2. In Claude, open **Settings → Capabilities → Skills** and upload the file. (Alternatively, attach the `.skill` file to a chat — if your account allows skill creation, the file card shows a **Save skill** button.)
3. Start a new conversation and ask a course question. The skill activates automatically when the topic matches; you can also invoke it by name with `/pdc-course-ta`.

If the Skills option is not available on your account, you don't have to miss out: the `.skill` file is a zip archive. Rename it to `.zip`, extract it, and paste the contents of `SKILL.md` (plus the two files in `references/`) at the start of a conversation as context.

**Claude Code (terminal)**:

```bash
# from your home directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
curl -LO https://github.com/APMonitor/pdc/raw/master/TA_Skill/pdc-course-ta.skill
unzip pdc-course-ta.skill && rm pdc-course-ta.skill
```

This creates `~/.claude/skills/pdc-course-ta/`, and the skill is available in every session.

## Use

Talk to it like a TA at office hours. Examples of things it does well:

- **Concept help** — *"Why does integral action remove offset but cause windup when the heater saturates?"*
- **Homework coaching** — *"I got Kp = 8.5 °C/% and θp = 140 s from my TCLab step test and my PI controller is sluggish — what am I doing wrong?"* (It will sanity-check your fit and coach you to re-read the plot rather than just handing you numbers.)
- **Quiz me** — *"Quiz me on second-order systems, one question at a time, and keep score."* Every assignment's Generative AI Learning section has ready-made prompts like this.
- **TCLab and code debugging** — paste your Python error or your controller code; it knows the `tclab` package, the digital twin (`tclab.setup(connected=False)`), and the velocity-form PID used in the course apps.
- **Report coaching** — bring your plots and numbers and it will critique your "What to Turn In" report against the assignment's questions.
- **Project + EE support (classes 26–41)** — circuits, sensors, actuator drive circuits, power budgets, SCADA architecture, and the electrical safety review for your microcontroller project.
- **Going deeper** — ask about Bode plots, state space, Smith predictors, or MPC; it will teach beyond the course and point you to follow-on resources like [Dynamic Optimization](https://apmonitor.com/do).

## What it will not do

The skill enforces the course AI policy, so expect it to redirect you if you ask it to:

- solve your specific graded assignment problem outright or write your report's results for you;
- answer quiz or exam questions being taken for a grade;
- invent data, plots, or "observations" for a lab you didn't run (it will point you to the TCLab digital twin or the browser apps instead — real data in minutes).

You are the engineer of record for everything you submit. Use the TA to learn faster, verify your work, and push further — then own the result.

## For instructors

The skill is plain Markdown inside a zip. To adapt it for your own course: extract, edit `SKILL.md` (policy and tutoring behavior), `references/course-map.md` (schedule, links, apps), and `references/course-notes.md` (notation and key results), then re-zip the folder and rename it `.skill`. The review HTML shows the kind of behavioral testing used to check that the TA coaches instead of solving.
