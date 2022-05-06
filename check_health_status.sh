#!/bin/bash
while :
do 
    # Airflow Endpoint URL
    ENDPOINT_URL="http://35.159.32.72:8080/"
    status=$(curl -s --user "airflow:airflow" "${ENDPOINT_URL}/api/v1/health" | jq -r '.scheduler' | jq -r '.status')
    echo "$status" 
    if [ $status ==  "healthy" ]
    then
        echo "Airflow Scheduler is healthy"
    else
        echo "Unhealthy, sent alert"
        # exit with errors
        # send alert code ... Messaging .. Slack/Teams Alerts ..
        exit 1
    fi  

    sleep 5
done


# Prometheus and Stats D 
