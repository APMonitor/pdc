# PDC Course TA - Knowledge File

Reference material for the Process Dynamics and Control TA (apmonitor.com/pdc).
Part 1 is the course map; Part 2 is the course notes (notation, key results, misconceptions).

---

# Course Map - Process Dynamics and Control (apmonitor.com/pdc)

Base URL for course pages: `https://apmonitor.com/pdc/index.php/Main/<PageName>`
Apps: `https://apmonitor.com/apps/<app>/` · EE lessons: `https://apmonitor.com/dde/index.php/Main/<PageName>`

## Schedule (class -> Topic | Quiz | Assignment | TCLab Activity)

| Class | Topic | Quiz | Assignment | TCLab Activity | App |
|---|---|---|---|---|---|
| 1 | GenerativeAI (Generative AI for Process Control) | QuizGenerativeAI | AgenticPreview (Course Preview with GenAI) + InstallPython | TCLabGenAI (TCLab Setup with an AI Assistant) | tclab-sim |
| 2 | SolveDifferentialEquations / PythonDifferentialEquations (ODEINT, GEKKO) | QuizSolveODEs | Catalytic Converter Light-off (on PDS site: apmonitor.com/pds .../AutomotiveMonitoring) | TCLabSim (Step Test Simulation) | tclab-sim |
| 3 | DynamicModeling (Physics-based Modeling) | QuizBalanceEquations | DeriveBalanceEquations | TCLabConvection | tclab-sim |
| 4 | PhysicsBasedModels (Transient Balances) | QuizTransientBalanceEquations | TankBlending | TCLabRadiative | blend, tclab-sim |
| 5 | ModelLinearization | QuizLinearization | LinearizeDiffEqns | TCLabLinearize | tclab-sim |
| 6 | FirstOrderSystems + FirstOrderPlusDeadTime + FirstOrderGraphical | QuizFirstOrderGraphical | FirstOrderFit (Graphical FOPDT) | TCLabFOPDT | tclab-sim |
| 7 | FirstOrderOptimization | QuizFirstOrderRegression | DynamicParameterRegression | TCLabRegression | tclab-sim |
| 8 | FeedbackControl (Control Design) | QuizControlDesign | ControllerDesign | TCLabControlDesign | tclab |
| 9 | ProportionalControl | QuizProportionalControl | TankLevel | TCLabPOnlyControl | level, tclab |
| 10 | ProportionalIntegralControl | QuizProportionalIntegralControl | SpeedControl (Auto Cruise) | TCLabPIControl | speed, tclab |
| 11 | ProportionalIntegralDerivative | QuizProportionalIntegralDerivative | ControlBlending | TCLabPIDControl | blend, tclab |
| 12-13 | ExamModeling review; Exam on Dynamics and Control | - | Practice Exam | - | - |
| 14 | LevelControl (Case Study) | QuizLevelControl | LevelControl | TCLabPIControlTuning | 2tank, tclab |
| 15 | StirredReactor (Nonlinear Control) | QuizReactorControl | StirredReactor | TCLabPIDControlTuning | reactor, tclab |
| 16 | DiabeticBloodGlucose (Disturbances) | QuizDiabetesControl | DiabeticBloodGlucose | TCLabPIDFeedforward | diabetic, cascade |
| 17 | FlowValves (Valve Design) | QuizFlowValves | ValveDesign | TCLabActuator | valve, tclab |
| 18 | SensorSignals + DataAcquisition | QuizSensors | SensorDesign | TCLabSensor | tclab |
| 19 | LaplaceTransforms | QuizLaplaceTransforms | LaplaceApplications | TCLabImpulseResponse | tclab |
| 20 | TransferFunctions | QuizTransferFunctions | TransferFunctionBlockDiagrams | TCLabBlockDiagram | tclab |
| 21 | SecondOrderSystems + SecondOrderGraphical | QuizSecondOrderSystems | SecondOrderApplications | TCLabOnOffControl | tclab-sim, tclab |
| 22 | SecondOrderOptimization | QuizSecondOrderOptimization | SecondOrderOptimizationFit | TCLabSecondOrder | tclab-sim |
| 23 | CascadeControl + FeedforwardControl | QuizFeedforwardCascade | FeedforwardCascadeControl | TCLabCascadeControl | cascade, tclab |
| 24-25 | ExamControl review; Exam (sensors, actuators, dynamics) | - | Practice Exam | - | - |
| 26 | ProcessControlProject intro + EE overview | - | Control Project + EECircuits (EE 1) | - | all apps as digital twins |
| 27-28 | Project help | - | EESensors (EE 2) | - | - |
| 29-30 | Project help | - | EEActuators (EE 3) | - | - |
| 31-32 | Project help | - | EEMotors (EE 4) | - | - |
| 33 | Project help | - | Project Report (2 pages) + Presentation (5 min) | - | - |
| 34-35 | Data-Driven Engineering (apmonitor.com/dde) | - | EEScada (EE 5) | - | - |
| 36-37 | Data-Driven Engineering | - | EEPower (EE 6) | - | - |
| 38-39 | Data-Driven Engineering | - | EEStorage (EE 7) | - | - |
| 40-41 | Data-Driven Engineering | - | EESafety (EE 8, required before project demo) | - | - |
| 42 / Final | FinalExam review; Final Exam | - | - | - | - |

