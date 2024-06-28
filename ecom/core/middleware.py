from django.utils.timezone import now
import datetime
import logging
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('middleware_logger')

class UserSessionMiddleware(MiddlewareMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def process_request(self, request):
        try:
            self.process_user_session(request)
        except Exception as e:
            # Handle exceptions or log errors
            print(f"Error processing session data: {e}")

    def process_user_session(self, request):
        last_active_key = f"{request.user.id}_last_active"
        time_spent_key = f"{request.user.id}_time_spent_today"

        # Retrieve the last active time from the session, converting from string back to datetime
        last_active = request.session.get(last_active_key)
        if last_active:
            last_active = datetime.datetime.fromisoformat(last_active)

        # Check if last_active is not set or if it's a new day
        if not last_active or now().date() > last_active.date():
            request.session[time_spent_key] = 0
            last_active = now()

        time_delta = now() - last_active
        total_time_spent = request.session.get(time_spent_key, 0) + time_delta.total_seconds()

        # Update the session, converting datetime to string
        request.session[time_spent_key] = total_time_spent
        request.session[last_active_key] = last_active.isoformat()