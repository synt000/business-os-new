from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.domains.campaign.models import Campaign
from src.domains.campaign.services.publish_service import CampaignPublishService
from src.domains.campaign.execution_models import CampaignExecutionLog
from src.telegram_bot.alert import send_ceo_alert


scheduler = BackgroundScheduler()


def process_scheduled_campaigns():

    print("[Scheduler] Checking campaigns")

    db: Session = SessionLocal()

    try:

        campaigns = (
            db.query(Campaign)
            .filter(
                Campaign.status == "scheduled",
                Campaign.scheduled_at <= datetime.utcnow()
            )
            .all()
        )

        print(
            f"[Scheduler] Found {len(campaigns)} scheduled campaigns"
        )


        for campaign in campaigns:

            execution = CampaignExecutionLog(
                campaign_id=campaign.id,
                status="running",
                attempt_count=1,
                worker_name="campaign_scheduler"
            )

            db.add(execution)
            db.commit()

            try:

                campaign.status = "processing"
                db.commit()

                CampaignPublishService.publish(
                    db,
                    campaign.id
                )

                campaign.status = "published"

                execution.status = "success"
                execution.completed_at = datetime.utcnow()
                execution.next_retry_at = None

                db.commit()

                print(
                    f"[Scheduler] Published {campaign.id}"
                )

            except Exception as e:

                campaign.status = "scheduled"

                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                execution.next_retry_at = None

                db.commit()

                try:
                    send_ceo_alert(
                        "🚨 Campaign Publish Failed\n\n"
                        f"Campaign ID: {campaign.id}\n"
                        f"Campaign: {getattr(campaign, 'name', campaign.id)}\n"
                        f"Error: {str(e)}"
                    )
                except Exception as alert_error:
                    print(
                        "[Telegram Alert ERROR]",
                        campaign.id,
                        alert_error
                    )

                print(
                    "[Scheduler ERROR]",
                    campaign.id,
                    e
                )

    finally:

        db.close()



def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            process_scheduled_campaigns,
            "interval",
            seconds=30,
            max_instances=1,
            coalesce=True
        )

        scheduler.add_job(
            process_retry_campaigns,
            "interval",
            seconds=30,
            max_instances=1,
            coalesce=True
        )

        scheduler.start()

        print(
            "[Campaign Scheduler] Started"
        )


def process_retry_campaigns():

    print("[Retry Worker] Checking failed executions")

    db: Session = SessionLocal()

    try:
        executions = (
            db.query(CampaignExecutionLog)
            .filter(
                CampaignExecutionLog.status == "failed",
                CampaignExecutionLog.retry_count < CampaignExecutionLog.max_retries
            )
            .all()
        )

        print(
            f"[Retry Worker] Found {len(executions)} retries"
        )

        for execution in executions:
            try:
                execution.status = "running"
                execution.retry_count += 1
                execution.attempt_count += 1

                db.commit()

                CampaignPublishService.publish(
                    db,
                    execution.campaign_id
                )

                execution.status = "success"
                execution.completed_at = datetime.utcnow()
                execution.next_retry_at = None

                db.commit()

                try:
                    send_ceo_alert(
                        "✅ Campaign Retry Succeeded\n\n"
                        f"Campaign ID: {execution.campaign_id}\n"
                        f"Retry Count: {execution.retry_count}\n"
                        "Status: Published successfully"
                    )
                except Exception as alert_error:
                    print(
                        "[Telegram Alert ERROR]",
                        execution.campaign_id,
                        alert_error
                    )

                print(
                    f"[Retry Worker] Success {execution.campaign_id}"
                )

            except Exception as e:

                execution.error_message = str(e)

                if execution.retry_count >= execution.max_retries:
                    execution.status = "failed_permanent"
                    execution.next_retry_at = None

                    try:
                        send_ceo_alert(
                            "🚨 Campaign Permanent Failure\n\n"
                            f"Campaign ID: {execution.campaign_id}\n"
                            f"Retry Count: {execution.retry_count}\n"
                            f"Max Retries: {execution.max_retries}\n"
                            f"Error: {execution.error_message}"
                        )
                    except Exception as alert_error:
                        print(
                            "[Telegram Alert ERROR]",
                            execution.campaign_id,
                            alert_error
                        )

                    print(
                        f"[Retry Worker] Permanent failure {execution.campaign_id}"
                    )

                else:
                    execution.status = "failed"

                    backoff_seconds = (
                        60 * (2 ** execution.retry_count)
                    )

                    execution.next_retry_at = (
                        datetime.utcnow()
                        + timedelta(seconds=backoff_seconds)
                    )

                    print(
                        f"[Retry Worker] Retry scheduled in {backoff_seconds}s"
                    )

                db.commit()

                print(
                    "[Retry Worker ERROR]",
                    execution.campaign_id,
                    e
                )

    finally:
        db.close()
