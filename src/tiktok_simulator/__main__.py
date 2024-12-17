from tiktok_simulator.constants import STEPS_COUNT
from tiktok_simulator.simulator import TikTokSimulator
from tiktok_simulator.user_interests import UserInterestByAuthorStats, AuthorStats, UserInterestByVideoStats, VideoStats
from tiktok_simulator.user_journey import UserJourneyTopN

if __name__ == '__main__':
    simulator = TikTokSimulator()
    simulator.init()

    tag = "foodie"

    user_journey = UserJourneyTopN(STEPS_COUNT)
    simulator.set_user_journey(user_journey)

    simulator.run(tag=tag)

    for author_stat in AuthorStats:
        user_interest = UserInterestByAuthorStats(author_stat)
        user_journey.set_user_interest(user_interest)
        simulator.run(tag=tag, skip_scraping=True)

    for video_stat in VideoStats:
        user_interest = UserInterestByVideoStats(video_stat)
        user_journey.set_user_interest(user_interest)
        simulator.run(tag=tag, skip_scraping=True)

    simulator.teardown()
