import abc
import logging
from abc import ABC

from tiktok_simulator.user_interests import UserInterestDefault, UserInterestBase

logger = logging.getLogger(__name__)


class UserJourney(ABC):
    """
    Represents the base class for user journeys with an abstract method for getting user journey data based on user interests.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self._user_interest: UserInterestBase = UserInterestDefault()
        self._video_url_template = "https://www.tiktok.com/@{author_id}/video/{video_id}"

    def set_user_interest(self, user_interest: UserInterestBase):
        self._user_interest = user_interest

    def get_user_interest(self) -> UserInterestBase:
        return self._user_interest

    @abc.abstractmethod
    def get_user_journey_data(self, item_list) -> list[dict[str, str | list | dict]]:
        pass


class UserJourneyTopN(UserJourney):
    """
    Represents the user journey strategy for the top N videos based on user interests.
    """

    def __init__(self, steps: int = 3):
        self.__steps = steps
        super().__init__()

    def _get_user_journey_item(self, item: dict[str, str | list | dict]):
        video_id = item["id"]
        author_id = item["author"]["uniqueId"]
        video_url = self._video_url_template.format(author_id=author_id, video_id=video_id)

        journey_item = {
            "video_id": video_id,
            "desc": item["desc"],
            "author_id": author_id,
            "video_url": video_url,
            "stats": item["stats"],
            "authorStats": item["authorStats"],
            "tags": [row["hashtagName"] for row in item["textExtra"]]
        }
        return journey_item

    def get_user_journey_data(self, item_list):
        logger.info(f"Simulating UserJourneyTopN by {self._user_interest.name}")

        assert self._user_interest is not None, "User interest is not set"
        sorted_item_list = self._user_interest.sort_metadata(item_list)[:self.__steps]
        return list(map(self._get_user_journey_item, sorted_item_list))
