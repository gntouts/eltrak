from EltrakLib.TrackerFactory import get_factory
import concurrent.futures


def brute_force_track(tracking_number: str):
    trackers = [get_factory(courier).get_tracker()
                for courier in ['speedex', 'acs', 'elta', 'skroutz', 'easymail', 'geniki']]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(trackers)) as executor:
        future_scan_results = {executor.submit(
            tracker.track_silently, tracking_number): tracker for tracker in trackers}
        
        results = []
        for future in concurrent.futures.as_completed(future_scan_results):
            data = future.result()
            if data:
                results.append(data)
        if len(results)> 0:
            res = [result for result in results if result.found]
            return res[0] if len(res) > 0 else None
        return None