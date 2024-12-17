# TikTok User Journey Simulator

---

The simulator uses Undetected Chrome Driver (Patches for Bot Detection) and Seleniumwire (Capturing Network Traffic) to
interact with TikTok's web interface, scraping video metadata and generating user journey data based on configurable
user interest models.

---

## Docs

---

- [Problem Statement](docs/problem_statement.md)
- [System Design](docs/system_design.md)

---

## Repository Structure

---

```
.
├── data/                       # Stores scraped metadata and generated user journey data
├── docs/                       # Project documentation
└── src/
├    └── tiktok_simulator/      # Main package directory
├        ├── __init__.py
├        ├── __main__.py        # Entry point for the simulator
├        ├── constants.py       # Constant values used across the project
├        ├── exceptions.py      # Custom exception classes
├        ├── scraper.py         # TikTok video metadata scraper
├        ├── simulator.py       # Core simulation logic
├        ├── user_interests.py  # User interest models
├        ├── user_journey.py    # User journey generation
├        └── utils.py           # Utility functions
├── requirements.txt            # Requirements txt file
├── setup.py                    # Project setup and dependency configuration
└── README.md
```

---

## Data Flow

---

The TikTok User Journey Simulator follows this high-level data flow:

1. The `TikTokSimulator` initializes the Chrome WebDriver and sets up the user journey.
2. The `TikTokVideoMetadataScraper` fetches video metadata for a given hashtag from TikTok.
3. The `UserJourney` implementation (e.g., `UserJourneyTopN`) generates user interactions based on the scraped metadata
   and the configured `UserInterest` model.
4. The simulator processes these interactions, simulating user behavior on the platform.
5. Results are stored as JSON files in the `data/` directory for further analysis.

```
[TikTokSimulator] -> [TikTokVideoMetadataScraper] -> [UserJourney] & [UserInterest] -> [Data Storage]
```

---

## Usage Instructions

---

### Installation

---

1. Ensure you have Python 3.12 or later and Chrome browser installed.
2. Clone the repository:
   ```
   git clone https://github.com/Ameykolhe/tiktok-user-journey-simulation.git
   cd tiktok-user-journey-simulation
   ```
3. Install the required dependencies:
   ```
   pip install -e .
   ```

---

### Configuration

---

The simulator's behavior can be customized by modifying the following files:

- `src/tiktok_simulator/constants.py`: Adjust simulation parameters such as the number of steps in a user journey.
- `src/tiktok_simulator/user_interests.py`: Define custom user interest models to simulate different user behaviors.
- Run `python3 -m tiktok_simulator.login` and log in with your TikTok account. This is a one-time setup that saves login
  information and cookies in your local Chrome user profile, enabling data scraping.

---

### Usage

---

1. Using Default Journey and Interest Models:

   ```python
   from tiktok_simulator.simulator import TikTokSimulator

   tag = "foodie"
   
   simulator = TikTokSimulator()
   simulator.init()
   simulator.run(tag=tag)
   ```

2. Using Customer User Interest Models:

   ```python
   from tiktok_simulator.user_interests import UserInterestByAuthorStats
   from tiktok_simulator.user_interests import AuthorStats
   
   # Run simulation with author-based interest model
   user_interest = UserInterestByAuthorStats(AuthorStats.FOLLOWER_COUNT)
   user_journey.set_user_interest(user_interest)
   simulator.run(tag=tag, skip_scraping=True)
   ```

   ```python
   from tiktok_simulator.user_interests import UserInterestByVideoStats
   from tiktok_simulator.user_interests import VideoStats
   
   # Run simulation with video-based interest model
   user_interest = UserInterestByVideoStats(VideoStats.PLAY_COUNT)
   user_journey.set_user_interest(user_interest)
   simulator.run(tag=tag, skip_scraping=True)
   ```

3. Don't forget to close selenium

   ```python
   simulator.teardown()
   ```

---

### Debugging

---

To enable verbose logging:

- Modify `src/tiktok_simulator/__init__.py`:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

OR

- Run the simulator with the `--debug` flag:
   ```
   python -m tiktok_simulator --debug
   ```

---

### Troubleshooting

---

1. WebDriver issues:
    - Ensure Chrome is installed and the path is correctly set in your system's PATH variable.

2. Rate limiting:
    - Implemented exponential backoff in the `scraper.py` file.

3. Data parsing errors:
    - Check the raw response from TikTok in the `scraper.py` file and update the parsing logic if the API response
      format has changed.

