from instaloader import Profile
import instaloader
from config import Config


def download_profile_posts(insta_object: instaloader.Instaloader, config: Config):

    profile = Profile.from_username(insta_object.context, config.username)
    for i, post in enumerate(profile.get_posts()):
        if i >= config.post_limit:
            break
        if post.is_video:   
            insta_object.filename_pattern = "VID_{date_utc:%Y%m%d_%H%M%S}"
            item_type = 'video'
        else:               
            insta_object.filename_pattern = "IMG_{date_utc:%Y%m%d_%H%M%S}"
            item_type = 'image'

        insta_object.download_post(post, target=profile.username)