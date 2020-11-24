import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils.decorators import require_basic_auth
from utils.exceptions import get_stacktrace_str
from world.models import Campaign, Map, Action, CampaignProperty


@require_basic_auth
@require_http_methods(["GET"])
def load_campaign(request, campaign_name):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        user_properties = CampaignProperty.objects.filter(user=request.user)

        response = {
            'status': 'ok',
            'message': f'Campaign loaded (name={campaign_name}, id={campaign.id})',
            'date': timezone.localtime(campaign.updated).isoformat(timespec='microseconds'),
            'campaign': {
                'properties': [{'name': x.name, 'value': x.value} for x in user_properties],
                'maps': [x.name for x in campaign.map_set.all()]
            }
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@require_basic_auth
@require_http_methods(["GET"])
def load_map(request, campaign_name, map_name):
    try:
        tile_map = get_object_or_404(Map, campaign__name=campaign_name, name=map_name)

        response = {
            'status': 'ok',
            'message': f'Map loaded (name={map_name}, id={tile_map.id})',
            'date': timezone.localtime(tile_map.saved).isoformat(timespec='microseconds'),
            'map': json.loads(tile_map.data)
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@csrf_exempt
@require_basic_auth
@require_http_methods(["POST"])
def save_map(request, campaign_name, map_name):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        tile_map = Map.objects.get_or_create(campaign=campaign, name=map_name)
        data = request.body.decode('utf-8')
        json.loads(data)
        tile_map.data = data
        tile_map.saved = datetime.now()
        tile_map.save()

        response = {
            'status': 'ok',
            'message': f'Map saved (name={map_name}, id={tile_map.id})',
            'date': timezone.localtime(tile_map.saved).isoformat(timespec='microseconds'),
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@csrf_exempt
@require_basic_auth
@require_http_methods(["DELETE"])
def delete_map(request, campaign_name, map_name):
    try:
        tile_map = get_object_or_404(Map, campaign__name=campaign_name, name=map_name)
        tile_map_id = tile_map.id
        tile_map.delete()

        response = {
            'status': 'ok',
            'message': f'Map deleted (name={map_name}, id={tile_map_id})',
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@require_basic_auth
@require_http_methods(["GET"])
def all_actions(request, campaign_name, map_name):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        tile_map = get_object_or_404(Map, campaign=campaign, name=map_name)
        actions = list(tile_map.action_set.all().filter(created__gt=tile_map.saved))

        response = {
            'status': 'ok',
            'message': f'Actions loaded (len={len(actions)})',
            'date': timezone.localtime(
                actions[-1].created if actions else tile_map.saved).isoformat(timespec='microseconds'),
            'actions': [json.loads(x.data) for x in actions],
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@require_basic_auth
@require_http_methods(["GET"])
def load_actions(request, campaign_name, datetime_iso: str):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        actions = list(campaign.action_set.filter(
            created__gt=datetime.fromisoformat(datetime_iso)).exclude(user=request.user))

        response = {
            'status': 'ok',
            'message': f'Actions loaded (len={len(actions)})',
            'date': timezone.localtime(
                actions[-1].created).isoformat(timespec='microseconds') if actions else datetime_iso,
            'actions': [json.loads(x.data) for x in actions],
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@csrf_exempt
@require_basic_auth
@require_http_methods(["POST"])
def add_actions(request, campaign_name):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        data = request.body.decode('utf-8')
        actions = json.loads(data)['actions']
        for action_data in actions:
            tile_map = Map.objects.get(name=action_data['map'])
            Action.objects.create(campaign=campaign, map=tile_map, user=request.user, data=json.dumps(action_data))

        response = {
            'status': 'ok',
            'message': f'Actions added (len={len(actions)})',
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)


@csrf_exempt
@require_basic_auth
@require_http_methods(["DELETE"])
def reset_actions(request, campaign_name):
    try:
        campaign = get_object_or_404(Campaign, name=campaign_name)
        actions = list(campaign.action_set.all())
        for action in actions:
            action.delete()

        response = {
            'status': 'ok',
            'message': f'Actions deleted (len={len(actions)})',
        }
    except Http404 as e:
        response = {'status': 'nok', 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 'nok', 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 'nok', 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=200 if response['status'] == 'ok' else 500)
