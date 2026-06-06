# Threat Model Help

### With thanks from Gemini :)

The official **OWASP Automated Threat Event Reference** (often referred to as the OWASP Automated Threats to Web Applications project, or the "OAT" codes) **does not include an official, native mapping to the STRIDE model within its core handbook.**

The OAT handbook is fundamentally designed around an *ontology of abuse*—classifying how attackers misuse *inherent, valid business logic and functionality* via automation, rather than exploiting structural code bugs.

However, because teams frequently use STRIDE for architecture-level threat modeling and OAT for application/business-logic-level threat modeling, security teams often manually map them.

---

## The Cross-Reference Matrix

The vast majority of the 21+ defined OWASP Automated Threats (OAT-001 through OAT-021) collapse heavily into **Denial of Service (DoS)**, **Spoofing**, and **Information Disclosure**.

The matrix below shows how the primary OAT events typically map to STRIDE based on the *primary security property* they violate during an automated attack:

| STRIDE Category | Primary Violated Property | Applicable OWASP Automated Threats (OAT) |
| --- | --- | --- |
| **S**poofing | Authentication / Identity | * **OAT-007 (Credential Stuffing):** Mass login attempts using leaked creds.<br>

<br>* **OAT-008 (Credential Cracking):** Brute-forcing login forms. |
| **T**ampering | Integrity | * **OAT-012 (Cashing Out):** Using stolen payment cards/validated gift cards.<br>

<br>* **OAT-016 (Skewing):** Repeated automated actions to alter metrics (e.g., likes, votes, SEO). |
| **R**epudiation | Non-repudiation / Audit | * *Rarely the primary driver for OATs*, but automated actions that intentionally mimic valid user behavior often break transactional audit trails. |
| **I**nformation Disclosure | Confidentiality | * **OAT-004 (Fingerprinting):** Automated requests to identify OS, software, or APIs.<br>

<br>* **OAT-011 (Scraping):** Mass harvesting of proprietary data, pricing, or content.<br>

<br>* **OAT-018 (Web Scraping):** Collecting sensitive code or layout structures. |
| **D**enial of Service | Availability | * **OAT-005 (Scalping):** Mass buying limited-supply goods, denying availability to real users.<br>

<br>* **OAT-006 (Expediting):** Speed-running workflows to bypass standard time queues.<br>

<br>* **OAT-013 (Sniping):** Bidding at the last possible microsecond to crowd out others.<br>

<br>* **OAT-015 (Denial of Service):** Direct layer 7 application resource exhaustion.<br>

<br>* **OAT-021 (Denial of Inventory):** Holding items in e-commerce carts to deplete stock. |
| **E**levation of Privilege | Authorization | * **OAT-009 (Capcha Bypass):** Programmatic solving of challenges to execute actions.<br>

<br>* **OAT-010 (Carding):** Mass validation of card details to exploit merchant accounts. |

---

A lot of teams run into exactly what you are experiencing. While dedicated threat modeling tools like Threat Dragon or IriusRisk are great in theory because they maintain a database of threats under the hood, their learning curve and rigid UI can kill the momentum of a collaborative workshop.

Using **Draw.io** or **Visio** gives teams total creative freedom. The challenge, of course, is that a blank canvas can lead to inconsistent, messy diagrams that don't actually surface threats.

Creating a localized **Modelling & Style Guide** is the perfect way to fix this. To make your guide successful, it needs to establish a strict layout language, map out how to deal with complex elements, and give teams a structured way to actually document the threats they find.

---

## 1. The Visual Language (The Legend)

Your style guide must start with a standardized element library so that a diagram created by Team A looks identical to one created by Team B.

