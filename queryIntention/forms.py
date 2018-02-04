from django import forms

from queryIntention.models import MemberFeature


class QueryIntentionContextForm(forms.Form):
    # os_choices = [('os_00', 'Android'), ('os_01', 'Windows'), ('os_02', 'iOS'), ('os_03', 'Unknown')]
    # channel_choices = [('ch_01', 'Mobile'), ('ch_00', 'Desktop'), ('ch_02', 'Unknown')]
    # language_choices = [('loc_00', 'English'), ('loc_01', 'NonEnglish')]
    # country_choices = [('loc_02', 'US'), ('loc_03', 'NonUS')]
    origin_choices = [('Tablet', 'Tablet'), ('Phone', 'Phone'), ('Desktop', 'Desktop'), ('API', 'API'),
                      ('Unknown', 'Unknown')]

    memberId = forms.IntegerField(required=True)
    raw_query = forms.CharField(max_length=128)
    # os = forms.ChoiceField(choices=os_choices)
    # channel = forms.ChoiceField(choices=channel_choices)
    # language = forms.ChoiceField(choices=language_choices)
    # country = forms.ChoiceField(choices=country_choices)
    origin = forms.ChoiceField(choices=origin_choices)


class MemberFeatureForm(forms.ModelForm):
    class Meta:
        model = MemberFeature
        exclude = []
