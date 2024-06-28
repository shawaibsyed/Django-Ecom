from datetime import datetime, timedelta
import pytz

class UserSessionTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the session start time if not already set
        if 'session_start_time' not in request.session:
            request.session['session_start_time'] = datetime.now(pytz.utc).isoformat()
        response = self.get_response(request)
        # Calculate the time spent on the current session
        session_start_time = datetime.fromisoformat(request.session['session_start_time'])
        current_time = datetime.now(pytz.utc)
        time_spent = current_time - session_start_time

        # Update the session time spent
        if 'total_time_spent_today' not in request.session:
            request.session['total_time_spent_today'] = timedelta(0)
        request.session['total_time_spent_today'] += time_spent
        request.session['session_start_time'] = current_time.isoformat()  # Reset session start time
        # Optionally reset the counter at the end of the day
        if current_time - session_start_time > timedelta(days=1):
            request.session['total_time_spent_today'] = timedelta(0)
        # Print the session data for debugging
        print("Total Time Spent Today:", request.session['total_time_spent_today'])
        return response