| Element | Draw.io / Visio Shape | Style Rule |
| --- | --- | --- |
| **Process** | Circle or Rounded Rectangle | Must contain a clear name indicating *what* it does (e.g., "Process Payment", "Validate JWT"). **Never** leave it as a vague acronym. |
| **Data Store** | Two parallel lines (open rectangle) | Represents data at rest (S3 bucket, SQL Database, Local Cache). Always note if the data is encrypted at rest. |
| **External Interactor** | Square / Rectangle (or Actor icon) | Users, third-party APIs (e.g., Stripe, SendGrid), or legacy internal systems outside the team's control. |
| **Data Flow** | Directed Arrow ($\rightarrow$) | **Must be labeled with the data payload** (e.g., "HTTPS: TLS 1.3 / User Credentials"). Avoid generic "Connects to" labels. |
| **Trust Boundary** | Red, Dashed Line | Intersects any data flow where the level of trust changes (e.g., Internet to Public Subnet, or Web App to Database). |

---

## 2. Diagramming Rules of Thumb

To prevent diagrams from turning into unreadable "spaghetti monsters," enforce these three layout rules in your guide:

* **Left-to-Right / Top-to-Bottom Flow:** Structure the diagram chronologically based on a standard user request lifecycle. Ingress on the left/top, databases and backend processes on the right/bottom.
* **The "One-Page" Rule:** If a system is too massive, do not cram it into one diagram. Use **Level 0** (High-level architecture), **Level 1** (Component view), and **Level 2** (Detailed microservice breakdown) tabs in Draw.io.
* **Keep Boundaries Clean:** Trust boundaries should never clip through the middle of a process or data store shape. They must neatly separate them.

---

## 3. Creating a "Threat Catalogue" Template

Because Draw.io and Visio cannot auto-generate threats, your guide needs to provide a structured Markdown or spreadsheet template that sits *next* to the drawing.

When a team draws a **Trust Boundary**, they must reference your STRIDE-to-OAT matrix to brainstorm what can go wrong. Instruct them to log threats using this strict, repeatable syntax:

```markdown
### [Threat ID] e.g., T-01: Automated Inventory Depletion during Checkout
* **DFD Element Affected:** Data Flow #4 (User adding item to cart) & Process #2 (Inventory DB Update)
* **STRIDE Category:** Denial of Service (DoS)
* **OAT Reference:** OAT-021 (Denial of Inventory)
* **Threat Description:** An attacker uses an automated bot script to continuously add items to their shopping cart without completing the checkout, artificially exhausting stock levels and preventing legitimate users from purchasing goods.
* **Current Mitigation:** Carts expire and release inventory after 15 minutes. 
* **Risk Score / Action:** High. (Action: Implement rate-limiting on the `/cart/add` endpoint and introduce CAPTCHA tracking for anomalous session behavior).

```

---

## 4. The "Definition of Done"

The biggest trap teams fall into with Draw.io is drawing a gorgeous cloud architecture diagram instead of a **Threat Model Data Flow Diagram (DFD)**. Infrastructure components (like Load Balancers, Gateways, and Firewalls) often clutter the threat modeling space.

Your guide should explicitly state:

> 💡 **The Threat Modeling Goal:** We are tracking how **data moves, changes state, and crosses trust boundaries**. If a component doesn't inspect, alter, or store data (like a simple network pass-through switch), do not let it clutter the diagram. Focus entirely on where the application logic makes a security decision.

Here is a sample layout and accompanying guide section that you can drop directly into your Modelling & Style Guide.

This scenario models a classic **User Login & Multi-Factor Authentication (MFA) flow**, which is a prime target for both standard architectural attacks (STRIDE) and business-logic automation attacks (OAT).

---

# Visual Anchor Example: User Authentication Flow

### Scenario Context

* **Goal:** A user attempts to log in via a web portal.
* **Trust Boundary:** The system transitions from completely untrusted (the public Internet) to trusted (the internal corporate network/database layer).

### The Draw.io / Visio DFD Blueprint

Below is the layout logic teams should follow. You can recreate this easily using standard shapes:

