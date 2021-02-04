# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

bucket = "6bf8ad0732605327"
org = "b6cceae0afcd3264"
token = "e4Z0o1Xi9VlQH8V4Axuuf1gFNeAEdu1DXwcJ4ENpkjSIB9a67EEajiSN3GOu3JCOQakTjpPTxS2woXRseW-fPQ=="
url = "https://us-central1-1.gcp.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(
	url=url,
	token=token,
	org=org
)


def send_job_influxdb():
	for x in range(100):
		time.sleep(2)
		write_api = client.write_api(write_options=SYNCHRONOUS)
		p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature",random.uniform(1, 100))
		write_api.write(bucket=bucket, org=org, record=p)



class Helloworld_testPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
							octoprint.plugin.StartupPlugin):

	def on_after_startup(self):
		self._logger.info("QWERTYUIOP")
		send_job_influxdb()
		self._logger.info("ZXCVBNM")

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/helloworld_test.js"],
			css=["css/helloworld_test.css"],
			less=["less/helloworld_test.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			helloworld_test=dict(
				displayName="Helloworld_test Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="zhaojunqin93",
				repo="OctoPrint-Helloworld_test",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/zhaojunqin93/OctoPrint-Helloworld_test/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Helloworld_test Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Helloworld_testPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

