class Metrics:
    """
    Metrics tracker for hybrid search API.
    """
    def __init__(self):
        self.request_count = 0
        self.latency_sum = 0.0

    def record_request(self, latency_seconds):
        """
        Record a search request with its latency.

        Args:
            latency_seconds: Time taken for the request in seconds
        """
        self.request_count += 1
        self.latency_sum += latency_seconds

    def get_avg_latency(self):
        """
        Get average latency in seconds.

        Returns:
            float: Average latency or 0.0 if no requests
        """
        if self.request_count == 0:
            return 0.0
        return self.latency_sum / self.request_count

    def get_metrics(self):
        """
        Get metrics in Prometheus text format.

        Returns:
            str: Prometheus-formatted metrics
        """
        avg_latency = self.get_avg_latency()
        return f"""# HELP hybrid_search_requests_total Total number of search requests processed
# TYPE hybrid_search_requests_total counter
hybrid_search_requests_total {self.request_count}

# HELP hybrid_search_avg_latency_seconds Average latency of search requests in seconds
# TYPE hybrid_search_avg_latency_seconds gauge
hybrid_search_avg_latency_seconds {avg_latency}
"""

# Global metrics instance
metrics = Metrics()

def get_metrics():
    """
    Get current metrics in Prometheus format.

    Returns:
        str: Prometheus-formatted metrics
    """
    return metrics.get_metrics()

def record_request(latency_seconds):
    """
    Record a search request latency.

    Args:
        latency_seconds: Time taken for the request in seconds
    """
    metrics.record_request(latency_seconds)