```text
[ EXTERNAL INTERACTOR ]
     ( 1. Public User )
             │
             │  Data Flow [DF-01]: HTTPS (TLS 1.3) POST /login
             │  Payload: Username, Password (Plaintext in transit)
             ▼
======================================================================== [ TRUST BOUNDARY 1: Internet to DMZ ]
             │
             ▼
    [ PROCESS ELEMENT ]
     ( 2. Auth Service ) ◄─── Data Flow [DF-03]: Internal HTTPS POST /sms-send
             │           │   Payload: User Phone Number, Random 6-digit OTP Token
             │           │
             │           ▼
             │   [ EXTERNAL INTERACTOR ]
             │    ( 3. SMS Gateway Provider / e.g., Twilio )
             │
             ├─────────────────────────────────────────┐
             │                                         │
             │ Data Flow [DF-02]: Encrypted TCP/IP     │ Data Flow [DF-04]: Encrypted TCP/IP
             │ Payload: Username Hash, SHA-256 Query   │ Payload: Write temporary OTP code, 
             │                                         │ Set 5-min TTL
             ▼                                         ▼
    [ DATA STORE ELEMENT ]                    [ DATA STORE ELEMENT ]
     ( 4. User DB / SQL )                      ( 5. Session Cache / Redis )

```

---

### How to Instruct Teams to Analyze This Diagram

Your guide should teach teams to look at specific intersection points on this diagram to catch both STRIDE and OWASP Automated (OAT) threats:

#### 1. Intersecting the Trust Boundary (Data Flow [DF-01])

* **The Question:** "As data crosses from the public Internet into the Auth Service, what can an automated attacker do?"
* **The Threat:**
* **STRIDE:** Spoofing / Denial of Service.
* **OAT Reference:** **OAT-007 (Credential Stuffing)** & **OAT-008 (Credential Cracking)**.
* **Guidance Memo:** Because this endpoint is public-facing, malicious actors will attempt mass credential spray attacks. The Auth Service must have rate-limiting, IP reputation checks, or behavioral bot detection *before* querying the database.



#### 2. Analyzing the Data Stores (Elements 4 & 5)

* **The Question:** "What happens to the credentials at rest, and how temporary is the MFA token?"
* **The Threat:**
* **STRIDE:** Information Disclosure / Tampering.
* **OAT Reference:** **OAT-009 (CAPTCHA / Challenge Bypass)**.
* **Guidance Memo:** Element 5 (Redis) holds the OTP token. If the token doesn't have a strict Time-To-Live (TTL) or if it's predictable, bots can brute-force the 6-digit PIN before it expires. The process updating Element 4 (User DB) must hash passwords using an algorithm like Argon2id or bcrypt to mitigate disclosure risks if the database itself is compromised.



#### 3. Outsourcing Trust (Element 3)

* **The Question:** "What happens if our downstream dependency fails or is abused?"
* **The Threat:**
* **STRIDE:** Denial of Service (Financial / Application Resource Exhaustion).
* **OAT Reference:** **OAT-015 (Denial of Service)**.
* **Guidance Memo:** An attacker can loop the login process to trigger infinite MFA SMS requests. This results in massive financial billing costs from the SMS provider (Element 3) and can exhaust connection pools on the Auth Service (Element 2). Teams must ensure there is a "per-user" cooldown timer on requesting a new SMS.



---

### Pro-Tip for your Style Guide:

When embedding this into your corporate wiki (like Confluence or an internal Markdown repository), attach the **actual XML code of a template Draw.io diagram**. This allows teams to copy-paste the exact visual anchor diagram into their own workspace, delete the sample elements, and start drawing with the correct, pre-configured shapes right away.

These four specific OWASP Automated Threats (OATs) highlight the conceptual difference between the two models: STRIDE looks at *software vulnerabilities* (bugs in code logic or architecture), while OAT looks at *abuse of business logic* (using valid features exactly how they were built, but at a speed and scale that causes harm).

When mapping **OAT-014, 017, 019, and 020** to STRIDE, they primarily map as follows:

---

