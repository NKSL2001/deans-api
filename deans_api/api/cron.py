import requests
import logging
import datetime
from .models import Crisis
from django_cron import CronJobBase, Schedule

logger = logging.getLogger("django")

def construct_report_data():
    """
    Construct report data for email or API requests.
    """
    payload = {"new_crisis": [], "recent_resolved_crisis": [], "active_crisis": []}
    created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    
    try:
        new_crisis = Crisis.objects.filter(crisis_time__gte=created_time)
        recent_resolved_crisis = Crisis.objects.filter(updated_at__gte=created_time, crisis_status="RS")
        active_crisis = Crisis.objects.exclude(crisis_status="RS")
        
        for crisis_set, key in [(new_crisis, "new_crisis"), 
                                (recent_resolved_crisis, "recent_resolved_crisis"), 
                                (active_crisis, "active_crisis")]:
            for i in crisis_set:
                payload[key].append({
                    "crisis_time": i.crisis_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "location": i.crisis_location1,
                    "status": i.crisis_status,
                    # Other fields as needed
                })
        return payload
    except Exception as e:
        logger.error(f"Error constructing report data: {str(e)}")
        return payload

class CronEmail(CronJobBase):
    RUN_EVERY_MINS = 1
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.CronEmail'

    def do(self):
        """
        Send email or API report.
        """
        url = "http://notification:8000/reports/"
        payload = construct_report_data()
        headers = {'Content-Type': "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                logger.info("Report successfully sent.")
            else:
                logger.error(f"Failed to send report: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            logger.error(f"Error sending report: {str(e)}")
