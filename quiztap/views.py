from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsMeetVerified
from core.filters import ChainFilterBackend, IsOwnerFilterBackend, StatusFilterBackend
from core.paginations import StandardResultsSetPagination
from quiztap.models import Competition, Question, UserCompetition
from quiztap.permissions import IsParticipatedInCompetition
from quiztap.serializers import (
    CompetitionSerializer,
    QuestionSerializer,
    UserAnswerSerializer,
    UserCompetitionSerializer,
)


class CompetitionViewList(ListAPIView):
    filter_backends = [ChainFilterBackend, StatusFilterBackend]
    queryset = Competition.objects.filter(is_active=True).order_by("-created_at")
    pagination_class = StandardResultsSetPagination
    serializer_class = CompetitionSerializer


class QuestionView(RetrieveAPIView):
    http_method_names = ["get"]
    serializer_class = QuestionSerializer
    queryset = Question.objects.filter(can_be_shown=True)


class EnrollInCompetitionView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsMeetVerified]
    filter_backends = [IsOwnerFilterBackend]
    pagination_class = StandardResultsSetPagination
    queryset = UserCompetition.objects.all()
    serializer_class = UserCompetitionSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class UserAnswerView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsMeetVerified, IsParticipatedInCompetition]
    serializer_class = UserAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class ParticipantsNumberView(RetrieveAPIView):
    pass
