import string

import plotly.graph_objs as go
import plotly.offline as opy
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from queryIntention.forms import QueryIntentionContextForm, MemberFeatureForm
from queryIntention.intentionModel import IntentionModel
from queryIntention.models import MemberFeature
from queryIntention.queryTagger import QueryTagger

intention_models = IntentionModel()
query_tagger = QueryTagger()
punctuation_remover = str.maketrans('', '', string.punctuation)
job_keywords = set(['jobs', 'job', 'position', 'positions'])
post_start_word = '#'


def demo(request):
    context_dict = dict()

    if request.method == 'POST':
        form = QueryIntentionContextForm(request.POST)
        if form.is_valid():
            context_dict['graphs'] = True
            context_dict['form'] = form

            queryIntentionContext = form.cleaned_data
            memberId = queryIntentionContext.get('memberId')
            raw_query = queryIntentionContext.get('raw_query')
            memberFeature = MemberFeature.objects.get(memberId=memberId)
            feature_dict = memberFeature.get_fields_as_dict()

            # search history
            sh_labels = []
            sh_values = []
            for f_name, f_value in feature_dict.items():
                if f_name.startswith('hist'):
                    sh_values.append(f_value)
                    label = ' '.join(f_name.split('_')[1:]).lower()
                    sh_labels.append(label)

            sh_trace = go.Pie(labels=sh_labels, values=sh_values, textinfo='label+percent', hoverinfo='label+percent')
            sh_data = go.Data([sh_trace])
            sh_layout = go.Layout(title='Search History')
            sh_figure = go.Figure(data=sh_data, layout=sh_layout)
            sh_div = opy.plot(sh_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['search_history_graph'] = sh_div

            # get all features
            tags = query_tagger.tag(raw_query)
            for tag in tags:
                feature_dict['has' + tag.capitalize()] = 1.0

            if raw_query.startswith(post_start_word):
                feature_dict['hasPost'] = 1.0

            keywords = set(raw_query.translate(punctuation_remover).lower().split())
            feature_dict['keyWordsCnt'] = float(len(keywords))

            if keywords.intersection(job_keywords):
                feature_dict['hasJob'] = 1.0

            origin = queryIntentionContext.get('origin')
            if origin == 'Tablet' or origin == 'Phone':
                feature_dict['ch_01'] = 1.0
            elif origin == 'Desktop':
                feature_dict['ch_00'] = 1.0
            else:
                feature_dict['ch_02'] = 1.0

            # all intention scores and logits
            intention_labels = []
            intention_scores = []
            intention_logits = []
            for intention in intention_models.get_intention_lables():
                intention_labels.append(intention)
                score, logit = intention_models.predict(feature_dict, intention)
                intention_scores.append(score)
                intention_logits.append(logit)

            # Intention score graph
            is_trace = go.Bar(x=intention_labels, y=intention_scores,
                              text=['{:.2f}'.format(score) for score in intention_scores],
                              textposition='auto', textfont=dict(color='salmon'),
                              hoverinfo='x+text')
            is_data = go.Data([is_trace])
            is_layout = go.Layout(title="Intention Scores", yaxis=dict(range=[0, 1]))
            is_figure = go.Figure(data=is_data, layout=is_layout)
            is_div = opy.plot(is_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['intention_scores_graph'] = is_div

            # Intention logit graph

            ## Logit breakdown
            sh_logits = []
            fp_logits = []
            tagger_logits = []
            query_context_logits = []

            # Logit detail breakdown
            sh_logits_details = dict()
            fp_logits_details = dict()
            tagger_logits_details = dict()
            query_context_logits_details = dict()

            for intention_label, logit_dict in zip(intention_labels, intention_logits):

                sh_logit = 0.0
                fp_logit = 0.0
                tagger_logit = 0.0
                query_context_logit = 0.0

                for feature_name, logit in logit_dict.items():
                    if feature_name.startswith('hist_'):
                        sh_logit += logit
                        sh_logit_detail_label, sh_logit_detail_value = sh_logits_details.get(feature_name[5:].lower(),
                                                                                             ([], []))
                        sh_logit_detail_label.append(intention_label)
                        sh_logit_detail_value.append(logit)
                        sh_logits_details[feature_name[5:].lower()] = (sh_logit_detail_label, sh_logit_detail_value)
                    elif feature_name.startswith('fp_'):
                        fp_logit += logit
                        fp_logit_detail_label, fp_logit_detail_value = fp_logits_details.get(feature_name[3:].lower(),
                                                                                             ([], []))
                        fp_logit_detail_label.append(intention_label)
                        fp_logit_detail_value.append(logit)
                        fp_logits_details[feature_name[3:].lower()] = (fp_logit_detail_label, fp_logit_detail_value)
                    elif feature_name.startswith('has'):
                        tagger_logit += logit
                        tagger_logit_detail_label, tagger_logit_detail_value = tagger_logits_details.get(
                            feature_name[3:].lower(),
                            ([], []))
                        tagger_logit_detail_label.append(intention_label)
                        tagger_logit_detail_value.append(logit)
                        tagger_logits_details[feature_name[3:].lower()] = (
                            tagger_logit_detail_label, tagger_logit_detail_value)

                    else:
                        query_context_logit += logit
                        query_context_logit_detail_label, query_context_logit_detail_value = query_context_logits_details.get(
                            feature_name.lower(),
                            ([], []))
                        query_context_logit_detail_label.append(intention_label)
                        query_context_logit_detail_value.append(logit)
                        query_context_logits_details[feature_name.lower()] = (
                            query_context_logit_detail_label, query_context_logit_detail_value)

                sh_logits.append(sh_logit)
                fp_logits.append(fp_logit)
                tagger_logits.append(tagger_logit)
                query_context_logits.append(query_context_logit)

            il_sh_trace = go.Bar(x=intention_labels, y=sh_logits, name='SearchHistory',
                                 text=['{:.2f}'.format(logit) for logit in sh_logits],
                                 textposition='auto', hoverinfo='name+text')
            il_fp_trace = go.Bar(x=intention_labels, y=fp_logits, name='FootPrint',
                                 text=['{:.2f}'.format(logit) for logit in fp_logits],
                                 textposition='auto', hoverinfo='name+text')
            il_tagger_trace = go.Bar(x=intention_labels, y=tagger_logits, name='QueryTagger',
                                     text=['{:.2f}'.format(logit) for logit in tagger_logits],
                                     textposition='auto', hoverinfo='name+text')
            il_query_context_trace = go.Bar(x=intention_labels, y=query_context_logits, name='OtherContext',
                                            text=['{:.2f}'.format(logit) for logit in query_context_logits],
                                            textposition='auto', hoverinfo='name+text')
            il_data = go.Data([il_sh_trace, il_fp_trace, il_tagger_trace, il_query_context_trace])
            il_layout = go.Layout(title="Intention logits", barmode='relative', yaxis=dict(hoverformat='.2f'))
            il_figure = go.Figure(data=il_data, layout=il_layout)
            il_div = opy.plot(il_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['intention_logits_graph'] = il_div

            ## logit break down graph
            ### break down for sh
            sh_detail_traces = []
            for sh_trace_name, sh_trace_data in sh_logits_details.items():
                sh_detail_trace = go.Bar(x=sh_trace_data[0], y=sh_trace_data[1], name=sh_trace_name,
                                         text=['{:.2f}'.format(logit) for logit in sh_trace_data[1]],
                                         textposition='auto', hoverinfo='name+text')
                sh_detail_traces.append(sh_detail_trace)

            sh_detail_data = go.Data(sh_detail_traces)
            sh_detail_layout = go.Layout(title="Search History logits", barmode='relative',
                                         yaxis=dict(hoverformat='.2f'))
            sh_detail_figure = go.Figure(data=sh_detail_data, layout=sh_detail_layout)
            sh_detail_div = opy.plot(sh_detail_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['sh_detail_graph'] = sh_detail_div

            ### break down for fp
            fp_detail_traces = []
            for fp_trace_name, fp_trace_data in fp_logits_details.items():
                fp_detail_trace = go.Bar(x=fp_trace_data[0], y=fp_trace_data[1], name=fp_trace_name,
                                         text=['{:.2f}'.format(logit) for logit in fp_trace_data[1]],
                                         textposition='auto', hoverinfo='name+text')
                fp_detail_traces.append(fp_detail_trace)

            fp_detail_data = go.Data(fp_detail_traces)
            fp_detail_layout = go.Layout(title="Foot Print logits", barmode='relative',
                                         yaxis=dict(hoverformat='.2f'))
            fp_detail_figure = go.Figure(data=fp_detail_data, layout=fp_detail_layout)
            fp_detail_div = opy.plot(fp_detail_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['fp_detail_graph'] = fp_detail_div

            ### break down for tagger
            tagger_detail_traces = []
            for tagger_trace_name, tagger_trace_data in tagger_logits_details.items():
                tagger_detail_trace = go.Bar(x=tagger_trace_data[0], y=tagger_trace_data[1], name=tagger_trace_name,
                                             text=['{:.2f}'.format(logit) for logit in tagger_trace_data[1]],
                                             textposition='auto', hoverinfo='name+text')
                tagger_detail_traces.append(tagger_detail_trace)

            tagger_detail_data = go.Data(tagger_detail_traces)
            tagger_detail_layout = go.Layout(title="Query Tagger logits", barmode='relative',
                                             yaxis=dict(hoverformat='.2f'))
            tagger_detail_figure = go.Figure(data=tagger_detail_data, layout=tagger_detail_layout)
            tagger_detail_div = opy.plot(tagger_detail_figure, auto_open=False, output_type='div', show_link=False)
            context_dict['tagger_detail_graph'] = tagger_detail_div

            ### break down for query_context
            query_context_detail_traces = []
            for query_context_trace_name, query_context_trace_data in query_context_logits_details.items():
                query_context_detail_trace = go.Bar(x=query_context_trace_data[0], y=query_context_trace_data[1],
                                                    name=query_context_trace_name,
                                                    text=['{:.2f}'.format(logit) for logit in
                                                          query_context_trace_data[1]],
                                                    textposition='auto', hoverinfo='name+text')
                query_context_detail_traces.append(query_context_detail_trace)

            query_context_detail_data = go.Data(query_context_detail_traces)
            query_context_detail_layout = go.Layout(title="Other Context logits", barmode='relative',
                                                    yaxis=dict(hoverformat='.2f'))
            query_context_detail_figure = go.Figure(data=query_context_detail_data, layout=query_context_detail_layout)
            query_context_detail_div = opy.plot(query_context_detail_figure, auto_open=False, output_type='div',
                                                show_link=False)
            context_dict['query_context_detail_graph'] = query_context_detail_div

            return render(request, 'queryIntention/query_intention_demo.html', context_dict)
    else:
        form = QueryIntentionContextForm()
        context_dict['form'] = form
        return render(request, 'queryIntention/query_intention_demo.html', context_dict)


def make_member(request):
    if request.method == 'POST':
        form = MemberFeatureForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('queryIntention:query_intention_demo'))

    form = MemberFeatureForm()
    context_dict = dict()
    context_dict['form'] = form
    return render(request, 'queryIntention/make_member.html', context_dict)


def memberId_checker(request):
    memberId = request.GET.get('memberId')
    try:
        MemberFeature.objects.get(memberId=memberId)
        return HttpResponse('exist')
    except MemberFeature.DoesNotExist:
        pass

    return HttpResponse('nonexist')