### 1. OAT-014: Vulnerability Scanning

* **Definition:** Attackers using automated tools to crawl, fuzz, and enumerate your web app's endpoints, paths, or variables to look for exposed configurations or known bugs.
* **STRIDE Mapping:** **Information Disclosure** (Primary) & **Denial of Service** (Secondary)
* **The Logic:** The immediate goal of scanning is reconnaissance—discovering unadvertised or hidden aspects of your application's architecture (**Information Disclosure**). However, because high-intensity fuzzing and aggressive scanning engines throw massive volumes of unoptimized requests at the application layer, they frequently exhaust server resources, leading to an accidental or intentional application-level **Denial of Service**.

### 2. OAT-017: Spamming

* **Definition:** Using bots to inject malicious, misleading, or unwanted content into public or private forms (e.g., comment fields, product reviews, forum threads, or messaging services).
* **STRIDE Mapping:** **Tampering** (Primary) & **Spoofing** (Secondary)
* **The Logic:** By filling database-backed views with fake text, ads, SEO links, or phishing payloads, the attacker is altering the intended state and integrity of your application’s content (**Tampering**). Furthermore, because these bots usually generate fake names, emails, and personas to get past basic submission rules, they are **Spoofing** valid human entities.

### 3. OAT-019: Account Creation

* **Definition:** Programmatically registering a massive volume of fake profiles or accounts through your standard user sign-up endpoint.
* **STRIDE Mapping:** **Spoofing** (Primary) & **Denial of Service** (Secondary)
* **The Logic:** The fundamental act of register-botting relies on generating fake, non-existent identities to bypass the business logic barrier, which falls cleanly under **Spoofing** identity. The downstream result, however, is a **Denial of Service** to the database layer (bloating data storage) or a financial DoS (exhausting cloud infrastructure costs, or wasting paid API cycles like welcome emails or SMS verifications).

### 4. OAT-020: Account Aggregation

* **Definition:** Rogue or unauthorized middleware/aggregators scraping a user's account data, or consolidating logins/credentials across thousands of users into an outside dashboard without explicit tenant or platform approval.
* **STRIDE Mapping:** **Information Disclosure** (Primary) & **Spoofing** (Secondary)
* **The Logic:** The core behavior of an unauthorized aggregator is harvesting large tranches of business-critical, private user data (**Information Disclosure**). To achieve this at scale without formal API integrations, the aggregating scripts must repeatedly log in using hardcoded credentials or harvested session keys, effectively **Spoofing** legitimate user sessions to trick the platform into delivering data.

---

### Style Guide Cheat Sheet Matrix

You can append this directly to your template mapping matrix:

| OAT Code & Name | Primary STRIDE | Secondary STRIDE | Modeling Focus for Teams |
| --- | --- | --- | --- |
| **OAT-014** Vulnerability Scanning | Information Disclosure | Denial of Service | "Ensure public API processes handle unhandled inputs gracefully and use active rate-limiting to block aggressive crawl rates." |
| **OAT-017** Spamming | Tampering | Spoofing | "Validate that any process writing user text to a public Data Store sanitizes data and uses anti-bot heuristics (like CAPTCHA or invisible honey-pots)." |
| **OAT-019** Account Creation | Spoofing | Denial of Service | "Protect the Sign-Up process element with behavioral tracking. Enforce restrictions on anomalous mass registration from single networks." |
| **OAT-020** Account Aggregation | Information Disclosure | Spoofing | "Analyze public data endpoints. Ensure security telemetry can flag a single IP process attempting to read/scrape multiple distinct user accounts." |

You've hit on the exact subset of the OAT ontology that makes security teams pause.

**OAT-001 (Carding), OAT-002 (Card Cracking), OAT-003 (Cashing Out), and OAT-010 (Carding / Card Testing)** are hyper-focused on financial workflows. What makes them challenging to map to STRIDE is that they don't break the encryption, they don't exploit a traditional coding bug, and they don't necessarily "spoof" a system user in the traditional sense. Instead, they weaponize the payment processing pipeline itself.

