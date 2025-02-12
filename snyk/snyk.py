from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge, CollectorRegistry
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Snyk Metrics Exporter")
registry = CollectorRegistry()

dependencies_gauge = Gauge('snyk_dependencies_total', 'Total dependencies', ['service'], registry=registry)
issues_gauge = Gauge('snyk_issues_total', 'Total issues', ['service'], registry=registry)
vulnerable_paths_gauge = Gauge('snyk_vulnerable_paths_total', 'Total vulnerable paths', ['service'], registry=registry)
severity_gauge = Gauge('snyk_issues_by_severity_total', 'Issues by severity', ['service', 'severity'], registry=registry)

def parse_snyk_log(content: str, service: str):
    """Parse un fichier log Snyk et met à jour les métriques Prometheus."""
    try:
        logger.info(f"Parsing log for service {service}")
        
        dependencies_match = re.search(r'Tested (\d+) dependencies', content)
        issues_match = re.search(r'found (\d+) issues', content)
        paths_match = re.search(r'(\d+) vulnerable paths', content)

        if dependencies_match:
            dependencies_gauge.labels(service=service).set(int(dependencies_match.group(1)))
        if issues_match:
            issues_gauge.labels(service=service).set(int(issues_match.group(1)))
        if paths_match:
            vulnerable_paths_gauge.labels(service=service).set(int(paths_match.group(1)))

        severities = {
            'critical': len(re.findall(r'\[Critical Severity\]', content, re.IGNORECASE)),
            'high': len(re.findall(r'\[High Severity\]', content, re.IGNORECASE)),
            'medium': len(re.findall(r'\[Medium Severity\]', content, re.IGNORECASE)),
            'low': len(re.findall(r'\[Low Severity\]', content, re.IGNORECASE))
        }
        
        for severity, count in severities.items():
            severity_gauge.labels(service=service, severity=severity).set(count)
            
        logger.info(f"Successfully parsed metrics for {service}")
        
    except Exception as e:
        logger.error(f"Error parsing log for {service}: {str(e)}")
        raise

@app.get("/metrics")
async def metrics():
    """Endpoint Prometheus pour exposer les métriques."""
    try:
        logger.info("Starting metrics collection")
        
        log_files = [
            ('/app/logs/snyk-cities.log', 'cities'),
            ('/app/logs/snyk-communities.log', 'communities'),
            ('/app/logs/snyk-categories.log', 'categories'),
            ('/app/logs/snyk-products.log', 'products')
        ]

        for log_file, service_name in log_files:
            file_path = Path(log_file)
            if file_path.exists():
                logger.info(f"Reading {log_file}")
                content = file_path.read_text(encoding='utf-8')
                parse_snyk_log(content, service_name)
            else:
                logger.warning(f"File not found: {log_file}")

        return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
        
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}")
        return Response(
            status_code=500,
            content=f"Error generating metrics: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9469)