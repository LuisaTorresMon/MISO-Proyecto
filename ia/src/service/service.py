from ..utils.utils import CommonUtils

commonUtils = CommonUtils()

class Service:

    def __init__(self):
        pass

    def predict_ia(self, subject, context):
        prediction = commonUtils.get_ia_prediction(subject, context)
        return prediction