from diagrams import Diagram
from diagrams.generic.blank import Blank
from diagrams.programming.language import Java
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.framework import FastAPI

with Diagram("Snyk CI Pipeline with Grafana", show=True):
    github_actions = GithubActions("CI Pipeline")
    snyk_tests = GithubActions("Run Snyk Tests")

    categories = Java("Categories Service")
    cities = Java("Cities Service")
    communities = Java("Communities Service")

    wrapper = FastAPI("Wrapper Script")

    prometheus = Prometheus("Metrics")
    grafana = Grafana("Snyk Security Dashboard")

    github_actions >> snyk_tests
    snyk_tests >> categories
    snyk_tests >> cities
    snyk_tests >> communities
    wrapper << snyk_tests
    prometheus << wrapper
    grafana << prometheus
