import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Optional


class ShowSystemResourceSchema(MetaParser):

    schema = {
        Optional("uptime"): str,
        Optional("version"): str,
        Optional("build_time"): str,
        Optional("free_memory"): str,
        Optional("cpu_load"): str,
        Optional("platform"): str,
    }


class ShowSystemResource(ShowSystemResourceSchema):

    cli_command = "/system resource print"

    def cli(self, output=None):

        if output is None:
            output = self.device.execute(
                self.cli_command
            )

        parsed = {}

        p = re.compile(
            r"^\s*(?P<key>[\w\-]+)\s*:\s*(?P<value>.+)$"
        )

        for line in output.splitlines():

            m = p.match(line)

            if not m:
                continue

            key = m.group("key")
            value = m.group("value")

            key = key.replace("-", "_")

            parsed[key] = value

        return parsed
