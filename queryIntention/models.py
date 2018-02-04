from django.db import models


class MemberFeature(models.Model):
    memberId = models.IntegerField(unique=True, primary_key=True)
    hist_PROFILE_VIEW = models.FloatField(blank=True, null=True)
    hist_COMPANY_VIEW = models.FloatField(blank=True, null=True)
    hist_JOB_VIEW = models.FloatField(blank=True, null=True)
    hist_GROUP_VIEW = models.FloatField(blank=True, null=True)
    hist_SCHOOL_VIEW = models.FloatField(blank=True, null=True)
    hist_PEOPLE_SEARCH = models.FloatField(blank=True, null=True)
    hist_JOB_SEARCH = models.FloatField(blank=True, null=True)
    hist_COMPANY_SEARCH = models.FloatField(blank=True, null=True)
    hist_GROUP_SEARCH = models.FloatField(blank=True, null=True)
    hist_SCHOOL_SEARCH = models.FloatField(blank=True, null=True)
    hist_FEDERATED_SEARCH = models.FloatField(blank=True, null=True)
    hist_CONTENT_SEARCH = models.FloatField(blank=True, null=True)
    hist_PROFILE_INVITE = models.FloatField(blank=True, null=True)
    hist_PROFILE_MESSAGE = models.FloatField(blank=True, null=True)
    hist_COMPANY_FOLLOW = models.FloatField(blank=True, null=True)
    hist_COMPANY_UNFOLLOW = models.FloatField(blank=True, null=True)
    hist_GROUP_JOIN = models.FloatField(blank=True, null=True)
    hist_GROUP_LEAVE = models.FloatField(blank=True, null=True)
    hist_SCHOOL_FOLLOW = models.FloatField(blank=True, null=True)
    hist_SCHOOL_UNFOLLOW = models.FloatField(blank=True, null=True)
    hist_TOPIC_SEARCH = models.FloatField(blank=True, null=True)
    fp_CareerOpportunityResponse = models.FloatField(blank=True, null=True)
    fp_JobSeekerResponse = models.FloatField(blank=True, null=True)
    fp_RecruiterResponse = models.FloatField(blank=True, null=True)
    fp_SalesPersonResponse = models.FloatField(blank=True, null=True)
    fp_OthersResponse = models.FloatField(blank=True, null=True)
    fp_education = models.FloatField(blank=True, null=True)
    fp_entrepreneurship = models.FloatField(blank=True, null=True)
    fp_finance = models.FloatField(blank=True, null=True)
    fp_retail = models.FloatField(blank=True, null=True)
    fp_technology = models.FloatField(blank=True, null=True)
    fp_BusinessTraveler = models.FloatField(blank=True, null=True)
    fp_ItCommittee = models.FloatField(blank=True, null=True)
    fp_MassAffluent = models.FloatField(blank=True, null=True)
    fp_AmexCreditCard = models.FloatField(blank=True, null=True)
    fp_JobSeekerIntent = models.FloatField(blank=True, null=True)
    fp_RecruitingIntent = models.FloatField(blank=True, null=True)

    def get_fields_as_dict(self):
        result = dict()
        for field in self._meta.get_fields():
            value = getattr(self, field.name, None)
            if value:
                result[field.name] = value
        return result