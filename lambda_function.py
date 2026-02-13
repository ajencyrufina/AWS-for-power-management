import json
import os
import pymysql
import logging
import boto3

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SES client
ses = boto3.client('ses')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    # Environment variables
    host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    sender_email = os.environ['SENDER_EMAIL']  # verified SES sender email

    # Connect to RDS MySQL
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    try:
        device_id = event.get('device_id')
        current_power = float(event.get('current_power', 0))

        with connection.cursor() as cursor:
            # Fetch sanctioned power and associated user email
            cursor.execute(
                "SELECT d.sanctioned_power, u.email FROM devices d JOIN users u ON d.user_id = u.user_id WHERE d.device_id = %s",
                (device_id,)
            )
            result = cursor.fetchone()

        if result:
            sanctioned_power, user_email = result
            sanctioned_power = float(sanctioned_power)
            usage_ratio = (current_power / sanctioned_power) * 100

            # Determine message type
            if usage_ratio > 100:
                subject = f"⚠️ Power Limit Exceeded — Device {device_id}"
                message = (
                    f"Hello,\n\n"
                    f"Your device ({device_id}) has exceeded its sanctioned power limit.\n"
                    f"Current Power: {current_power}W\n"
                    f"Sanctioned Limit: {sanctioned_power}W\n\n"
                    f"Please take necessary action to avoid overuse."
                )
            elif usage_ratio > 85:
                subject = f"⚠️ High Power Usage Alert — Device {device_id}"
                message = (
                    f"Hello,\n\n"
                    f"Your device ({device_id}) is operating above 85% of its sanctioned power.\n"
                    f"Current Power: {current_power}W\n"
                    f"Sanctioned Limit: {sanctioned_power}W\n\n"
                    f"Please ensure efficient consumption of power."
                )
            else:
                subject = f"✅ Power Usage Normal — Device {device_id}"
                message = (
                    f"Hello,\n\n"
                    f"Your device ({device_id}) is operating within safe limits.\n"
                    f"Current Power: {current_power}W\n"
                    f"Sanctioned Limit: {sanctioned_power}W\n\n"
                    f"Keep up the efficient usage!"
                )

            # Log all key info (visible in CloudWatch)
            logger.info(f"Device: {device_id}, User: {user_email}, Sanctioned: {sanctioned_power}, Current: {current_power}")
            logger.info("📧 Email details:")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Body:\n{message}")

            # Send personalized email through SES
            ses.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [user_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': message}}
                }
            )

            logger.info(f"✅ Email sent to {user_email}")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Email sent successfully",
                    "user_email": user_email,
                    "subject": subject,
                    "body": message
                })
            }

        else:
            msg = f"Device {device_id} not found in database."
            logger.warning(msg)
            return {"statusCode": 404, "body": json.dumps({"message": msg})}

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    finally:
        connection.close()
