import json
from datetime import datetime
from json.decoder import JSONDecodeError

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils.decorators import require_basic_auth, redirect_preflight
from utils.exceptions import get_stacktrace_str
from world.models import Campaign, Map, Action, CampaignProperty, MapProperty


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def load_world(request):
    try:
        campaigns = Campaign.objects.all().order_by('name')
        response = {
            'status': 200,
            'message': f'World loaded',
            'world': {
                'campaigns': [{'name': x.name, 'id': x.campaign_id} for x in campaigns]
            }
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def load_campaign(request, campaign_id):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        user_properties = CampaignProperty.objects.filter(campaign=campaign, user=request.user)
        properties = [{'name': x.name, 'value': x.value} for x in user_properties]
        property_names = [p.name for p in user_properties]
        default_properties = CampaignProperty.objects.filter(campaign=campaign, user__isnull=True)
        for p in default_properties:
            if p.name not in property_names:
                properties.append({'name': p.name, 'value': p.value})

        response = {
            'status': 200,
            'message': f'Campaign loaded (name={campaign.name}, id={campaign.campaign_id})',
            'date': timezone.localtime(campaign.updated).isoformat(timespec='microseconds'),
            'campaign': {
                'properties': properties,
                'maps': [{'name': x.name, 'id': x.map_id} for x in campaign.map_set.order_by('name')]
            }
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def load_campaign_property(request, campaign_id, property_name):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        props = CampaignProperty.objects.filter(campaign=campaign, user=request.user, name=property_name)
        prop = props[0] if props else get_object_or_404(CampaignProperty,
                                                        campaign=campaign, user=None, name=property_name)

        response = {
            'status': 200,
            'message': f'Campaign Property loaded (campaign_name={campaign.name}, name={property_name})',
            'campaign': {'properties': [{'name': prop.name, 'value': prop.value}]}
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}, property={property_name}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["POST"])
def save_campaign_property(request, campaign_id, property_name):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        prop = CampaignProperty.objects.get_or_create(campaign=campaign, user=request.user, name=property_name)[0]
        prop.name = property_name
        prop.value = request.body.decode('utf-8')
        prop.save()

        response = {
            'status': 200,
            'message': f'Campaign Property saved (campaign_name={campaign.name}, '
                       f'name={property_name}, value={prop.value})',
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["POST"])
def default_campaign_property(request, campaign_id, property_name):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        prop = CampaignProperty.objects.get_or_create(campaign=campaign, user=None, name=property_name)[0]
        prop.name = property_name
        prop.value = request.body.decode('utf-8')
        prop.save()

        response = {
            'status': 200,
            'message': f'Campaign Property default (campaign_name={campaign.name}, '
                       f'name={property_name}, value={prop.value})',
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["DELETE"])
def delete_campaign_property(request, campaign_id, property_name):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        prop = get_object_or_404(CampaignProperty, campaign=campaign, user=request.user, name=property_name)
        prop.delete()

        response = {
            'status': 200,
            'message': f'Campaign Property deleted (campaign_name={campaign.name})',
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}, name={property_name}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def load_map(request, campaign_id, map_id):
    try:
        tile_map = get_object_or_404(Map, campaign__campaign_id=campaign_id, map_id=map_id)

        response = {
            'status': 200,
            'message': f'Map loaded (name={tile_map.name}, id={map_id})',
            'date': timezone.localtime(tile_map.saved).isoformat(timespec='microseconds'),
            'map': json.loads(tile_map.data)
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}, map={map_id}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def load_map_properties(request, campaign_id, map_id):
    try:
        tile_map = get_object_or_404(Map, campaign__campaign_id=campaign_id, map_id=map_id)
        user_properties = MapProperty.objects.filter(map=tile_map, user=request.user)
        properties = [{'name': x.name, 'value': x.value} for x in user_properties]
        property_names = [p.name for p in user_properties]
        default_properties = MapProperty.objects.filter(map=tile_map, user__isnull=True)
        for p in default_properties:
            if p.name not in property_names:
                properties.append({'name': p.name, 'value': p.value})

        response = {
            'status': 200,
            'message': f'Map Properties loaded (len={len(properties)})',
            'date': timezone.localtime(tile_map.saved).isoformat(timespec='microseconds'),
            'properties': properties
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e) + f' (campaign={campaign_id}, map={map_id}'}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["POST"])
def save_map(request, campaign_id, map_id):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        tile_map = Map.objects.get_or_create(campaign=campaign, map_id=map_id)[0]
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        tile_map.name = data['name']
        tile_map.data = json_data
        tile_map.saved = timezone.now()
        tile_map.save()

        response = {
            'status': 200,
            'message': f'Map saved (name={tile_map.name}, id={map_id})',
            'date': timezone.localtime(tile_map.saved).isoformat(timespec='microseconds'),
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["DELETE"])
def delete_map(request, campaign_id, map_id):
    try:
        tile_map = get_object_or_404(Map, campaign__campaign_id=campaign_id, map_id=map_id)
        tile_map.delete()

        response = {
            'status': 200,
            'message': f'Map deleted (name={tile_map.name}, id={map_id})',
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@require_basic_auth
@require_http_methods(["GET"])
def map_actions(request, campaign_id, map_id):
    try:
        tile_map = get_object_or_404(Map, campaign__campaign_id=campaign_id, map_id=map_id)
        actions = list(tile_map.action_set.all().filter(created__gt=tile_map.saved))

        response = {
            'status': 200,
            'message': f'Actions loaded (len={len(actions)})',
            'date': timezone.localtime(
                actions[-1].created if actions else tile_map.saved).isoformat(timespec='microseconds'),
            'actions': [json.loads(x.data) for x in actions],
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@csrf_exempt
@redirect_preflight
@require_basic_auth
@require_http_methods(["POST"])
def update_actions(request, campaign_id, datetime_iso: str):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        data = request.body.decode('utf-8')
        actions_post = json.loads(data)['actions'] if data else []
        for action in actions_post:
            if action.get('map'):
                tile_map = get_object_or_404(Map, campaign=campaign, map_id=action['map'])
                Action.objects.create(campaign=campaign, map=tile_map, user=request.user, data=json.dumps(action))
            else:
                Action.objects.create(campaign=campaign, user=request.user, data=json.dumps(action))

        actions = Action.objects.filter(campaign=campaign, created__gt=datetime.fromisoformat(datetime_iso))
        date = timezone.localtime(actions.last().created).isoformat(timespec='microseconds') if actions else datetime_iso
        actions = list(actions.exclude(user=request.user))

        response = {
            'status': 200,
            'message': f'Actions loaded (len={len(actions_post)}). Actions downloaded (len={len(actions)})',
            'date': date,
            'actions': [json.loads(x.data) for x in actions],
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])


@redirect_preflight
@csrf_exempt
@require_basic_auth
@require_http_methods(["DELETE"])
def reset_actions(request, campaign_id):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
        actions = list(campaign.action_set.all())
        for action in actions:
            action.delete()

        response = {
            'status': 200,
            'message': f'Actions deleted (len={len(actions)})',
        }
    except Http404 as e:
        response = {'status': 404, 'message': str(e)}
    except JSONDecodeError as e:
        response = {'status': 400, 'message': "JSONDecodeError: " + str(e)}
    except Exception as e:
        response = {'status': 500, 'message': get_stacktrace_str(e)}
    return JsonResponse(response, safe=False, status=response['status'])
