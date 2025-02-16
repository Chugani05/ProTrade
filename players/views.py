from .models import Player
from .serializers import PlayerSerializer


def player_list(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, request=request)
    return serializer.json_response()


def player_detail():
    pass


def add_player():
    pass


def transfer_player():
    pass