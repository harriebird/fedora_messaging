#
# Copyright © Michal Čihař <michal@weblate.org>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os

import fedora_messaging
from django.apps import AppConfig
from django.conf import settings

from weblate.utils.version import VERSION


def configure_fedora_messaging():
    if settings.FEDORA_MESSAGING_CONF:
        fedora_messaging.config.conf.load_config(
            config_path=settings.FEDORA_MESSAGING_CONF
        )
    if "CI_AMQP_HOST" in os.environ:
        fedora_messaging.config.conf.update(
            amqp_url="amqp://{}?connection_attempts=3&retry_delay=5".format(
                os.environ["CI_AMQP_HOST"]
            )
        )
    fedora_messaging.config.conf.setup_logging()
    messaging_version = fedora_messaging.config.conf["client_properties"]["version"]
    version = f"Weblate-{VERSION} {messaging_version}"
    fedora_messaging.config.conf["client_properties"] = {
        "app": "Weblate",
        "product": "Weblate Fedora Messaging",
        "information": "https://github.com/WeblateOrg/fedora_messaging",
        "version": version,
    }


class FedoraConfig(AppConfig):
    name = "weblate_fedora_messaging"
    label = "weblate_fedora_messaging"
    verbose_name = "Weblate Fedora Messaging"

    def ready(self):
        super().ready()
        configure_fedora_messaging()
