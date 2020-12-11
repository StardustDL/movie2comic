Task f -depends frontend

Task b -depends backend-dev

Task backend-dev {
    Exec { python -m backend }
}

Task frontend {
    Exec { docker-compose -f .\docker-compose.dev.yml up httpd }
}