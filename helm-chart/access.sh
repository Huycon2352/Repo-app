#!/bin/bash

prometheus_url=$(kubectl get svc -n prometheus | grep stable-kube-prometheus-sta-prometheus | awk '{print $4}')
grafana_url=$(kubectl get svc -n prometheus | grep stable-grafana | awk '{print $4}')
grafana_user="admin"
grafana_password=$(kubectl get secret stable-grafana -n prometheus -o jsonpath="{.data.admin-password}" | base64 --decode)



# Print or use these variables
echo "------------------------"

echo
echo "Prometheus URL: $prometheus_url":9090
echo
echo "Grafana URL: $grafana_url"
echo "Grafana User: $grafana_user"
echo "Grafana Password: $grafana_password"
echo "------------------------"
