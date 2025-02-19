from django.http import HttpResponse, JsonResponse
from datetime import date
from decimal import Decimal

from .models import Player
from .serializers import PlayerSerializer

from teams.models import Team

from users.utils import auth_required
from shared.utils import required_get_method, required_post_method, get_valid_json


@required_get_method
def player_list(request: HttpResponse) -> JsonResponse:
    players = Player.objects.all()
    if position_query := request.GET.get('position'):
        players = players.filter(position=position_query)
    if team_query := request.GET.get('team'):
        players = players.filter(team__slug=team_query)
    serializer = PlayerSerializer(players, request=request)
    return serializer.json_response()


@required_get_method
def player_detail(request: HttpResponse, player_slug: str) -> JsonResponse:
    try:
        player = Player.objects.get(slug=player_slug)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Player not found'}, status=404)
    serializer = PlayerSerializer(player, request=request)
    return serializer.json_response() 


@required_post_method
@get_valid_json('name', 'slug', 'position', 'birth-date', 'market-value', 'team-slug')
@auth_required
def add_player(request: HttpResponse) -> JsonResponse:
    if request.data['position'] not in Player.Position:
        return JsonResponse({'error': 'Invalid position'}, status=400)
    try:
        birth_date=date.fromisoformat(request.data['birth-date'])
    except ValueError:
        return JsonResponse({'error': 'Invalid birth date'}, status=400)
    try:
        team = Team.objects.get(slug=request.data['team-slug'])
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)
    if Player.objects.filter(slug=request.data['slug']).exists():
        return JsonResponse({'error': 'Player already exists'}, status=400)
    player = Player.objects.create(
        name=request.data['name'], 
        slug=request.data['slug'], 
        position=request.data['position'],
        birth_date=birth_date,
        market_value=float(request.data['market-value']),
        team=team
        )
    return JsonResponse({'id': player.pk})


@required_post_method
@get_valid_json('slug')
@auth_required
def delete_player(request: HttpResponse) -> JsonResponse:
    try:
        player = Player.objects.get(slug=request.data['slug'])
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Player not found'}, status=404)
    player_id = player.pk
    player.delete()
    return JsonResponse({'id': player_id})


@required_post_method
@get_valid_json('player-slug', 'team-slug')
@auth_required
def transfer_player(request: HttpResponse) -> JsonResponse:
    try:
        player = Player.objects.get(slug=request.data['player-slug'])
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Player not found'}, status=404)
    try:
        new_team = Team.objects.get(slug=request.data['team-slug'])
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)
    if player.team.league != new_team.league:
        player.market_value += player.market_value * Decimal(0.1)
    player.team = new_team
    player.save()
    return JsonResponse({'id': player.pk})