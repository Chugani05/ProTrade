from django.http import HttpResponse

from .models import Player
from .serializers import PlayerSerializer

from users.utils import auth_required
from shared.utils import required_get_method, required_post_method, get_valid_json


@required_get_method
def player_list(request: HttpResponse):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, request=request)
    return serializer.json_response()


@required_get_method
def player_detail(request: HttpResponse, player_slug: str):
    player = Player.objects.get(slug=player_slug)
    serializer = PlayerSerializer(player, request=request)
    return serializer.json_response() 


@required_post_method
@get_valid_json('name', 'slug', 'position', 'birth-date', 'market-value')
@auth_required
def add_player(request):
    pass


@required_post_method
@get_valid_json('slug')
@auth_required
def delete_player():
    pass


@required_post_method
@get_valid_json('player-slug', 'team-slug')
@auth_required
def transfer_player():
    pass