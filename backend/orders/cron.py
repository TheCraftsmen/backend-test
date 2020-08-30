import logging

from django.urls import reverse
from django.conf import settings
from slackclient import SlackClient

from .models import Menu

sc = SlackClient(settings.SLACK_TOKEN)


def send_meal_notification():
    """This function send menu notfication to a slack.
    need set value in settings (SLACK_TOKEN, SLACK_CHANNEL)
    :returns: bool -- the return code.

    """
    try:
        menu = Menu.objects.last()
        url = reverse('menu_detail', kwargs={'pk': menu.id})
        sc.api_call(
            "chat.postMessage",
            channel=settings.SLACK_CHANNEL,
            text="No te olvides del almuerzo :higuain: {}".format(url)
        )
    except Exception as e:
        logging.exception(
            '[retry meal_notification] Exception: {}'.format(str(e))
        )
