import boto3
import datetime
import requests
import os


def get_dates():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    month_start = today.replace(day=1)
    return today, yesterday, month_start


def get_cost_data(client, start, end, granularity, group_by_key=None):
    params = {
        'TimePeriod': {'Start': start.strftime('%Y-%m-%d'), 'End': end.strftime('%Y-%m-%d')},
        'Granularity': granularity,
        'Metrics': ['UnblendedCost'],
    }
    if group_by_key:
        params['GroupBy'] = [{'Type': 'DIMENSION', 'Key': group_by_key}]
    return client.get_cost_and_usage(**params)


def print_table(title, groups, key_label):
    print(f"\n{title}")
    print("{:<50} {:>10}".format(key_label, "Cost ($)"))
    print("-" * 62)

    total = 0.0
    for group in groups:
        key = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        total += amount
        print("{:<50} {:>10.2f}".format(key, amount))

    print("-" * 62)
    print("{:<50} {:>10.2f}".format(f"Total ({key_label})", total))
    return total


def post_to_discord(webhook_url, daily_total, month_total, report_date):
    summary = (
        f"📊 AWS Cost Summary for {report_date.strftime('%Y-%m-%d')}\n"
        f"• Total (Daily): ${daily_total:.2f}\n"
        f"• Total (MTD): ${month_total:.2f}"
    )
    payload = {"content": summary}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("\n✅ Summary successfully posted to Discord.")
        else:
            print(f"\n⚠️  Failed to post to Discord: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"\n❌ Error posting to Discord: {e}")


def main():
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("❌ DISCORD_WEBHOOK_URL is not set in environment.")
        return

    client = boto3.client('ce')
    today, yesterday, month_start = get_dates()

    service_resp = get_cost_data(client, yesterday, today, 'DAILY', 'SERVICE')
    usage_resp = get_cost_data(client, yesterday, today, 'DAILY', 'USAGE_TYPE')
    month_resp = get_cost_data(client, month_start, today, 'MONTHLY')

    daily_total = print_table(f"📆 AWS Daily Cost by SERVICE for {yesterday}", service_resp['ResultsByTime'][0]['Groups'], "Service")
    print_table(f"🛠️  Detailed Daily Cost by USAGE_TYPE for {yesterday}", usage_resp['ResultsByTime'][0]['Groups'], "Usage Type")

    month_total = float(month_resp['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    print("\n📅 Month-to-Date AWS Cost")
    print("-" * 30)
    print(f"{'Total (MTD)':<20} {month_total:.2f}")

    post_to_discord(webhook_url, daily_total, month_total, yesterday)


if __name__ == "__main__":
    main()
