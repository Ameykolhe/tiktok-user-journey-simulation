# System Design

---

## Key Components

---

### Browser Automation Layer

---

- Interacts with TikTok’s frontend to perform login actions, navigate to video pages, and load dynamic content.
- Uses patched web drivers (e.g., undetected_chromedriver) to launch headless browser sessions that mimic real user
  behavior.

---

### Proxy and Network Layer

---

- Uses tools like Selenium Wire or Browsermob Proxy to intercept network traffic for extracting API endpoints, tokens,
  and data payloads.
- Integrates with a proxy rotation service to cycle through IP addresses, mitigating IP bans.

---

### Authentication & Session Management

---

- Stores user login sessions locally via browser profiles to reduce frequent logins.
- Automates login when necessary (e.g., uses managed services to solve captchas or provides virtual phone numbers for
  SMS-based 2FA).

---

### Data Extraction Layer

---

#### Strategies

- Frontend Scraping
    - Use Selenium to load the page.
    - Extract data from rendered HTML elements.
    - Handle elements and waiting conditions for content load.
- HTTP Request Extraction
    - Intercept network calls using Selenium Wire or Browsermob Proxy.
    - Identify backend API endpoints and extract JSON payloads.
    - Store and reuse tokens from cookies and headers for direct HTTP calls.

#### Challenges and Solutions

- **Dynamic Content:** Use explicit waits, or fallbacks methods if elements are not found. Keep selectors updated.
- **Short Lived Tokens:** Refresh cookies and tokens by reloading the session or re-triggering login workflows.
- **Rate Limits (429 Responses):** Log failed attempts and schedule retries after a delay (Exponential Backoff).
- **Missing Frontend Triggers:**
    - Pure HTTP requests won’t trigger video views or event tracking.
    - Use Selenium’s browser actions to watch a few seconds of each video, thus generating tokens and data states
      consistent with real user sessions.

---

### Scalability & Orchestration

---

**Horizontal Scaling:** With multiple TikTok accounts, each is assigned to its own container. This prevents
cross-contamination of sessions and allows parallel scraping.

#### Approach

- **Containerization:** Each scraper runs in a container with its own browser instance and configuration.
- **Kubernetes:** Scale up or down the number of scrapers based on load and account requirements.
- **Scheduling and Coordination (Airflow):** Airflow DAGs manage scraping schedules, trigger scraping jobs periodically,
  handle retries on failure

---

### Data Storage & Processing

---

- **Real-time ingestion:** data is pushed to Kafka or a message queue for downstream consumers.
- **Batch ingestion:** data is stored in object storage (e.g., S3) or a relational/noSQL database for batch processing.

---