Assignments and TCLab activities end with a "What to Turn In" section: a short PDF report (1-2 pages) answering listed questions with correct plots, justifications, and assumptions. Students may use AI to help write it but own every claim.

## Simulation and control apps (https://apmonitor.com/apps)

| App | URL path | What it does / used for |
|---|---|---|
| TCLab Control Studio | tclab | Two-heater TCLab digital twin + physical device over Web Serial; manual or velocity-form PID (Types A/B/C), safety latch, CSV export. All TCLab control exercises. |
| TCLab Simulation Studio | tclab-sim | Fit first-order, convective, or convective+radiative energy balances to step-test data with sliders and a live sum-of-absolute-errors objective; two-heater extension. All TCLab modeling exercises. |
| Tank Level Control Studio | level | Gravity-drained tank, manual or PID, sensor noise and valve disturbances (TankLevel assignment). |
| Vehicle Speed Control Studio | speed | Cruise control with quadratic drag (gain varies with speed), hills/wind/cargo disturbances (SpeedControl). |
| Blending Tank Control Studio | blend | Outlet concentration control with 0-2 mol/L actuator constraint (TankBlending, ControlBlending). |
| Two-Tank Level Control Studio | 2tank | Interacting tanks, splitter valve changes dynamics (LevelControl case study). |
| Stirred Reactor Control Studio | reactor | Exothermic CSTR, cooling jacket, 400 K runaway alarm (StirredReactor). |
| Artificial Pancreas Control Studio | diabetic | Type-I diabetes, reverse-acting PID, meals/exercise, 64-104 mg/dL band (DiabeticBloodGlucose). |
| Feedforward Cascade Control Studio | cascade | Feedback vs feedforward vs cascade side by side with a lit P&ID signal path (FeedforwardCascadeControl, TCLabPIDFeedforward, TCLabCascadeControl). |
| Distillation Column Control Studio | distillation | 32-stage binary column, distillate composition via reflux ratio; project digital-twin option. |
| Valve Design | valve | Cv sizing, linear vs equal-percentage trim, inherent vs installed characteristic (ValveDesign). |

## EE mini-assignments (classes 26-41), each linking a Data-Driven Engineering lesson

