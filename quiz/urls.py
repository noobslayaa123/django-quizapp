from django.urls import path, include
from django.contrib.auth.models import User
from .models import *
from rest_framework import routers, serializers, viewsets,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import views


class TblQuizListSerizlizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TblQuizlist
        fields =  '__all__'



class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'

class PlayerViewSet(viewsets.ModelViewSet):

    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


class PlayerQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayerQuestions
		fields = ['pid','questionid','choice']


class PlayerQuestionViewset(viewsets.ModelViewSet):

    serializer_class = PlayerQuestionSerializer
    queryset = PlayerQuestions.objects.all()

# ViewSets define the view behavior.
class QuizlistViewset(viewsets.ModelViewSet):
    model = TblQuizlist
    serializer_class = TblQuizListSerizlizer
    queryset = TblQuizlist.objects.all()

    def get_queryset(self):
        queryset = TblQuizlist.objects.all()
        status = self.request.query_params.get('status')


        if status:
        	if status=="live":
        		queryset = queryset.filter(quizstatus=1)

        return queryset



class ChoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = TblChoices
        fields =  ['choice1','choice2','choice3']


class ChoicesViewSet(viewsets.ModelViewSet):
    queryset = TblChoices.objects.all()
    serializer_class = ChoiceSerializers


class QuestionSerializerModel(serializers.ModelSerializer):
	class Meta:
		model = TbQuestions
		fields = '__all__'

class QuestionSerializer(serializers.Serializer):

    choice_set = ChoiceSerializers(many=True)

    class Meta:
        model = TbQuestions
        fields = '__all__'

    def create(self, validated_data):
        choice_validated_data = validated_data.pop('choice_set')
        question = TbQuestions.objects.create(**validated_data)
        choice_set_serializer = self.fields['choice_set']
        for each in choice_validated_data:
            each['question'] = question
        choices = choice_set_serializer.create(choice_validated_data)
        return question
# class TbQuestionsSerializer(serializers.Serializer):
# 	quer = QuestionSerializerModel(required=False)
# 	choices = ChoiceSerializers(many=True)

class QuestionsViewset(viewsets.ModelViewSet):
	serializer_class = QuestionSerializerModel
	queryset = TbQuestions.objects.all()
# class QuestionsView(APIView):
# 	queryset = TbQuestions.objects.all()
# 	# def post(self, request, *args, **kwargs):

# 	# 	serializer = QuestionSerializer(data=request.data)
# 	# 	if serializer.is_valid():
# 	# 		question = serializer.save()
# 	# 		serializer = QuestionSerializer(question)
# 	# 		return Response(serializer.data, status=status.HTTP_201_CREATED)
# 	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 	def get(self, request,  *args, **kwargs):
# 		snippets = TbQuestions.objects.all()

# 		serializer_context = {
# 			'request': request
# 		}
# 		serializer = TbQuestionsSerializer(snippets,context=serializer_context,many=True)
# 		return Response(serializer.data,status=status.HTTP_200)

# class QuestionsViewset(viewsets.ModelViewSet):
#     queryset = TbQuestions.objects.all()
#     serializer_class = TbQuestionsSerializer

















router = routers.DefaultRouter()
router.register(r'quizlist', QuizlistViewset)
router.register(r'questions', QuestionsViewset)
router.register(r'choices', ChoicesViewSet)
router.register(r'player', PlayerViewSet)
router.register(r'playerchoicelist',PlayerQuestionViewset)




urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('getquestions/',views.getquestions),
    path('playerstatus/',views.playerstatus),
    path('playersetchoice/',views.playerchoice)

]
