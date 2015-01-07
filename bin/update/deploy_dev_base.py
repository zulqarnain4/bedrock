import logging

from commander.deploy import task

from deploy_base import *  # noqa


log = logging.getLogger(__name__)


@task
def database(ctx):
    # only ever run this one on demo and dev.
    management_cmd('bedrock_truncate_database --yes-i-am-sure')
    management_cmd('syncdb --migrate --noinput')
    management_cmd('rnasync')
    management_cmd('update_security_advisories --force --quiet')
    management_cmd('cron update_reps_ical')
    management_cmd('cron update_tweets')