| PDC page | DDE lesson page | Content |
|---|---|---|
| EECircuits | CircuitAnalysis | Ohm's law, power, dividers, LED resistor, project circuit sketch |
| EESensors | SensorSignal | Sensor selection, ADC resolution, calibration, noise |
| EEActuators | ActuatorControl | Transistor/MOSFET/relay drives, PWM, flyback diodes, safe state |
| EEMotors | MotorsAndDrives | DC/stepper/servo/induction+VFD, drivers, stall current, affinity laws |
| EEScada | ScadaSytems (note the site's spelling) | PLC/DCS/SCADA levels, Modbus/OPC UA, alarms, interlocks |
| EEPower | PowerSystems | AC/DC, three-phase, transformers, power budget, brownout |
| EEStorage | EnergyStorage | mAh, C-rate, chemistry, UPS, battery sizing |
| EESafety | ElectricalSafety | Shock/arc, grounding, GFCI, LOTO, Class I Div 1/2, project safety review (required before demo) |

## Prompt-planning (Agentic) pages - Machine Learning for Engineers (apmonitor.com/pds)

- AgenticWorkplan - structured project workplans (used for the control project)
- AgenticCoding - structured coding prompts with testing/validation
- AgenticVisualization - plots and dashboards
- AgenticReports - reports and presentations

## Other key pages

- CourseSchedule, CourseSyllabus, HomePage (course overview), ArduinoTemperatureControl (TCLab hardware), InstallPython, ProcessControlProject.
- Course sections on HomePage: Dynamic Modeling; Equipment Design (sensors, valves, DAQ); Control Design (P/PI/PID, stability, cascade/feedforward); Optimal Control (optimization, MPC).
- Related courses: Dynamic Optimization https://apmonitor.com/do (MPC, MHE), Machine Learning for Engineers https://apmonitor.com/pds, Data-Driven Engineering https://apmonitor.com/dde.

---

# Course Notes - Standard Notation, Key Results, and Misconceptions

Use these forms and symbols so tutoring matches the course website and lectures. Verify any derived number against limiting cases before presenting it.

## General balance equation

Accumulation = In - Out + Generation. Every dynamic model in the course starts here (total mass, component, or energy). Units must match term by term.

## First-Order Plus Dead Time (FOPDT)

tau_p * dy/dt = -y + K_p * u(t - theta_p)      (y, u are deviation variables)

- K_p = process gain = Delta_y / Delta_u at steady state [output units / input units]
- tau_p = time constant (63.2% of the way to the new steady state after the dead time)
- theta_p = dead time (delay before the output starts moving)

**Graphical fitting from a step test:**
1. Delta_u = input step size; Delta_y = total output change.
2. K_p = Delta_y / Delta_u.
3. theta_p = time from input step until the output first responds.
4. Find t_0.632 where y has covered 0.632*Delta_y; then tau_p = t_0.632 - theta_p.

Analytic step response (step Delta_u at t=0): y(t) = K_p*Delta_u*(1 - exp(-(t-theta_p)/tau_p)) for t >= theta_p, 0 before.

## P-only control and offset

u = u_bar + K_c*e. Closed-loop offset for a setpoint change on a first-order process:
offset = Delta_SP / (1 + K_c*K_p). Offset shrinks with larger K_c but never reaches zero; high K_c destabilizes processes with dead time. Surge tanks often *want* P-only (level absorbs disturbances).

## PI / PID standard (position) form

u(t) = u_bar + K_c*e(t) + (K_c/tau_I)*Integral(e dt) - K_c*tau_D * d(PV)/dt

- Integral removes offset; windup occurs when the actuator saturates - anti-reset windup pauses integration at limits.
- Derivative on measurement (PV), not error, avoids derivative kick on setpoint changes; derivative amplifies noise (filter or reduce tau_D).

**Discrete velocity form (used with TCLab, sample time dt):**
Delta_u_k = K_c*(e_k - e_k-1) + (K_c*dt/tau_I)*e_k - K_c*tau_D*(PV_k - 2*PV_k-1 + PV_k-2)/dt
u_k = u_k-1 + Delta_u_k, clipped to [0, 100]%.
Types in the TCLab Control Studio app: A = P and D act on error; B = D on PV; C = P and D on PV (only I acts on error - no proportional kick).

## IMC tuning correlations (FOPDT-based, the course standard)

PI: K_c = (1/K_p) * tau_p/(theta_p + tau_c),  tau_I = tau_p, with closed-loop time constant tau_c:
- aggressive:    tau_c = max(0.1*tau_p, 0.8*theta_p)
- moderate:      tau_c = max(1.0*tau_p, 8.0*theta_p)
- conservative:  tau_c = max(10*tau_p, 80*theta_p)

PID: K_c = (1/K_p)*(tau_p + 0.5*theta_p)/(tau_c + 0.5*theta_p), tau_I = tau_p + 0.5*theta_p, tau_D = tau_p*theta_p/(2*tau_p + theta_p).

Simple starter used in early TCLab exercises: K_c = 1/K_p, tau_I = tau_p.

## Second-order systems

tau^2 * y'' + 2*zeta*tau * y' + y = K_p * u

- zeta > 1 overdamped, = 1 critically damped, < 1 underdamped (oscillates).
- Overshoot ratio OS = exp(-pi*zeta/sqrt(1-zeta^2)); decay ratio = OS^2.
- Period of oscillation P = 2*pi*tau/sqrt(1-zeta^2). Read OS and P from the plot to get zeta and tau.
- Two first-order lags in series (two tanks, heater+sensor) give an overdamped second-order (S-shaped) response.

## Laplace / transfer functions

- Purpose: turn linear ODEs into algebra; G(s) = Y(s)/U(s) with zero initial conditions (deviation variables).
- Dead time: e^(-theta_p*s). FOPDT: G(s) = K_p*e^(-theta_p*s)/(tau_p*s + 1).
- Closed loop: Y/Y_sp = G_c*G_p/(1 + G_c*G_p) (unity feedback). Checks: s=0 gives steady-state gain; denominator roots give stability; final value theorem y(inf) = lim s->0 of s*Y(s) (only if stable).

## Feedforward and cascade

- Feedforward gain: K_ff = -K_d/K_p (K_d = disturbance gain, K_p = MV gain); enters the controller output additively. Requires a *measured* disturbance; errors in the model leave residual upset for feedback to clean up.
- Cascade: inner (secondary) loop must be noticeably faster than the outer (primary) and must intercept the disturbance; tune inner loop first. On the TCLab: T2 or heater power as secondary, T1 as primary; heater 2 acts as a measured disturbance for feedforward exercises.

## TCLab physical model and typical values

Energy balance (single heater, lumped):
m*c_p*dT/dt = U*A*(T_a - T) + epsilon*sigma*A*(T_a^4 - T^4) + alpha*Q      (T in K for the radiation term!)

Standard parameters: m = 0.004 kg, c_p = 500 J/kg-K, A = 0.0012 m^2, U ~ 10 W/m^2-K (4-10 typical fit range), epsilon = 0.9, sigma = 5.67e-8 W/m^2-K^4, T_a ~ 23 degC, alpha_1 = 0.01 W/% (heater 1), alpha_2 = 0.0075 W/% (heater 2).

Typical identified FOPDT for heater 1 -> T1: K_p ~ 0.6-0.9 degC/%, tau_p ~ 120-180 s, theta_p ~ 10-25 s. If a student reports values wildly outside these (e.g., negative K_p, theta_p > tau_p, tau_p of 2 s), question the fit before the tuning.

Hardware notes: blue USB = data, white adapter = heater power; `pip install tclab`; `tclab.setup(connected=False)` runs the digital twin; temperatures above ~55-60 degC are hot to the touch and the course caps tests around there.

## Common misconceptions to watch for

- Gain vs speed: K_p says *how far* the output goes, tau_p says *how fast* - students routinely conflate them.
- Time constant is not "time to finish": 63.2% at one tau, ~98% at four tau.
- P-only offset is not a tuning bug; integral action, not bigger K_c, is the fix (and sometimes offset is acceptable).
- Windup: after a long saturation, the loop overshoots badly not because K_c is wrong but because the integral accumulated.
- Radiation in Celsius: T^4 terms must use Kelvin; a sign or unit slip here makes the tank "heat itself."
- Linearization point must be a steady state of the nonlinear model, and the linear model lives in deviation variables.
- Dead time vs lag: a higher-order lag looks like dead time on a plot; both limit achievable K_c, but only true delay is e^(-theta*s).
- Derivative action: helps damping on clean signals, chatters the actuator on noisy ones; derivative-on-PV avoids setpoint kick.
- Correlation vs causation in fitted/ARX models: a good fit on training data says nothing about extrapolation to new operating conditions.

## Verification habits to model and demand

Units check term by term; limiting cases (t -> 0, t -> infinity, inputs to zero); signs (hot things cool toward ambient); steady-state balances close; numerical simulation overlays analytic solutions; and on this course, TCLab data is the final referee - a controller that only works in simulation is not done.