When translating these financial threats into STRIDE language, they primarily sit across **Spoofing**, **Tampering**, and **Denial of Service** (specifically *Financial* DoS).

---

### 1. OAT-001: Carding & OAT-012: Cashing Out

*(Note: OAT-012 is "Cashing Out," but it shares identical STRIDE traits with OAT-001 as they are the two bookends of the financial fraud cycle).*

* **Definitions:** * **OAT-001:** Mass-testing lists of stolen credit card numbers against a payment gateway or e-commerce checkout to see which ones are still valid.
* **OAT-012:** Automatically using those confirmed stolen cards, gift certificates, or loyalty points to purchase high-value goods or transfer funds.


* **STRIDE Mapping:** **Spoofing** (Primary) & **Tampering** (Secondary)
* **The Logic:** At its core, the automated bot is presenting stolen payment credentials to an external financial interactor. The bot is **Spoofing** the identity of the legitimate, authorized cardholder. From a transaction perspective, it also constitutes **Tampering** because it injects unauthorized transactions into the payment processing data stream, altering the financial ledger fraudulently.

### 2. OAT-002: Card Cracking

* **Definition:** The brute-forcing of missing values on a partially known credit card. Attackers already have the card number but use bots to rapidly guess the missing Expiration Date and CVV/CSC security codes across thousands of parallel requests.
* **STRIDE Mapping:** **Tampering** (Primary) & **Denial of Service** (Secondary)
* **The Logic:** Unlike standard authentication spoofing, the attacker is actively fuzzing fields to manipulate the integrity of a payment transaction block until it switches from "Declined" to "Approved." This is a brute-force manipulation of transactional state (**Tampering**). Secondarily, it causes severe **Financial Denial of Service**. Every card network (Visa, Mastercard, etc.) charges merchants a fee for declined transactions. A massive card-cracking attack can rack up thousands of dollars in charge penalties in minutes, effectively denying the business its operational capital.

### 3. OAT-010: Carding / Card Testing

* **Definition:** Using a merchant's checkout process to verify the validity of stolen credit cards by making tiny, nominal purchases (often $1 or less). If the transaction succeeds, the attacker logs the card as "good" and sells it on the dark web.
* **STRIDE Mapping:** **Spoofing** (Primary) & **Denial of Service** (Secondary)
* **The Logic:** Similar to OAT-001, the bot is **Spoofing** the financial identity of an innocent cardholder. However, the secondary impact here is heavily shifted toward **Denial of Service**. Card testing triggers massive merchant chargeback rates. If a business's fraud ratio spikes above 1%, payment processors (like Stripe or Adyen) will completely freeze the merchant account—resulting in a catastrophic, literal **Denial of Service** to the company's entire revenue model.

---

### Visualizing the Financial Threat Pipeline

When teams map these threats in Draw.io or Visio, they shouldn't just look at their own internal code. They need to look at the **external boundaries** where their application talks to third-party payment gateways.

```text
[ CLIENT BROWSER / BOT ] 
          │
          │  Data Flow: /checkout/validate (Card, Expiry, CVV)
          ▼
   ( 1. E-Commerce App ) 
          │
          ======================================= [ TRUST BOUNDARY ]
          │
          │  Data Flow: Outbound API Request (Card Processing)
          ▼
[ EXTERNAL INTERACTOR: Payment Gateway ] <─── [OAT-002: Card Cracking tries to brute-force CVV]
(e.g., Stripe, Adyen, PayPal)           <─── [OAT-010: High volume of $1 authorization checks]

```

### Guidance for Your Teams on Financial Threats

Add this specific directive to your modeling guide for any team handling money, carts, or checkout services:

