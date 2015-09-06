from django.contrib.sessions.serializers import PickleSerializer
from billings.models import ValidatedTransaction

class TransactionValidator(PickleSerializer):
    """
    Simple service to keep transactions validated

    Yeah, i wrote the service in the service, so you can research a service when researching a service
    """
    def _encode(self, obj):
        return self.dumps(obj).encode('base64').rstrip('\n')

    def _decode(self, data):
        return self.loads(data.decode('base64'))

    def invalidate(self, username, sign):
        transaction = ValidatedTransaction(username=username,
                                        tranzaction_id=sign,
                                        is_validated=False)

        transaction.save()

        trz_cookie = {"trz_id": sign, "status":"processing"}
        return self._encode(trz_cookie)

    def get_id(self, cookie_data):
        trz_cookie = self._decode(cookie_data)
        return trz_cookie["trz_id"]

    def validate(self, username, trz_id):
        try:
            applicant = ValidatedTransaction.objects.get(tranzaction_id__iexact=trz_id)
        except Exception as ex:
            return False

        if applicant.username == username:
            applicant.is_validated = True
            applicant.save()
            return True
        else:
            return False
