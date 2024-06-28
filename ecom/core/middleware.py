from django.utils.timezone import now
import datetime
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('middleware_logger')

class UserSessionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request to get the response
        response = self.get_response(request)
        # After getting the response, process user session data
        self.process_user_session(request)
        return response

    def process_request(self, request):
        # Ensure user is authenticated before proceeding
        if not request.user or not request.user.is_authenticated:
            logger.error("User is not authenticated or no user attached to request.")
            return

    def process_user_session(self, request):
        if not request.user or not request.user.is_authenticated:
            return  # Do nothing if user is not authenticated

        user_id = request.user.id
        last_active_key = f"{user_id}_last_active"
        time_spent_key = f"{user_id}_time_spent_today"

        # Retrieve the last active time from the session, converting from string back to datetime
        last_active = request.session.get(last_active_key)
        if last_active:
            last_active = datetime.datetime.fromisoformat(last_active)

        # Check if last_active is not set or if it's a new day
        current_time = now()
        if not last_active or current_time.date() > last_active.date():
            request.session[time_spent_key] = 0  # Reset the time spent for the new day
            last_active = current_time

        # Calculate the time delta since the last active time
        time_delta = current_time - last_active
        total_time_spent = request.session.get(time_spent_key, 0) + time_delta.total_seconds()

        # Update the session, converting datetime to string for storage
        request.session[time_spent_key] = total_time_spent
        request.session[last_active_key] = current_time.isoformat()
        logger.debug(f"Updated session for user {user_id}: Last active at {last_active}, Total time spent today: {total_time_spent} seconds")

        # Mark session as modified to make sure it gets saved
        request.session.modified = True