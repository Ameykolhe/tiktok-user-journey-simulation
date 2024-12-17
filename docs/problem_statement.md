# TikTok User Journey Simulation

---

## Part 1: Coding Task

---

Python script to simulate a basic TikTok user journey starting from a seed hashtag.

### Requirements

1. Accepts a seed hashtag (e.g., #foodie) as input.
2. Scrapes metadata from the first 3 videos related to the hashtag:
    1. Video title/caption.
    2. Creator username.
    3. Number of likes.
    4. Number of shares
    5. any other metadata you think would be useful in evaluating the user's journey on the platform
3. Simulates a "user journey" by selecting one of the scraped videos and following a related video chain for 2
   additional steps (a total of 3 videos in the journey).

### Output

- The script tiktoker.py
- A structured JSON file containing:
    - The starting hashtag.
    - Metadata for all videos in the journey, organized by step (e.g., Step 1, Step 2, Step 3).

### Constraints

- You can use mock data or predefined JSON API responses to simulate TikTok’s content structure or real data.
- Handle errors gracefully (e.g., missing data or network issues).
- Use libraries like requests, playwright, or selenium (your choice).

### Bonus (Optional)

- Simulate a "user interest" by choosing the next video based on specific criteria (e.g., most likes or specific
  hashtags in the metadata).
- Introduce simple delays or randomized behaviors to make the journey more realistic.

### Submission

GitHub repository, a sample might contain:

- Python script named tiktok_user_journey.py.
- A sample JSON file (user_journey.json) with the scraped journey.
- A brief explanation (in comments or a README.md) of your approach.

---

## Part 2: System Design Task

---

Write a brief document (300-500 words) answering the following:

### How would you scale this solution to:

- Simulate multiple user avatars with distinct behaviors (e.g., likes/dislikes, following patterns)
- What challenges would you face, and how would you address them?

### Bonus (Optional):

Outline how you would store and analyze user journey data to provide insights on trends or patterns.

### Submission

Answers to the above. Can appear in the same repo.