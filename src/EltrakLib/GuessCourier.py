from EltrakLib.TrackerFactory import get_factory
import concurrent.futures


def brute_force_track(tracking_number: str):
    trackers = [get_factory(courier).get_tracker()
                for courier in ['speedex', 'acs', 'elta', 'skroutz', 'easymail']]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(trackers)) as executor:
        future_scan_results = {executor.submit(
            tracker.track_silently, tracking_number): tracker for tracker in trackers}
        for future in concurrent.futures.as_completed(future_scan_results):
            data = future.result()
            if data:
                return data
