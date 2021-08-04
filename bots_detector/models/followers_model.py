from bots_detector.models.base_model import Model


class FollowersModel(Model):
    
    def predict(self, profile):
        return profile['NumFollowing'] > 500
