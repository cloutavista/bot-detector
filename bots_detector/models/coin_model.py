from bots_detector.models.base_model import Model


class CoinModel(Model):

    def predict(self, profile):
        return sum(profile['StakeEntryStats'].values()) > 0
