import abc
from abc import ABC
from enum import Enum


class VideoStats(Enum):
    DIGG_COUNT = "diggCount"
    SHARE_COUNT = "shareCount"
    COMMENT_COUNT = "commentCount"
    PLAY_COUNT = "playCount"
    COLLECT_COUNT = "collectCount"


class AuthorStats(Enum):
    FOLLOWING_COUNT = "followingCount"
    FOLLOWER_COUNT = "followerCount"
    HEART_COUNT = "heartCount"
    VIDEO_COUNT = "videoCount"
    DIGG_COUNT = "diggCount"
    HEART = "heart"


class UserInterestBase(ABC):
    """
    Represents the base class for user interests with an abstract method for
    sorting metadata.
    """

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def sort_metadata(self, item_list):
        pass


class UserInterestDefault(UserInterestBase):
    """
    Represents the default user interest strategy.
    Default strategy does not sort the metadata
    """

    def __init__(self):
        super().__init__("UserInterestDefault")

    def sort_metadata(self, item_list):
        return item_list


class UserInterestByAuthorStats(UserInterestBase):
    """
    Represents the user interest strategy based on author statistics.
    """

    def __init__(self, stat_name: AuthorStats):
        self.stat_name = stat_name
        super().__init__(f"UserInterestByAuthorStats{stat_name.value.capitalize()}")

    def sort_metadata(self, item_list):
        return sorted(item_list, key=lambda x: x["authorStats"][self.stat_name.value], reverse=True)


class UserInterestByVideoStats(UserInterestBase):
    """
    Represents the user interest strategy based on video statistics.
    """

    def __init__(self, stat_name: str):
        self.stat_name = stat_name
        super().__init__(f"UserInterestByVideoStats{stat_name.value.capitalize()}")

    def sort_metadata(self, item_list):
        return sorted(item_list, key=lambda x: x["stats"][self.stat_name.value], reverse=True)
