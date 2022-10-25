from .celery import app
import celery_pubsub




@app.task
def cookies_validate(**kwargs):
    celery_pubsub.publish('auth.cookies.requests', data={
        'id': kwargs.get('uuid'),
        'access-cookie':kwargs.get('access_cookie', ''),
        'refresh-cookie':kwargs.get('access_cookie', ''),
    })


@app.task
def awaitReturn(rr, **kwargs):
    if( not rr.taskID == kwargs.get('task_id')):
        pass
    
    rr.result='Meaw'
    if rr: #== kwargs.get('data', '').get('taskID', ''):
        return True



    
