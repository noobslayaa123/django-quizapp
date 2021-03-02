from django.shortcuts import render
from rest_framework import routers, serializers, viewsets,status
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from quiz.urls import *

from django.views.decorators.csrf import csrf_exempt

from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

@csrf_exempt
def playerstatus(request):
    if request.method=="POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        status = body['status']
        pdetails=body['pid']
        print(body)
        if status=='active':
            player=Player.objects.get(pid=pdetails)
            player.live_sts=1
            player.save()
            return HttpResponse(status=200)
        else:
            try:
                player=Player.objects.get(pid=pdetails)
                player.live_sts=0
                player.save()
            except Exception as e:
                print(e)
            return HttpResponse(status=200)
    if request.method=="GET":
        pid = request.GET.get('pid')
        print(pid)
        player=Player.objects.get(pid=pid)
        data={
        "status":player.live_sts
        }
        return JsonResponse(data, safe=False)

    return HttpResponse(status=403)


class PlayerQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlayerQuestions
		fields = ['pid','questionid','choice']
@csrf_exempt
def playerchoice(request):
    if request.method=="POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        serializer = PlayerQuestionSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            raw_query="""SELECT
        (count(CASE WHEN choice=1 THEN 1 END)*100)/count(pid) as perc1,
        (count(CASE WHEN choice=2 THEN 1 END)*100)/count(pid) as perc2,
    	(count(CASE WHEN choice=3 THEN 1 END)*100)/count(pid) as perc3
    FROM
       player_questions where questionid="""+str(body["questionid"])
            cursor = connection.cursor()
            cursor.execute(raw_query)

            datapoll = dictfetchall(cursor)
            stringified_data = datapoll

            return JsonResponse(stringified_data, status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=="GET":
        qid = request.GET.get('qid')
        print(qid)
        raw_query="""SELECT
    (count(CASE WHEN choice=1 THEN 1 END)*100)/count(pid) as perc1,
    (count(CASE WHEN choice=2 THEN 1 END)*100)/count(pid) as perc2,
	(count(CASE WHEN choice=3 THEN 1 END)*100)/count(pid) as perc3
FROM
   player_questions where questionid="""+str(qid)
        cursor = connection.cursor()
        cursor.execute(raw_query)

        datapoll = dictfetchall(cursor)
        stringified_data = datapoll

        return JsonResponse(stringified_data, status=200,safe=False)


    return HttpResponse(status=403)





@csrf_exempt
def getquestions(request):
    if request.method=="GET":
        retdata={}

        raw_query = "select tq.quizname,tq.quizid from tbl_quizlist tq where tq.quizstatus=1"

        cursor = connection.cursor()
        cursor.execute(raw_query)

        data = dictfetchall(cursor)
        stringified_data = data



        #print(stringified_data)
        #print(type(stringified_data))
        # jsondata = {}
        # quiz={}
        # question={}
        # agent['agentid'] = 'john'
        # content['eventType'] = 'view'
        # content['othervar'] = "new"
        #
        # jsondata['agent'] = agent
        # jsondata['content'] = content
        quizlistf={}

        for n in stringified_data:
            livequiz={}
            # print(n)
            # print(type(n))




            for key,value in n.items():
                #print(n["quizname"])
                qid=n["quizid"]
                quiz={}





                # quiz["QuizId"]=qid
                # quiz["QuizName"]=n["quizname"]
                h=TbQuestions.objects.filter(quizid=qid)

                for k in h.iterator():
                    #print(k.questionid)
                    #print(k.question)
                    qt={}
                    questions={}

                #     quid=k.questionid
                #     #print(k.question)
                #     questions['QuestionId'].append(quid)
                #     questions["QuestionText"].append(k.question)
                #     choices={}
                    choicelist=TblChoices.objects.filter(questionid=k.questionid)
                    choices={}
                    for c in choicelist.iterator():
                        choices['C1'] = c.choice1
                        choices['C2'] = c.choice2
                        choices['Answer'] = c.choice3
                        # print(c.choice1)
                        # print(c.choice2)
                        # print(c.choice3)

                    #print(questions["choices"])
                    #questions["choices"]=choices
                    questions["choices"]=choices
                    questions["ID"]=k.questionid
                    questions["TXT"]=k.question
                    #print(questions)
                    quiz[str(k.questionid)]=questions
                    #print(quiz)
                quiz["QuizID"]=n["quizid"]
                quiz["QuizName"]=n["quizname"]
                quizlistf[str(n["quizid"])]=quiz
                #print(quizlistf)
                #print("MESSAGE")

                #print(str(n["quizid"]))




                #     questions["choices"].append(choices)
                #     print(questions)
                # quizinfo["questions"]=questions
                # quizinfo["QuizId"]=qid
                # quizinfo["Quizname"]=n["quizname"]
                # print(quizinfo)
                # break
                    #print(questions)
                #livequiz["quizes"]=quiz
                #print(quiz)
                break








        #return HttpResponse(stringified_data, content_type="application/json")

        return JsonResponse(quizlistf, safe=False)