> 💳 **Financial Flow Guardrails:** When threat modeling any checkout or payment element, teams must look past infrastructure availability. You must model for **Resource and Financial Exhaustion**.
> Ask the team:
> 1. *What happens if an external actor triggers 50,000 failed credit card validations in an hour?* (Mitigates **OAT-002 / OAT-010** via velocity blocks).
> 2. *Does our payment processor allow us to set a minimum transaction limit to prevent card testing?* (Mitigates **OAT-010**).
> 3. *Can an attacker spoof a payment confirmation response from our gateway?* (Mitigates **OAT-012**).
> 
> 

| OAT Code | Primary STRIDE | Secondary STRIDE | Style Guide Anchor Point |
| --- | --- | --- | --- |
| **OAT-001** / **OAT-012** | Spoofing | Tampering | Check user identity verification and credential validation states. |
| **OAT-002** | Tampering | Denial of Service | Monitor payment validation endpoints for rapid, incremental parameter variations (Fuzzing). |
| **OAT-010** | Spoofing | Denial of Service | Check business logic for low-value transaction filtering and automated chargeback threshold alerts. |

Good catch! I skipped over **OAT-003 (Ad Fraud)** entirely.

Ad Fraud is a fascinating threat to model because it targets a component of web applications that developers often treat as completely passive: embedded advertising scripts, tracking pixels, and affiliate links.

Here is how OAT-003 maps to STRIDE and how your teams should approach it on a diagram.

---

### OAT-003: Ad Fraud

* **Definition:** Using automated bots to simulate human interaction with online advertisements, banners, sponsored links, or affiliate tokens embedded within your web application. This is done either to artificially inflate advertising revenue (if you host the ads) or to drain a competitor's advertising budget (if you click their ads on your site).
* **STRIDE Mapping:** **Spoofing** (Primary) & **Tampering** (Secondary)
* **The Logic:** The bot's primary mechanism of action is **Spoofing** a legitimate, high-intent human consumer. It simulates realistic mouse movements, scroll depths, and browser headers to mimic valid traffic. Secondarily, it represents **Tampering** because it injects fraudulent clickstream events and telemetry payload data into the marketing database. This alters the financial integrity of the advertising ledger, forcing a mismatch between real conversions and billed clicks.

---

### How to Model OAT-003 in Draw.io / Visio

Teams usually struggle to threat model Ad Fraud because the actual advertising exchange happens entirely in the user's browser, bypassing the core application backend.

To guide your teams, instruct them to draw the **Third-Party External Interactors** that handle marketing data:

```text
       [ MALICIOUS BOT ]
               │
               │  1. Spoofed User Interactions (Clicks & Views)
               ▼
       ( 2. Client Browser )
               │
               ├─────────────────────────────────────────┐
               │                                         │
               │ 2a. Valid/Invalid Requests              │ 2b. Telemetry Data
               ▼                                         ▼
   [ PROCESS: Web Server ]                 [ EXTERNAL INTERACTOR ]
   ( Serves page layout & ad scripts )     ( Ad Network / Affiliate API )
                                           ( e.g., Google Ads, Impact )
                                                         │
                                                         ▼
                                             [OAT-003: Inflates revenue /]
                                             [Drains ad spend metrics    ]

```

### Guidance for Your Teams on Ad Fraud

Add this section to your guide for marketing sites, e-commerce platforms, or applications using affiliate tracking:

> 📈 **Marketing & Telemetry Guardrails:** If our application displays third-party ads, tracks ad conversions, or processes affiliate links, we must recognize that client-side traffic cannot be implicitly trusted.
> Ask the team:
> 1. *Are we relying purely on client-side JavaScript to track ad completions, or are we validating conversions using a server-to-server API?* (Mitigates **Spoofing** via verified backend tracking).
> 2. *Does our third-party ad network handle bot detection natively, or are we passing custom session markers to help flag automated click behavior?* (Mitigates **Tampering** of ad metrics).
> 
> 

With that final financial piece added, your style guide will have a rock-solid foundation for helping teams map automated business logic abuse straight back to their structural architectural diagrams!