from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F, Min
from .models import Issue, Agent, Mechanic

def add_agents():
    for i in range(4):
        Agent.objects.create(queue=0)
def add_mechanics():
    for i in range(10):
        Mechanic.objects.create(availability=True)
# add_agents()
# add_mechanics()

class NewIssueView(View):
    def get(self, request):
        return render(request, 'new_issue.html')

    def post(self, request):
        user_id = request.POST.get('user_id')
        location = request.POST.get('location')
        problem = request.POST.get('problem')

        issue = Issue.objects.create(userID=user_id, location=location, problem=problem)

        agent = Agent.objects.order_by('queue').first()
        agent.queue += 1
        issue.assigned_agent=agent.agentID

        mechanic = Mechanic.objects.filter(availability=True).order_by('mechanicID').first()
        if mechanic:
            issue.status = 'ASSIGNED'
            issue.assigned_mech = mechanic.mechanicID
            mechanic.availability = False
            mechanic.save()
        issue.save()
        temp=eval(agent.issue_list)
        temp.append(issue.issueID)
        agent.issue_list=str(temp)
        agent.save()
        mech_list=Mechanic.objects.all();
        agent_list=Agent.objects.all()

        return render(request, 'issue_created.html', {'issue': issue,'agent':agent,'mech_list':mech_list,'agent_list':agent_list})
    

def details(request,id):
    issue=Issue.objects.get(issueID=id)
    return render(request, "details.html",{'issue':issue})

def clear_issue(request,id):
    issue=Issue.objects.get(issueID=id)
    agent=Agent.objects.get(agentID=int(issue.assigned_agent))
    mech=Mechanic.objects.get(mechanicID=issue.assigned_mech)
    agent.queue -= 1
    agent.save()
    mech.availability=True
    issue.status='CLEARED'
    issue.save()
    assign_issue=Issue.objects.filter(status="INQUEUE").order_by('time').first()
    if(assign_issue):
        assign_issue.assigned_mech=mech.mechanicID
        assign_issue.status="ASSIGNED"
        assign_issue.save()
        mech.availability=False
    mech.save()
    return render(request,"details.html",{'issue':issue})

def delete(request,id):
    issue=Issue.objects.get(issueID=id)
    if(issue.status=="CLEARED"):
        issue.delete()
    return redirect(all_issues)


def all_issues(request):
    issues=[]
    for id in Agent.objects.values('agentID'):
        temp=Issue.objects.filter(assigned_agent=id['agentID']).order_by('time')
        temp2=[id['agentID']]
        for i in temp:
            temp2.append(i)
        issues.append(temp2)
    return render(request, "all_issues.html",{'issues':issues})